1. Создайте виртуальную среду: `python -m venv venv`
2. Активируйте ее: `venv\Scripts\activate`
1. Установите зависимости: `pip install -r requirements.txt`
2. Запустите: `python main.py` или `python -m calculator`

Структура
```
calculator/
├── __init__.py
├── __main__.py
├── calculator_logic.py
├── calculator_history.py
├── calculator_ui.py
├── config.py
├── ui/
│   ├── ui_display.py
│   ├── ui_top_buttons.py
│   ├── ui_history.py
│   ├── ui_themes.py
│   └── ui_buttons.py
└── themes/
    ├── light.qss
    └── dark.qss
main.py
requirements.txt
README.md
.gitignore
```
