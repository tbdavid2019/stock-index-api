from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import os
import platform
import re

# 創建數據目錄
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def setup_driver():
    """設置並返回 webdriver"""
    options = webdriver.ChromeOptions()
    
    # 判斷是否在 Docker 環境
    if os.path.exists('/.dockerenv'):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/usr/bin/chromium"
    else:
        # 本地開發環境 (macOS)
        options.add_argument("--headless=new")
        if platform.system() == 'Darwin':
            options.binary_location = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    
    try:
        # Selenium 4.6+ 會自動管理 driver，不需要手動指定
        driver = webdriver.Chrome(options=options)
        return driver
    except Exception as e:
        print(f"Driver 初始化失敗: {e}")
        return None

def fetch_goodinfo_components(driver, etf_name):
    """
    從 Goodinfo 抓取 ETF 成分股
    etf_name: '0050' 或 '中100' (中型100)
    """
    # URL encode 中文
    import urllib.parse
    keyword = f"{etf_name}成分股"
    encoded = urllib.parse.quote(keyword)
    url = f"https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=%E7%86%B1%E9%96%80%E6%8E%92%E8%A1%8C&INDUSTRY_CAT={encoded}"
    
    print(f"前往 Goodinfo: {url}")
    
    try:
        driver.get(url)
        time.sleep(5)
        
        stock_dict = {}
        
        # Goodinfo 的資料表格 ID 是 tblStockList
        table = driver.find_element(By.ID, "tblStockList")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        print(f"找到 {len(rows)} 列資料")
        
        for row in rows[1:]:  # 跳過表頭
            try:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 2:
                    code = cols[0].text.strip()
                    name = cols[1].text.strip()
                    
                    # 驗證股票代碼 (4位數字)
                    if code.isdigit() and len(code) == 4 and name:
                        stock_dict[code] = name
            except:
                continue
        
        return stock_dict if len(stock_dict) > 0 else None
        
    except Exception as e:
        print(f"Goodinfo 抓取錯誤: {e}")
        return None

def save_json(data, filename):
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"資料已寫入: {filepath}")

if __name__ == "__main__":
    
    # Goodinfo 的分類名稱
    # 0050成分股, 中100成分股
    targets = {
        "0050": "0050",
        "0100": "中100"
    }
    
    driver = setup_driver()
    if not driver:
        print("無法初始化瀏覽器，程式結束")
        exit(1)
        
    all_data = {}
    
    try:
        for output_name, goodinfo_name in targets.items():
            print(f"\n{'='*50}")
            print(f"正在抓取 {output_name} ({goodinfo_name}) 成分股")
            print(f"{'='*50}")
            
            data = fetch_goodinfo_components(driver, goodinfo_name)
            
            if data and len(data) > 0:
                print(f"✓ 成功抓到 {len(data)} 檔成分股")
                save_json(data, f"stock_data_{output_name}.json")
                all_data[output_name] = data
            else:
                print(f"✗ {output_name} 抓取失敗")
            
            # 避免請求太快被擋
            time.sleep(3)
                
        # 彙總存檔
        if all_data:
            save_json(all_data, "all_stock_data.json")
            print(f"\n總結: 成功抓取 {len(all_data)} 個 ETF 的成分股")
        else:
            print("\n抓取失敗！")
            
    finally:
        driver.quit()