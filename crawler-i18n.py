import requests
from bs4 import BeautifulSoup
import json
import os
import re
import urllib.request

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

# 費城半導體 30 檔龍頭清單 (SOX)
FALLBACK_SOX = {
    "NVDA": "NVIDIA Corporation",
    "TSM": "Taiwan Semiconductor Manufacturing Co. (ADR)",
    "AVGO": "Broadcom Inc.",
    "AMD": "Advanced Micro Devices, Inc.",
    "QCOM": "Qualcomm Incorporated",
    "INTC": "Intel Corporation",
    "TXN": "Texas Instruments Incorporated",
    "MU": "Micron Technology, Inc.",
    "AMAT": "Applied Materials, Inc.",
    "LRCX": "Lam Research Corporation",
    "ASML": "ASML Holding N.V. (ADR)",
    "ADI": "Analog Devices, Inc.",
    "KLAC": "KLA Corporation",
    "MRVL": "Marvell Technology, Inc.",
    "NXPI": "NXP Semiconductors N.V.",
    "MCHP": "Microchip Technology Incorporated",
    "ON": "ON Semiconductor Corporation",
    "MPWR": "Monolithic Power Systems, Inc.",
    "TER": "Teradyne, Inc.",
    "QRVO": "Qorvo, Inc.",
    "SWKS": "Skyworks Solutions, Inc.",
    "WDC": "Western Digital Corporation",
    "ENTG": "Entegris, Inc.",
    "ARM": "Arm Holdings plc",
    "SNPS": "Synopsys, Inc.",
    "CDNS": "Cadence Design Systems, Inc.",
    "GFS": "GlobalFoundries Inc.",
    "CRUS": "Cirrus Logic, Inc.",
    "MTSI": "MACOM Technology Solutions Holdings",
    "RMBS": "Rambus Inc."
}

# 恒生科技指數 30 檔成分股 (HSTECH)
FALLBACK_HSTECH = {
    "0700.HK": "Tencent (騰訊控股)",
    "9988.HK": "Alibaba (阿里巴巴-W)",
    "3690.HK": "Meituan (美團-W)",
    "1810.HK": "Xiaomi (小米集團-W)",
    "9888.HK": "Baidu (百度集團-SW)",
    "0981.HK": "SMIC (中芯國際)",
    "1024.HK": "Kuaishou (快手-W)",
    "9999.HK": "NetEase (網易-S)",
    "2015.HK": "Li Auto (理想汽車-W)",
    "9618.HK": "JD.com (京東集團-SW)",
    "0285.HK": "BYD Electronic (比亞迪電子)",
    "0241.HK": "Alibaba Health (阿里健康)",
    "0268.HK": "Kingdee (金蝶國際)",
    "0772.HK": "China Literature (閱文集團)",
    "1347.HK": "Hua Hong (華虹半導體)",
    "2013.HK": "Weimob (微盟集團)",
    "0992.HK": "Lenovo (聯想集團)",
    "2382.HK": "Sunny Optical (舜宇光學科技)",
    "3888.HK": "Kingsoft (金山軟件)",
    "6618.HK": "JD Health (京東健康)",
    "9866.HK": "NIO (蔚來-SW)",
    "9868.HK": "XPeng (小鵬汽車-W)",
    "9626.HK": "Bilibili (嗶哩嗶哩-W)",
    "6690.HK": "Haier Smart Home (海爾智家)",
    "0763.HK": "ZTE (中興通訊)",
    "0522.HK": "ASMPT (ASMPT Limited)",
    "1797.HK": "East Buy (東方甄選)",
    "2858.HK": "Yixin (易鑫集團)",
    "0020.HK": "SenseTime (商湯-W)",
    "6060.HK": "ZhongAn Online (眾安在綫)"
}

# 國泰永續高股息 (00878)
FALLBACK_TW00878 = {
    "2357": "華碩", "2382": "廣達", "3231": "緯創", "2301": "光寶科", "2891": "中信金",
    "2886": "兆豐金", "2882": "國泰金", "2881": "富邦金", "2454": "聯發科", "2303": "聯電",
    "2884": "玉山金", "2890": "永豐金", "2892": "第一金", "2880": "華南金", "5880": "合庫金",
    "2409": "友達", "3481": "群創", "2379": "瑞昱", "3711": "日月光投控", "2308": "台達電",
    "2603": "長榮", "2609": "陽明", "2615": "萬海", "1101": "台泥", "1102": "亞泥",
    "1216": "統一", "1301": "台塑", "1303": "南亞", "2002": "中鋼", "2105": "正新"
}

# 群益台灣精選高息 (00919)
FALLBACK_TW00919 = {
    "2603": "長榮", "2382": "廣達", "2454": "聯發科", "2609": "陽明", "3231": "緯創",
    "2303": "聯電", "2891": "中信金", "2615": "萬海", "2357": "華碩", "2449": "京元電子",
    "3711": "日月光投控", "6176": "瑞儀", "5347": "世界", "2886": "兆豐金", "2890": "永豐金",
    "2884": "玉山金", "2881": "富邦金", "2882": "國泰金", "3034": "聯詠", "2379": "瑞昱",
    "2885": "元大金", "2880": "華南金", "5880": "合庫金", "2887": "台新新光金", "2892": "第一金",
    "2301": "光寶科", "5483": "中美晶", "4958": "臻鼎-KY", "6239": "力成", "1504": "東元"
}

# 復華台灣科技優息 (00929)
FALLBACK_TW00929 = {
    "2454": "聯發科", "3034": "聯詠", "2303": "聯電", "2382": "廣達", "3711": "日月光投控",
    "2379": "瑞昱", "3231": "緯創", "2301": "光寶科", "6239": "力成", "2449": "京元電子",
    "2357": "華碩", "5347": "世界", "6176": "瑞儀", "3037": "欣興", "2344": "華邦電",
    "2408": "南亞科", "3045": "台灣大", "4904": "遠傳", "2458": "義隆", "5483": "中美晶",
    "6269": "台郡", "8299": "群聯", "6121": "新普", "2347": "聯強", "6669": "緯穎",
    "3529": "力旺", "3264": "欣銓", "3005": "神基", "6278": "台表科", "2385": "群光",
    "3702": "大聯大", "2474": "可成", "2412": "中華電", "5469": "瀚宇博", "3014": "聯陽",
    "6414": "樺漢", "3596": "智易", "3036": "文曄", "2353": "宏碁", "2324": "仁寶"
}

# 櫃買富櫃50 (TPEX50)
FALLBACK_TPEX50 = {
    "6488": "環球晶", "8299": "群聯", "3293": "鈊象", "3105": "穩懋", "3529": "力旺",
    "6510": "精測", "5483": "中美晶", "8069": "元太", "5347": "世界", "4966": "譜瑞-KY",
    "6770": "力積電", "3264": "欣銓", "6121": "新普", "6274": "台燿", "3131": "弘塑",
    "3587": "閎康", "6223": "旺矽", "3680": "家登", "8358": "金居", "6138": "茂達",
    "8938": "明安", "4147": "中裕", "6446": "藥華藥", "6472": "保瑞", "1795": "美時",
    "4743": "合一", "6547": "高端疫苗", "4105": "東洋", "4128": "中天", "3081": "聯亞",
    "4979": "華星光", "3455": "由田", "5425": "台半", "8086": "宏捷科", "3374": "精材",
    "6188": "廣明", "5289": "宜鼎", "3691": "碩禾", "6147": "頎邦", "5457": "宣德",
    "3218": "大學光", "8454": "富邦媒", "6182": "合晶", "5371": "中光電", "3211": "順達",
    "5274": "信驊", "6533": "晶心科", "6683": "創鑫工程", "6768": "志強-KY", "7769": "鴻勁"
}

# 完整 225 檔東京證交所日經 225 內嵌備援清單
FALLBACK_NIKKEI225 = {
    "1332.T": "Nissui", "1605.T": "Inpex", "1721.T": "Comsys Holdings", "1801.T": "Taisei",
    "1802.T": "Obayashi Corp.", "1803.T": "Shimizu", "1808.T": "Haseko Corp.", "1812.T": "Kajima",
    "1925.T": "Daiwa House Industry", "1928.T": "Sekisui House", "1963.T": "JGC Corporation",
    "2002.T": "Nisshin Seifun Group", "2269.T": "Meiji Holdings", "2282.T": "NH Foods",
    "2413.T": "M3", "2432.T": "Dena", "2501.T": "Sapporo Holdings", "2502.T": "Asahi Group Holdings",
    "2503.T": "Kirin Holdings", "2768.T": "Sojitz", "2801.T": "Kikkoman", "2802.T": "Ajinomoto",
    "285A.T": "Kioxia Holdings", "2871.T": "Nichirei", "2914.T": "Japan Tobacco",
    "3086.T": "J. Front Retailing", "3092.T": "ZOZO", "3099.T": "Isetan Mitsukoshi Holdings",
    "3289.T": "Tokyu Land", "3382.T": "Seven & I Holdings Co.", "3401.T": "Teijin",
    "3402.T": "Toray Industries", "3405.T": "Kuraray", "3407.T": "Asahi Kasei",
    "3436.T": "SUMCO", "3659.T": "Nexon", "3697.T": "SHIFT Inc.", "3861.T": "Oji Holdings Corporation",
    "4004.T": "Resonac", "4005.T": "Sumitomo Chemical", "4021.T": "Nissan Chemical Industries",
    "4042.T": "Tosoh", "4043.T": "Tokuyama Corporation", "4061.T": "Denka", "4063.T": "Shin-Etsu Chemical",
    "4151.T": "Kyowa Hakko Kirin", "4183.T": "Mitsui Chemicals", "4188.T": "Mitsubishi Chemical Holdings",
    "4208.T": "Ube Industries", "4307.T": "Nomura Research Institute", "4324.T": "Dentsu",
    "4385.T": "Mercari", "4452.T": "Kao Corp.", "4502.T": "Takeda Pharmaceutical Company",
    "4503.T": "Astellas Pharma", "4506.T": "Sumitomo Dainippon Pharma", "4507.T": "Shionogi",
    "4519.T": "Chugai Pharmaceutical", "4523.T": "Eisai Co.", "4543.T": "Terumo",
    "4568.T": "Daiichi Sankyo", "4578.T": "Otsuka Holdings", "4661.T": "Oriental Land",
    "4689.T": "LY Corporation", "4704.T": "Trend Micro", "4751.T": "CyberAgent",
    "4755.T": "Rakuten", "4901.T": "Fujifilm Holdings", "4902.T": "Konica Minolta Holdings",
    "4911.T": "Shiseido", "5019.T": "Idemitsu Kosan", "5020.T": "Eneos Holdings",
    "5101.T": "Yokohama Rubber", "5108.T": "Bridgestone", "5201.T": "AGC Inc.",
    "5214.T": "Nippon Electric Glass", "5233.T": "Taiheiyo Cement", "5301.T": "Tokai Carbon",
    "5332.T": "Toto Ltd.", "5333.T": "NGK Insulators", "5401.T": "Nippon Steel",
    "5406.T": "Kobe Steel", "5411.T": "JFE Holdings", "543A.T": "Archion",
    "5631.T": "Japan Steel Works", "5706.T": "Mitsui Mining & Smelting", "5711.T": "Mitsubishi Materials",
    "5713.T": "Sumitomo Metal Mining", "5714.T": "Dowa Holdings", "5801.T": "Furukawa Electric",
    "5802.T": "Sumitomo Electric Industries", "5803.T": "Fujikura", "5831.T": "Shizuoka Financial Group",
    "6098.T": "Recruit Holdings", "6103.T": "Okuma Holdings", "6113.T": "Amada Co. Ltd.",
    "6146.T": "Disco Corporation", "6178.T": "Japan Post Holdings", "6273.T": "SMC Corporation",
    "6301.T": "Komatsu", "6302.T": "Sumitomo Heavy Industries", "6305.T": "Hitachi Construction Machinery",
    "6326.T": "Kubota", "6361.T": "Ebara", "6367.T": "Daikin Industries",
    "6471.T": "NSK Ltd.", "6472.T": "NTN", "6473.T": "JTEKT", "6479.T": "MinebeaMitsumi",
    "6501.T": "Hitachi", "6503.T": "Mitsubishi Electric", "6504.T": "Fuji Electric",
    "6506.T": "Yaskawa Electric Corporation", "6526.T": "Socionext", "6532.T": "Baycurrent",
    "6594.T": "Nidec", "6645.T": "Omron", "6701.T": "NEC", "6702.T": "Fujitsu",
    "6723.T": "Renesas Electronics", "6724.T": "Seiko Epson", "6752.T": "Panasonic",
    "6753.T": "Sharp Corporation", "6758.T": "Sony", "6762.T": "TDK", "6770.T": "Alps Alpine",
    "6841.T": "Yokogawa Electric", "6857.T": "Advantest", "6861.T": "Keyence", "6902.T": "Denso",
    "6920.T": "Lasertec", "6954.T": "FANUC", "6963.T": "Rohm", "6971.T": "Kyocera",
    "6976.T": "Taiyo Yuden", "6981.T": "Murata Manufacturing", "6988.T": "Nitto Denko",
    "7004.T": "Kanadevia", "7011.T": "Mitsubishi Heavy Industries", "7012.T": "Kawasaki Heavy Industries",
    "7013.T": "IHI", "7186.T": "Yokohama Financial Group", "7201.T": "Nissan",
    "7202.T": "Isuzu Motors", "7203.T": "Toyota Motor", "7211.T": "Mitsubishi Motors",
    "7261.T": "Mazda Motor", "7267.T": "Honda Motor", "7269.T": "Suzuki Motor",
    "7270.T": "Subaru", "7272.T": "Yamaha Motor Company", "7453.T": "Muji",
    "7532.T": "Pan Pacific International Holdings", "7731.T": "Nikon", "7733.T": "Olympus",
    "7735.T": "SCREEN Holdings", "7741.T": "Hoya Corporation", "7751.T": "Canon Inc.",
    "7752.T": "Ricoh", "7832.T": "Bandai Namco Holdings", "7911.T": "Toppan Printing",
    "7912.T": "Dai Nippon Printing", "7951.T": "Yamaha Corporation", "7974.T": "Nintendo",
    "8001.T": "Itochu", "8002.T": "Marubeni", "8015.T": "Toyota Tsusho", "8031.T": "Mitsui & Co.",
    "8035.T": "Tokyo Electron", "8053.T": "Sumitomo", "8058.T": "Mitsubishi",
    "8233.T": "Takashimaya", "8252.T": "Marui Group", "8253.T": "Credit Saison", "8267.T": "Aeon",
    "8304.T": "Aozora Bank", "8306.T": "Mitsubishi UFJ Financial Group", "8308.T": "Resona Holdings",
    "8309.T": "Sumitomo Mitsui Trust Holdings", "8316.T": "Sumitomo Mitsui Financial Group",
    "8331.T": "Chiba Bank", "8354.T": "Fukuoka Financial Group", "8411.T": "Mizuho Financial Group",
    "8591.T": "Orix", "8601.T": "Daiwa Securities Group", "8604.T": "Nomura Holdings",
    "8630.T": "Sompo Holdings", "8697.T": "Japan Exchange Group", "8725.T": "MS&AD Insurance Group",
    "8750.T": "Dai-ichi Life", "8766.T": "Tokio Marine Holdings", "8795.T": "T&D Holdings",
    "8801.T": "Mitsui Fudosan", "8802.T": "Mitsubishi Estate", "8804.T": "Tokyo Tatemono",
    "8830.T": "Sumitomo Realty & Development", "9001.T": "Tobu Railway", "9005.T": "Tokyu",
    "9007.T": "Odakyu Electric Railway", "9008.T": "Keio", "9009.T": "Keisei Electric Railway",
    "9020.T": "East Japan Railway Company", "9021.T": "West Japan Railway Company",
    "9022.T": "Central Japan Railway Company", "9064.T": "Yamato Holdings", "9101.T": "Nippon Yusen",
    "9104.T": "Mitsui O.S.K. Lines", "9107.T": "Kawasaki Kisen Kaisha", "9147.T": "Nippon Express Holdings",
    "9201.T": "Japan Airlines", "9202.T": "ANA Holdings", "9432.T": "Nippon Telegraph & Telephone",
    "9433.T": "KDDI", "9434.T": "SoftBank", "9501.T": "Tokyo Electric Power Company",
    "9502.T": "Chubu Electric Power", "9503.T": "Kansai Electric Power", "9531.T": "Tokyo Gas",
    "9532.T": "Osaka Gas", "9602.T": "Toho", "9735.T": "Secom", "9766.T": "Konami",
    "9843.T": "Nitori", "9983.T": "Fast Retailing", "9984.T": "SoftBank Group"
}


def save_stock_data(data, filename):
    """保存數據到文件"""
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved {len(data)} items to {filepath}")


def get_twse_taiex_data():
    """抓取台灣證交所官方 OpenAPI 上市公司清單 (TAIEX / TWSE)"""
    url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
    print(f"Accessing TWSE OpenAPI: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = json.loads(r.read().decode('utf-8'))
        result = {
            item['公司代號'].strip(): (item.get('公司簡稱') or item.get('公司名稱')).strip()
            for item in raw if item.get('公司代號')
        }
        if len(result) >= 900:
            return result
    except Exception as e:
        print(f"Warning: TWSE OpenAPI failed: {e}")
    # 讀取本地快取
    cached_path = os.path.join(DATA_DIR, "taiex_data.json")
    if os.path.exists(cached_path):
        with open(cached_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_tpex_otc_data():
    """抓取櫃買中心官方 OpenAPI 上櫃公司清單 (TPEX / OTC)"""
    url = "https://www.tpex.org.tw/openapi/v1/mopsfin_t187ap03_O"
    print(f"Accessing TPEx OpenAPI: {url}")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            raw = json.loads(r.read().decode('utf-8'))
        result = {
            item['SecuritiesCompanyCode'].strip(): (item.get('CompanyAbbreviation') or item.get('CompanyName')).strip()
            for item in raw if item.get('SecuritiesCompanyCode')
        }
        if len(result) >= 700:
            return result
    except Exception as e:
        print(f"Warning: TPEx OpenAPI failed: {e}")
    cached_path = os.path.join(DATA_DIR, "tpex_data.json")
    if os.path.exists(cached_path):
        with open(cached_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


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
            return stock_dict
    except Exception as e:
        print(f"Warning: Nikkei 225 scrape failed: {e}")
    
    return dict(FALLBACK_NIKKEI225)


def get_hsi_data():
    """抓取香港恒生指數 (HSI) 成分股"""
    url = "https://en.wikipedia.org/wiki/Hang_Seng_Index"
    print(f"Accessing URL for HSI: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    hsi = {}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        for t in soup.find_all('table', {'class': 'wikitable'}):
            headers_text = [th.text.strip() for th in t.find_all('th')]
            if any('Ticker' in h for h in headers_text) and any('Name' in h for h in headers_text):
                for row in t.find_all('tr')[1:]:
                    tds = row.find_all('td')
                    if len(tds) >= 2:
                        m = re.search(r'(\d{1,5})', tds[0].text.strip())
                        if m:
                            code = f"{m.group(1).zfill(4)}.HK"
                            hsi[code] = tds[1].text.strip()
        if len(hsi) >= 70:
            return hsi
    except Exception as e:
        print(f"Warning: HSI scrape failed: {e}")
    
    cached_path = os.path.join(DATA_DIR, "hsi_data.json")
    if os.path.exists(cached_path):
        with open(cached_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_dax40_data():
    """抓取德國法蘭克福 DAX 40 指數成分股"""
    url = "https://en.wikipedia.org/wiki/DAX"
    print(f"Accessing URL for DAX40: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    dax = {}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        for t in soup.find_all('table', {'class': 'wikitable'}):
            headers_text = [th.text.strip() for th in t.find_all('th')]
            if any('Ticker' in h for h in headers_text) and any('Company' in h for h in headers_text):
                for row in t.find_all('tr')[1:]:
                    tds = row.find_all('td')
                    if len(tds) >= 3:
                        ticker = tds[0].text.strip()
                        comp = tds[2].text.strip()
                        if ticker and comp:
                            sym = ticker if '.' in ticker else f"{ticker}.DE"
                            dax[sym] = comp
        if len(dax) >= 38:
            return dax
    except Exception as e:
        print(f"Warning: DAX40 scrape failed: {e}")
    cached_path = os.path.join(DATA_DIR, "dax40_data.json")
    if os.path.exists(cached_path):
        with open(cached_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_ftse100_data():
    """抓取英國倫敦富時 100 指數成分股"""
    url = "https://en.wikipedia.org/wiki/FTSE_100_Index"
    print(f"Accessing URL for FTSE100: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    ftse = {}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        for t in soup.find_all('table', {'class': 'wikitable'}):
            headers_text = [th.text.strip() for th in t.find_all('th')]
            if any('Ticker' in h for h in headers_text) and any('Company' in h for h in headers_text):
                for row in t.find_all('tr')[1:]:
                    tds = row.find_all('td')
                    if len(tds) >= 2:
                        comp = tds[0].text.strip()
                        ticker = tds[1].text.strip()
                        if ticker and comp:
                            sym = ticker if '.' in ticker else f"{ticker}.L"
                            ftse[sym] = comp
        if len(ftse) >= 95:
            return ftse
    except Exception as e:
        print(f"Warning: FTSE100 scrape failed: {e}")
    cached_path = os.path.join(DATA_DIR, "ftse100_data.json")
    if os.path.exists(cached_path):
        with open(cached_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_eurostoxx50_data():
    """抓取歐洲藍籌 50 指數成分股 (EURO STOXX 50)"""
    url = "https://en.wikipedia.org/wiki/EURO_STOXX_50"
    print(f"Accessing URL for EUROSTOXX50: {url}")
    headers = {'User-Agent': 'Mozilla/5.0'}
    stoxx = {}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        for t in soup.find_all('table', {'class': 'wikitable'}):
            headers_text = [th.text.strip() for th in t.find_all('th')]
            if any('Ticker' in h for h in headers_text) and any('Name' in h for h in headers_text):
                for row in t.find_all('tr')[1:]:
                    tds = row.find_all('td')
                    if len(tds) >= 3:
                        ticker = tds[0].text.strip()
                        comp = tds[2].text.strip()
                        if ticker and comp:
                            stoxx[ticker] = comp
        if len(stoxx) >= 48:
            return stoxx
    except Exception as e:
        print(f"Warning: EUROSTOXX50 scrape failed: {e}")
    cached_path = os.path.join(DATA_DIR, "eurostoxx50_data.json")
    if os.path.exists(cached_path):
        with open(cached_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def get_us_slickcharts_data(index_key):
    """從 Slickcharts 抓取標普500、那斯達克100、道瓊30"""
    urls = {
        'sp500': "https://www.slickcharts.com/sp500",
        'nasdaq100': "https://www.slickcharts.com/nasdaq100",
        'dowjones': "https://www.slickcharts.com/dowjones"
    }
    if index_key not in urls:
        return None

    stock_dict = {}
    try:
        url = urls[index_key]
        print(f"Accessing URL for {index_key}: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')[1:]
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    company_name = cols[1].text.strip()
                    symbol = cols[2].text.strip()
                    if symbol and company_name:
                        stock_dict[symbol] = company_name

            if index_key == 'sp500':
                for sym, name in FRONTIER_US_STOCKS.items():
                    stock_dict.setdefault(sym, name)

            return stock_dict
    except Exception as e:
        print(f"Warning: Slickcharts {index_key} fetch error: {e}")

    filepath = os.path.join(DATA_DIR, f"{index_key}_data.json")
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            local_data = json.load(f)
        if index_key == 'sp500':
            for sym, name in FRONTIER_US_STOCKS.items():
                local_data.setdefault(sym, name)
        return local_data
    return None


def collect_all_indices():
    """收集全球與台灣所有指數與市場數據"""
    results = {}

    # 1. 台灣大盤全市場 (TWSE / TPEx / TW_ALL)
    taiex = get_twse_taiex_data()
    if taiex:
        save_stock_data(taiex, "taiex_data.json")
        results["TAIEX"] = len(taiex)

    tpex = get_tpex_otc_data()
    if tpex:
        save_stock_data(tpex, "tpex_data.json")
        results["TPEX"] = len(tpex)

    if taiex or tpex:
        twall = {**taiex, **tpex}
        save_stock_data(twall, "twall_data.json")
        results["TW_ALL"] = len(twall)

    # 2. 台灣熱門指數與 ETF
    tw_sources = [
        ("tw0050_data.json", "fund_0050.json", None),
        ("tw0100_data.json", "fund_0100.json", None),
        ("tw0056_data.json", "fund_台灣高股息.json", None),
        ("tw00713_data.json", "fund_台灣高股息低波動ETF.json", None),
        ("tw00850_data.json", "fund_臺灣ESG永續ETF.json", None),
        ("tw00940_data.json", "fund_臺灣價值高息ETF.json", None),
        ("tw00878_data.json", None, FALLBACK_TW00878),
        ("tw00919_data.json", None, FALLBACK_TW00919),
        ("tw00929_data.json", None, FALLBACK_TW00929),
        ("tpex50_data.json", None, FALLBACK_TPEX50),
    ]
    for target_file, src_fund, fallback_dict in tw_sources:
        data = None
        if src_fund:
            src_path = os.path.join(DATA_DIR, src_fund)
            if os.path.exists(src_path):
                with open(src_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
        if not data and fallback_dict:
            data = dict(fallback_dict)
        if data:
            save_stock_data(data, target_file)
            key_name = target_file.replace("_data.json", "").upper()
            results[key_name] = len(data)

    # 3. 美股 (SP500, NASDAQ100, DOWJONES, SOX)
    for k in ['sp500', 'nasdaq100', 'dowjones']:
        us_data = get_us_slickcharts_data(k)
        if us_data:
            save_stock_data(us_data, f"{k}_data.json")
            results[k.upper()] = len(us_data)

    save_stock_data(FALLBACK_SOX, "sox_data.json")
    results["SOX"] = len(FALLBACK_SOX)

    # 4. 日股 (NIKKEI225)
    jp_data = get_nikkei225_data()
    save_stock_data(jp_data, "nikkei225_data.json")
    results["NIKKEI225"] = len(jp_data)

    # 5. 港股 (HSI, HSTECH)
    hsi_data = get_hsi_data()
    if hsi_data:
        save_stock_data(hsi_data, "hsi_data.json")
        results["HSI"] = len(hsi_data)

    save_stock_data(FALLBACK_HSTECH, "hstech_data.json")
    results["HSTECH"] = len(FALLBACK_HSTECH)

    # 6. 歐股 (DAX40, FTSE100, EUROSTOXX50)
    dax_data = get_dax40_data()
    if dax_data:
        save_stock_data(dax_data, "dax40_data.json")
        results["DAX40"] = len(dax_data)

    ftse_data = get_ftse100_data()
    if ftse_data:
        save_stock_data(ftse_data, "ftse100_data.json")
        results["FTSE100"] = len(ftse_data)

    stoxx_data = get_eurostoxx50_data()
    if stoxx_data:
        save_stock_data(stoxx_data, "eurostoxx50_data.json")
        results["EUROSTOXX50"] = len(stoxx_data)

    return results


if __name__ == "__main__":
    print("Starting data collection for all global & Taiwan indices...")
    results = collect_all_indices()
    print("\nCollection Summary:")
    for index_name, count in sorted(results.items()):
        print(f"  • {index_name:<14}: {count:>5} constituents")
