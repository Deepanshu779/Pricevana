"""
Pricevana Application Runner & Main Entrypoint
"""
import os
import sys

# Ensure current directory is in python search path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.config import PORT, HOST, FLASK_DEBUG

app = create_app()

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=FLASK_DEBUG)
