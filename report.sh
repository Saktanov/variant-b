#!/bin/bash

if [ "$#" -lt 2 ]; then
    echo "Использование: $0 <каталог> <ERROR|WARN> [--top N]"
    exit 1
fi

DIR="$1"
LEVEL="$2"
TOP=""

if [ ! -d "$DIR" ]; then
    echo "Ошибка: каталог '$DIR' не существует."
    exit 1
fi

if [ "$LEVEL" != "ERROR" ] && [ "$LEVEL" != "WARN" ]; then
    echo "Ошибка: уровень должен быть ERROR или WARN."
    exit 1
fi

if [ "$#" -eq 4 ]; then
    if [ "$3" != "--top" ]; then
        echo "Ошибка: неизвестный параметр $3"
        exit 1
    fi

    if ! [[ "$4" =~ ^[0-9]+$ ]] || [ "$4" -eq 0 ]; then
        echo "Ошибка: N должен быть положительным числом."
        exit 1
    fi

    TOP="$4"
elif [ "$#" -ne 2 ]; then
    echo "Использование: $0 <каталог> <ERROR|WARN> [--top N]"
    exit 1
fi

echo "Модуль                 Сообщения"
echo "--------------------------------"

RESULT=$(grep -rho "\[$LEVEL\]" "$DIR" 2>/dev/null | sort | uniq -c)

if [ -z "$RESULT" ]; then
    echo "Сообщений уровня $LEVEL не найдено."
    exit 0
fi

echo "$RESULT" | sort -nr | awk '{print $2, $1}' | while read module count; do
    printf "%-22s %s\n" "$module" "$count"
done
