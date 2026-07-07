#!/bin/bash

# Проверка запуска от root
if [ "$EUID" -ne 0 ]; then
    echo "Ошибка: скрипт нужно запускать от root (sudo)."
    exit 1
fi

echo "=== 1. Создание пользователя user с группой default_users ==="
groupadd -f default_users
if id "user" &>/dev/null; then
    echo "Пользователь user уже существует"
else
    useradd -m -g default_users user
    echo "Пользователь user создан"
fi

echo "=== 2. Создание группы secret_users и пользователей secret_* ==="
groupadd -f secret_users

for username in secret_agent secret_spy secret_boss; do
    if id "$username" &>/dev/null; then
        echo "Пользователь $username уже существует"
    else
        useradd -m -g secret_users "$username"
        echo "Пользователь $username создан"
    fi
done

echo "=== 3. Установка прав 770 на домашние папки secret_users ==="
for username in secret_agent secret_spy secret_boss; do
    homedir="/home/$username"
    if [ -d "$homedir" ]; then
        chgrp -R secret_users "$homedir"
        chmod 770 "$homedir"
        echo "Права на $homedir: $(stat -c %A $homedir)"
    fi
done

echo "=== 4. Установка прав 777 на /var ==="
chmod 777 /var
echo "Права на /var: $(stat -c %A /var)"

echo "=== 5. Установка Apache2 и вывод состояния ==="
apt update -y
apt install -y apache2
systemctl start apache2
systemctl enable apache2
echo "Состояние службы apache2:"
systemctl status apache2 --no-pager || echo "Не удалось получить статус"

echo "=== 6. Добавление строки sudo для default_users в /etc/sudoers ==="
SUDOERS_LINE="%default_users ALL=(ALL) NOPASSWD:ALL"
if grep -q "^%default_users" /etc/sudoers; then
    echo "Строка для default_users уже присутствует в /etc/sudoers"
else
    echo "$SUDOERS_LINE" >> /etc/sudoers
    echo "Строка добавлена в /etc/sudoers"
fi

# Проверка синтаксиса sudoers
if visudo -c; then
    echo "Синтаксис /etc/sudoers корректен"
else
    echo "Ошибка в /etc/sudoers! Проверьте вручную."
fi

echo "=== Настройка завершена ==="
