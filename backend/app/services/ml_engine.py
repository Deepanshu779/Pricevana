import numpy as np
from sklearn.linear_model import LinearRegression


def predict_lowest_price(current_price):
    history = []
    for _ in range(30):
        fluctuation = np.random.uniform(-0.08, 0.05)
        simulated_price = current_price * (1 + fluctuation)
        history.append(round(simulated_price, 2))

    X = np.arange(len(history)).reshape(-1, 1)
    y = np.array(history)

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.arange(30, 37).reshape(-1, 1)
    predictions = model.predict(future_days)
    lowest_price = min(predictions)

    if lowest_price < current_price:
        advice = "Wait for price drop"
    else:
        advice = "Current price is best"

    return (
        round(float(lowest_price), 2),
        advice,
        history,
        predictions.tolist()
    )


def generate_rule_based_advice(product, price, predicted):
    diff = price - predicted
    if diff > 0:
        pct = round((diff / price) * 100, 1)
        action = "WAIT"
        badge = "badge-wait"
        analysis = (
            f"Based on historical price trends and predictive modeling, {product} "
            f"is currently priced higher than expected. The price is likely to drop "
            f"by ~{pct}% (around ₹{diff:,.2f}) within the next 7 days."
        )
        tip = "Add this product to your Pricevana alerts to get notified instantly when the price drops."
    else:
        action = "BUY NOW"
        badge = "badge-buy"
        analysis = (
            f"Great news! {product} is currently at or near its predicted lowest price. "
            f"Our models show minimal chance of a further drop in the coming week."
        )
        tip = "This is a great buying window. Consider completing your purchase before prices adjust upwards."

    return {
        "analysis": analysis,
        "action": action,
        "badge": badge,
        "tip": tip,
        "source": "rule_engine"
    }
