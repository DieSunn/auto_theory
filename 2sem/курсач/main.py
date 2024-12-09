from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_data():
    try:
        # Получаем данные из POST-запроса
        data = request.get_json()
        
        # Проверяем, что пришёл словарь
        if not isinstance(data, dict):
            return jsonify({'error': 'Данные должны быть словарём {id: слово}'}), 400
        
        # Пример обработки: собираем строки вида "id: слово"
        processed_data = [f"{key}: {value}" for key, value in data.items()]
        
        return jsonify({
            'message': 'Данные успешно обработаны',
            'processed_data': processed_data
        }), 200
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(debug=True)
