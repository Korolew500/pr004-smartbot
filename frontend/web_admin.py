"""Веб-интерфейс администратора с управлением синонимами"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from backend.admin_console import AdminConsole
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'

admin_console = None

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'secure_password'

def init_web_admin(console: AdminConsole):
    global admin_console
    admin_console = console
    print("Веб-интерфейс администратора инициализирован")

@app.before_request
def check_auth():
    if request.endpoint not in ['login', 'static'] and not session.get('authenticated'):
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
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
    session.pop('authenticated', None)
    return redirect(url_for('login'))

@app.route('/')
def admin_dashboard():
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

@app.route('/stats')
def stats():
    stats_data = {
        "users": 42,
        "keywords": 15,
        "requests_today": 128,
        "uptime": time.time() - 1680000000
    }
    return jsonify(stats_data)

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    # ... существующий код ...

@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error_code=500), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)