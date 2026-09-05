import os
import logging
from dotenv import load_dotenv

load_dotenv()

SUPPORTED_PRODUCT_DOMAINS = ("amazon.in", "flipkart.com", "myntra.com")

PORT = int(os.getenv("PORT", 5000))
DEFAULT_HOST = "0.0.0.0" if os.getenv("PORT") or os.getenv("RENDER") else "127.0.0.1"
HOST = os.getenv("HOST", DEFAULT_HOST)
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "0") in ("1", "true", "True")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pricevana")
