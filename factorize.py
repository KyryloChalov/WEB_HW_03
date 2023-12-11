"""
Напишіть реалізацію функції factorize, яка приймає список чисел та повертає список чисел, 
на які числа з вхідного списку поділяються без залишку.

Реалізуйте синхронну версію та виміряйте час виконання.

Потім покращіть продуктивність вашої функції, реалізувавши використання кількох ядер процесора 
для паралельних обчислень і замірте час виконання знову. 
Для визначення кількості ядер на машині використовуйте функцію cpu_count() з пакета multiprocessing
"""
import concurrent.futures
import logging

from time import time
from multiprocessing import cpu_count

from colors import RESET, YELLOW, CYAN, GRAY
from input_output import Console

NUMB = (128, 255, 99999, 10651060, 545654, 5584456, 6779716, 9339035, 55, 555)

logger = logging.getLogger("time_log")
logger.setLevel(logging.DEBUG)
logging.basicConfig(
    level=logging.DEBUG, format=f"> Done in {YELLOW}%(message)s sec{RESET}"
)


def factorize(*number):
    """
    приймає список чисел та повертає список чисел,
    на які числа з вхідного списку поділяються без залишку
    """
    result = "\n".join(
        f"{GRAY}Number {RESET}{num}\t{GRAY}dividers: {CYAN}"
        f"{', '.join(str(i) for i in range(1, num + 1) if num % i == 0)}{RESET}"
        for num in number
    )
    return result


def synchronic():
    """синхронна версія"""

    Console.output(YELLOW + "\n\tSynchronic code\n" + RESET)
    timer = time()
    Console.output(factorize(*NUMB))
    logger.debug(time() - timer)


def parallel():
    """паралельна версія"""

    Console.output(f"\n\t{YELLOW}Parallel code{GRAY} ({cpu_count() = }){RESET}\n")
    timer = time()

    with concurrent.futures.ProcessPoolExecutor(cpu_count()) as executor:
        for _, func in zip(NUMB, executor.map(factorize, NUMB)):
            Console.output(func)

    logger.debug(time() - timer)


if __name__ == "__main__":
    synchronic()

    parallel()
