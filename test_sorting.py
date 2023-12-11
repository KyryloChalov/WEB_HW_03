""" тестування для модуля sort_path """
import shutil
from time import time

from colors import GRAY, RESET
from input_output import Console
from sorting import sorting

shutil.rmtree("D:\\000", ignore_errors=True)
input(f"{GRAY}Folder 'D:\\000' was removed.{RESET}      press enter >>> ")  # пауза
shutil.copytree("D:\\000_Original", "D:\\000")
input(f"{GRAY}Folder 'D:\\000' was prepared.{RESET}     press enter >>> ")  # пауза

timer = time()
# Console.output(sorting("d:\\000", "+"))
Console.output(sorting("d:\\000"))
# Console.output(sorting("d:\\00"))
# Console.output(sorting())
Console.output(f" --- Done in {time() - timer} sec")
