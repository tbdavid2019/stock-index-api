# Stock Index API

提供台灣股市指數、美股主要指數與日股日經 225（Nikkei 225）成分股及台灣 ETF 基金持股資料的 API 服務。

## 功能

### 1. 國際與跨市場指數成分股
- **S&P 500**（自動涵蓋前沿科技與太空概念股如 SPCX, DXYZ, ASTS, RKLB, CRWV, FN, CLS）
- **NASDAQ 100**
- **Dow Jones (道瓊工業指數)**
- **日經 225 (Nikkei 225 / N225 / JP225)**：東京證券交易所 225 檔核心龍頭成分股（如 8035.T Tokyo Electron, 9984.T SoftBank Group, 6857.T Advantest, 6146.T Disco, 4063.T Shin-Etsu 等），具備 Wikipedia 線上解析與 225 檔完整內嵌備援。

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

### 抓取國際與日股指數成分股
```bash
source myenv/bin/activate
python crawler-i18n.py
```

執行後會在 `data/` 目錄下生成：
- `sp500_data.json` - S&P 500 成分股（含 Frontier 概念股）
- `nasdaq100_data.json` - NASDAQ 100 成分股
- `dowjones_data.json` - 道瓊工業指數成分股
- `nikkei225_data.json` - 日經 225 指數成分股（完整 225 檔）
- `fund_0050.json` - 0050 持股明細
- `fund_0100.json` - 0100 持股明細
- `fund_*.json` - 其他基金持股明細
- `funds_summary.json` - 所有基金摘要

### 資料格式
與現有各指數 API 格式完全一致：
```json
{
  "8035.T": "Tokyo Electron",
  "9984.T": "SoftBank Group",
  "AAPL": "Apple Inc.",
  "2330": "台積電"
}
```

## 排程自動化

### GitHub Actions 自動更新

專案已提供 GitHub Actions workflow：
- 檔案位置：`.github/workflows/update-data.yml`
- 排程時間：**台灣時間每天 04:30**
- 執行內容：
  1. 執行 `crawler-mops-individual.py`
  2. 執行 `crawler-i18n.py`
  3. 上傳 `data/*.json` 到 Cloudflare KV
  4. 若 `data/` 內容有變更，自動 commit 並 push 回 repo

### GitHub Secrets 設定
請先在 GitHub repository settings 中設定以下 Secrets：
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_API_TOKEN`
- `CLOUDFLARE_KV_NAMESPACE_ID`

### 本機手動執行
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cd data
npm ci
cd ..

export CLOUDFLARE_KV_NAMESPACE_ID=your_namespace_id
export CLOUDFLARE_API_TOKEN=your_api_token
bash ./upload2KV.sh
```

## Cloudflare KV 映射鍵值

透過 `upload2KV.sh` 同步發布以下鍵值至 Cloudflare Workers KV：
- `SP500` -> `sp500_data.json`
- `nasdaq100` -> `nasdaq100_data.json`
- `dowjones` -> `dowjones_data.json`
- `NIKKEI225` -> `nikkei225_data.json`
- `N225` -> `nikkei225_data.json`
- `JP225` -> `nikkei225_data.json`
- `TW0050` -> `fund_0050.json`
- `TW0100` -> `fund_0100.json`

## API 端點 (FastAPI)

啟動 API 伺服器：
```bash
uvicorn app:app --reload --port 8000
```

主要端點：
- `GET /` - API 狀態與端點指引
- `GET /indices` - 獲取所有市場與指數列表（`TW`, `US`, `JP`）
- `GET /stocks/{index_name}` - 獲取指定指數成分股（支援 `SP500`, `NASDAQ100`, `DOWJONES`, `NIKKEI225`, `N225`, `JP225`, `0050`, `0100`）
- `GET /stock/{stock_code}` - 依股票代號查詢（支援台股代號、美股代號、日股代號如 `8035` 或 `8035.T`）
- `GET /search/{company_name}` - 依公司名稱模糊搜尋跨市場成分股
- `GET /market/{market}` - 獲取指定市場（`TW`, `US`, `JP`）的所有指數成分股

## 專案結構
```
.
├── app.py                          # FastAPI 主程式
├── crawler-mops-individual.py      # MOPS 基金持股爬蟲（自動偵測最新季度）
├── crawler-i18n.py                 # 國際與日經指數爬蟲（含 Frontier 概念股擴充）
├── upload2KV.sh                    # Cloudflare KV 上傳腳本
├── data/                           # 資料目錄
│   ├── sp500_data.json
│   ├── nasdaq100_data.json
│   ├── dowjones_data.json
│   ├── nikkei225_data.json        # 日經 225 成分股
│   ├── fund_0050.json             # 固定檔名，自動更新
│   ├── fund_0100.json
│   └── funds_summary.json
└── requirements.txt
```

## 注意事項

1. **SSL 證書**：MOPS 網站證書有問題，程式中使用 `verify=False`。
2. **容錯機制**：日經 225 爬蟲內嵌 225 檔完整備援清單，若 Wikipedia 頁面改版或網路超時自動平滑降級。
3. **無硬編碼金鑰**：所有金鑰憑證均透過環境變數注入，嚴禁硬編碼。
