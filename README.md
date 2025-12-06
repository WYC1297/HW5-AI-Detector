# 🔍 AI / Human 文章檢測器

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://hw5-ai-detector.streamlit.app)

## 概述

這是一個基於機器學習的 AI/Human 文章分類工具，能夠檢測給定的文本是由 AI 生成還是人類撰寫的。

### 核心特徵

- **高準確率**: 95.74% 的分類準確度，AUC 得分 0.9918
- **即時預測**: 輸入文本後立即顯示判斷結果（AI% / Human%）
- **詳細分析**: 提供文本統計、概率分布圖表和置信度信息
- **友好界面**: 基於 Streamlit 的互動式 Web 應用

## 模型性能

| 指標 | 值 |
|------|-----|
| 準確度 | 95.74% |
| AUC | 0.9918 |
| 精確度（Human） | 96% |
| 精確度（AI） | 96% |
| 召回率（Human） | 98% |
| 召回率（AI） | 92% |

## 技術棧

### 後端
- **Python 3.10**
- **scikit-learn**: 機器學習模型（Naive Bayes）
- **pandas**: 數據處理
- **numpy**: 數值計算

### 前端
- **Streamlit**: Web 應用框架
- **matplotlib/seaborn**: 數據可視化

### 算法
- **特徵提取**: TF-IDF 向量化（最多 5000 個特徵，1-2 元語法）
- **分類器**: 多項式樸素貝葉斯
- **訓練數據**: 487,235 個文本樣本

## 項目結構

```
HW5/
├── app.py                    # Streamlit 應用主文件
├── train_model.py            # 模型訓練腳本
├── AI_Human.csv              # 訓練數據集
├── requirements.txt          # Python 依賴
├── .gitignore               # Git 忽略文件
├── models/                  # 訓練好的模型（首次運行後生成）
│   └── ai_detector_model.pkl
└── README.md                # 本文件
```

## 安裝和運行

### 本地運行

1. **克隆倉庫**
   ```bash
   git clone https://github.com/WYC1297/HW5-AI-Detector.git
   cd HW5
   ```

2. **建立虛擬環境**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Mac/Linux
   ```

3. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

4. **訓練模型（首次）**
   ```bash
   python train_model.py
   ```

5. **運行應用**
   ```bash
   streamlit run app.py
   ```

6. **訪問應用**
   
   打開瀏覽器訪問 `http://localhost:8501`

### Streamlit Cloud 部署

應用已部署在 Streamlit Cloud，可直接訪問：

🔗 **[https://hw5-ai-detector.streamlit.app](https://hw5-ai-detector.streamlit.app)**

## 使用方式

1. 在文本框中輸入要檢測的文章（至少 20 字符）
2. 點擊 **分析** 按鈕
3. 查看結果：
   - **AI 生成概率**: 文章是 AI 生成的可能性
   - **人類撰寫概率**: 文章是人類撰寫的可能性
   - **信心度**: 模型對預測的確信程度
4. 查看詳細的文本統計和可視化

### 示例

側邊欄提供了兩個示例文本：
- **AI 生成示例**: 正式、結構化的技術文本
- **人類撰寫示例**: 自然、非正式的個人文本

## 數據集

訓練數據包含：
- **總樣本數**: 487,235
- **人類文本**: 305,797 個
- **AI 生成文本**: 181,438 個
- **訓練集**: 389,788 個樣本（80%）
- **測試集**: 97,447 個樣本（20%）

## API 接口

模型通過 pickle 序列化保存，可以在其他 Python 應用中使用：

```python
import pickle

# 加載模型
with open('./models/ai_detector_model.pkl', 'rb') as f:
    model = pickle.load(f)

# 進行預測
text = "Your text here..."
prediction = model.predict([text])  # 0 = 人類, 1 = AI
probabilities = model.predict_proba([text])  # [human_prob, ai_prob]
```

## 開發過程

### AI 對話記錄

詳細的 ChatGPT 開發對話記錄請見 `AI_Conversation_Log.md`

### 主要步驟

1. **數據探索**: 分析 AI_Human.csv 數據集
2. **特徵工程**: 使用 TF-IDF 向量化
3. **模型訓練**: 使用 Naive Bayes 分類器
4. **性能評估**: 95.74% 準確度
5. **應用開發**: 使用 Streamlit 創建交互式界面
6. **部署**: 部署到 Streamlit Cloud

## 限制與注意事項

- ✅ **優點**: 快速推理、高準確度、易於部署
- ⚠️ **限制**:
  - 模型基於英文文本訓練
  - 性能可能因語言和領域而異
  - 對特別長或特別短的文本識別效果可能不佳
  - 不能識別混合人類+AI 的文本

## 改進方向

未來可能的改進包括：
- [ ] 支持多語言檢測
- [ ] 使用 BERT/GPT 等預訓練模型
- [ ] 實現更精細的置信度估計
- [ ] 添加批量檢測功能
- [ ] 記錄預測歷史和趨勢分析

## 許可證

MIT License

## 作者

**WANG** - 物聯網課程 HW5 項目

## 聯繫方式

如有問題或建議，請提交 Issue 或 Pull Request。

---

**最後更新**: 2025年12月6日

**模型訓練日期**: 2025年12月6日

**版本**: 1.0.0
