#!/usr/bin/env bash
set -euo pipefail

# Переходим в папку скрипта (корень проекта)
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

# 1) обновить код
git pull --ff-only

# 2) установить зависимости (если файл есть)
if [[ -f requirements.txt ]]; then
  "$DIR/.venv/bin/pip" install -r requirements.txt
fi

# 3) перезапуск сервиса
systemctl restart atelier-bot

# 4) короткий статус
systemctl --no-pager --lines=20 status atelier-bot
