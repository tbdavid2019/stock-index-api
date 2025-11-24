
# 股票指數 API

一個基於 FastAPI 的服務，提供台灣 ETF（0050、0100）和標普 500 指數的成分股資訊。

## 功能特點

- 🔄 每日自動更新股票成分資料
- 🌏 支援台灣和美國市場
- 🔍 靈活的搜尋功能
- 🐳 Docker 支援與自動排程
- 📊 RESTful API 端點

## API 端點

- `/` - API 介紹和可用端點列表
- `/indices` - 獲取所有可用指數
- `/stocks/{index_name}` - 獲取特定指數的成分股
- `/stock/{stock_code}` - 依股票代號搜尋
- `/search/{company_name}` - 依公司名稱搜尋（模糊搜尋）
- `/market/{market}` - 獲取指定市場（TW/US）的所有股票

## 系統需求

- Python 3.11+
- Docker 和 Docker Compose（用於容器化部署）
- Chrome/Chromium（用於網路爬蟲）

## 安裝說明

1. 複製專案：
```bash
git clone https://github.com/tbdavid2019/stock-index-api.git
cd stock-index-api
```

2. 設置虛擬環境（建議但非必要）：
```bash
python -m venv myenv
source myenv/bin/activate  # Windows 系統使用：myenv\Scripts\activate
```

3. 安裝相依套件：
```bash
pip install -r requirements.txt
```

## 使用方法

### 本地開發

1. 執行爬蟲獲取初始資料：
```bash
python crawler.py
python crawler-i18n.py
```

2. 啟動 API 伺服器：
```bash
uvicorn app:app --reload
```

API 將在 `http://localhost:8000` 運行

### Docker 部署

1. 建立並啟動容器：
```bash
docker-compose up --build -d
```

這個指令會：
- 建立 Docker 映像檔
- 在端口 8000 啟動服務
- 設置每日凌晨 01:00 更新資料
- 建立持久化資料存儲

2. 停止服務：
```bash
docker-compose down
```

## API 文檔

服務運行後，可訪問：
- Swagger UI：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

## 資料來源

- 台灣 ETF 成分股：[玩股網](https://www.wantgoo.com/)
- 標普 500 成分股：[SlickCharts](https://www.slickcharts.com/sp500)

## 專案結構

```
stock-index-api/
├── app.py              # FastAPI 應用程式
├── crawler.py          # 台股爬蟲
├── crawler-sp500.py    # 標普 500 爬蟲
├── requirements.txt    # Python 相依套件
├── Dockerfile         
├── docker-compose.yml
├── start.sh           # Docker 啟動腳本
├── crontab            # 排程任務
└── data/              # 股票資料儲存
```

## 開發指南

### 新增功能

1. 建立新分支：
```bash
git checkout -b feature/your-feature-name
```

2. 進行修改
3. 提交 Pull Request

### 執行測試

```bash
# TODO: 新增測試說明
```

## 參與貢獻

1. Fork 本專案
2. 建立功能分支
3. 提交變更
4. 推送到分支
5. 建立 Pull Request

## 授權條款

本專案使用 MIT 授權條款 - 詳見 LICENSE 檔案

## 聯絡方式

- 作者：[@tbdavid2019](https://github.com/tbdavid2019)
- 專案連結：[https://github.com/tbdavid2019/stock-index-api](https://github.com/tbdavid2019/stock-index-api)

## 致謝

- [FastAPI](https://fastapi.tiangolo.com/)
- [Selenium](https://www.selenium.dev/)
- [Docker](https://www.docker.com/)

## 更新日誌

### [1.0.0] - 2024-01-XX
- 初始版本發布
- 支援台股 ETF（0050、0100）成分股查詢
- 支援標普 500 成分股查詢
- Docker 容器化部署支援
- 自動更新排程

## 更新個股指數資料

### 資料更新流程

本專案透過爬蟲自動抓取最新的指數成分股資料：

**台股指數 (0050, 0100)**
- 執行 `crawler.py` → 爬取玩股網的成分股資料
- 產生檔案：`stock_data_0050.json`, `stock_data_0100.json`

**美股指數 (SP500, NASDAQ100, DOWJONES)**
- 執行 `crawler-i18n.py` → 爬取 SlickCharts 的資料
- 產生檔案：`sp500_data.json`, `nasdaq100_data.json`, `dowjones_data.json`

### 手動更新步驟

```bash
# 1. 啟動虛擬環境
source myenv/bin/activate

# 2. 執行爬蟲（更新台股）
python crawler.py

# 3. 執行爬蟲（更新美股）
python crawler-i18n.py
```

### 上傳到 Cloudflare KV

將更新後的資料上傳到 Cloudflare Workers KV 儲存：

```bash
# 1. 進入 data 目錄
cd data/

# 2. 登入 Cloudflare (首次需要)
wrangler login

# 3. 上傳各指數資料到 KV
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "SP500" "$(cat sp500_data.json)"
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "TW0050" "$(cat stock_data_0050.json)"
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "TW0051" "$(cat stock_data_0100.json)"
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "nasdaq100" "$(cat nasdaq100_data.json)"
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "dowjones" "$(cat dowjones_data.json)"
```

### 一鍵執行腳本

也可以直接執行完整的更新和上傳流程：

```bash
bash upload2KV.sh
```

這個腳本會自動：
1. 啟動虛擬環境
2. 執行兩個爬蟲更新資料
3. 上傳所有資料到 Cloudflare KV

### 自動化排程

在 Docker 環境中，系統會透過 `crontab` 自動執行：
- **每天凌晨 1:00** - 執行 `crawler.py` 更新台股資料
- **每天凌晨 1:10** - 執行 `crawler-i18n.py` 更新美股資料

### 資料存儲位置

- **本地儲存**：`data/` 目錄下的 JSON 檔案
- **雲端儲存**：Cloudflare Workers KV (Namespace ID: `5e8e4092fd964584a2152c4a6f948d47`)

## 常見問題

### Q: 如何修改更新時間？
A: 修改 `crontab` 檔案中的排程設定。

### Q: 資料儲存在哪裡？
A: 所有資料都儲存在 `data` 目錄下的 JSON 檔案中，並可選擇上傳到 Cloudflare KV 進行雲端儲存。

### Q: 如何確認服務正常運行？
A: 訪問 `http://localhost:8000/docs` 查看 API 文檔和測試端點。


---

# Stock Index API



A FastAPI-based service that provides stock constituent information for Taiwan ETFs (0050, 0100) and S&P 500 index.

## Features

- 🔄 Daily auto-updating stock constituent data
- 🌏 Support for both Taiwan and US markets
- 🔍 Flexible search capabilities
- 🐳 Docker support with automated scheduling
- 📊 RESTful API endpoints

## API Endpoints

- `/` - API introduction and available endpoints
- `/indices` - Get all available indices
- `/stocks/{index_name}` - Get constituents for a specific index
- `/stock/{stock_code}` - Search stock by code
- `/search/{company_name}` - Search companies by name (fuzzy search)
- `/market/{market}` - Get all stocks for specified market (TW/US)

## Prerequisites

- Python 3.9+
- Docker and Docker Compose (for containerized deployment)
- Chrome/Chromium (for web scraping)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tbdavid2019/stock-index-api.git
cd stock-index-api
```

2. Set up a virtual environment (optional but recommended):
```bash
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Local Development

1. Run the crawlers to fetch initial data:
```bash
python crawler.py
python crawler-i18n.py
```

2. Start the API server:
```bash
uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

### Docker Deployment

1. Build and start the container:
```bash
docker-compose up --build -d
```

This will:
- Build the Docker image
- Start the service on port 8000
- Set up daily updates at 01:00
- Create a persistent volume for data storage

2. Stop the service:
```bash
docker-compose down
```

## API Documentation

Once the service is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Data Sources

- Taiwan ETF constituents: [WantGoo](https://www.wantgoo.com/)
- S&P 500 constituents: [SlickCharts](https://www.slickcharts.com/sp500)

## Project Structure

```
stock-index-api/
├── app.py              # FastAPI application
├── crawler.py          # Taiwan stocks crawler
├── crawler-sp500.py    # S&P 500 crawler
├── requirements.txt    # Python dependencies
├── Dockerfile         
├── docker-compose.yml
├── start.sh           # Docker entry point
├── crontab            # Scheduled tasks
└── data/              # Stock data storage
```

## Development

### Adding New Features

1. Create a new branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes
3. Submit a pull request

### Running Tests

```bash
# TODO: Add test instructions
```

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Contact

- Created by [@tbdavid2019](https://github.com/tbdavid2019)
- Project Link: [https://github.com/tbdavid2019/stock-index-api](https://github.com/tbdavid2019/stock-index-api)

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Selenium](https://www.selenium.dev/)
- [Docker](https://www.docker.com/)



```
stock-index-api/
│
├── app.py            # API 服務
├── crawler.py        # 爬蟲程式
├── requirements.txt  # 依賴套件
├── data/            # 存放爬蟲獲取的數據
│   └── .gitkeep
├── README.md        # 專案說明
└── .gitignore       # Git 忽略檔案
```
