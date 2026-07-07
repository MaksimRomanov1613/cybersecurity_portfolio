#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Ошибка: скрипт нужно запускать от root (sudo)."
    exit 1
fi

INFO_FILE="info"
> "$INFO_FILE"

echo "======== УСТАНОВЛЕННЫЕ ПАКЕТЫ ========" >> "$INFO_FILE"
dpkg -l >> "$INFO_FILE" 2>&1

echo "" >> "$INFO_FILE"
echo "======== ЗАПУЩЕННЫЕ ПРОЦЕССЫ ========" >> "$INFO_FILE"
ps aux >> "$INFO_FILE" 2>&1

echo "" >> "$INFO_FILE"
echo "======== ОТКРЫТЫЕ ПОРТЫ ========" >> "$INFO_FILE"
ss -tuln >> "$INFO_FILE" 2>&1

echo "" >> "$INFO_FILE"
echo "======== ВЕРСИЯ ЯДРА И ОС ========" >> "$INFO_FILE"
uname -a >> "$INFO_FILE"
cat /etc/os-release >> "$INFO_FILE"

# Установка cowsay и sl (уже стоят, не повредит)
apt update -y
apt install -y cowsay sl

# Упаковка
tar -cf OS_RESULT.tar "$INFO_FILE"
rm -f "$INFO_FILE"
echo "Архив OS_RESULT.tar создан."
