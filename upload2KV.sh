#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="$ROOT_DIR/data"
PYTHON_BIN="${PYTHON_BIN:-python3}"
KV_NAMESPACE_ID="${CLOUDFLARE_KV_NAMESPACE_ID:-}"

if [[ -z "$KV_NAMESPACE_ID" ]]; then
  echo "CLOUDFLARE_KV_NAMESPACE_ID is required." >&2
  exit 1
fi

if [[ -z "${GITHUB_ACTIONS:-}" && -z "${VIRTUAL_ENV:-}" && -f "$ROOT_DIR/.venv/bin/activate" ]]; then
  # Use the local virtual environment automatically for manual runs.
  # shellcheck disable=SC1091
  source "$ROOT_DIR/.venv/bin/activate"
fi

cd "$ROOT_DIR"

"$PYTHON_BIN" crawler-mops-individual.py || true
"$PYTHON_BIN" crawler-i18n.py

cd "$DATA_DIR"

if [[ ! -d node_modules ]]; then
  echo "Node.js dependencies are missing in $DATA_DIR. Run 'npm ci' in the data directory first." >&2
  exit 1
fi

upload_json() {
  local key="$1"
  local file_path="$2"

  if [[ -f "$file_path" ]]; then
    npx wrangler kv key put "$key" \
      --namespace-id="$KV_NAMESPACE_ID" \
      --path "$file_path" \
      --remote
  else
    echo "Warning: File $file_path does not exist, skipping key $key" >&2
  fi
}

# --- US Markets ---
upload_json "SP500" "sp500_data.json"
upload_json "nasdaq100" "nasdaq100_data.json"
upload_json "NASDAQ100" "nasdaq100_data.json"
upload_json "dowjones" "dowjones_data.json"
upload_json "DOWJONES" "dowjones_data.json"
upload_json "SOX" "sox_data.json"
upload_json "PHLX" "sox_data.json"

# --- JP Markets ---
upload_json "NIKKEI225" "nikkei225_data.json"
upload_json "N225" "nikkei225_data.json"
upload_json "JP225" "nikkei225_data.json"

# --- TW Core ETFs & Popular Indices ---
upload_json "TW0050" "tw0050_data.json"
upload_json "0050" "tw0050_data.json"
upload_json "TW0100" "tw0100_data.json"
upload_json "0100" "tw0100_data.json"
upload_json "TW0051" "tw0100_data.json"
upload_json "0051" "tw0100_data.json"
upload_json "TW0056" "tw0056_data.json"
upload_json "0056" "tw0056_data.json"
upload_json "TW00878" "tw00878_data.json"
upload_json "00878" "tw00878_data.json"
upload_json "TW00919" "tw00919_data.json"
upload_json "00919" "tw00919_data.json"
upload_json "TW00929" "tw00929_data.json"
upload_json "00929" "tw00929_data.json"
upload_json "TW00940" "tw00940_data.json"
upload_json "00940" "tw00940_data.json"
upload_json "TW00713" "tw00713_data.json"
upload_json "00713" "tw00713_data.json"
upload_json "TW00850" "tw00850_data.json"
upload_json "00850" "tw00850_data.json"
upload_json "TPEX50" "tpex50_data.json"
upload_json "006201" "tpex50_data.json"

# --- TW Whole Markets (TWSE / TPEx / All) ---
upload_json "TAIEX" "taiex_data.json"
upload_json "TWSE" "taiex_data.json"
upload_json "TPEX" "tpex_data.json"
upload_json "OTC" "tpex_data.json"
upload_json "TW_ALL" "twall_data.json"
upload_json "TWALL" "twall_data.json"

# --- HK Markets ---
upload_json "HSI" "hsi_data.json"
upload_json "HANGSENG" "hsi_data.json"
upload_json "HSTECH" "hstech_data.json"

# --- EU Markets ---
upload_json "DAX40" "dax40_data.json"
upload_json "DAX" "dax40_data.json"
upload_json "FTSE100" "ftse100_data.json"
upload_json "FTSE" "ftse100_data.json"
upload_json "EUROSTOXX50" "eurostoxx50_data.json"
upload_json "STOXX50" "eurostoxx50_data.json"
