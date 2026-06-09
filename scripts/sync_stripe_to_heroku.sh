#!/usr/bin/env bash
# Push Stripe test keys from local .env to Heroku config vars.
# Usage: heroku login && bash scripts/sync_stripe_to_heroku.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP="${HEROKU_APP:-esa-project}"
ENV_FILE="${ROOT}/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Missing $ENV_FILE — add STRIPE_PUBLISHABLE_KEY and STRIPE_SECRET_KEY first."
  exit 1
fi

# Parse .env safely (bash `source` breaks on DATABASE_URL etc.)
read_stripe_var() {
  python3 - "$ENV_FILE" "$1" <<'PY'
import sys
from pathlib import Path
key = sys.argv[2]
for line in Path(sys.argv[1]).read_text().splitlines():
    line = line.strip()
    if not line or line.startswith('#') or '=' not in line:
        continue
    k, v = line.split('=', 1)
    if k.strip() == key:
        print(v.strip().strip('"').strip("'"))
        break
PY
}

STRIPE_PUBLISHABLE_KEY="$(read_stripe_var STRIPE_PUBLISHABLE_KEY)"
STRIPE_SECRET_KEY="$(read_stripe_var STRIPE_SECRET_KEY)"
STRIPE_WEBHOOK_SECRET="$(read_stripe_var STRIPE_WEBHOOK_SECRET)"

if [[ -z "$STRIPE_PUBLISHABLE_KEY" || -z "$STRIPE_SECRET_KEY" ]]; then
  echo "STRIPE_PUBLISHABLE_KEY and STRIPE_SECRET_KEY must be set in .env"
  exit 1
fi

echo "Setting Stripe config on Heroku app: $APP"
echo "  publishable key length: ${#STRIPE_PUBLISHABLE_KEY}"
echo "  secret key length: ${#STRIPE_SECRET_KEY}"

heroku config:set \
  STRIPE_PUBLISHABLE_KEY="$STRIPE_PUBLISHABLE_KEY" \
  STRIPE_SECRET_KEY="$STRIPE_SECRET_KEY" \
  -a "$APP"

if [[ -n "$STRIPE_WEBHOOK_SECRET" ]]; then
  heroku config:set STRIPE_WEBHOOK_SECRET="$STRIPE_WEBHOOK_SECRET" -a "$APP"
fi

echo "Done. Restarting dynos..."
heroku restart -a "$APP"
echo "Open /payments/ as parent_demo — you should see the Stripe test mode banner."
