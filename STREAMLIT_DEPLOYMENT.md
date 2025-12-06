# 🚀 Streamlit Cloud 部署指南

## 📋 準備完成清單
- ✅ 代碼已上傳到 GitHub：https://github.com/WYC1297/HW5-AI-Detector
- ✅ 所有依賴已列在 `requirements.txt`
- ✅ Streamlit 配置文件已準備 (`.streamlit/config.toml`)
- ✅ 模型文件已包含在倉庫中

---

## 🔐 部署步驟

### 第1步：訪問 Streamlit Cloud

1. 打開瀏覽器訪問 https://share.streamlit.io
2. 點擊右上角 **「Sign in」** 按鈕
3. 選擇 **「Continue with GitHub」**
4. 授權 Streamlit 訪問你的 GitHub 帳戶

### 第2步：創建新應用

1. 登錄後，點擊 **「New app」** 按鈕
2. 在表單中填入以下信息：

   | 字段 | 值 |
   |-----|-----|
   | **Repository** | `WYC1297/HW5-AI-Detector` |
   | **Branch** | `main` |
   | **Main file path** | `app.py` |

3. 點擊 **「Deploy」** 按鈕

### 第3步：等待部署完成

- 部署通常需要 **2-5 分鐘**
- 可以在頁面上實時查看部署日誌
- 完成後會自動打開應用頁面

---

## 🎯 部署後的 URL

部署完成後，你的應用將可以通過以下 URL 訪問：

```
https://hw5-ai-detector.streamlit.app
```

或根據你的設置，可能是：
```
https://<your-username>-hw5-ai-detector.streamlit.app
```

**確切 URL 會在部署完成後顯示**

---

## ✨ 功能檢查清單

部署後，請驗證以下功能是否正常運作：

### 基本功能
- ✅ 應用載入無錯誤
- ✅ 側邊欄顯示正確
- ✅ 模型信息顯示正確

### 測試功能
- ✅ 點擊「加載 AI 生成的範例」按鈕 → 文本加載
- ✅ 點擊「加載人類撰寫的範例」按鈕 → 文本加載
- ✅ 多次點擊按鈕 → 每次顯示不同範例
- ✅ 輸入自己的文本 → 可以分析

### 分析功能
- ✅ 點擊「🔍 分析」按鈕 → 顯示結果
- ✅ 顯示 AI/Human 概率
- ✅ 顯示信心度百分比
- ✅ 圖表正確顯示
- ✅ 統計信息顯示正確

### 高級功能
- ✅ 特徵分析部分顯示
- ✅ 特徵對比表格正確
- ✅ 可視化圖表正確
- ✅ 判別依據信息完整

---

## 🔧 常見問題解決

### 問題1：部署失敗，顯示「Module not found」

**解決方案：**
- 確認 `requirements.txt` 中包含所有依賴
- 檢查 `app.py` 中的 import 語句

### 問題2：模型文件無法找到

**解決方案：**
- 確認 `models/` 文件夾已上傳到 GitHub
- 檢查路徑是否正確：`./models/ai_detector_model.pkl`

### 問題3：應用加載緩慢

**解決方案：**
- 模型加載使用了 `@st.cache_resource` 裝飾器，首次加載會較慢
- 第一次訪問可能需要 30-60 秒
- 之後會快速加載（從緩存）

### 問題4：CSV 文件顯示為指針

**解決方案：**
- 這是正常的！Git LFS 指針文件已正確配置
- 應用不需要直接讀取 CSV（模型已訓練）

---

## 📊 應用監控

部署後，可以在 Streamlit Cloud 儀表板中監控應用：

- **App health** - 應用健康狀態
- **Logs** - 實時日誌查看
- **Settings** - 修改部署設置
- **Share** - 分享應用 URL

---

## 🔄 更新應用

如果在本地做了修改，只需：

```powershell
git add .
git commit -m "修改說明"
git push origin main
```

Streamlit Cloud 會自動檢測更新並重新部署（通常在 2-5 分鐘內）

---

## 📝 提交信息

完成部署後，記錄以下信息用於作業提交：

**AI 對話日誌:** ✅ `AI_Conversation_Log.md`

**GitHub 倉庫:** ✅ https://github.com/WYC1297/HW5-AI-Detector

**Streamlit Demo:** 🌐 https://hw5-ai-detector.streamlit.app（部署完成後）

---

## 💡 提示

- 如遇到任何問題，檢查 Streamlit Cloud 的部署日誌
- 大文件通過 Git LFS 管理，不會影響部署速度
- 應用是完全公開的，任何人都可以訪問你的 URL

祝部署順利！🎉
