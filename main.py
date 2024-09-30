import difflib


def compare_files(file1, file2):
    """
    Сравнивает два файла и отображает разницу с учётом русского языка.

    Args:
        file1: Путь к первому файлу.
        file2: Путь ко второму файлу.
    """

    try:
        with open(file1,
                  'r', encoding='utf-8') as f1, open(file2,
                                                     'r',
                                                     encoding='utf-8') as f2:
            file1_content = f1.readlines()
            file2_content = f2.readlines()

        diff = difflib.ndiff(file1_content, file2_content)

        added_lines = 0
        removed_lines = 0

        print("Различия в файлах:")
        for line in diff:
            if line.startswith('+'):
                added_lines += 1
                print(f"\033[92m{line[1:]}\033[0m", end="")  # Убираем '+'
            elif line.startswith('-'):
                removed_lines += 1
                print(f"\033[91m{line[1:]}\033[0m", end="")  # Убираем '-'
            else:
                print(line, end="")

        print("\nСводка:")
        print(f"Добавленные строки: {added_lines}")
        print(f"Удаленные строки: {removed_lines}")

        print("\nСравнение по строкам:")
        for i, (line1, line2) in enumerate(zip(file1_content, file2_content)):
            if line1 == line2:
                print(f"  {line1.rstrip()}\t{line2.rstrip()}")
            else:
                for j, (char1, char2) in enumerate(zip(line1, line2)):
                    if char1 == char2:
                        print(char1, end="")
                    elif char1 != char2:
                        if i == added_lines - 1 and j == 0:
                            print(f"\033[92m{char2}\033[0m", end="")
                        else:
                            print(f"\033[91m{char1}\033[0m", end="")
                print(f"\t\033[92m{line2[j+1:]}\033[0m", end="")
                print()
                added_lines -= 1

    except FileNotFoundError:
        print(f"Ошибка: Один или оба файла не найдены.")


if __name__ == '__main__':
    file1_path = "file1.txt"  # Замените на путь к вашему первому файлу
    file2_path = "file2.txt"  # Замените на путь к вашему второму файлу
    compare_files(file1_path, file2_path)
