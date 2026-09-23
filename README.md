# InevioLibs — три независимые сетевые технологии

Библиотеки, выделенные из InevioNet. Каждая самодостаточна (только stdlib Python),
собирается и работает НЕЗАВИСИМО от проекта. Точка входа и точка выхода у каждой свои.

## Структура
| Папка          | Технология              | Суть одним предложением |
|----------------|-------------------------|-------------------------|
| supernode\     | Коллективное обучение   | Узел, доказавший надёжную доставку, становится супер-узлом и передаёт опыт сети |
| sporerecon\    | Разведка сети           | Реальные факты о сети (DNS, маршрут, ISP, соседи, тип инфраструктуры) через nslookup/tracert/arp без прав админа |
| stealth\       | Адаптивная скрытность   | Замкнутый цикл «зонд -> маскировка -> отправка -> обучение» с байесовским выбором канала |

## Сборка и установка
    .\build_all.ps1              # тесты всех трёх + wheel-пакеты в dist\
    .\build_all.ps1 -Exe         # то же + standalone .exe (PyInstaller)
    .\build_all.ps1 -SkipTests   # только сборка, без тестов
    .\install_all.ps1            # установка всех wheel из dist\ в текущий Python

По отдельности:
    cd supernode ; python -m pip wheel . --no-deps -w ..\dist
    python -m pip install ..\dist\supernode-1.0.0-py3-none-any.whl

## Тесты (каждая библиотека отдельно)
    cd supernode  ; python -m unittest discover -s tests -v
    cd sporerecon ; python -m unittest discover -s tests -v
    cd stealth    ; python -m unittest discover -s tests -v

## REST-порты (для любых языков: C#, Go, JS, PHP...)
    supernode  -> http://127.0.0.1:8701
    sporerecon -> http://127.0.0.1:8702
    stealth    -> http://127.0.0.1:8704  (приёмник фрагментов: 8703)

## Где применяется ВНЕ InevioNet
    supernode  — роевая робототехника, federated learning, V2X, любые mesh, где обученный узел учит остальных
    sporerecon — инвентаризация сетей, red-team разведка без админа, антифрод-геолокация по DNS/ISP
    stealth    — исследование covert-каналов и DPI/IDS на СВОИХ сетях, privacy-инструменты (только легально)

В каждой папке лежит свой README.md: что это, для чего, как использовать.

## Лицензирование (Dual Licensing)
- Сообщество: AGPL-3.0 (файл LICENSE)
- Бизнес: коммерческая лицензия (файл LICENSE-COMMERCIAL.md)
- Copyright (c) 2026 dimon027081

