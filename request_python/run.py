from app.route import app

if __name__ == '__main__':
    app.run(host='0.0.0.0', use_reloader=False, threaded=True, debug=False, port=8080)
