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

def get_stock_data(index_code):
    """抓取指定指數的成分股數據"""
    driver = setup_driver()
    stock_dict = {}
    
    try:
        url = f"https://www.wantgoo.com/index/{index_code}/stocks"
        driver.get(url)
        time.sleep(10)
        
        # 嘗試定位表格
        table = None
        selectors = [
            "//table[contains(@class, 'constituent-list')]",
            "//div[contains(@class, 'table')]//table",
            "//table"
        ]
        
        for selector in selectors:
            try:
                table = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if table:
                    break
            except:
                continue
        
        if table:
            rows = table.find_elements(By.TAG_NAME, "tr")[1:]  # 跳過表頭
            
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if cols:
                    company_info = cols[0].text.split('\n')
                    if len(company_info) == 2:
                        stock_code = company_info[1].strip()  # 股票代號
                        company_name = company_info[0]        # 公司名稱
                        stock_dict[stock_code] = company_name
                        print(f"Added: {stock_code} -> {company_name}")
            
            return stock_dict
        else:
            print("無法找到表格元素")
            return None
            
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
    # 定義要抓取的指數列表
    indices = {
        "^539": "0050",
        "^543": "0100"
    }
    
    # 抓取所有指數的成分股
    all_data = {}
    
    for index_code, index_name in indices.items():
        print(f"\nFetching data for {index_name}...")
        stock_data = get_stock_data(index_code)
        
        if stock_data:
            all_data[index_name] = stock_data
            # 保存單個指數的數據
            save_stock_data(stock_data, f"stock_data_{index_name}.json")
            print(f"Successfully fetched {len(stock_data)} stocks for {index_name}")
        else:
            print(f"Failed to fetch data for {index_name}")
    
    # 保存所有數據到一個文件
    if all_data:
        save_stock_data(all_data, "all_stock_data.json")
        print("\nAll data saved successfully!")
    else:
        print("\nNo data was collected!")