import os

# Рабочая папка — текущая
base_dir = "."

# Имя файла для сохранения списка
output_file = "file_list.txt"

with open(output_file, "w", encoding="utf-8") as f:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == output_file:
                continue  # Пропустить сам файл-вывод
            rel_path = os.path.relpath(os.path.join(root, file), base_dir)
            f.write(rel_path + "\n")

print(f"Список файлов сохранён в {output_file}")
