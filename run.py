# run.py
from app import create_app
app = create_app()

if __name__ == "__main__":
    host = False"192.168.43.226"
    app.run(host="0.0.0.0", port=8080, debug=True)