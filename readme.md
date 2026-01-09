# Stock Index API

提供台灣股市指數成分股與基金持股資料的 API 服務。

## 功能

### 1. 國際指數成分股
- S&P 500
- NASDAQ 100  
- Dow Jones

### 2. 台灣 ETF 基金持股
從公開資訊觀測站 (MOPS) 抓取基金每季持股明細。

#### 目前支援的基金
| 基金名稱 | 股票代碼 | 檔案名稱格式 | 持股數 |
|---------|---------|-------------|--------|
| 元大台灣卓越50 | 0050 | `fund_元大台灣卓越50_114_04.json` | 54 |
| 元大台灣中型100 | 0100 | `fund_元大台灣中型100_114_04.json` | 104 |
| 元大台灣高股息 | 0056 | `fund_台灣高股息_114_04.json` | 54 |
| 元大摩臺 | 0057 | `fund_摩臺_114_04.json` | 90 |
| 元大台灣高股息低波動 | 00713 | `fund_台灣高股息低波動ETF_114_04.json` | 55 |
| 元大臺灣ESG永續 | 00850 | `fund_臺灣ESG永續ETF_114_04.json` | 109 |
| 元大臺灣價值高息 | 00940 | `fund_臺灣價值高息ETF_114_04.json` | 54 |

*註：檔名格式為 `fund_{基金名稱}_{年度}_{季度}.json`*

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

**自動偵測最新季度**：腳本會根據當前日期自動計算最新可用的季度（延遲一季）。

執行後會在 `data/` 目錄下生成：
- `fund_元大台灣卓越50_114_04.json` - 0050 持股明細
- `fund_元大台灣中型100_114_04.json` - 0100 持股明細
- `fund_*.json` - 其他基金持股明細
- `funds_summary_114_04.json` - 所有基金摘要

### 資料格式
```json
[
  {
    "股票代號": "2330",
    "股票名稱": "台積電",
    "持股比率": "47.12%",
    "產業類別": "半導體業"
  }
]
```

## 自訂設定

### 手動指定季度
編輯 `crawler-mops-individual.py` 最後幾行：

```python
# 取消註解並修改：
roc_year = 115  # 民國年
season = 1      # 季度 (1-4)
```

### 新增基金映射
編輯 `FUND_NAME_MAPPING` 字典：

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
1. 抓取最新資料
2. 上傳到 Cloudflare KV Storage

### 使用 Docker
```bash
docker-compose up -d
```

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
4. **檔名格式**：統一使用 `fund_{基金名稱}_{年度}_{季度}.json`

## 專案結構
```
.
├── app.py                          # Flask API 主程式
├── crawler-mops-individual.py      # MOPS 基金持股爬蟲 (自動偵測最新季度)
├── crawler-i18n.py                 # 國際指數爬蟲
├── crawler-sp500.py                # S&P 500 爬蟲
├── crawler.py                      # 舊版爬蟲
├── upload2KV.sh                    # 上傳腳本
├── data/                           # 資料目錄
│   ├── fund_元大台灣卓越50_114_04.json
│   ├── fund_元大台灣中型100_114_04.json
│   └── funds_summary_114_04.json
└── requirements.txt
```

## 貢獻

歡迎提交 PR 新增更多基金映射或改進爬蟲邏輯！
