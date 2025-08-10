"""Веб-интерфейс администратора"""

from flask import Flask, render_template, request
from backend.admin_console import AdminConsole

app = Flask(__name__)

# TODO: Реализовать интеграцию с AdminConsole
@app.route('/')
def admin_dashboard():
    """Панель управления администратора"""
    return render_template('admin_dashboard.html')

@app.route('/add_keyword', methods=['POST'])
def add_keyword():
    """Добавление ключевого слова через веб-интерфейс"""
    keyword = request.form.get('keyword')
    response = request.form.get('response')
    # TODO: Реализовать вызов AdminConsole
    return f"Добавлено ключевое слово: {keyword} -> {response}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)