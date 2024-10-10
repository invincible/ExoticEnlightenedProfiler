import difflib
import html


def compare_texts(text1, text2):
    """
    Сравнивает два текста и возвращает разницу в виде HTML.

    Args:
        text1: Содержимое первого файла.
        text2: Содержимое второго файла.
    
    Returns:
        str: HTML-строка с результатом сравнения.
    """

    file1_content = text1.splitlines()
    file2_content = text2.splitlines()

    html_output = "<style>\n"
    html_output += "del { background-color: #ffe0e0; text-decoration: line-through; }\n"
    html_output += "add { background-color: #e0ffe0; }\n"
    html_output += "</style>\n"

    html_output += "<h3>Различия в текстах:</h3>\n"

    for i, (line1, line2) in enumerate(zip(file1_content, file2_content)):
        matcher = difflib.SequenceMatcher(None, line1, line2)

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                html_output += html.escape(line1[i1:i2])
            elif tag == 'insert':
                html_output += f"<add>{html.escape(line2[j1:j2])}</add>"
            elif tag == 'delete':
                html_output += f"<del>{html.escape(line1[i1:i2])}</del>"
            elif tag == 'replace':
                html_output += f"<del>{html.escape(line1[i1:i2])}</del><add>{html.escape(line2[j1:j2])}</add>"

        html_output += "<br>\n"  # Переход на новую строку

    # Обработка оставшихся строк, если файлы разной длины
    for line in file1_content[len(file2_content):]:
        html_output += f"<del>{html.escape(line)}</del><br>\n"
    for line in file2_content[len(file1_content):]:
        html_output += f"<add>{html.escape(line)}</add><br>\n"

    return html_output


if __name__ == '__main__':
    file1_path = "file1.txt"  # Замените на путь к вашему первому файлу
    file2_path = "file2.txt"  # Замените на путь к вашему второму файлу
    compare_files(file1_path, file2_path)
