# WEB_HW_03
Домашнє завдання #3

part 1: 
======
sorting.py - сортування файлів у вказаному фолдері за розширеннями з використанням кількох потоків 

виклик можливий як з командної строки:
py sorting.py <path> <replace(optional>) 

так і з іншої програми в якості функції:
sorting(<path>, <replace=None>)

        path - фолдер для сортування 
        replace - якщо встановлено "+" - файли з однаковими іменами буде перезаписано

part 2:
======
factorize.py - реалізовано функцію factorize, яка приймає список чисел та повертає список чисел, 
                на які числа з вхідного списку поділяються без залишку

    def synchronic() - синхронна версія - обчислення виконуються одним потоком

    def parallel() - паралельна версія - реалізовано використання кількох ядер процесора 
                        для паралельних обчислень 

    в процесі роботи програми проводяться заміри часу виконання для обох варіантів 

factorize_detail.py - зроблено деталізований вивід даних для демонстрації різниці
                        між синхронною та паралельною версією обчислень: 
                        в першому варіанті данні обробляються послідовно 
                        в другому - легко побачити, що послідовність завершення процесів
                        залежить від вхідних даних


решта файлів - службові