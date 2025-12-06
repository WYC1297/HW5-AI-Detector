"""
訓練 AI/Human 文章分類模型
"""
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_auc_score
import pickle
import os
from pathlib import Path

def load_data(csv_path):
    """加載數據"""
    print(f"加載數據從 {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"數據形狀: {df.shape}")
    print(f"類別分布:\n{df['generated'].value_counts()}")
    return df

def create_pipeline():
    """創建分類管道"""
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8,
            sublinear_tf=True,
            stop_words='english'
        )),
        ('classifier', MultinomialNB(alpha=1.0))
    ])
    return pipeline

def train_model(csv_path, output_dir='./models'):
    """訓練模型"""
    # 創建輸出目錄
    Path(output_dir).mkdir(exist_ok=True)
    
    # 加載數據
    df = load_data(csv_path)
    X = df['text'].values
    y = df['generated'].values
    
    # 分割數據 (由於數據量大，使用 20% 作為測試集)
    print("\n分割數據...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"訓練集大小: {len(X_train)}")
    print(f"測試集大小: {len(X_test)}")
    
    # 創建和訓練模型
    print("\n訓練模型...")
    pipeline = create_pipeline()
    pipeline.fit(X_train, y_train)
    
    # 評估模型
    print("\n評估模型...")
    y_pred = pipeline.predict(X_test)
    y_pred_proba = pipeline.predict_proba(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    auc_score = roc_auc_score(y_test, y_pred_proba[:, 1])
    
    print(f"準確度: {accuracy:.4f}")
    print(f"AUC 分數: {auc_score:.4f}")
    print(f"\n分類報告:\n{classification_report(y_test, y_pred, target_names=['Human', 'AI'])}")
    print(f"\n混淆矩陣:\n{confusion_matrix(y_test, y_pred)}")
    
    # 保存模型
    model_path = os.path.join(output_dir, 'ai_detector_model.pkl')
    print(f"\n保存模型到 {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(pipeline, f)
    
    # 保存模型評估結果
    results = {
        'accuracy': accuracy,
        'auc_score': auc_score,
        'classification_report': classification_report(y_test, y_pred, target_names=['Human', 'AI']),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist(),
        'model_path': model_path
    }
    
    return pipeline, results

if __name__ == '__main__':
    csv_path = r'c:\Users\WANG\Desktop\WANG\研究所\課程\碩二上\物聯網\HW5\AI_Human.csv'
    model, results = train_model(csv_path)
    print("\n✓ 模型訓練完成！")
