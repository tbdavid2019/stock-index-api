import requests
from bs4 import BeautifulSoup
import json
import os

# 創建數據目錄
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


def get_stock_data(index_name):
    """抓取指定指數的成分股數據"""
    urls = {
        'sp500': "https://www.slickcharts.com/sp500",
        'nasdaq100': "https://www.slickcharts.com/nasdaq100",
        'dowjones': "https://www.slickcharts.com/dowjones"
    }
    
    if index_name not in urls:
        print(f"Invalid index name: {index_name}")
        return None

    stock_dict = {}
    try:
        url = urls[index_name]
        print(f"Accessing URL for {index_name}: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        
        if not table:
            print(f"No table found for {index_name}")
            return None
        
        # 獲取所有行（跳過表頭）
        rows = table.find_all('tr')[1:]
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:  # 確保至少有公司名稱和代號欄位
                company_name = cols[1].text.strip()
                symbol = cols[2].text.strip()
                if symbol and company_name:
                    stock_dict[symbol] = company_name
                    print(f"Added {index_name}: {symbol} -> {company_name}")

        return stock_dict
    except Exception as e:
        print(f"Error occurred while fetching {index_name} data: {str(e)}")
        return None

def save_stock_data(data, filename):
    """保存數據到文件"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Data saved to {filepath}")

def collect_all_indices():
    """收集所有指數的數據"""
    indices = {
        'sp500': 'sp500_data.json',
        'nasdaq100': 'nasdaq100_data.json',
        'dowjones': 'dowjones_data.json'
    }
    
    results = {}
    for index_name, filename in indices.items():
        print(f"\nStarting {index_name} data collection...")
        stock_data = get_stock_data(index_name)
        if stock_data:
            save_stock_data(stock_data, filename)
            results[index_name] = len(stock_data)
            print(f"✓ Successfully collected {len(stock_data)} {index_name} stocks")
        else:
            print(f"✗ Failed to collect {index_name} data")
    
    return results

if __name__ == "__main__":
    print("Starting data collection for all indices...")
    results = collect_all_indices()
    
    print("\nCollection Summary:")
    for index_name, count in results.items():
        print(f"{index_name}: {count} stocks collected")