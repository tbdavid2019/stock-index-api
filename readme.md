
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

- Python 3.9+
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
python crawler-sp500.py
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

## 常見問題

### Q: 如何修改更新時間？
A: 修改 `crontab` 檔案中的排程設定。

### Q: 資料儲存在哪裡？
A: 所有資料都儲存在 `data` 目錄下的 JSON 檔案中。

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
python crawler-sp500.py
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
