# tests — тесты библиотеки stealth
Запуск из корня библиотеки (папка stealth\):
    python -m unittest discover -s tests -v
    python -m pytest tests -v
test_stealth.py включает loopback-тест: реальный send -> listener -> сборка сообщения.
