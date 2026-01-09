# Stock Index API

提供台灣股市指數成分股與基金持股資料的 API 服務。

## 功能

### 1. 國際指數成分股
- S&P 500
- NASDAQ 100  
- Dow Jones

### 2. 台灣 ETF 基金持股
從公開資訊觀測站 (MOPS) 抓取基金每季持股明細，**自動偵測最新季度**。

#### 目前支援的基金
| 基金名稱 | 股票代碼 | 檔案名稱 | 持股數 |
|---------|---------|---------|--------|
| 元大台灣卓越50 | 0050 | `fund_0050.json` | ~50 |
| 元大台灣中型100 | 0100 | `fund_0100.json` | ~100 |
| 元大台灣高股息 | 0056 | `fund_台灣高股息.json` | ~50 |
| 元大摩臺 | 0057 | `fund_摩臺.json` | ~86 |
| 元大台灣高股息低波動 | 00713 | `fund_台灣高股息低波動ETF.json` | ~51 |
| 元大臺灣ESG永續 | 00850 | `fund_臺灣ESG永續ETF.json` | ~105 |
| 元大臺灣價值高息 | 00940 | `fund_臺灣價值高息ETF.json` | ~50 |

*註：檔名固定，每次執行會自動覆蓋為最新季度資料*

## 使用方式

### 安裝依賴
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

### 抓取基金持股資料
```bash
source myenv/bin/activate
python crawler-mops-individual.py
```

**自動偵測最新季度**：
- 腳本會根據當前日期自動計算最新可用的季度（延遲一季公布）
- 例如：2026年1月執行 → 自動抓取 2025 Q4 資料
- 檔名固定，每次執行會覆蓋舊資料

執行後會在 `data/` 目錄下生成：
- `fund_0050.json` - 0050 持股明細（最新季度）
- `fund_0100.json` - 0100 持股明細（最新季度）
- `fund_*.json` - 其他基金持股明細
- `funds_summary.json` - 所有基金摘要

### 資料格式
**與 SP500/NASDAQ100 格式完全一致**：
```json
{
  "2330": "台積電",
  "2881": "富邦金",
  "2882": "國泰金",
  "1301": "台塑"
}
```

*註：簡單的 `{"股票代號": "股票名稱"}` 格式，與現有 API 完全相容*

## 排程自動化

### 設定 Cron Job
```bash
# 每季第一個月的第 5 天執行（基金持股資料通常延遲一季公布）
0 2 5 1,4,7,10 * cd /path/to/stock-index-api && ./upload2KV.sh
```

由於檔名固定，排程腳本**無需修改**即可自動抓取最新資料！

## 自訂設定

### 手動指定季度
編輯 `crawler-mops-individual.py` 最後幾行：

```python
# 取消註解並修改：
roc_year = 115  # 民國年
season = 1      # 季度 (1-4)
```

### 新增基金映射
編輯 `FUND_NAME_MAPPING` 字典以使用股票代碼作為檔名：

```python
FUND_NAME_MAPPING = {
    '元大台灣卓越50': '0050',
    '元大台灣中型100': '0100',
    '你的基金名稱': '股票代碼',
}
```

## 部署與上傳

### 上傳到 Cloudflare KV
```bash
./upload2KV.sh
```

這會：
1. 抓取最新資料（自動偵測季度）
2. 上傳到 Cloudflare KV Storage

## API 端點

- `GET /api/sp500` - S&P 500 成分股
- `GET /api/nasdaq100` - NASDAQ 100 成分股
- `GET /api/dowjones` - Dow Jones 成分股
- `GET /api/0050` - 元大台灣卓越50 持股
- `GET /api/0100` - 元大台灣中型100 持股

## 注意事項

1. **SSL 證書**：MOPS 網站證書有問題，程式中使用 `verify=False`
2. **更新頻率**：基金持股每季更新一次
3. **資料來源**：公開資訊觀測站 (https://mopsov.twse.com.tw)
4. **檔名固定**：每次執行覆蓋舊檔案，方便排程自動化
5. **資料清洗**：自動過濾「小計」、「總計」等統計行

## 專案結構
```
.
├── app.py                          # Flask API 主程式
├── crawler-mops-individual.py      # MOPS 基金持股爬蟲（自動偵測最新季度）
├── crawler-i18n.py                 # 國際指數爬蟲
├── upload2KV.sh                    # 上傳腳本
├── data/                           # 資料目錄
│   ├── fund_0050.json             # 固定檔名，自動更新
│   ├── fund_0100.json
│   └── funds_summary.json
└── requirements.txt
```

## 貢獻

歡迎提交 PR 新增更多基金映射或改進爬蟲邏輯！
