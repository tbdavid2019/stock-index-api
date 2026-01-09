"""
解析 MOPS 基金持股回應，將每個基金的持股分別儲存
"""
import requests
import pandas as pd
import json
import os
import re
from io import StringIO
from bs4 import BeautifulSoup

# 設定資料目錄
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# 基金名稱到股票代碼的映射
FUND_NAME_MAPPING = {
    '元大台灣卓越50': '0050',
    '元大台灣中型100': '0100',
    '元大MSCI台灣': '006203',
    '元大台灣ESG永續': '00850',
    # 可以繼續添加更多映射
}

def extract_fund_code_from_company_id(company_id: str) -> str:
    """
    從公司代號提取基金代碼
    例如：A00005 -> 可能需要查表或其他邏輯
    """
    # 這裡可能需要額外的映射邏輯
    return company_id

def parse_individual_funds(html_content: str, year: int, season: int):
    """
    解析 HTML 回應，提取每個基金的持股資料
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 尋找所有包含基金名稱的標題
    # 通常格式為：<table class='noBorder'> 包含基金名稱
    fund_sections = []
    
    # 策略：尋找包含「公司代號」和基金名稱的區塊
    all_tables = soup.find_all('table')
    
    current_fund = None
    current_fund_code = None
    
    for table in all_tables:
        table_text = table.get_text()
        
        # 檢查是否包含基金名稱標題
        # 格式：「元大台灣卓越50證券投資信託基金    公司代號：    A00005」
        if '公司代號：' in table_text and '證券投資信託基金' in table_text:
            # 提取基金名稱
            lines = table_text.strip().split('\n')
            for line in lines:
                if '證券投資信託基金' in line:
                    # 嘗試從映射表找到對應的股票代碼
                    for fund_name, code in FUND_NAME_MAPPING.items():
                        if fund_name in line:
                            current_fund = fund_name
                            current_fund_code = code
                            print(f"找到基金: {current_fund} ({current_fund_code})")
                            break
                    
                    # 如果沒有在映射表中，嘗試自動提取
                    if not current_fund:
                        # 簡化基金名稱
                        match = re.search(r'元大(.+?)證券投資信託基金', line)
                        if match:
                            current_fund = match.group(1).strip()
                            print(f"找到未映射的基金: {current_fund}")
        
        # 檢查是否為持股明細表格（包含「股票代號」欄位）
        if current_fund and '股票代號' in table_text and '持股比率' in table_text:
            try:
                # 使用 pandas 解析這個表格
                df_list = pd.read_html(StringIO(str(table)))
                for df in df_list:
                    if '股票代號' in df.columns:
                        # 清理資料
                        df = df.dropna(how='all')
                        
                        # 過濾掉小計和總計行
                        if '股票代號' in df.columns:
                            df = df[~df['股票代號'].astype(str).str.contains('小計|總計', na=False)]
                        
                        # 儲存此基金的持股
                        # 使用固定檔名（不含年度季度），方便排程自動更新
                        if current_fund_code:
                            # 使用股票代碼作為檔名
                            filename = f"fund_{current_fund_code}.json"
                        else:
                            # 使用基金名稱作為檔名
                            safe_name = re.sub(r'[^\w\s-]', '', current_fund).replace(' ', '_')
                            filename = f"fund_{safe_name}.json"
                        
                        save_path = os.path.join(DATA_DIR, filename)
                        
                        # 提取需要的欄位並轉換為簡單的 key-value 格式（與 SP500 一致）
                        if '股票代號' in df.columns and '股票名稱' in df.columns:
                            # 轉換為 {"股票代號": "股票名稱"} 格式
                            fund_data = dict(zip(df['股票代號'].astype(str), df['股票名稱'].astype(str)))
                            
                            with open(save_path, 'w', encoding='utf-8') as f:
                                json.dump(fund_data, f, ensure_ascii=False, indent=2)
                            
                            print(f"✓ {current_fund}: {len(fund_data)} 筆 -> {filename}")
                            
                            fund_sections.append({
                                'fund_name': current_fund,
                                'fund_code': current_fund_code,
                                'holdings_count': len(fund_data),
                                'file': filename
                            })
                        
                        # 重置當前基金（準備下一個）
                        current_fund = None
                        current_fund_code = None
                        break
            except Exception as e:
                print(f"解析表格失敗: {e}")
    
    return fund_sections

def get_all_fund_holdings(year: int, season: int):
    """
    獲取所有基金的持股資料並分別儲存
    """
    url = "https://mopsov.twse.com.tw/mops/web/ajax_t78sb04"
    
    payload = {
        'encodeURIComponent': '1',
        'step': '1',
        'firstin': '1',
        'off': '1',
        'keyword4': '',
        'code1': '',
        'TYPEK2': '',
        'checkbtn': '',
        'queryName': 'co_id',
        'inpuType': 'co_id',
        'TYPEK': 'all',
        'isnew': 'false',
        'co_id': '',
        'year': str(year),
        'season': f"{season:02d}",
        'type': '05'
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Referer': 'https://mopsov.twse.com.tw/mops/web/t78sb35_new',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    
    print(f"發送 POST 請求: 年度={year}, 季度={season:02d}")
    
    try:
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        response = requests.post(url, data=payload, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        
        print(f"回應狀態碼: {response.status_code}")
        print(f"回應長度: {len(response.text)} 字元\n")
        
        # 解析並儲存各個基金
        fund_sections = parse_individual_funds(response.text, year, season)
        
        print(f"\n總共處理了 {len(fund_sections)} 個基金")
        
        # 儲存摘要
        summary_path = os.path.join(DATA_DIR, "funds_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(fund_sections, f, ensure_ascii=False, indent=2)
        print(f"摘要已儲存至: {summary_path}")
        
        return fund_sections
        
    except Exception as e:
        print(f"請求失敗: {e}")
        raise

if __name__ == "__main__":
    from datetime import datetime
    
    # 自動計算最新的年度和季度
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    
    # 轉換為民國年
    roc_year = current_year - 1911
    
    # 計算季度 (基金持股通常延遲一季公布)
    # 1-3月 -> 上一年Q4, 4-6月 -> Q1, 7-9月 -> Q2, 10-12月 -> Q3
    if current_month <= 3:
        season = 4
        roc_year -= 1  # 上一年的 Q4
    elif current_month <= 6:
        season = 1
    elif current_month <= 9:
        season = 2
    else:
        season = 3
    
    print(f"自動偵測: 民國 {roc_year} 年第 {season} 季")
    print(f"(西元 {roc_year + 1911} 年 Q{season})")
    print(f"如需指定其他季度，請修改下方參數\n")
    
    # 如果需要手動指定，取消註解並修改以下兩行：
    # roc_year = 114
    # season = 4
    
    try:
        funds = get_all_fund_holdings(year=roc_year, season=season)
        print(f"\n✅ 成功！共處理 {len(funds)} 個基金")
    except Exception as e:
        print(f"❌ 執行失敗: {e}")
