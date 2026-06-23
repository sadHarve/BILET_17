from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Файл для хранения кафе
DATA_FILE = 'cafes.json'

# Создаем файл если его нет
def init_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

# Загружаем список кафе
def load_cafes():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# Сохраняем список кафе
def save_cafes(cafes):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(cafes, f, ensure_ascii=False, indent=2)

# ГЛАВНАЯ СТРАНИЦА - показывает все кафе
@app.route('/')
def index():
    cafes = load_cafes()
    return render_template('index.html', cafes=cafes)

# СТРАНИЦА ДОБАВЛЕНИЯ
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('name')
        cuisine = request.form.get('cuisine')
        rating = float(request.form.get('rating'))
        avg_check = float(request.form.get('avg_check'))
        
        # Сохраняем новое кафе
        cafes = load_cafes()
        cafes.append({
            'name': name,
            'cuisine': cuisine,
            'rating': rating,
            'avg_check': avg_check
        })
        save_cafes(cafes)
        
        # Возвращаемся на главную
        return redirect(url_for('index'))
    
    return render_template('add.html')

# УДАЛЕНИЕ КАФЕ по его номеру (индексу)
@app.route('/delete/<int:index>')
def delete(index):
    cafes = load_cafes()
    if 0 <= index < len(cafes):
        del cafes[index]
        save_cafes(cafes)
    return redirect(url_for('index'))

# ЗАПУСК ПРИЛОЖЕНИЯ
if __name__ == '__main__':
    init_data()
    app.run(debug=True, host='0.0.0.0', port=5000)