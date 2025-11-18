from flask import Flask, request, send_file, jsonify, send_from_directory
from flask_cors import CORS
from pylovepdf.ilovepdf import ILovePdf
import tempfile
import os
import shutil

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для фронтенда

# ⚠️ ВАЖНО: Получите ключи на https://developer.ilovepdf.com/
# Бесплатный план: 250 запросов/месяц
ILOVEPDF_PUBLIC_KEY = os.environ.get('ILOVEPDF_PUBLIC_KEY', '')
ILOVEPDF_SECRET_KEY = os.environ.get('ILOVEPDF_SECRET_KEY', '')

@app.route('/')
def index():
    frontend_path = os.path.join(os.path.dirname(__file__), 'frontend')
    return send_from_directory(frontend_path, 'index.html')

@app.route('/health')
def health():
    return "OK"

@app.route('/compress', methods=['POST'])
def compress():
    logs = []

    if not ILOVEPDF_PUBLIC_KEY or not ILOVEPDF_SECRET_KEY:
        return jsonify({"error": "API ключи iLovePDF не настроены"}), 500

    file = request.files.get('file')
    logs.append(f"1. File object: {file}")
    logs.append(f"2. File type: {type(file)}")

    if not file:
        return jsonify({"error": "Файл не найден", "logs": logs}), 400

    logs.append(f"3. Filename: {file.filename}")
    logs.append(f"4. Content type: {file.content_type}")

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Только PDF файлы", "logs": logs}), 400

    input_path = None
    output_path = None

    try:
        # Сохраняем загруженный файл
        input_path = tempfile.mktemp(suffix=".pdf")
        logs.append(f"5. Temp path: {input_path}")

        # Читаем данные
        file_data = file.read()
        logs.append(f"6. File data type: {type(file_data)}")
        logs.append(f"7. File data length: {len(file_data) if file_data else 0}")

        # Записываем в файл
        with open(input_path, 'wb') as f:
            f.write(file_data)

        logs.append(f"8. File saved successfully")

        # Инициализируем iLovePDF
        ilovepdf = ILovePdf(ILOVEPDF_PUBLIC_KEY, verify_ssl=True)

        # Создаём задачу сжатия
        task = ilovepdf.new_task('compress')
        task.add_file(input_path)

        # Создаём временную папку для результата
        output_folder = tempfile.mkdtemp()
        task.set_output_folder(output_folder)

        # Выполняем сжатие (без параметров)
        task.execute()

        # Скачиваем результат
        task.download()

        # Находим скачанный файл в папке
        output_files = os.listdir(output_folder)
        if not output_files:
            raise Exception("Файл не был скачан")
        output_path = os.path.join(output_folder, output_files[0])

        # Получаем информацию о размерах
        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = round((1 - compressed_size / original_size) * 100, 1)

        response = send_file(
            output_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"[Сжато] {file.filename}"
        )

        # Добавляем заголовки с информацией о сжатии
        response.headers['X-Original-Size'] = str(original_size)
        response.headers['X-Compressed-Size'] = str(compressed_size)
        response.headers['X-Reduction-Percent'] = str(reduction)

        return response

    except Exception as e:
        import traceback
        logs.append(f"ERROR: {str(e)}")
        logs.append(f"TRACEBACK: {traceback.format_exc()}")
        return jsonify({"error": f"Ошибка сжатия: {str(e)}", "logs": logs}), 500

    finally:
        # Очищаем временные файлы
        if 'input_path' in locals() and os.path.exists(input_path):
            try:
                os.remove(input_path)
            except:
                pass

        # Очищаем папку с результатом
        if 'output_folder' in locals() and os.path.exists(output_folder):
            try:
                shutil.rmtree(output_folder)
            except:
                pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)