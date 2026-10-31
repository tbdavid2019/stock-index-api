# Changelog

All notable changes to the `stock-index-api` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
