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

"$PYTHON_BIN" crawler-mops-individual.py
"$PYTHON_BIN" crawler-i18n.py

cd "$DATA_DIR"

if [[ ! -d node_modules ]]; then
  echo "Node.js dependencies are missing in $DATA_DIR. Run 'npm ci' in the data directory first." >&2
  exit 1
fi

upload_json() {
  local key="$1"
  local file_path="$2"

  npx wrangler kv key put "$key" \
    --namespace-id="$KV_NAMESPACE_ID" \
    --path "$file_path" \
    --remote
}

upload_json "SP500" "sp500_data.json"
upload_json "TW0050" "fund_0050.json"
upload_json "TW0100" "fund_0100.json"
upload_json "nasdaq100" "nasdaq100_data.json"
upload_json "dowjones" "dowjones_data.json"
