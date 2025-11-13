# ⚡ Шпаргалка по командам

## 🏃 Локальный запуск (БЕЗ Docker)

```bash
# 1. Перейдите в backend
cd backend

# 2. Создайте виртуальное окружение
python -m venv venv

# 3. Активируйте его
venv\Scripts\activate          # Windows
source venv/bin/activate       # Linux/Mac

# 4. Установите зависимости
pip install -r requirements.txt

# 5. Создайте .env файл
copy .env.example .env         # Windows
cp .env.example .env           # Linux/Mac

# 6. Отредактируйте .env и добавьте ваши ключи iLovePDF

# 7. Запустите сервер
python run_local.py

# Сервер запустится на http://localhost:8000
```

---

## 🐳 Запуск с Docker (опционально)

```bash
# 1. Соберите образ
docker build -t mega-pdf-compressor ./backend

# 2. Запустите контейнер
docker run -p 8000:8000 --env-file backend/.env mega-pdf-compressor

# Или с явными переменными:
docker run -p 8000:8000 \
  -e ILOVEPDF_PUBLIC_KEY=your_key \
  -e ILOVEPDF_SECRET_KEY=your_secret \
  mega-pdf-compressor
```

---

## 🚂 Деплой на Railway

```bash
# 1. Закоммитьте код
git add .
git commit -m "Ready for deploy"
git push origin main

# 2. Зайдите на railway.app
# 3. New Project → Deploy from GitHub repo
# 4. Выберите репозиторий
# 5. Settings → Root Directory → backend
# 6. Variables → добавьте ILOVEPDF_PUBLIC_KEY и ILOVEPDF_SECRET_KEY
# 7. Settings → Networking → Generate Domain
```

---

## 🌐 GitHub Pages

```bash
# 1. Обновите URL в frontend/index.html (строка 62)
# 2. Закоммитьте
git add frontend/index.html
git commit -m "Update backend URL"
git push

# 3. GitHub → Settings → Pages
# 4. Source: main branch, / (root)
# 5. Ваш сайт: https://username.github.io/mega-pdf-compressor/frontend/
```

---

## 🔍 Проверка работы

```bash
# Проверьте health endpoint
curl http://localhost:8000/health          # Локально
curl https://your-app.up.railway.app/health  # Railway

# Должно вернуть: OK
```

---

## 🛑 Остановка

```bash
# Локальный сервер: Ctrl+C

# Деактивировать venv:
deactivate

# Остановить Docker:
docker ps                    # Найдите CONTAINER ID
docker stop <container_id>
```

---

## 📝 Полезные ссылки

- iLovePDF API: https://developer.ilovepdf.com/
- Railway: https://railway.app/
- MEGA SDK: https://mega.nz/sdk/

