import os


def check_project_structure():
    print("Проверка структуры проекта...")
    print("=" * 50)

    for root, dirs, files in os.walk("."):
        # Пропускаем папки .venv и другие служебные
        if '.venv' in root or '__pycache__' in root:
            continue

        level = root.replace(".", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")

        subindent = " " * 2 * (level + 1)
        for file in files:
            if file.endswith('.py') or file in ['requirements.txt']:
                print(f"{subindent}{file}")


if __name__ == "__main__":
    check_project_structure()