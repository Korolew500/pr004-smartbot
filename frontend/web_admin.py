...

@app.route('/search_synonyms')
def search_synonyms():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Пустой запрос"}), 400
        
    try:
        results = admin_console.search_synonyms(query)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

...