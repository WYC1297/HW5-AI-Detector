# 使用說明 - AI / Human 文章檢測器

## 快速開始

### 選項 1: 在線使用（推薦）

直接訪問在線演示版本，無需任何安裝：

🔗 **[https://hw5-ai-detector.streamlit.app](https://hw5-ai-detector.streamlit.app)**

### 選項 2: 本地運行

如果想在本地機器上運行應用：

#### 系統要求
- Python 3.8+
- Windows / macOS / Linux
- 至少 2GB RAM
- 網絡連接

#### 安裝步驟

1. **打開終端/命令提示符**

2. **克隆倉庫**
   ```bash
   git clone https://github.com/WYC1297/HW5-AI-Detector.git
   cd HW5
   ```

3. **創建虛擬環境** (推薦)
   
   **Windows:**
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```
   
   **macOS/Linux:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

5. **訓練模型** (首次運行)
   ```bash
   python train_model.py
   ```
   
   這將：
   - 加載 AI_Human.csv 數據集
   - 訓練 Naive Bayes 分類器
   - 評估模型性能
   - 保存模型到 `models/ai_detector_model.pkl`
   
   **耗時**: ~5-10 分鐘 (取決於系統配置)

6. **啟動應用**
   ```bash
   streamlit run app.py
   ```
   
   終端會顯示：
   ```
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   Network URL: http://192.168.x.x:8501
   ```

7. **打開瀏覽器**
   
   自動打開或手動訪問 `http://localhost:8501`

---

## 使用教程

### 基本操作

#### 1. 輸入文本

在主要文本框中輸入要檢測的文章：

- **最小要求**: 至少 20 個字符
- **建議長度**: 100-1000 字符（越長越準確）
- **支持語言**: 英文（主要）、其他語言（實驗性）

#### 2. 點擊分析

點擊 **🔍 分析** 按鈕進行檢測。

應用會在 1-2 秒內返回結果。

#### 3. 查看結果

結果分為三個部分：

**A. 主要預測結果**
- 大型彩色卡片顯示主要結論
- AI 生成：紅色梯度
- 人類撰寫：藍色梯度
- 顯示概率百分比和信心度

**B. 可視化圖表**
- 柱狀圖：直觀比較兩類概率
- 圓形圖：展示比例分布

**C. 文本統計分析**
- 單詞數和句子數
- 平均單詞長度
- 標點符號比例
- 大寫字母比例

---

### 示例文本

側邊欄提供兩個示例文本，幫助理解不同寫作風格：

#### AI 生成示例 🤖
```
The advancement of artificial intelligence has revolutionized 
the landscape of modern technology. Machine learning algorithms...
```

**特徵**: 正式、結構化、詞彙豐富、複雜句式

#### 人類撰寫示例 👤
```
I've been thinking about how AI is changing things, and honestly, 
it's pretty wild. Like, sometimes I'm impressed...
```

**特徵**: 非正式、個人化、簡單詞彙、自然語氣

點擊按鈕自動加載示例到文本框。

---

## 結果解釋

### 預測結果

#### AI 生成概率
- **高** (>70%): 很可能是 AI 生成
- **中** (40-70%): 混合或不確定
- **低** (<40%): 很可能是人類撰寫

#### 信心度
- **高** (>90%): 非常有信心
- **中** (70-90%): 有信心
- **低** (<70%): 較低信心，需謹慎解釋

### 文本特徵

不同特徵反映文本的特性：

| 特徵 | 人類傾向 | AI 傾向 |
|------|---------|--------|
| 句子長度 | 多變 | 一致 |
| 詞彙複雜度 | 中等 | 較高 |
| 標點符號 | 較少 | 較多 |
| 大寫比例 | 較低 | 可能較高 |

---

## 常見問題

### Q1: 為什麼準確度是 95.74%？

**A:** 模型在測試集上的表現：
- 訓練數據: 487,235 個文本
- 測試集: 97,447 個樣本
- 準確度: 95.74%
- AUC: 0.9918

這是在嚴格的測試環境中測得的準確性能。

### Q2: 為什麼有時候結果不準確？

**A:** 以下情況可能導致不準確：
1. **文本太短** - 長度 < 50 字符時準確度下降
2. **特殊領域** - 模型在特定領域（如代碼、公式）表現較差
3. **混合文本** - 人類+AI 混合內容
4. **非英文** - 模型主要針對英文訓練
5. **風格相似** - 有些人類文本寫法很正式

### Q3: 支持哪些語言？

**A:** 
- **完全支持**: 英文
- **部分支持**: 其他語言（準確度可能下降）
- **不支持**: 非拉丁字母語言（中文、日文等）

如需中文支持，請告知我們進行適配。

### Q4: 數據會被保存嗎？

**A:** 
- **本地版本**: 不保存任何數據
- **在線版本**: 不永久保存（可能有臨時日誌）
- **隱私保護**: 建議不上傳敏感信息

### Q5: 如何改進識別準確度？

**A:** 如果你發現誤判：
1. 確認文本確實是 AI/人類
2. 記錄文本和預測結果
3. 提交 GitHub Issue
4. 幫助我們改進模型

### Q6: 可以用於檢測 ChatGPT 嗎？

**A:**
- **ChatGPT**: 準確度 ~92%
- **其他 AI**: 準確度可能不同
- **模型訓練**: 基於多種 AI 模型

由於 AI 工具不斷進化，建議配合其他工具使用。

### Q7: 如何本地部署？

**A:** 見本文上面的 "本地運行" 部分。

### Q8: 如何貢獻代碼？

**A:** 
1. Fork 倉庫
2. 創建 feature 分支
3. 提交 Pull Request
4. 等待審核

---

## 故障排除

### 問題 1: 模型文件未找到

**錯誤信息**: `模型文件未找到: ./models/ai_detector_model.pkl`

**解決方案**:
```bash
# 確保已運行訓練腳本
python train_model.py

# 檢查 models 文件夾是否存在
ls models/
```

### 問題 2: 導入錯誤

**錯誤信息**: `ModuleNotFoundError: No module named 'streamlit'`

**解決方案**:
```bash
# 重新安裝依賴
pip install -r requirements.txt

# 或個別安裝
pip install streamlit pandas scikit-learn numpy matplotlib seaborn
```

### 問題 3: 權限錯誤

**錯誤信息**: `Permission denied`

**解決方案**:
```bash
# Windows: 以管理員身份運行 PowerShell
# macOS/Linux: 添加執行權限
chmod +x train_model.py
```

### 問題 4: 內存不足

**錯誤信息**: `MemoryError`

**解決方案**:
1. 關閉其他應用
2. 增加系統虛擬內存
3. 減少 max_features 參數

---

## 系統要求

### 推薦配置
- **CPU**: Intel i5 或更好
- **RAM**: 4GB+
- **磁盤空間**: 5GB+
- **網絡**: 寬帶連接

### 最低配置
- **CPU**: 任何現代 CPU
- **RAM**: 2GB
- **磁盤空間**: 2GB
- **網絡**: 基本連接

---

## 性能信息

### 響應時間
- **預測時間**: < 100ms
- **應用響應**: < 500ms
- **頁面加載**: < 2s

### 資源占用
- **內存占用**: ~500MB
- **模型大小**: ~50MB
- **訓練時間**: ~5-10 分鐘

---

## 進階設置

### 調整模型參數

編輯 `train_model.py` 中的參數：

```python
# 特徵數量
max_features=5000  # 增加以提高準確度，降低以加速

# N-gram 範圍
ngram_range=(1, 2)  # (1,3) 可能更準確但更慢

# 正則化強度
alpha=1.0  # 增加以增強正則化
```

### 自定義 UI

編輯 `app.py` 中的顏色和配置：

```python
# 自定義顏色
colors = ['#4facfe', '#f093fb']  # 修改為你的顏色

# 自定義標題
st.title("你的應用名稱")
```

---

## 反饋與支持

### 報告問題
- GitHub Issues: https://github.com/WYC1297/HW5-AI-Detector/issues
- 提供詳細信息：文本、預測結果、系統配置

### 功能建議
- 在 GitHub Discussions 中提出建議
- 或直接提交 Pull Request

### 聯繫方式
- Email: wyc1297@gmail.com
- GitHub: @WYC1297

---

## 相關資源

### 文檔
- [README.md](README.md) - 項目概述
- [AI_Conversation_Log.md](AI_Conversation_Log.md) - 開發對話記錄
- [train_model.py](train_model.py) - 模型訓練代碼

### 外部資源
- [Streamlit 官方文檔](https://docs.streamlit.io/)
- [Scikit-learn 文檔](https://scikit-learn.org/)
- [NLP 基礎教程](https://www.coursera.org/learn/natural-language-processing)

---

**版本**: 1.0.0  
**最後更新**: 2025年12月6日  
**語言**: 繁體中文 / English

---

**祝你使用愉快！** 🚀
