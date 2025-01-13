source myenv/bin/activate

python crawler-i18n.py
python crawler.py



# wrangler login
cd data/
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "SP500" "$(cat sp500_data.json)"
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "TW0050" "$(cat stock_data_0050.json)"
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "TW0051" "$(cat stock_data_0100.json)"
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "nasdaq100" "$(cat nasdaq100_data.json)"
wrangler kv:key put --namespace-id=5e8e4092fd964584a2152c4a6f948d47 "dowjones" "$(cat dowjones_data.json)"

