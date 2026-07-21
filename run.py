# run.py
from app import create_app
app = create_app()

if __name__ == "__main__":
    # print('Root Path:', app.root_path)
    # print('Template folder:', app.template_folder)
    
    host = "192.168.43.226"
    
    
    app.run(host=host or "127.0.0.1", port=8080, debug=True)