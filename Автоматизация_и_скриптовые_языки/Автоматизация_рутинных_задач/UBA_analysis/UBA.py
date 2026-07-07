#!/usr/bin/env python3
import time
import sys
from pynput import keyboard
from statistics import stdev

def record_input(prompt):
    print(prompt, end='', flush=True)
    timestamps = []
    entered_chars = []

    def on_press(key):
        try:
            if hasattr(key, 'char') and key.char is not None:
                timestamps.append(time.perf_counter())
                entered_chars.append(key.char)
            elif key == keyboard.Key.enter:
                return False
        except AttributeError:
            pass

    with keyboard.Listener(on_press=on_press, suppress=False) as listener:
        listener.join()

    print()
    if len(timestamps) < 2:
        return []
    intervals = [timestamps[i+1] - timestamps[i] for i in range(len(timestamps)-1)]
    return intervals

def main():
    print("Анализ поведенческого ввода с клавиатуры")
    print("Вам будет предложено дважды ввести одну и ту же строку.\n")

    intervals1 = record_input("Введите строку (1-й раз): ")
    if len(intervals1) < 2:
        print("Недостаточно данных для анализа. Завершение.")
        sys.exit(1)

    intervals2 = record_input("Введите ту же строку (2-й раз): ")
    if len(intervals2) < 2:
        print("Недостаточно данных для анализа. Завершение.")
        sys.exit(1)

    try:
        std1 = stdev(intervals1)
        std2 = stdev(intervals2)
    except Exception as e:
        print(f"Ошибка при расчёте статистики: {e}")
        sys.exit(1)

    if abs(std1 - std2) > 0.1:
        print("Обнаружены отклонения в поведении. Возможно, вводил другой человек")
    else:
        print("Ввод соответствует исходному пользователю")

if __name__ == "__main__":
    main()
