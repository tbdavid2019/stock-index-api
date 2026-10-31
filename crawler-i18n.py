import requests
from bs4 import BeautifulSoup
import json
import os
import re

# 創建數據目錄
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 創新科技與太空先鋒股（Frontier Tickers）
FRONTIER_US_STOCKS = {
    "SPCX": "SpaceX (SPCX)",
    "DXYZ": "Destiny Tech100 / SpaceX (DXYZ)",
    "ASTS": "AST SpaceMobile (ASTS)",
    "RKLB": "Rocket Lab (RKLB)",
    "CRWV": "CoreWeave (CRWV)",
    "FN": "Fabrinet (FN)",
    "CLS": "Celestica (CLS)",
}

# 完整 225 檔東京證交所日經 225 內嵌備援清單（保障網路離線或頁面結構變更時不中斷）
FALLBACK_NIKKEI225 = {
    "1332.T": "Nissui",
    "1605.T": "Inpex",
    "1721.T": "Comsys Holdings",
    "1801.T": "Taisei",
    "1802.T": "Obayashi Corp.",
    "1803.T": "Shimizu",
    "1808.T": "Haseko Corp.",
    "1812.T": "Kajima",
    "1925.T": "Daiwa House Industry",
    "1928.T": "Sekisui House",
    "1963.T": "JGC Corporation",
    "2002.T": "Nisshin Seifun Group",
    "2269.T": "Meiji Holdings",
    "2282.T": "NH Foods",
    "2413.T": "M3",
    "2432.T": "Dena",
    "2501.T": "Sapporo Holdings",
    "2502.T": "Asahi Group Holdings",
    "2503.T": "Kirin Holdings",
    "2768.T": "Sojitz",
    "2801.T": "Kikkoman",
    "2802.T": "Ajinomoto",
    "285A.T": "Kioxia Holdings",
    "2871.T": "Nichirei",
    "2914.T": "Japan Tobacco",
    "3086.T": "J. Front Retailing",
    "3092.T": "ZOZO",
    "3099.T": "Isetan Mitsukoshi Holdings",
    "3289.T": "Tokyu Land",
    "3382.T": "Seven & I Holdings Co.",
    "3401.T": "Teijin",
    "3402.T": "Toray Industries",
    "3405.T": "Kuraray",
    "3407.T": "Asahi Kasei",
    "3436.T": "SUMCO",
    "3659.T": "Nexon",
    "3697.T": "SHIFT Inc.",
    "3861.T": "Oji Holdings Corporation",
    "4004.T": "Resonac",
    "4005.T": "Sumitomo Chemical",
    "4021.T": "Nissan Chemical Industries",
    "4042.T": "Tosoh",
    "4043.T": "Tokuyama Corporation",
    "4061.T": "Denka",
    "4063.T": "Shin-Etsu Chemical",
    "4151.T": "Kyowa Hakko Kirin",
    "4183.T": "Mitsui Chemicals",
    "4188.T": "Mitsubishi Chemical Holdings",
    "4208.T": "Ube Industries",
    "4307.T": "Nomura Research Institute",
    "4324.T": "Dentsu",
    "4385.T": "Mercari",
    "4452.T": "Kao Corp.",
    "4502.T": "Takeda Pharmaceutical Company",
    "4503.T": "Astellas Pharma",
    "4506.T": "Sumitomo Dainippon Pharma",
    "4507.T": "Shionogi",
    "4519.T": "Chugai Pharmaceutical",
    "4523.T": "Eisai Co.",
    "4543.T": "Terumo",
    "4568.T": "Daiichi Sankyo",
    "4578.T": "Otsuka Holdings",
    "4661.T": "Oriental Land",
    "4689.T": "LY Corporation",
    "4704.T": "Trend Micro",
    "4751.T": "CyberAgent",
    "4755.T": "Rakuten",
    "4901.T": "Fujifilm Holdings",
    "4902.T": "Konica Minolta Holdings",
    "4911.T": "Shiseido",
    "5019.T": "Idemitsu Kosan",
    "5020.T": "Eneos Holdings",
    "5101.T": "Yokohama Rubber",
    "5108.T": "Bridgestone",
    "5201.T": "AGC Inc.",
    "5214.T": "Nippon Electric Glass",
    "5233.T": "Taiheiyo Cement",
    "5301.T": "Tokai Carbon",
    "5332.T": "Toto Ltd.",
    "5333.T": "NGK Insulators",
    "5401.T": "Nippon Steel",
    "5406.T": "Kobe Steel",
    "5411.T": "JFE Holdings",
    "543A.T": "Archion",
    "5631.T": "Japan Steel Works",
    "5706.T": "Mitsui Mining & Smelting",
    "5711.T": "Mitsubishi Materials",
    "5713.T": "Sumitomo Metal Mining",
    "5714.T": "Dowa Holdings",
    "5801.T": "Furukawa Electric",
    "5802.T": "Sumitomo Electric Industries",
    "5803.T": "Fujikura",
    "5831.T": "Shizuoka Financial Group",
    "6098.T": "Recruit Holdings",
    "6103.T": "Okuma Holdings",
    "6113.T": "Amada Co. Ltd.",
    "6146.T": "Disco Corporation",
    "6178.T": "Japan Post Holdings",
    "6273.T": "SMC Corporation",
    "6301.T": "Komatsu",
    "6302.T": "Sumitomo Heavy Industries",
    "6305.T": "Hitachi Construction Machinery",
    "6326.T": "Kubota",
    "6361.T": "Ebara",
    "6367.T": "Daikin Industries",
    "6471.T": "NSK Ltd.",
    "6472.T": "NTN",
    "6473.T": "JTEKT",
    "6479.T": "MinebeaMitsumi",
    "6501.T": "Hitachi",
    "6503.T": "Mitsubishi Electric",
    "6504.T": "Fuji Electric",
    "6506.T": "Yaskawa Electric Corporation",
    "6526.T": "Socionext",
    "6532.T": "Baycurrent",
    "6594.T": "Nidec",
    "6645.T": "Omron",
    "6701.T": "NEC",
    "6702.T": "Fujitsu",
    "6723.T": "Renesas Electronics",
    "6724.T": "Seiko Epson",
    "6752.T": "Panasonic",
    "6753.T": "Sharp Corporation",
    "6758.T": "Sony",
    "6762.T": "TDK",
    "6770.T": "Alps Alpine",
    "6841.T": "Yokogawa Electric",
    "6857.T": "Advantest",
    "6861.T": "Keyence",
    "6902.T": "Denso",
    "6920.T": "Lasertec",
    "6954.T": "FANUC",
    "6963.T": "Rohm",
    "6971.T": "Kyocera",
    "6976.T": "Taiyo Yuden",
    "6981.T": "Murata Manufacturing",
    "6988.T": "Nitto Denko",
    "7004.T": "Kanadevia",
    "7011.T": "Mitsubishi Heavy Industries",
    "7012.T": "Kawasaki Heavy Industries",
    "7013.T": "IHI",
    "7186.T": "Yokohama Financial Group",
    "7201.T": "Nissan",
    "7202.T": "Isuzu Motors",
    "7203.T": "Toyota Motor",
    "7211.T": "Mitsubishi Motors",
    "7261.T": "Mazda Motor",
    "7267.T": "Honda Motor",
    "7269.T": "Suzuki Motor",
    "7270.T": "Subaru",
    "7272.T": "Yamaha Motor Company",
    "7453.T": "Muji",
    "7532.T": "Pan Pacific International Holdings",
    "7731.T": "Nikon",
    "7733.T": "Olympus",
    "7735.T": "SCREEN Holdings",
    "7741.T": "Hoya Corporation",
    "7751.T": "Canon Inc.",
    "7752.T": "Ricoh",
    "7832.T": "Bandai Namco Holdings",
    "7911.T": "Toppan Printing",
    "7912.T": "Dai Nippon Printing",
    "7951.T": "Yamaha Corporation",
    "7974.T": "Nintendo",
    "8001.T": "Itochu",
    "8002.T": "Marubeni",
    "8015.T": "Toyota Tsusho",
    "8031.T": "Mitsui & Co.",
    "8035.T": "Tokyo Electron",
    "8053.T": "Sumitomo",
    "8058.T": "Mitsubishi",
    "8233.T": "Takashimaya",
    "8252.T": "Marui Group",
    "8253.T": "Credit Saison",
    "8267.T": "Aeon",
    "8304.T": "Aozora Bank",
    "8306.T": "Mitsubishi UFJ Financial Group",
    "8308.T": "Resona Holdings",
    "8309.T": "Sumitomo Mitsui Trust Holdings",
    "8316.T": "Sumitomo Mitsui Financial Group",
    "8331.T": "Chiba Bank",
    "8354.T": "Fukuoka Financial Group",
    "8411.T": "Mizuho Financial Group",
    "8591.T": "Orix",
    "8601.T": "Daiwa Securities Group",
    "8604.T": "Nomura Holdings",
    "8630.T": "Sompo Holdings",
    "8697.T": "Japan Exchange Group",
    "8725.T": "MS&AD Insurance Group",
    "8750.T": "Dai-ichi Life",
    "8766.T": "Tokio Marine Holdings",
    "8795.T": "T&D Holdings",
    "8801.T": "Mitsui Fudosan",
    "8802.T": "Mitsubishi Estate",
    "8804.T": "Tokyo Tatemono",
    "8830.T": "Sumitomo Realty & Development",
    "9001.T": "Tobu Railway",
    "9005.T": "Tokyu",
    "9007.T": "Odakyu Electric Railway",
    "9008.T": "Keio",
    "9009.T": "Keisei Electric Railway",
    "9020.T": "East Japan Railway Company",
    "9021.T": "West Japan Railway Company",
    "9022.T": "Central Japan Railway Company",
    "9064.T": "Yamato Holdings",
    "9101.T": "Nippon Yusen",
    "9104.T": "Mitsui O.S.K. Lines",
    "9107.T": "Kawasaki Kisen Kaisha",
    "9147.T": "Nippon Express Holdings",
    "9201.T": "Japan Airlines",
    "9202.T": "ANA Holdings",
    "9432.T": "Nippon Telegraph & Telephone",
    "9433.T": "KDDI",
    "9434.T": "SoftBank",
    "9501.T": "Tokyo Electric Power Company",
    "9502.T": "Chubu Electric Power",
    "9503.T": "Kansai Electric Power",
    "9531.T": "Tokyo Gas",
    "9532.T": "Osaka Gas",
    "9602.T": "Toho",
    "9735.T": "Secom",
    "9766.T": "Konami",
    "9843.T": "Nitori",
    "9983.T": "Fast Retailing",
    "9984.T": "SoftBank Group"
}


def get_nikkei225_data():
    """抓取日經 225 指數成分股數據（含 Wikipedia 解析與內嵌完整備援）"""
    url = "https://en.wikipedia.org/wiki/Nikkei_225"
    print(f"Accessing URL for nikkei225: {url}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    stock_dict = {}
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for a in soup.find_all('a', href=re.compile(r'topSearchStr=([0-9A-Za-z]{4})')):
            m = re.search(r'topSearchStr=([0-9A-Za-z]{4})', a['href'])
            if not m:
                continue
            code = m.group(1)
            li = a.find_parent('li')
            if li:
                first_a = li.find('a')
                name = first_a.get_text(strip=True) if first_a else ''
                ticker = f"{code}.T"
                if ticker and name:
                    stock_dict[ticker] = name
        
        if len(stock_dict) == 225:
            print(f"Successfully scraped {len(stock_dict)} constituents from Wikipedia")
            return stock_dict
        else:
            print(f"Warning: Scraped {len(stock_dict)} stocks (expected 225). Falling back to embedded list.")
    except Exception as e:
        print(f"Error occurred while scraping Nikkei 225 data: {str(e)}. Falling back to embedded list.")
    
    # 網路抓取失敗或個數不完整時使用內嵌完整備援
    return dict(FALLBACK_NIKKEI225)


def get_stock_data(index_name):
    """抓取指定指數的成分股數據"""
    index_key = index_name.lower()
    
    if index_key in ('nikkei225', 'n225', 'jp225'):
        return get_nikkei225_data()

    urls = {
        'sp500': "https://www.slickcharts.com/sp500",
        'nasdaq100': "https://www.slickcharts.com/nasdaq100",
        'dowjones': "https://www.slickcharts.com/dowjones"
    }
    
    if index_key not in urls:
        print(f"Invalid index name: {index_name}")
        return None

    stock_dict = {}
    try:
        url = urls[index_key]
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

        # 針對 S&P 500 自動擴充前沿科技與太空概念股 (Frontier Tickers)
        if index_key == 'sp500':
            for sym, name in FRONTIER_US_STOCKS.items():
                stock_dict.setdefault(sym, name)
                print(f"Ensured frontier ticker in {index_name}: {sym} -> {name}")

        return stock_dict
    except Exception as e:
        print(f"Error occurred while fetching {index_name} data: {str(e)}")
        # 若為 S&P 500 且抓取失敗，若本地已有檔案則讀取並補齊 frontier
        filepath = os.path.join(DATA_DIR, f"{index_key}_data.json")
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    local_data = json.load(f)
                if index_key == 'sp500':
                    for sym, name in FRONTIER_US_STOCKS.items():
                        local_data.setdefault(sym, name)
                return local_data
            except Exception:
                pass
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
        'dowjones': 'dowjones_data.json',
        'nikkei225': 'nikkei225_data.json'
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
