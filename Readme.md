# ChronoSync - 共用行事曆

ChronoSync 是一個共用行事曆應用，旨在幫助團隊成員協調和計劃活動。

## 功能

- 共用行事曆
- 事件增刪查改
- 團隊成員之間的事件同步
- [其他功能...]

## 開始使用

### 前置要求

- Node.js
- MongoDB

Table of Contents

- [專案簡介](#專案簡介)
- [開啟流程](#開啟流程)
  - [一、 建立資料庫](#一-建立資料庫)
  - [二、 啟動後端](#二-啟動後端)
  - [三、 啟動前端](#三-啟動前端)
- [簡短示例](#簡短示例)
  - [User](#user)
  - [Admin](#admin)

## 開啟流程

### 二、 啟動後端

#### Setup

`cd backend` 後：
若有用 conda 的話請先 `conda deactivate`
1. 創建虛擬環境
    ```sh
    python3 -m venv venv
    ```
   - 替代方法（VSCode）：在 VSCode 裡打開 Command Palette，用 Python: Create Environment 選擇 venv，否則 VSCode 可能會找不到對應的 intepreter
2. 進入虛擬環境
   - （Windows）：
     ```sh
     .venv/Scripts/activate
     ```
   - （MacOS）：
     ```sh
     source .venv/bin/activate
     ```
3. 安裝所需套件
   ```sh
   pip install -r requirements.txt
   ```

#### Run the server

進入 backend 與虛擬環境後：

1. ```sh
   cd app
   ```
2. 用 uvicorn 替 FastAPI 開啟 server
   ```sh
   uvicorn main:app --reload
   ```
4. 接著上 http://localhost:8000/docs ，如果可以看到 APIs 就成功了！

### 三、 啟動前端

1. 再開一個 terminal
2. ```sh
   cd src/frontend
   ```
3. 安裝 dependencies
   ```sh
   npm install
   ```
4. 開啟 server
   ```sh
   npm run dev
   ```
5. 開啟 http://localhost:5173 （建議使用 Google Chrome），就可以使用網站啦！