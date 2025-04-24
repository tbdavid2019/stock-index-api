docker build -t stock-index-api .



#運行容器：
docker run -d -p 8090:8000 -v $(pwd)/data:/app/data --name stock-api stock-index-api