from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

# 創建數據目錄
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

def setup_driver():
    """設置並返回 webdriver"""
    service = Service(ChromeDriverManager().install())
    
    options = webdriver.ChromeOptions()
    
    # 檢查是否在 Docker 環境中
    if os.path.exists('/.dockerenv'):
        options.binary_location = "/usr/bin/chromium"  # 只在 Docker 中設置
    
    # 加入無頭模式設置
    options.add_argument("--headless=new")  # 新版無頭模式
    options.add_argument("--window-size=1920,1080")  # 設置視窗大小
    options.add_argument('--disable-gpu')  # 無頭模式建議加入
    
    # 其他設置保持不變
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-notifications')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': '''
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        '''
    })
    
    return driver

def get_sp500_data():
    """抓取 SP500 成分股數據"""
    driver = setup_driver()
    stock_dict = {}
    
    try:
        url = "https://www.slickcharts.com/sp500"
        print(f"Accessing URL: {url}")
        driver.get(url)
        time.sleep(10)
        
        # 等待表格加載
        table = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        # 獲取所有行
        rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # 跳過表頭
        
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) >= 3:  # 確保至少有公司名稱和代號欄位
                company_name = cols[1].text.strip()
                symbol = cols[2].text.strip()
                if symbol and company_name:
                    stock_dict[symbol] = company_name
                    print(f"Added: {symbol} -> {company_name}")
        
        return stock_dict
            
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None
        
    finally:
        driver.quit()

def save_stock_data(data, filename):
    """保存數據到文件"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filepath}")

if __name__ == "__main__":
    print("Starting SP500 data collection...")
    
    sp500_data = get_sp500_data()
    
    if sp500_data:
        save_stock_data(sp500_data, "sp500_data.json")
        print(f"\n✓ Successfully collected {len(sp500_data)} SP500 stocks")
    else:
        print("\n✗ Failed to collect SP500 data")