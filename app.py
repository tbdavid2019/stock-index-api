from fastapi import FastAPI, HTTPException
from typing import Dict, Optional, List
import json
import os

app = FastAPI(
    title="Stock Index API",
    description="提供全球市場（台股、美股、日股、港股、歐股）指數與全市場成分股查詢微服務"
)

# 數據目錄
DATA_DIR = "data"

# 市場與支援指數分類
MARKET_INDICES = {
    "TW": [
        "0050", "0100", "0056", "00878", "00919", "00929", "00940",
        "00713", "00850", "TPEX50", "TAIEX", "TPEX", "TW_ALL"
    ],
    "US": ["SP500", "NASDAQ100", "DOWJONES", "SOX"],
    "JP": ["NIKKEI225"],
    "HK": ["HSI", "HSTECH"],
    "EU": ["DAX40", "FTSE100", "EUROSTOXX50"]
}

# 指數別名與檔案映射 (市場, 檔名, 規範指數名)
INDEX_FILE_MAPPING = {
    # 台灣證券交易所與熱門指數
    "0050": ("TW", "tw0050_data.json", "0050"),
    "TW0050": ("TW", "tw0050_data.json", "0050"),
    "0100": ("TW", "tw0100_data.json", "0100"),
    "TW0100": ("TW", "tw0100_data.json", "0100"),
    "0051": ("TW", "tw0100_data.json", "0100"),
    "TW0051": ("TW", "tw0100_data.json", "0100"),
    "0056": ("TW", "tw0056_data.json", "0056"),
    "TW0056": ("TW", "tw0056_data.json", "0056"),
    "00878": ("TW", "tw00878_data.json", "00878"),
    "TW00878": ("TW", "tw00878_data.json", "00878"),
    "00919": ("TW", "tw00919_data.json", "00919"),
    "TW00919": ("TW", "tw00919_data.json", "00919"),
    "00929": ("TW", "tw00929_data.json", "00929"),
    "TW00929": ("TW", "tw00929_data.json", "00929"),
    "00940": ("TW", "tw00940_data.json", "00940"),
    "TW00940": ("TW", "tw00940_data.json", "00940"),
    "00713": ("TW", "tw00713_data.json", "00713"),
    "TW00713": ("TW", "tw00713_data.json", "00713"),
    "00850": ("TW", "tw00850_data.json", "00850"),
    "TW00850": ("TW", "tw00850_data.json", "00850"),
    "TPEX50": ("TW", "tpex50_data.json", "TPEX50"),
    "006201": ("TW", "tpex50_data.json", "TPEX50"),
    "TAIEX": ("TW", "taiex_data.json", "TAIEX"),
    "TWSE": ("TW", "taiex_data.json", "TAIEX"),
    "TSE": ("TW", "taiex_data.json", "TAIEX"),
    "TPEX": ("TW", "tpex_data.json", "TPEX"),
    "OTC": ("TW", "tpex_data.json", "TPEX"),
    "TW_ALL": ("TW", "twall_data.json", "TW_ALL"),
    "TWALL": ("TW", "twall_data.json", "TW_ALL"),
    "ALL_TW": ("TW", "twall_data.json", "TW_ALL"),

    # 美股四大主流指數
    "SP500": ("US", "sp500_data.json", "SP500"),
    "S&P500": ("US", "sp500_data.json", "SP500"),
    "NASDAQ100": ("US", "nasdaq100_data.json", "NASDAQ100"),
    "NDX": ("US", "nasdaq100_data.json", "NASDAQ100"),
    "DOWJONES": ("US", "dowjones_data.json", "DOWJONES"),
    "DJI": ("US", "dowjones_data.json", "DOWJONES"),
    "SOX": ("US", "sox_data.json", "SOX"),
    "PHLX": ("US", "sox_data.json", "SOX"),
    "SOXX": ("US", "sox_data.json", "SOX"),

    # 日股日經 225
    "NIKKEI225": ("JP", "nikkei225_data.json", "NIKKEI225"),
    "N225": ("JP", "nikkei225_data.json", "NIKKEI225"),
    "JP225": ("JP", "nikkei225_data.json", "NIKKEI225"),

    # 港股恒生與恒生科技
    "HSI": ("HK", "hsi_data.json", "HSI"),
    "HANGSENG": ("HK", "hsi_data.json", "HSI"),
    "HSTECH": ("HK", "hstech_data.json", "HSTECH"),

    # 歐股德國、英國與泛歐
    "DAX40": ("EU", "dax40_data.json", "DAX40"),
    "DAX": ("EU", "dax40_data.json", "DAX40"),
    "FTSE100": ("EU", "ftse100_data.json", "FTSE100"),
    "FTSE": ("EU", "ftse100_data.json", "FTSE100"),
    "UK100": ("EU", "ftse100_data.json", "FTSE100"),
    "EUROSTOXX50": ("EU", "eurostoxx50_data.json", "EUROSTOXX50"),
    "SX5E": ("EU", "eurostoxx50_data.json", "EUROSTOXX50"),
    "STOXX50": ("EU", "eurostoxx50_data.json", "EUROSTOXX50")
}

def load_stock_data(file_name: str) -> Dict:
    """載入股票數據（具備相容性備援搜尋）"""
    try:
        path = os.path.join(DATA_DIR, file_name)
        if not os.path.exists(path):
            # 支援舊版命名 stock_data_0050 -> fund_0050.json 或 tw0050_data.json
            if "stock_data_" in file_name:
                alt1 = file_name.replace("stock_data_", "fund_")
                alt2 = file_name.replace("stock_data_", "tw") + "_data.json"
                for alt in [alt1, alt2]:
                    alt_path = os.path.join(DATA_DIR, alt)
                    if os.path.exists(alt_path):
                        path = alt_path
                        break
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


@app.get("/")
async def read_root():
    """API 根路徑"""
    return {
        "message": "Welcome to Stock Index API (Global & Taiwan Equities Universe)",
        "supported_markets": list(MARKET_INDICES.keys()),
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
    """獲取所有市場可用的指數與大盤列表"""
    return {"indices": MARKET_INDICES}


@app.get("/stocks/{index_name}")
async def get_index_stocks(index_name: str):
    """獲取指定指數或大盤的所有成分股"""
    index_clean = index_name.strip().upper()
    
    if index_clean in INDEX_FILE_MAPPING:
        market, filename, canonical = INDEX_FILE_MAPPING[index_clean]
        data = load_stock_data(filename)
        if not data:
            raise HTTPException(status_code=404, detail=f"Data for {index_name} not found")
        return {"market": market, "index": canonical, "stocks": data}

    # 舊版命名相容相依性檢查
    legacy_file = f"stock_data_{index_clean.lower()}.json"
    legacy_path = os.path.join(DATA_DIR, legacy_file)
    if os.path.exists(legacy_path):
        data = load_stock_data(legacy_file)
        return {"market": "TW", "index": index_clean, "stocks": data}

    raise HTTPException(status_code=404, detail=f"Index '{index_name}' not found")


@app.get("/stock/{stock_code}")
async def get_stock_info(stock_code: str):
    """根據股票代號查詢全球所屬市場與指數公司資訊"""
    result = {}
    code_raw = stock_code.strip()
    code_upper = code_raw.upper()

    # 1. 檢查台股 (TW)
    bare_tw = code_upper.replace(".TW", "").replace(".TWO", "")
    for idx in MARKET_INDICES["TW"]:
        _, filename, canonical = INDEX_FILE_MAPPING[idx]
        data = load_stock_data(filename)
        for c in [code_raw, code_upper, bare_tw]:
            if c in data:
                result["TW"] = {
                    "index": canonical,
                    "company": data[c]
                }
                break
        if "TW" in result:
            break

    # 2. 檢查美股 (US)
    for idx in MARKET_INDICES["US"]:
        _, filename, canonical = INDEX_FILE_MAPPING[idx]
        data = load_stock_data(filename)
        for c in [code_raw, code_upper]:
            if c in data:
                result["US"] = {
                    "index": canonical,
                    "company": data[c]
                }
                break
        if "US" in result:
            break

    # 3. 檢查日股 (JP)
    bare_jp = code_upper.replace(".T", "")
    for idx in MARKET_INDICES["JP"]:
        _, filename, canonical = INDEX_FILE_MAPPING[idx]
        data = load_stock_data(filename)
        for c in [code_raw, code_upper, f"{bare_jp}.T", bare_jp]:
            if c in data:
                result["JP"] = {
                    "index": canonical,
                    "company": data[c]
                }
                break
        if "JP" in result:
            break

    # 4. 檢查港股 (HK)
    bare_hk = code_upper.replace(".HK", "")
    padded_hk = bare_hk.zfill(4)
    for idx in MARKET_INDICES["HK"]:
        _, filename, canonical = INDEX_FILE_MAPPING[idx]
        data = load_stock_data(filename)
        for c in [code_raw, code_upper, f"{padded_hk}.HK", padded_hk, bare_hk]:
            if c in data:
                result["HK"] = {
                    "index": canonical,
                    "company": data[c]
                }
                break
        if "HK" in result:
            break

    # 5. 檢查歐股 (EU)
    for idx in MARKET_INDICES["EU"]:
        _, filename, canonical = INDEX_FILE_MAPPING[idx]
        data = load_stock_data(filename)
        for c in [code_raw, code_upper]:
            if c in data:
                result["EU"] = {
                    "index": canonical,
                    "company": data[c]
                }
                break
        if "EU" in result:
            break

    if not result:
        raise HTTPException(status_code=404, detail=f"Stock '{stock_code}' not found across all markets")
    return result


@app.get("/search/{company_name}")
async def search_company(company_name: str):
    """根據公司名稱搜尋全球股票（跨市場模糊搜尋）"""
    query = company_name.lower().strip()
    result = {m: {} for m in MARKET_INDICES.keys()}

    for market, indices in MARKET_INDICES.items():
        for idx in indices:
            _, filename, canonical = INDEX_FILE_MAPPING[idx]
            data = load_stock_data(filename)
            matches = {
                code: name for code, name in data.items()
                if query in name.lower() or query in code.lower()
            }
            if matches:
                result[market][canonical] = matches

    # 清理沒有結果的市場
    result = {k: v for k, v in result.items() if v}
    if not result:
        raise HTTPException(status_code=404, detail=f"No matches found for '{company_name}'")
    return result


@app.get("/market/{market}")
async def get_market_stocks(market: str):
    """獲取指定市場的所有指數與成分股數據"""
    market_upper = market.upper().strip()
    if market_upper not in MARKET_INDICES:
        raise HTTPException(
            status_code=404,
            detail=f"Invalid market '{market}'. Supported markets: {list(MARKET_INDICES.keys())}"
        )

    result = {}
    for idx in MARKET_INDICES[market_upper]:
        _, filename, canonical = INDEX_FILE_MAPPING[idx]
        data = load_stock_data(filename)
        if data:
            result[canonical] = data

    if not result:
        raise HTTPException(status_code=404, detail=f"No data found for market '{market}'")
    return {"market": market_upper, "data": result}
