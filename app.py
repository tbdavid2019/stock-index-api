from fastapi import FastAPI, HTTPException
from typing import Dict, Optional, List
import json
import os

app = FastAPI(
    title="Stock Index API",
    description="提供台股指數與美股 SP500、NASDAQ100、道瓊斯指數成分股查詢服務"
)

# 數據目錄
DATA_DIR = "data"

# 定義美股指數列表
US_INDICES = ["SP500", "NASDAQ100", "DOWJONES"]

def load_stock_data(file_name: str) -> Dict:
    """載入股票數據"""
    try:
        with open(os.path.join(DATA_DIR, file_name), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

@app.get("/")
async def read_root():
    """API 根路徑"""
    return {
        "message": "Welcome to Stock Index API",
        "available_endpoints": [
            "/indices",
            "/stocks/{index_name}",
            "/stock/{stock_code}",
            "/search/{company_name}",
            "/market/{market}"
        ]
    }

@app.get("/indices")
async def get_indices():
    """獲取所有可用的指數列表"""
    indices = {
        "TW": ["0050", "0100"],
        "US": US_INDICES
    }
    return {"indices": indices}

@app.get("/stocks/{index_name}")
async def get_index_stocks(index_name: str):
    """獲取指定指數的所有成分股"""
    index_name = index_name.upper()
    
    if index_name in US_INDICES:
        data = load_stock_data(f"{index_name.lower()}_data.json")
        if not data:
            raise HTTPException(status_code=404, detail=f"{index_name} data not found")
        return {"market": "US", "index": index_name, "stocks": data}
    elif index_name in ["0050", "0100"]:
        data = load_stock_data(f"stock_data_{index_name}.json")
        if not data:
            raise HTTPException(status_code=404, detail=f"Data for {index_name} not found")
        return {"market": "TW", "index": index_name, "stocks": data}
    else:
        raise HTTPException(status_code=404, detail="Invalid index name")

@app.get("/stock/{stock_code}")
async def get_stock_info(stock_code: str):
    """根據股票代號查詢公司資訊"""
    result = {}
    
    # 檢查台股
    tw_indices = ["0050", "0100"]
    for index in tw_indices:
        data = load_stock_data(f"stock_data_{index}.json")
        if stock_code in data:
            result["TW"] = {
                "index": index,
                "company": data[stock_code]
            }
    
    # 檢查美股
    for index in US_INDICES:
        data = load_stock_data(f"{index.lower()}_data.json")
        if stock_code in data:
            result["US"] = {
                "index": index,
                "company": data[stock_code]
            }

    if not result:
        raise HTTPException(status_code=404, detail=f"Stock {stock_code} not found")
    return result

@app.get("/search/{company_name}")
async def search_company(company_name: str):
    """根據公司名稱搜尋股票（模糊搜尋）"""
    result = {"TW": {}, "US": {}}
    
    # 搜尋台股
    tw_indices = ["0050", "0100"]
    for index in tw_indices:
        data = load_stock_data(f"stock_data_{index}.json")
        matches = {code: name for code, name in data.items() 
                  if company_name.lower() in name.lower()}
        if matches:
            result["TW"][index] = matches
    
    # 搜尋美股
    for index in US_INDICES:
        data = load_stock_data(f"{index.lower()}_data.json")
        matches = {code: name for code, name in data.items() 
                  if company_name.lower() in name.lower()}
        if matches:
            result["US"][index] = matches

    if not result["TW"] and not result["US"]:
        raise HTTPException(status_code=404, 
                          detail=f"No matches found for {company_name}")
    return result

@app.get("/market/{market}")
async def get_market_stocks(market: str):
    """獲取指定市場的所有股票"""
    market = market.upper()
    result = {}
    
    if market == "TW":
        for index in ["0050", "0100"]:
            data = load_stock_data(f"stock_data_{index}.json")
            if data:
                result[index] = data
    elif market == "US":
        for index in US_INDICES:
            data = load_stock_data(f"{index.lower()}_data.json")
            if data:
                result[index] = data
    else:
        raise HTTPException(status_code=404, detail="Invalid market")

    if not result:
        raise HTTPException(status_code=404,
                          detail=f"No data found for market {market}")
    return {"market": market, "data": result}