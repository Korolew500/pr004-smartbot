...
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
            return jsonify({"error": "Синоним не найден или ошибка удаления"}), 400
    except Exception as e:
        return jsonify({"error": f"Системная ошибка: {str(e)}"}), 500

...