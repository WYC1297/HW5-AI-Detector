"""
Streamlit 應用 - AI / Human 文章檢測器
"""
import streamlit as st
import pickle
import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from collections import Counter
import warnings
import random

# 忽略字體警告
warnings.filterwarnings('ignore', category=UserWarning, module='matplotlib')

# 設置中文字體
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

# 頁面配置
st.set_page_config(
    page_title="AI / Human 文章檢測器",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定義 CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    .ai-percentage {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }
    .human-percentage {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    """加載訓練好的模型"""
    model_path = './models/ai_detector_model.pkl'
    if not os.path.exists(model_path):
        st.error(f"❌ 模型文件未找到: {model_path}")
        st.info("請先運行 `python train_model.py` 來訓練模型")
        return None
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    return model

# AI 生成的範例
AI_EXAMPLES = [
    """The advancement of artificial intelligence has revolutionized the landscape of modern technology. Machine learning algorithms, neural networks, and deep learning models have enabled unprecedented capabilities in pattern recognition, natural language processing, and decision-making systems. These technologies have been integrated across various sectors including healthcare, finance, transportation, and entertainment, fundamentally transforming how organizations operate and deliver services to their customers.""",
    
    """Recent developments in artificial intelligence have demonstrated remarkable progress in various domains. The integration of deep learning methodologies with traditional computational frameworks has yielded significant improvements in accuracy and efficiency. Organizations worldwide are increasingly adopting AI-driven solutions to optimize their operational processes, enhance decision-making capabilities, and derive actionable insights from complex data structures.""",
    
    """The implementation of machine learning algorithms has proven instrumental in addressing contemporary challenges across multiple industries. Through sophisticated data analysis and predictive modeling, organizations can identify patterns and trends that would otherwise remain obscured. The proliferation of AI technologies has catalyzed transformation in sectors ranging from healthcare diagnostics to financial forecasting, demonstrating the versatility and applicability of these advanced computational methodologies.""",
    
    """Artificial intelligence represents a paradigm shift in technological innovation. The convergence of increased computational power, sophisticated algorithms, and expansive datasets has created unprecedented opportunities for automation and intelligent decision-making. Contemporary applications span from natural language understanding to computer vision, exemplifying the breadth of AI's transformative potential across diverse operational contexts.""",
    
    """The exponential growth of artificial intelligence capabilities has necessitated comprehensive examination of its implications. Advanced neural network architectures enable unprecedented levels of pattern recognition and inference. These technologies facilitate enhanced business intelligence, streamlined operations, and improved resource allocation. The systematic deployment of AI solutions across organizational hierarchies has become increasingly prevalent, reflecting its growing indispensability in competitive market environments."""
]

# 人類撰寫的範例
HUMAN_EXAMPLES = [
    """I've been thinking about how AI is changing things, and honestly, it's pretty wild. Like, sometimes I'm impressed by what these systems can do, but other times I'm genuinely concerned about where we're heading. My friend Sarah asked me the other day if I thought AI would take our jobs, and I didn't really have a good answer. I guess time will tell, right? Anyway, it's definitely an interesting time to be alive.""",
    
    """You know what's crazy? I was talking to my colleague yesterday about machine learning, and we got into this whole debate about whether computers can actually think. He's convinced they can, but I'm not so sure. I mean, they're just following rules that humans programmed, aren't they? But then again, I don't fully understand how neural networks work, so maybe I'm wrong. It's definitely something to ponder.""",
    
    """I recently read an article about deep learning, and it blew my mind. The author explained how these algorithms can recognize faces and understand language, which is pretty cool. I tried explaining it to my mom, but she just looked confused. I guess it's one of those topics that's really hard to explain to people who aren't into tech. Still, I think it's going to change the world in ways we can't even imagine yet.""",
    
    """My thoughts on AI have evolved over time. When I first heard about it, I thought it was just science fiction stuff. But now I use AI tools almost every day without even thinking about it. Sometimes I wonder if that's a good thing or not. It makes things easier, sure, but it also makes me a bit lazy. I try to balance it out by still doing things manually when I can.""",
    
    """I was at a coffee shop last week, and two people next to me were having this intense conversation about artificial intelligence. One of them kept saying we need to be careful about AI, and the other kept defending it. It got me thinking – maybe both sides have a point? I don't know enough to have a strong opinion either way, but I'm curious to learn more about it."""
]

def get_random_example(is_ai=True):
    """獲取隨機的範例文本"""
    examples = AI_EXAMPLES if is_ai else HUMAN_EXAMPLES
    return random.choice(examples)

def extract_features(text):
    """提取文本特徵用於分析"""
    # 基本統計
    sentences = text.split('.')
    words = text.split()
    
    features = {
        'word_count': len(words),
        'sentence_count': len([s for s in sentences if s.strip()]),
        'avg_word_length': np.mean([len(w) for w in words]) if words else 0,
        'avg_sentence_length': len(words) / len([s for s in sentences if s.strip()]) if any(sentences) else 0,
    }
    
    # 字符特性
    features['punctuation_ratio'] = len([c for c in text if c in '!?.,:;']) / len(text) if text else 0
    
    # 大寫字母比例
    uppercase_count = len([c for c in text if c.isupper()])
    features['uppercase_ratio'] = uppercase_count / len(text) if text else 0
    
    return features

def predict_and_analyze(model, text):
    """進行預測和分析"""
    if not text.strip():
        return None
    
    # 進行預測
    prediction = model.predict([text])[0]
    probabilities = model.predict_proba([text])[0]
    
    result = {
        'prediction': 'AI 生成' if prediction == 1 else '人類撰寫',
        'is_ai': prediction == 1,
        'human_probability': probabilities[0] * 100,
        'ai_probability': probabilities[1] * 100,
        'confidence': max(probabilities) * 100
    }
    
    return result

def show_statistics(text):
    """顯示文本統計"""
    features = extract_features(text)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("單詞數", features['word_count'])
    
    with col2:
        st.metric("句子數", features['sentence_count'])
    
    with col3:
        st.metric("平均單詞長度", f"{features['avg_word_length']:.1f}")
    
    with col4:
        st.metric("平均句子長度", f"{features['avg_sentence_length']:.1f}")
    
    # 第二行統計
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("標點符號比例", f"{features['punctuation_ratio']:.2%}")
    
    with col2:
        st.metric("大寫字母比例", f"{features['uppercase_ratio']:.2%}")

def clear_text():
    """清除文本的 callback 函數"""
    st.session_state.text_input = ""

def load_ai_example():
    """加載 AI 範例的 callback 函數"""
    st.session_state.text_input = get_random_example(is_ai=True)

def load_human_example():
    """加載人類範例的 callback 函數"""
    st.session_state.text_input = get_random_example(is_ai=False)
    """顯示特徵分析和洞察"""
    st.header("🔬 特徵分析與洞察")
    
    features = extract_features(text)
    
    # 特徵說明
    st.markdown("""
    ### 📊 文本特徵解釋
    
    以下是影響 AI/Human 判別的主要特徵及其含義：
    """)
    
    # 創建特徵對比表格
    feature_insights = {
        "特徵": [
            "單詞數",
            "平均單詞長度",
            "平均句子長度",
            "標點符號比例",
            "大寫字母比例"
        ],
        "當前文本": [
            f"{features['word_count']}",
            f"{features['avg_word_length']:.2f}",
            f"{features['avg_sentence_length']:.2f}",
            f"{features['punctuation_ratio']:.3f}",
            f"{features['uppercase_ratio']:.3f}"
        ],
        "AI 生成特徵": [
            "通常較長 (400-800)",
            "通常較長 (5.5-6.5)",
            "通常較長 (15-20)",
            "通常較低 (0.015-0.025)",
            "通常較低 (0.01-0.02)"
        ],
        "人類撰寫特徵": [
            "變化較大 (100-600)",
            "變化較大 (4.5-5.5)",
            "變化較大 (10-18)",
            "通常較高 (0.025-0.04)",
            "通常較高 (0.02-0.05)"
        ]
    }
    
    import pandas as pd
    df = pd.DataFrame(feature_insights)
    st.table(df)
    
    st.divider()
    
    # 特徵分析卡片
    st.markdown("### 💡 本文本的特徵分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📝 詞彙特徵:**
        - 單詞數反映文本的長度和豐富度
        - 平均單詞長度顯示詞彙的複雜性
        - AI 傾向使用更多專業術語和長詞彙
        - 人類寫作風格更多樣化和口語化
        """)
    
    with col2:
        st.markdown("""
        **🎯 結構特徵:**
        - 句子長度反映寫作風格和複雜度
        - AI 通常保持一致的句子結構
        - 人類文本有更多變化和節奏感
        - 標點符號比例體現表達習慣差異
        """)
    
    st.divider()
    
    # 檢測指標
    st.markdown("### 🎯 檢測指標詳解")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        **当前文本评分:**
        
        📊 **結構評分**
        - 句子複雜度: {'⭐' * min(5, int(features['avg_sentence_length'] / 4))}
        - 詞彙豐富度: {'⭐' * min(5, int(features['avg_word_length'] / 1.2))}
        """)
    
    with col2:
        confidence = result['confidence']
        prediction_type = "🤖 AI 生成" if result['is_ai'] else "👤 人類撰寫"
        
        st.markdown(f"""
        **判別結果:**
        
        🎯 **預測分類**: {prediction_type}
        - 信心度: {'█' * int(confidence / 10)}{'░' * (10 - int(confidence / 10))} {confidence:.1f}%
        - AI 概率: {result['ai_probability']:.1f}%
        - 人類概率: {result['human_probability']:.1f}%
        """)
    
    st.divider()
    
    # 特徵可視化
    st.markdown("### 📈 特徵對比圖")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    
    # 1. 句子長度分佈
    ax = axes[0, 0]
    sentences = [len(s.split()) for s in text.split('.') if s.strip()]
    if sentences:
        ax.hist(sentences, bins=10, color='#667eea', edgecolor='black', alpha=0.7)
        ax.set_title('Sentence Length Distribution', fontweight='bold')
        ax.set_xlabel('Words per Sentence')
        ax.set_ylabel('Frequency')
        ax.grid(alpha=0.3)
    
    # 2. 標點符號類型
    ax = axes[0, 1]
    punctuation_counts = {
        '.': text.count('.'),
        ',': text.count(','),
        '!': text.count('!'),
        '?': text.count('?'),
        ';': text.count(';'),
        ':': text.count(':')
    }
    punctuation_counts = {k: v for k, v in punctuation_counts.items() if v > 0}
    if punctuation_counts:
        ax.bar(punctuation_counts.keys(), punctuation_counts.values(), 
               color='#764ba2', edgecolor='black', alpha=0.7)
        ax.set_title('Punctuation Usage', fontweight='bold')
        ax.set_ylabel('Count')
        ax.grid(alpha=0.3, axis='y')
    
    # 3. 特徵指標對比
    ax = axes[1, 0]
    feature_names = ['Word\nLength', 'Sentence\nLength', 'Punctuation\nRatio', 'Uppercase\nRatio']
    feature_values = [
        min(features['avg_word_length'] / 7 * 100, 100),  # 正規化到 0-100
        min(features['avg_sentence_length'] / 20 * 100, 100),
        features['punctuation_ratio'] * 1000,
        features['uppercase_ratio'] * 1000
    ]
    colors_feature = ['#667eea', '#764ba2', '#4facfe', '#f093fb']
    ax.bar(feature_names, feature_values, color=colors_feature, edgecolor='black', alpha=0.7)
    ax.set_title('Text Features Analysis', fontweight='bold')
    ax.set_ylabel('Normalized Score')
    ax.set_ylim(0, 100)
    ax.grid(alpha=0.3, axis='y')
    
    # 4. 詞長分佈
    ax = axes[1, 1]
    word_lengths = [len(w) for w in text.split() if w]
    if word_lengths:
        ax.hist(word_lengths, bins=15, color='#f5576c', edgecolor='black', alpha=0.7)
        ax.set_title('Word Length Distribution', fontweight='bold')
        ax.set_xlabel('Characters per Word')
        ax.set_ylabel('Frequency')
        ax.axvline(np.mean(word_lengths), color='black', linestyle='--', linewidth=2, label=f"Mean: {np.mean(word_lengths):.1f}")
        ax.legend()
        ax.grid(alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.divider()
    
    # 判別依據
    st.markdown("### 🔍 判別依據")
    
    if result['is_ai']:
        st.info("""
        **🤖 該文本被判定為 AI 生成，主要特徵包括：**
        
        ✓ **結構化寫作**: 段落結構清晰，邏輯嚴密
        ✓ **詞彙豐富**: 使用複雜和專業的詞彙
        ✓ **一致風格**: 寫作風格保持高度一致
        ✓ **完美語法**: 語法和標點符號使用規範
        ✓ **機械化表達**: 缺乏個人特色和情感波動
        
        **常見特徵:**
        - 句子長度相對一致
        - 很少出現口語化表達
        - 標點符號使用精確
        - 詞彙選擇傾向於正式
        """)
    else:
        st.info("""
        **👤 該文本被判定為人類撰寫，主要特徵包括：**
        
        ✓ **自然表達**: 語言更加自然和口語化
        ✓ **風格多變**: 句子長度和風格變化較大
        ✓ **個人特色**: 具有明顯的個人寫作習慣
        ✓ **情感表達**: 包含更多主觀情感和觀點
        ✓ **非正式用語**: 可能包含縮略詞或非正式表達
        
        **常見特徵:**
        - 句子長度變化明顯
        - 經常使用口語化表達
        - 標點符號使用較為靈活
        - 詞彙選擇更加多樣化
        """)

def main():
    """主應用"""
    # 標題
    st.markdown("""
        <h1 style='text-align: center; color: #667eea;'>
        🔍 AI / Human 文章檢測器
        </h1>
        <p style='text-align: center; color: #666;'>
        使用機器學習檢測文章是由 AI 生成還是人類撰寫
        </p>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # 加載模型
    model = load_model()
    if model is None:
        st.stop()
    
    # 側邊欄 - 模型信息
    with st.sidebar:
        st.header("📊 模型信息")
        st.info("""
        **模型性能:**
        - 準確度: 95.74%
        - AUC: 0.9918
        - 訓練數據: 487,235 個樣本
        - 算法: Naive Bayes + TF-IDF
        """)
        
        st.header("📝 使用方式")
        st.markdown("""
        1. 在下方文本框輸入要檢測的文章
        2. 點擊「分析」按鈕
        3. 查看結果和統計信息
        
        💡 **提示:** 輸入的文本越長，檢測結果越準確
        """)
        
        st.divider()
        
        st.header("🧪 示例文本")
        if st.button("加載 AI 生成的範例", use_container_width=True, key="btn_ai", on_click=load_ai_example):
            pass
        
        if st.button("加載人類撰寫的範例", use_container_width=True, key="btn_human", on_click=load_human_example):
            pass
    
    # 初始化 session state
    if 'text_input' not in st.session_state:
        st.session_state.text_input = ""
    
    # 主要內容區
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # 文本輸入
        text_input = st.text_area(
            "📝 輸入要檢測的文章",
            height=200,
            placeholder="在此輸入你想檢測的文章（最少 50 個字）...",
            key="text_input"
        )
    
    with col2:
        st.empty()  # 占位符
    
    st.divider()
    
    # 分析按鈕
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        analyze_button = st.button("🔍 分析", use_container_width=True, type="primary")
    
    with col2:
        if st.button("🗑️ 清除", use_container_width=True, on_click=clear_text):
            pass
    
    # 分析結果
    if analyze_button:
        text = st.session_state.text_input.strip()
        
        if len(text) < 20:
            st.warning("⚠️ 請輸入至少 20 個字符的文本")
        else:
            # 進行預測
            result = predict_and_analyze(model, text)
            
            if result:
                # 結果展示
                st.divider()
                st.header("📋 檢測結果")
                
                # 大的結果卡片
                if result['is_ai']:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                                color: white; padding: 30px; border-radius: 15px; text-align: center;'>
                        <h2 style='margin: 0;'>🤖 AI 生成的文章</h2>
                        <h1 style='margin: 10px 0; font-size: 48px;'>{result['ai_probability']:.1f}%</h1>
                        <p style='margin: 0; font-size: 14px;'>信心度: {result['confidence']:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                                color: white; padding: 30px; border-radius: 15px; text-align: center;'>
                        <h2 style='margin: 0;'>👤 人類撰寫的文章</h2>
                        <h1 style='margin: 10px 0; font-size: 48px;'>{result['human_probability']:.1f}%</h1>
                        <p style='margin: 0; font-size: 14px;'>信心度: {result['confidence']:.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.divider()
                
                # 概率圖表
                col1, col2 = st.columns(2)
                
                with col1:
                    # 柱狀圖
                    fig, ax = plt.subplots(figsize=(8, 6))
                    categories = ['Human', 'AI']
                    probabilities = [result['human_probability'], result['ai_probability']]
                    colors = ['#4facfe', '#f093fb']
                    
                    bars = ax.bar(categories, probabilities, color=colors, edgecolor='black', linewidth=2)
                    
                    # 添加數值標籤
                    for bar, prob in zip(bars, probabilities):
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height,
                               f'{prob:.1f}%',
                               ha='center', va='bottom', fontsize=14, fontweight='bold')
                    
                    ax.set_ylim(0, 105)
                    ax.set_ylabel('Probability (%)', fontsize=12)
                    ax.set_title('AI vs Human Classification', fontsize=14, fontweight='bold')
                    ax.grid(axis='y', alpha=0.3)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                
                with col2:
                    # 圓形圖
                    fig, ax = plt.subplots(figsize=(8, 6))
                    sizes = [result['human_probability'], result['ai_probability']]
                    labels = [f"Human\n{result['human_probability']:.1f}%", 
                             f"AI\n{result['ai_probability']:.1f}%"]
                    colors = ['#4facfe', '#f093fb']
                    
                    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                                       autopct='', startangle=90,
                                                       textprops={'fontsize': 12, 'weight': 'bold'})
                    
                    ax.set_title('Probability Distribution', fontsize=14, fontweight='bold')
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                
                st.divider()
                
                # 文本統計
                st.header("📊 文本統計分析")
                show_statistics(text)
                
                st.divider()
                
                # 特徵分析和洞察
                show_feature_insights(text, result)
                
                st.divider()
                
                # 詳細信息
                st.header("📌 詳細信息")
                
                info_col1, info_col2, info_col3, info_col4 = st.columns(4)
                
                with info_col1:
                    st.metric("人類概率", f"{result['human_probability']:.2f}%")
                
                with info_col2:
                    st.metric("AI 概率", f"{result['ai_probability']:.2f}%")
                
                with info_col3:
                    st.metric("信心度", f"{result['confidence']:.2f}%")
                
                with info_col4:
                    st.metric("分類", "🤖 AI" if result['is_ai'] else "👤 人類")

if __name__ == '__main__':
    main()
