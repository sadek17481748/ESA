#!/usr/bin/env bash
# Push Gmail SMTP settings from local .env to Heroku.
# Usage: heroku login && bash scripts/sync_email_to_heroku.sh

set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
APP="${HEROKU_APP:-esa-project}"
ENV_FILE="${ROOT}/.env"

read_env_var() {
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

for var in ESA_PLATFORM_EMAIL EMAIL_HOST EMAIL_PORT EMAIL_USE_TLS EMAIL_HOST_USER EMAIL_HOST_PASSWORD DEFAULT_FROM_EMAIL; do
  if [[ -z "$(read_env_var "$var")" && "$var" != EMAIL_HOST_PASSWORD ]]; then
    echo "Optional/missing: $var"
  fi
done

USER_VAL="$(read_env_var EMAIL_HOST_USER)"
PASS_VAL="$(read_env_var EMAIL_HOST_PASSWORD)"
if [[ -z "$USER_VAL" || -z "$PASS_VAL" ]]; then
  echo "EMAIL_HOST_USER and EMAIL_HOST_PASSWORD must be set in .env (Gmail App Password)."
  exit 1
fi

heroku config:set \
  ESA_PLATFORM_EMAIL="$(read_env_var ESA_PLATFORM_EMAIL)" \
  EMAIL_HOST="$(read_env_var EMAIL_HOST)" \
  EMAIL_PORT="$(read_env_var EMAIL_PORT)" \
  EMAIL_USE_TLS="$(read_env_var EMAIL_USE_TLS)" \
  EMAIL_HOST_USER="$USER_VAL" \
  EMAIL_HOST_PASSWORD="$PASS_VAL" \
  DEFAULT_FROM_EMAIL="$(read_env_var DEFAULT_FROM_EMAIL)" \
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend \
  -a "$APP"

heroku restart -a "$APP"
echo "Done. Run: heroku run python manage.py send_test_email -a $APP"
