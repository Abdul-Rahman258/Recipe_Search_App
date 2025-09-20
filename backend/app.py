from flask import Flask
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routes (this registers the endpoints)
from routes import app

if __name__ == '__main__':
    app.run(debug=True, port=5000)