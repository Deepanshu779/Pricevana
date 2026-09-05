import os
import hashlib
import requests
import numpy as np
from flask import Blueprint, jsonify
from openai import OpenAI

from ..config import logger, OPENAI_API_KEY
from ..services.validator import get_json_payload, validate_external_url, parse_number
from ..services.ml_engine import predict_lowest_price, generate_rule_based_advice
from ..services.scraper import scrape_product_info
from ..data.mock_db import get_catalog_product, SEARCH_PRODUCTS

predictor_bp = Blueprint('predictor', __name__)


@predictor_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = get_json_payload()
        url = data.get("url")

        if not url:
            return jsonify({
                "error": "Product URL required"
            }), 400

        try:
            url = validate_external_url(url)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        # Check demo catalog first to avoid Selenium dependency for catalog URLs
        product = get_catalog_product(url)
        error = None
        if not product:
            product, error = scrape_product_info(url)

        if error:
            return jsonify({
                "error": error
            }), 422

        current_price = product["price"]
        predicted_price, advice, history, future = predict_lowest_price(current_price)

        return jsonify({
            "product_title": product["title"],
            "currentPrice": current_price,
            "predictedLowest": round(predicted_price, 2),
            "currency": "INR",
            "advice": advice,
            "history": history,
            "future_predictions": future,
            "price_source": product["price_source"],
            "url": url,
            "image_url": product.get("image_url")
        })

    except Exception as e:
        logger.error(f"Prediction endpoint exception: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500


@predictor_bp.route('/compare', methods=['POST'])
def compare():
    try:
        data = get_json_payload()
        title = data.get('title') or data.get('product') or data.get('name')
        current_url = str(data.get('url', ''))

        if not title:
            return jsonify({"error": "Title required"}), 400
        title = str(title)[:300]

        platforms = [
            {"name": "Amazon", "search_url": "https://www.amazon.in/s?k=", "price_sel": ".a-price-whole"},
            {"name": "Flipkart", "search_url": "https://www.flipkart.com/search?q=", "price_sel": "._30jeq3"},
            {"name": "Myntra", "search_url": "https://www.myntra.com/", "price_sel": ".product-discountedPrice"}
        ]

        seed = int(hashlib.md5(title.encode()).hexdigest(), 16)
        rng = np.random.default_rng(seed % 1000)
        try:
            current_price = parse_number(data.get('current_price', 1000), "Current price", positive=True)
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

        results = []
        for p in platforms:
            if p["name"].lower() in current_url.lower():
                results.append({
                    "platform": p["name"],
                    "price": current_price,
                    "url": current_url,
                    "available": True
                })
                continue

            price_variation = rng.uniform(0.90, 1.05)
            results.append({
                "platform": p["name"],
                "price": round(current_price * price_variation),
                "url": p["search_url"] + requests.utils.quote(title),
                "available": True
            })

        return jsonify({
            "comparisons": results,
            "platforms": results
        })

    except Exception as e:
        logger.error(f"Comparison endpoint exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@predictor_bp.route('/ai-advice', methods=['POST'])
def ai_advice():
    try:
        data = get_json_payload()
        product = data.get('product')
        price = data.get('price')
        predicted = data.get('predicted')

        if not product or price is None or predicted is None:
            return jsonify({"error": "Product, price and predicted price required"}), 400

        # Try calling OpenAI first if API key is configured
        api_key = OPENAI_API_KEY
        if api_key and not api_key.startswith("your_") and len(api_key) > 20:
            try:
                prompt = f"Product: {product}\nCurrent Price: ₹{price}\nPredicted Price: ₹{predicted}\n\nGive short buying advice (2 lines)."
                client = OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    timeout=5
                )
                return jsonify({
                    "advice": response.choices[0].message.content.strip()
                })
            except Exception as openai_err:
                logger.warning(f"OpenAI API failed: {openai_err}. Falling back to rule-based advice.")

        advice_data = generate_rule_based_advice(product, price, predicted)
        diff = price - predicted
        if diff > 0:
            pct = round((diff / price) * 100, 1)
            advice_text = (
                f"🎯 Strategic Buyer Tip: We predict a price drop of {pct}% (save ~₹{int(diff)}) over the coming week. "
                f"Setting a Pricevana Alert is highly recommended to catch the lowest rate."
            )
        else:
            advice_text = (
                f"🔥 Active Deal Alert: The current rate of ₹{price} is at its seasonal baseline. "
                f"Our predictive models project a potential upward adjustment soon. This is a recommended buy."
            )

        return jsonify({
            "advice": advice_text,
            "details": advice_data
        })

    except Exception as e:
        logger.error(f"AI advice endpoint exception: {str(e)}")
        return jsonify({"error": str(e)}), 500


@predictor_bp.route('/api/similar', methods=['POST'])
def get_similar_products():
    try:
        data = get_json_payload()
        title = data.get('title', '').lower()

        is_audio = "sony" in title or "headphones" in title or "audio" in title or "wh-1000" in title or "xm4" in title
        is_phone = "iphone" in title or "s24" in title or "galaxy" in title or "oneplus" in title or "smartphone" in title
        is_laptop = "macbook" in title or "laptop" in title or "ideapad" in title or "pavilion" in title
        is_clothing = "shorts" in title or "pajama" in title or "night" in title or "loungewear" in title or "socks" in title or "sneakers" in title

        if is_audio:
            alternatives = [
                {"title": "Bose QuietComfort 45 Bluetooth Headphones", "store": "Amazon", "price": 22999, "original_price": 29900, "discount": "23% OFF", "rating": 4.7, "url": "https://www.amazon.in/s?k=bose+quietcomfort+45"},
                {"title": "JBL Live 660NC Wireless Headphones", "store": "Flipkart", "price": 9999, "original_price": 14999, "discount": "33% OFF", "rating": 4.3, "url": "https://www.flipkart.com/search?q=jbl+live+660nc"},
                {"title": "Sony WH-CH720N Noise Cancelling Headphones", "store": "Amazon", "price": 7990, "original_price": 14990, "discount": "46% OFF", "rating": 4.2, "url": "https://www.amazon.in/s?k=sony+wh-ch720n"}
            ]
        elif is_phone:
            alternatives = [
                {"title": "Apple iPhone 14 (128GB, Midnight Blue)", "store": "Amazon", "price": 58999, "original_price": 69900, "discount": "15% OFF", "rating": 4.6, "url": "https://www.amazon.in/s?k=iphone+14"},
                {"title": "Samsung Galaxy S23 FE 5G (8GB, 128GB)", "store": "Flipkart", "price": 49999, "original_price": 79999, "discount": "37% OFF", "rating": 4.3, "url": "https://www.flipkart.com/search?q=samsung+s23+fe"},
                {"title": "OnePlus 12 (5G, 12GB RAM, 256GB)", "store": "Amazon", "price": 64999, "original_price": 69999, "discount": "7% OFF", "rating": 4.5, "url": "https://www.amazon.in/s?k=oneplus+12"}
            ]
        elif is_laptop:
            alternatives = [
                {"title": "Apple MacBook Air M1 (8GB, 256GB SSD)", "store": "Amazon", "price": 68990, "original_price": 99900, "discount": "31% OFF", "rating": 4.7, "url": "https://www.amazon.in/s?k=macbook+air+m1"},
                {"title": "ASUS Vivobook 15 (Intel Core i5, 16GB)", "store": "Flipkart", "price": 49990, "original_price": 69990, "discount": "28% OFF", "rating": 4.2, "url": "https://www.flipkart.com/search?q=asus+vivobook+15"},
                {"title": "HP 15s (12th Gen Intel Core i5, 16GB)", "store": "Amazon", "price": 52990, "original_price": 68990, "discount": "23% OFF", "rating": 4.3, "url": "https://www.amazon.in/s?k=hp+15s+core+i5"}
            ]
        elif is_clothing:
            alternatives = [
                {"title": "SMOWKLY Women Korean Shorts Pajama Set", "store": "Amazon", "price": 498, "original_price": 999, "discount": "50% OFF", "rating": 3.8, "url": "https://www.amazon.in/s?k=smowkly+shorts+pajama+set"},
                {"title": "Women Korean Striped Shorts Pajama Set", "store": "Amazon", "price": 498, "original_price": 999, "discount": "50% OFF", "rating": 3.9, "url": "https://www.amazon.in/s?k=striped+shorts+pajama+set"},
                {"title": "Puma Unisex Solid Classic Retro Sneakers", "store": "Myntra", "price": 2499, "original_price": 4999, "discount": "50% OFF", "rating": 4.2, "url": "https://www.myntra.com/sneakers"}
            ]
        else:
            alternatives = SEARCH_PRODUCTS[:3]

        return jsonify({"results": alternatives})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
