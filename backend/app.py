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
    output_folder = None

    try:
        # Сохраняем загруженный файл
        input_path = tempfile.mktemp(suffix=".pdf")
        logs.append(f"5. Temp path: {input_path}")

        # Сохраняем файл напрямую используя file.save()
        # Это правильный способ сохранения FileStorage объекта
        file.save(input_path)
        
        # Проверяем размер сохранённого файла
        saved_size = os.path.getsize(input_path)
        logs.append(f"6. File saved successfully")
        logs.append(f"7. Saved file size: {saved_size} bytes ({saved_size / 1024 / 1024:.2f} MB)")
        
        if saved_size == 0:
            raise Exception("Файл пустой после сохранения")
        
        if saved_size < 100:
            raise Exception(f"Файл слишком маленький: {saved_size} bytes - возможно, произошла ошибка при загрузке")

        logs.append(f"8. Initializing iLovePDF...")
        
        # Инициализируем iLovePDF
        ilovepdf = ILovePdf(ILOVEPDF_PUBLIC_KEY, verify_ssl=True)

        logs.append(f"9. Creating compress task...")
        
        # Создаём задачу сжатия
        task = ilovepdf.new_task('compress')
        task.add_file(input_path)

        logs.append(f"10. File added to task")

        # Создаём временную папку для результата
        output_folder = tempfile.mkdtemp()
        task.set_output_folder(output_folder)

        logs.append(f"11. Output folder: {output_folder}")
        logs.append(f"12. Executing compression...")

        # Выполняем сжатие
        task.execute()

        logs.append(f"13. Compression executed, downloading result...")

        # Скачиваем результат
        task.download()

        logs.append(f"14. Download complete, checking output folder...")

        # Находим скачанный файл в папке
        output_files = os.listdir(output_folder)
        logs.append(f"15. Files in output folder: {output_files}")
        
        if not output_files:
            raise Exception("Файл не был скачан - папка пустая")
            
        output_path = os.path.join(output_folder, output_files[0])
        
        # Проверяем, что файл существует и не пустой
        if not os.path.exists(output_path):
            raise Exception(f"Файл не найден: {output_path}")
            
        output_size = os.path.getsize(output_path)
        if output_size == 0:
            raise Exception("Сжатый файл пустой")
            
        logs.append(f"16. Output file: {output_path}, size: {output_size} bytes")

        # Получаем информацию о размерах
        original_size = os.path.getsize(input_path)
        compressed_size = output_size
        reduction = round((1 - compressed_size / original_size) * 100, 1)

        logs.append(f"17. Compression stats: {original_size} -> {compressed_size} bytes ({reduction}% reduction)")

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

        logs.append(f"18. Sending response...")

        return response

    except Exception as e:
        import traceback
        logs.append(f"ERROR: {str(e)}")
        logs.append(f"TRACEBACK: {traceback.format_exc()}")
        return jsonify({"error": f"Ошибка сжатия: {str(e)}", "logs": logs}), 500

    finally:
        # Очищаем временные файлы
        if input_path and os.path.exists(input_path):
            try:
                os.remove(input_path)
                logs.append(f"CLEANUP: Removed input file {input_path}")
            except Exception as e:
                logs.append(f"CLEANUP WARNING: Could not remove input file: {e}")

        # Очищаем папку с результатом
        if output_folder and os.path.exists(output_folder):
            try:
                shutil.rmtree(output_folder)
                logs.append(f"CLEANUP: Removed output folder {output_folder}")
            except Exception as e:
                logs.append(f"CLEANUP WARNING: Could not remove output folder: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)