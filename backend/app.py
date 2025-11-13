from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pylovepdf.ilovepdf import ILovePdf
import tempfile
import os

app = Flask(__name__)
CORS(app)  # Разрешаем CORS для фронтенда

# ⚠️ ВАЖНО: Получите ключи на https://developer.ilovepdf.com/
# Бесплатный план: 250 запросов/месяц
ILOVEPDF_PUBLIC_KEY = os.environ.get('ILOVEPDF_PUBLIC_KEY', '')
ILOVEPDF_SECRET_KEY = os.environ.get('ILOVEPDF_SECRET_KEY', '')

@app.route('/health')
def health():
    return "OK"

@app.route('/compress', methods=['POST'])
def compress():
    if not ILOVEPDF_PUBLIC_KEY or not ILOVEPDF_SECRET_KEY:
        return jsonify({"error": "API ключи iLovePDF не настроены"}), 500

    file = request.files.get('file')
    if not file:
        return jsonify({"error": "Файл не найден"}), 400

    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Только PDF файлы"}), 400

    input_path = None
    output_path = None

    try:
        # Сохраняем загруженный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
            f.write(file.read())
            input_path = f.name

        # Инициализируем iLovePDF
        ilovepdf = ILovePdf(ILOVEPDF_PUBLIC_KEY, verify_ssl=True)

        # Создаём задачу сжатия
        task = ilovepdf.new_task('compress')
        task.add_file(input_path)

        # Уровень сжатия: 'low', 'recommended', 'extreme'
        compression_level = request.form.get('level', 'recommended')
        task.set_output_folder(tempfile.gettempdir())
        task.execute(compression_level=compression_level)

        # Скачиваем результат
        task.download()
        output_path = task.output_file

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
        return jsonify({"error": f"Ошибка сжатия: {str(e)}"}), 500

    finally:
        # Очищаем временные файлы
        for path in [input_path, output_path]:
            if path and os.path.exists(path):
                try:
                    os.remove(path)
                except:
                    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)