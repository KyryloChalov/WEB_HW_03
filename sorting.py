""" sort_path module 
адаптовано для використання як у вигляді функції, 
так і в якості окремого скрипту для сортування файлів 
виклик: 
скрипт:  sort_path <dir> <replace>(optional)
або 
функція: sort_path(<dir>, <replace=None>)
"""

import shutil
import sys

from pathlib import Path
from threading import Thread

from colors import RED, YELLOW, GRAY, R, RESET
from input_output import Console
from normalization import normalize

FILE_LIST_TITLE = "\t_ List Of Files: _"
FILE_LIST_NAME = "_file_list_.txt"


CATEGORIES = {
    "Archives": [".zip", ".gz", ".tar"],
    "Audio": [".mp3", ".wav", ".flac", ".wma", ".ogg"],
    "Video": [".avi", ".mp4", ".mov", ".mkv"],
    "Images": [".jpeg", ".png", ".jpg", ".svg", ".gif"],
    "Documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "Python": [".py", ".pyw", ".cpy"],
    "Other": [""],
}


def archive_unpack(folder_path: Path) -> None:
    """unpack archive"""

    for key, val in CATEGORIES.items():
        # те, що починається з "arc" - то є категорія "архів" - трохи милиця
        if key.lower()[:3] == "arc":
            category_arc_key = key
            category_arc_val = val
            path_arc = folder_path.joinpath(category_arc_key)
            if path_arc.exists():
                for element_file in path_arc.glob("*"):
                    if all(
                        [
                            element_file.is_file(),
                            element_file.suffix in category_arc_val,
                        ]
                    ):
                        Console.output(f"\tUnpacking: {element_file.name} ...")
                        # shutil.unpack_archive(element_file, path_arc.joinpath(element_file.stem))
                        # # here we do multithreading
                        unpack_arc = Thread(
                            target=shutil.unpack_archive,
                            args=(element_file, path_arc.joinpath(element_file.stem)),
                        )
                        unpack_arc.start()


def del_empty_tree(path: Path) -> None:
    """deleting empty tree"""

    for element in path.glob("*"):
        if all([element.is_dir(), element.stem not in CATEGORIES]):
            shutil.rmtree(element)


def get_categories(file: Path) -> str:
    """get categories according file extensions"""

    extension = file.suffix.lower()

    for cat, list_of_extensions in CATEGORIES.items():
        if extension in list_of_extensions:
            return cat
    return "Other"


def move_file(file: Path, category: str, root_dir: Path, is_replace) -> None:
    """move file to target folder"""

    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        try:
            target_dir.mkdir()
        except FileExistsError:
            ...

    new_path = target_dir.joinpath(normalize(file.name))

    if all([new_path.exists(), new_path != file, not is_replace]):
        while new_path.exists():
            new_path = new_path.with_stem(new_path.stem + "_")
    try:
        file.replace(new_path)
    except PermissionError:
        print(f"{RED}PermissionError: {RESET}{new_path} Access is denied")


def sort_folder(path: Path, replace) -> None:
    """sort folder"""

    threads = []
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            # move_file(element, category, path, is_replace)
            # here we do multithreading
            move = Thread(target=move_file, args=(element, category, path, replace))
            move.start()
            threads.append(move)

    [el.join() for el in threads]


def number_str(count) -> str:
    """forming a beautiful row number"""
    return " " * (3 - len(str(count))) + str(count) + ". "


def list_files_screen(el_path: Path) -> None:
    """print file list to screen - main dir only"""

    file_list = el_path.joinpath(FILE_LIST_NAME)
    count = 0

    Console.output(YELLOW + FILE_LIST_TITLE + RESET)

    for element in el_path.glob("**/*"):
        if all([element.is_file(), element != file_list]):
            count += 1
            file_name = str(element)[len(str(el_path)) + 1 :]
            Console.output(GRAY + number_str(count) + RESET + file_name)


def list_files_write_file(el_path, glob_str) -> None:
    """write file list"""

    el_path = Path(el_path) # милиця?

    file_list = el_path.joinpath(FILE_LIST_NAME)
    count = 0
    text_to_file = FILE_LIST_TITLE + "\n"

    for element in el_path.glob(glob_str):
        if all([element.is_file(), element != file_list]):
            count += 1
            file_name = str(element)[len(str(el_path)) + 1 :]
            text_to_file += number_str(count) + file_name + "\n"

    with open(file_list, "w", encoding="utf8") as file_output:
        file_output.write(text_to_file)


def list_files(path: Path) -> None:
    """list of files in folders"""

    list_files_write_file(path, "**/*")  # for main dir

    for element_path in path.iterdir():  # for iterdir
        if element_path.is_dir():
            # list_files_write_file(element_path)
            # # here we do multithreading
            file_write = Thread(target=list_files_write_file, args=(str(element_path),"*"))
            file_write.start()


def sorting(*args) -> str:
    """main function"""

    # чи вказано теку для сортування?
    if len(args) >= 1 and args[0] != []:
        if isinstance(args[0], list):
            path = Path(args[0][0])  # окремий скрипт
        else:
            path = Path(args[0])  # виклик як функція
    else:
        # теку не вказано
        return f"\t{RED}no path to folder\n\t{GRAY}format:{R} sorting <path> {GRAY}<replace>{RESET}"

    if not path.exists():
        # вказано теку, що не існує
        return f"   {RED}folder {RESET}'{path}'{RED} does not exist{RESET}"

    # другий аргумент (будь-що, наприклад, "+") - робимо replace файлів якщо імена однакові
    if len(args) >= 2 and args[1] != []:
        if isinstance(args[1], list):
            replace = args[1][0]  # окремий скрипт
        else:
            replace = args[1]  # виклик як функція
    else:
        replace = None

    sort_folder(path, replace)

    list_files_screen(path)

    list_files(path)

    archive_unpack(path)

    del_empty_tree(path)

    return f"{YELLOW}\n*** Completed Successfully ***\n{RESET}"


if __name__ == "__main__":
    Console.output(sorting(sys.argv[1:][0:1], sys.argv[1:][1:2]))
