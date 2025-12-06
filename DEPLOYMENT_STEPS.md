# 🚀 GitHub 部署步驟

已完成本地 Git 初始化和首次提交。現在需要完成以下步驟將項目推送到 GitHub：

## 📋 必要步驟

### 1️⃣ 在 GitHub 上創建新倉庫

1. 登錄 [GitHub](https://github.com)
2. 點擊右上角 `+` 圖標 → `New repository`
3. 倉庫名稱：`HW5-AI-Detector` （或你喜歡的名稱）
4. 描述：`AI/Human Article Detection Tool with Machine Learning`
5. **不要** 初始化 README、.gitignore 或 License（我們已有這些文件）
6. 點擊 `Create repository`

### 2️⃣ 複製遠程倉庫 URL

在 GitHub 倉庫頁面，點擊綠色 `Code` 按鈕，複製 HTTPS URL（例如：`https://github.com/你的用戶名/HW5-AI-Detector.git`）

### 3️⃣ 在本地推送到 GitHub

在 PowerShell 中運行以下命令（將 `<你的HTTPS_URL>` 替換為實際的倉庫 URL）：

```powershell
cd "c:\Users\WANG\Desktop\WANG\研究所\課程\碩二上\物聯網\HW5"
git remote add origin <你的HTTPS_URL>
git branch -M main
git push -u origin main
```

**示例：**
```powershell
git remote add origin https://github.com/WYC1297/HW5-AI-Detector.git
git branch -M main
git push -u origin main
```

### 4️⃣ 驗證推送成功

- 刷新 GitHub 倉庫頁面
- 確認所有文件已上傳
- 檢查 README.md 是否正確顯示

---

## 📝 當前本地倉庫狀態

```
✅ Git 初始化完成
✅ 所有文件已添加
✅ 首次提交已完成（92c6890）
⏳ 等待遠程推送（需手動執行）
```

### 已提交的文件清單
- ✅ `app.py` - Streamlit 應用主程序
- ✅ `train_model.py` - 模型訓練腳本
- ✅ `requirements.txt` - Python 依賴列表
- ✅ `README.md` - 項目說明文檔
- ✅ `USAGE_GUIDE.md` - 使用指南
- ✅ `AI_Conversation_Log.md` - AI 對話日誌
- ✅ `QUICKSTART.md` - 快速開始指南
- ✅ `AI_Human.csv` - 訓練數據
- ✅ `.gitignore` - Git 配置文件
- ✅ `models/` - 訓練好的模型文件夾

---

## 🔗 後續步驟：Streamlit Cloud 部署

推送到 GitHub 後，可以在 [Streamlit Cloud](https://share.streamlit.io) 進行部署：

1. 訪問 https://share.streamlit.io
2. 使用 GitHub 帳號登錄
3. 點擊「New app」
4. 選擇倉庫：`HW5-AI-Detector`
5. 分支：`main`
6. 文件路徑：`app.py`
7. 點擊「Deploy」

部署完成後，你將獲得一個公開 URL，例如：`https://hw5-ai-detector.streamlit.app`

---

## ❓ 常見問題

**Q: 如何更新已推送的代碼？**
```powershell
git add .
git commit -m "功能說明"
git push origin main
```

**Q: 如果出現推送錯誤？**
- 確認 GitHub 帳號和密碼正確
- 如果使用二次驗證，需生成 Personal Access Token
- 或使用 SSH 密鑰替代 HTTPS

**Q: 大文件（CSV 數據）會影響推送嗎？**
- 可以，建議用 `git lfs` 管理大文件
- 或將 CSV 放在 `.gitignore` 中，部署時通過其他方式獲取

---

## 需要幫助？

- [GitHub 文檔](https://docs.github.com)
- [Streamlit 部署指南](https://docs.streamlit.io/streamlit-cloud/deploy-your-app)
