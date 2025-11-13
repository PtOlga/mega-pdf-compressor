"""
Локальный запуск для тестирования
Использование:
1. Создайте файл .env с вашими ключами iLovePDF
2. Установите зависимости: pip install -r requirements.txt
3. Запустите: python run_local.py
"""
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Проверяем наличие ключей
if not os.getenv('ILOVEPDF_PUBLIC_KEY') or not os.getenv('ILOVEPDF_SECRET_KEY'):
    print("⚠️  ОШИБКА: Не найдены API ключи!")
    print("Создайте файл .env на основе .env.example")
    exit(1)

print("✅ API ключи загружены")
print("🚀 Запуск сервера на http://localhost:8000")

from app import app
app.run(host='0.0.0.0', port=8000, debug=True)

