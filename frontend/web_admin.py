"""Веб-интерфейс администратора с аутентификацией и статистикой"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from backend.admin_console import AdminConsole
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Секретный ключ для сессий

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

@app.route('/stats')
def stats():
    """Статистика использования"""
    # Заглушка для статистики (реальная реализация потребует сбора данных)
    stats_data = {
        "users": 42,
        "keywords": 15,
        "requests_today": 128,
        "uptime": time.time() - 1680000000
    }
    return jsonify(stats_data)

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    """Добавление ключевого слова через веб-интерфейс"""
    global admin_console
    if not admin_console:
        return jsonify({"error": "AdminConsole не инициализирован"}), 500
    
    keyword = request.form.get('keyword')
    response = request.form.get('response')
    
    if not keyword or not response:
        return jsonify({"error": "Ключевое слово и ответ обязательны"}), 400
    
    try:
        result = admin_console.add_keyword(keyword, response)
        if result:
            return jsonify({"message": f"Добавлено: {keyword} → {response}"})
        else:
            return jsonify({"error": "Ошибка при добавлении ключевого слова"}), 500
    except Exception as e:
        return jsonify({"error": f"Системная ошибка: {str(e)}"}), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)