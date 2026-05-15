# Simple runner - works with your current app.py
import app

if __name__ == '__main__':
    print("Starting Crop AI System...")
    print("Open http://localhost:5000")
    app.app.run(debug=True, host='0.0.0.0', port=5000)