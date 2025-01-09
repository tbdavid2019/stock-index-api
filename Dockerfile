# 使用 Python 3.9 作為基礎映像
FROM python:3.9-slim

# 設置工作目錄
WORKDIR /app

# 安裝 Chrome 和相關依賴
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*

# 複製需要的文件
COPY requirements.txt .
COPY app.py .
COPY crawler.py .
COPY crawler-sp500.py .
COPY crontab /etc/cron.d/crontab

# 創建數據目錄
RUN mkdir -p data

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

# 安裝 cron
RUN apt-get update && apt-get -y install cron

# 設置 crontab
RUN chmod 0644 /etc/cron.d/crontab
RUN crontab /etc/cron.d/crontab

# 創建啟動腳本
COPY start.sh .
RUN chmod +x start.sh

# 暴露端口
EXPOSE 8000

# 運行啟動腳本
CMD ["./start.sh"]