source myenv/bin/activate

python crawler-mops-individual.py
python crawler-i18n.py

# 原本找不到 wrangler 指令 → 使用 pnpm install 安裝
# 新版 wrangler 語法改變 → 使用 pnpm wrangler kv key put 而非 wrangler kv:key put
# 需要使用 --path 參數從檔案讀取內容
# 需要加上 --remote 參數才會上傳到雲端而非本地
# wrangler login
pnpm install

cd data && \
pnpm wrangler kv key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --remote "SP500" --path sp500_data.json && \
pnpm wrangler kv key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --remote "TW0050" --path fund_元大台灣卓越50_114_04.json && \
pnpm wrangler kv key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --remote "TW0100" --path fund_元大台灣中型100_114_04.json && \
pnpm wrangler kv key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --remote "nasdaq100" --path nasdaq100_data.json && \
pnpm wrangler kv key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 --remote "dowjones" --path dowjones_data.json