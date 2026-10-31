# Stock Index API (Global & Taiwan Equities Universe)

提供全球主要市場（台股、美股、日股、港股、歐股）指數成分股、台灣證券交易所全市場上市櫃清單與熱門 ETF 基金成分股查詢的微服務 API。

## 支援市場與指數

### 1. 🇹🇼 台灣市場 (`TW`)
- **台灣全市場總集**：
  - **`TAIEX` / `TWSE`**：台灣證券交易所全體上市企業（1,099 檔，取自 TWSE 官方 OpenAPI）。
  - **`TPEX` / `OTC`**：證券櫃檯買賣中心全體上櫃企業（897 檔，取自 TPEx 官方 OpenAPI）。
  - **`TW_ALL`**：全體上市與上櫃股票總集（1,996 檔），供下游量化模型全盤預測。
- **核心與高息旗艦 ETF / 指數**：
  - **`0050`**：元大台灣卓越 50（50 檔）
  - **`0100` / `0051`**：元大台灣中型 100（100 檔）
  - **`0056`**：元大高股息 / 臺灣高股息指數（50 檔）
  - **`00878`**：國泰永續高股息（30 檔）
  - **`00919`**：群益台灣精選高息（30 檔）
  - **`00929`**：復華台灣科技優息（40 檔）
  - **`00940`**：元大臺灣價值高息（50 檔）
  - **`00713`**：元大台灣高息低波（50 檔）
  - **`00850`**：元大臺灣 ESG 永續（110 檔）
  - **`TPEX50` / `006201`**：櫃買富櫃 50 指數（50 檔）

### 2. 🇺🇸 美國市場 (`US`)
- **`SP500`**：標普 500 指數（自動涵蓋前沿科技與太空概念股如 `SPCX`, `DXYZ`, `ASTS`, `RKLB`, `CRWV`, `FN`, `CLS` 等 510 檔）。
- **`NASDAQ100`**：那斯達克 100 科技龍頭（101 檔）。
- **`DOWJONES`**：道瓊工業平均指數（30 檔）。
- **`SOX` / `PHLX`**：費城半導體指數（30 檔全球晶片龍頭：`NVDA`, `TSM`, `AVGO`, `AMD`, `QCOM`, `INTC`, `TXN`, `MU`, `ASML`, `ARM` 等）。

### 3. 🇯🇵 日本市場 (`JP`)
- **`NIKKEI225` / `N225` / `JP225`**：東京證券交易所 225 檔核心龍頭成分股（如 `8035.T` Tokyo Electron, `9984.T` SoftBank Group, `6857.T` Advantest, `6146.T` Disco 等），具備 Wikipedia 線上解析與 225 檔完整內嵌備援。

### 4. 🇭🇰 香港市場 (`HK`)
- **`HSI` / `HANGSENG`**：香港恒生指數藍籌股（85 檔，如 `0700.HK` 騰訊、`9988.HK` 阿里、`3690.HK` 美團、`1211.HK` 比亞迪、`0981.HK` 中芯國際等）。
- **`HSTECH`**：恒生科技指數（30 檔核心科技旗艦）。

### 5. 🇪🇺 歐洲市場 (`EU`)
- **`DAX40` / `DAX`**：德國法蘭克福指數（40 檔，如 `SAP.DE`, `SIE.DE`, `ALV.DE`, `AIR.PA`, `BMW.DE` 等）。
- **`FTSE100` / `FTSE`**：英國倫敦富時 100 指數（100 檔，如 `AZN.L`, `SHEL.L`, `HSBA.L`, `ULVR.L` 等）。
- **`EUROSTOXX50` / `STOXX50`**：歐洲藍籌 50 指數（50 檔，如 `ASML.AS`, `MC.PA`, `OR.PA`, `SAP.DE`, `AIR.PA` 等）。

---

## 快速使用

### 抓取與更新所有指數資料
```bash
python3 crawler-i18n.py
```
執行後會在 `data/` 目錄生成所有標準化的 JSON 字典：
```
data/
├── taiex_data.json         # 台灣上市全市場 (1,099 檔)
├── tpex_data.json          # 台灣上櫃全市場 (897 檔)
├── twall_data.json         # 台灣全市場總集 (1,996 檔)
├── tw0050_data.json        # 台灣 50 (50 檔)
├── tw0100_data.json        # 台灣中型 100 (100 檔)
├── tw0056_data.json        # 台灣高股息 (50 檔)
├── tw00878_data.json       # 國泰永續高息 (30 檔)
├── tw00919_data.json       # 群益精選高息 (30 檔)
├── tw00929_data.json       # 復華科技優息 (40 檔)
├── tw00940_data.json       # 元大價值高息 (50 檔)
├── tw00713_data.json       # 高息低波 (50 檔)
├── tw00850_data.json       # ESG永續 (110 檔)
├── tpex50_data.json        # 富櫃 50 (50 檔)
├── sp500_data.json         # 標普 500 (510 檔)
├── nasdaq100_data.json     # 那斯達克 100 (101 檔)
├── dowjones_data.json      # 道瓊 30 (30 檔)
├── sox_data.json           # 費城半導體 30 (30 檔)
├── nikkei225_data.json     # 日經 225 (225 檔)
├── hsi_data.json           # 恒生指數 (85 檔)
├── hstech_data.json        # 恒生科技 (30 檔)
├── dax40_data.json         # 德國 DAX 40 (40 檔)
├── ftse100_data.json       # 英國 FTSE 100 (100 檔)
└── eurostoxx50_data.json   # 歐洲藍籌 50 (50 檔)
```

### 啟動 FastAPI 服務
```bash
uvicorn app:app --reload --port 8000
```

### API 端點指引
- **`GET /indices`**：獲取所有市場（`TW`, `US`, `JP`, `HK`, `EU`）的可用指數清單。
- **`GET /stocks/{index_name}`**：獲取指定指數或全市場的所有成分股（支援別名如 `TW0050`, `TAIEX`, `TW_ALL`, `SOX`, `PHLX`, `HSI`, `DAX40` 等）。
- **`GET /stock/{stock_code}`**：跨市場搜尋單檔股票基本資訊（自動支援 `2330`, `NVDA`, `8035.T`, `0700.HK`, `SAP.DE`, `AZN.L`）。
- **`GET /search/{company_name}`**：全球跨市場模糊搜尋公司名稱或代號。
- **`GET /market/{market}`**：獲取指定市場（`TW`, `US`, `JP`, `HK`, `EU`）的所有指數及成分股字典。

---

## Cloudflare Workers KV 邊緣發布

執行 `upload2KV.sh` 即可將最新生成的成分股檔案上傳至 Cloudflare Workers KV（例如 `answerbook.david888.com`），供下游量化模型以毫秒級延遲讀取：
```bash
export CLOUDFLARE_KV_NAMESPACE_ID=your_namespace_id
export CLOUDFLARE_API_TOKEN=your_api_token
bash ./upload2KV.sh
```

## 注意事項與安全鐵律
1. **零金鑰外洩**：所有 Cloudflare Token、API Key 均透過環境變數注入，禁止硬編碼。
2. **多層備援機制**：
   - 台股優先透過 TWSE / TPEx 官方 OpenAPI，遇網路波動平滑降級至本地快取。
   - 美股、日股、港股、歐股均內嵌完整 Constituent Fallback 清單，永不中斷下游查詢。
