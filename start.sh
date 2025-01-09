#!/bin/bash

# 首次運行爬蟲
echo "Initial crawling..."
python crawler.py
python crawler-sp500.py

# 啟動 cron
service cron start

# 啟動 API 服務
uvicorn app:app --host 0.0.0.0 --port 8000