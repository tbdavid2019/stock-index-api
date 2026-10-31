# Changelog

All notable changes to the `stock-index-api` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-10-31

### Added
- **台灣全市場 (TWSE & TPEx) 官方 OpenAPI 接入**:
  - 接入台灣證券交易所 OpenAPI 抓取 1,099 檔上市公司清單，產出 `data/taiex_data.json`（支援 `TAIEX`, `TWSE` 查詢）。
  - 接入證券櫃檯買賣中心 OpenAPI 抓取 897 檔上櫃公司清單，產出 `data/tpex_data.json`（支援 `TPEX`, `OTC` 查詢）。
  - 合併產出 1,996 檔全市場股票清單 `data/twall_data.json`（支援 `TW_ALL`, `TWALL` 查詢），供下游量化模型按需獲取全市場時序預測標的。
- **台灣核心與高息旗艦 ETF 指數標準化**:
  - 標準化產出並支援：
    - `0050`（台灣 50 / `tw0050_data.json`，50 檔）
    - `0100` / `0051`（台灣中型 100 / `tw0100_data.json`，100 檔）
    - `0056`（台灣高股息 / `tw0056_data.json`，50 檔）
    - `00878`（國泰永續高股息 / `tw00878_data.json`，30 檔）
    - `00919`（群益精選高息 / `tw00919_data.json`，30 檔）
    - `00929`（復華科技優息 / `tw00929_data.json`，40 檔）
    - `00940`（元大臺灣價值高息 / `tw00940_data.json`，50 檔）
    - `00713`（元大台灣高息低波 / `tw00713_data.json`，50 檔）
    - `00850`（元大臺灣 ESG 永續 / `tw00850_data.json`，110 檔）
    - `TPEX50`（櫃買富櫃 50 / `tpex50_data.json`，50 檔）
- **全球核心市場大盤與半導體指數擴充**:
  - 🇺🇸 **美國 (`US`)**：新增 `SOX` / `PHLX`（費城半導體 30 檔全球晶片龍頭：`NVDA`, `TSM`, `AVGO`, `AMD`, `QCOM`, `INTC`, `TXN`, `MU`, `ASML`, `ARM` 等）。
  - 🇭🇰 **香港 (`HK`)**：新增 `HSI` / `HANGSENG`（恒生指數 85 檔藍籌）與 `HSTECH`（恒生科技 30 檔科技旗艦）。
  - 🇪🇺 **歐洲 (`EU`)**：新增 `DAX40`（德國 40 檔）、`FTSE100`（英國富時 100 檔）、`EUROSTOXX50`（歐洲藍籌 50 檔）。
- **FastAPI 全球多市場（TW, US, JP, HK, EU）五大核心架構升級 (`app.py`)**:
  - `/indices`：全面輸出五大市場分類目錄。
  - `/stocks/{index_name}`：全面支援大小寫、別名映射與相容模式。
  - `/stock/{stock_code}`：支援跨五大市場的代碼智慧解析（包含 `.TW`, `.T`, `.HK`, `.DE`, `.L`, `.PA` 等）。
  - `/search/{company_name}`：全球跨市場模糊搜尋公司名稱或代號。
  - `/market/{market}`：依市場代碼返回該市場全量指數與成分股字典。
- **Cloudflare Workers KV 批次上傳腳本擴充 (`upload2KV.sh`)**:
  - 補齊台股、美股、日股、港股、歐股所有大盤與 ETF 鍵值映射，一鍵同步發布至邊緣節點。
- **文檔全面更新**:
  - 更新 `readme.md` 說明新增之全球市場、指數代號、端點用法與資料結構。

### Security
- 嚴格遵守零洩漏鐵律，無任何硬編碼 API Key 或憑證。

## [1.1.0] - 2026-10-31

### Added
- **Nikkei 225 (日經 225 / N225 / JP225) 支援**:
  - `crawler-i18n.py` 新增日經 225 資料收集功能，抓取 Wikipedia 即時成分股資料，並內嵌 225 檔東京證券交易所龍頭成分股完整備援清單（包含 `8035.T` Tokyo Electron、`9984.T` SoftBank Group、`6857.T` Advantest、`6146.T` Disco、`4063.T` Shin-Etsu、`6920.T` Lasertec 等）。
  - 自動產出 `data/nikkei225_data.json`。
- **AI & Space Frontier Tickers 支援**:
  - 於 `crawler-i18n.py` 之 S&P 500 成分股資料收集流程中，自動補齊並確保創新科技與太空概念股：`SPCX`, `DXYZ`, `ASTS`, `RKLB`, `CRWV`, `FN`, `CLS`。
- **FastAPI 多市場與日股端點擴充 (`app.py`)**:
  - 新增 `JP_INDICES = ["NIKKEI225"]`。
  - `/indices` 新增 `"JP": ["NIKKEI225"]`。
  - `/stocks/{index_name}` 支援 `NIKKEI225`, `N225`, `JP225`，自動讀取 `nikkei225_data.json` 並回傳 `market: "JP"`。
  - `/stock/{stock_code}` 支援日股代號查詢（如 `8035` 與 `8035.T` 雙向解析相容）。
  - `/search/{company_name}` 支援日股公司名稱模糊搜尋。
  - `/market/{market}` 支援 `JP` 市場查詢。
- **Cloudflare KV 上傳擴充 (`upload2KV.sh`)**:
  - 新增 `NIKKEI225`, `N225`, `JP225` 三個 Key 指向 `nikkei225_data.json`，自動同步至 Cloudflare Workers KV。
- **專案文檔更新**:
  - 更新 `readme.md` 說明日股日經 225 端點、Frontier 概念股擴充與 KV 映射設定。

### Fixed
- **台股基金持股相容性**:
  - `app.py` 中 `load_stock_data()` 增強自動映射機制，若找不到 `stock_data_{index}.json` 則平滑降級讀取 `fund_{index}.json`。

### Security
- 遵循零洩漏鐵律，無任何硬編碼 API Key 或憑證。
