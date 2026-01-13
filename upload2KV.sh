source .venv/bin/activate

python3 crawler-mops-individual.py
python3 crawler-i18n.py

# 原本找不到 wrangler 指令 → 使用 pnpm install 安裝
# 新版 wrangler 語法改變 → 使用 pnpm wrangler kv key put 而非 wrangler kv:key put
# 需要使用 --path 參數從檔案讀取內容
# 需要加上 --remote 參數才會上傳到雲端而非本地
# wrangler login
pnpm install

cd data && \
pnpm wrangler kv key put SP500 --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --path sp500_data.json --remote && \
pnpm wrangler kv key put TW0050 --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --path fund_0050.json --remote && \
pnpm wrangler kv key put TW0100 --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --path fund_0100.json --remote && \
pnpm wrangler kv key put nasdaq100 --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --path nasdaq100_data.json --remote && \
pnpm wrangler kv key put dowjones --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --path dowjones_data.json --remote
