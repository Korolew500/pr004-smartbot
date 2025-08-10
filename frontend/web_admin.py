"""Веб-интерфейс администратора с управлением синонимами"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from backend.admin_console import AdminConsole

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Глобальная ссылка на консоль администратора
admin_console = None

# Конфигурация аутентификации
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'secure_password'

def init_web_admin(console: AdminConsole):
    """Инициализация веб-интерфейса администратора"""
    global admin_console
    admin_console = console
    print("Веб-интерфейс администратора инициализирован")

@app.before_request
def check_auth():
    """Проверка аутентификации для защищенных маршрутов"""
    if request.endpoint not in ['login', 'static'] and not session.get('authenticated'):
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Страница входа"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['authenticated'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template('login.html', error="Неверные учетные данные")
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Выход из системы"""
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/')
def admin_dashboard():
    """Панель управления администратора"""
    return render_template('admin_dashboard.html')

@app.route('/synonyms')
def synonyms_management():
    """Страница управления синонимами"""
    if not admin_console:
        return "AdminConsole не инициализирован", 500
    
    synonyms_data = admin_console.get_synonyms()
    return render_template('synonyms.html', synonyms=synonyms_data)

@app.route('/add_synonym', methods=['POST'])
def add_synonym():
    """Добавление нового синонима"""
    if not admin_console:
        return jsonify({"error": "AdminConsole не инициализирован"}), 500
        
    base_word = request.form.get('base_word')
    synonym = request.form.get('synonym')
    
    if not base_word or not synonym:
        return jsonify({"error": "Базовое слово и синоним обязательны"}), 400
    
    try:
        result = admin_console.add_synonym(base_word, synonym)
        if result:
            return jsonify({"message": f"Добавлен синоним: {synonym} → {base_word}"})
        else:
            return jsonify({"error": "Ошибка при добавлении синонима"}), 500
    except Exception as e:
        return jsonify({"error": f"Системная ошибка: {str(e)}"}), 500

@app.route('/remove_synonym', methods=['POST'])
def remove_synonym():
    """Удаление синонима"""
    if not admin_console:
        return jsonify({"error": "AdminConsole не инициализирован"}), 500
        
    base_word = request.form.get('base_word')
    synonym = request.form.get('synonym')
    
    if not base_word or not synonym:
        return jsonify({"error": "Базовое слово и синоним обязательны"}), 400
    
    try:
        result = admin_console.remove_synonym(base_word, synonym)
        if result:
            return jsonify({"message": f"Удален синоним: {synonym} → {base_word}"})
        else:
            return jsonify({"error": "Ошибка при удалении синонима"}), 500
    except Exception as e:
        return jsonify({"error": f"Системная ошибка: {str(e)}"}), 500

@app.route('/search_synonyms')
def search_synonyms():
    """Поиск синонимов по запросу"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({"error": "Пустой запрос"}), 400
        
    try:
        results = admin_console.search_synonyms(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stats')
def stats():
    """Статистика использования"""
    stats_data = {
        "users": 42,
        "keywords": 15,
        "requests_today": 128,
        "uptime": 3600 * 24
    }
    return jsonify(stats_data)

if __name__ == '__main__':
    app.run(debug=True)