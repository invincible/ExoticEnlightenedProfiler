import difflib


def compare_files(file1, file2):
    """
    Сравнивает два файла и отображает разницу в виде HTML.

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

        html_output = "<html>\n<head>\n<style>\n"
        html_output += "del { background-color: #ffe0e0; text-decoration: line-through; }\n"
        html_output += "add { background-color: #e0ffe0; }\n"
        html_output += "</style>\n</head>\n<body>\n"

        html_output += "<h2>Различия в файлах:</h2>\n"

        for i, (line1, line2) in enumerate(zip(file1_content, file2_content)):
            matcher = difflib.SequenceMatcher(None, line1, line2)

            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == 'equal':
                    html_output += line1[i1:i2]
                elif tag == 'insert':
                    html_output += f"<add>{line2[j1:j2]}</add>"
                elif tag == 'delete':
                    html_output += f"<del>{line1[i1:i2]}</del>"

            if j2 < len(
                    line2
            ):  # Проверка на наличие символов в line2 после сравнения
                html_output += f"<add>{line2[j2:]}</add>"

            html_output += "<br>\n"  # Переход на новую строку

        html_output += "</body>\n</html>"

        print(html_output)

    except FileNotFoundError:
        print(f"Ошибка: Один или оба файла не найдены.")


if __name__ == '__main__':
    file1_path = "file1.txt"  # Замените на путь к вашему первому файлу
    file2_path = "file2.txt"  # Замените на путь к вашему второму файлу
    compare_files(file1_path, file2_path)
