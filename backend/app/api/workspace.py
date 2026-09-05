from datetime import datetime
from markupsafe import escape
from flask import Blueprint, jsonify, request

from ..services.validator import get_json_payload, parse_number, next_id
from ..data.mock_db import (
    price_alerts,
    MOCK_COUPONS,
    inbox_emails,
    wallet,
    MOCK_GIFT_CARDS,
    GROCERY_ITEMS_PRICES
)

workspace_bp = Blueprint('workspace', __name__)


@workspace_bp.route('/api/coupons', methods=['POST'])
def get_coupons():
    try:
        data = get_json_payload()
        url = str(data.get('url', '')).lower()

        retailer = "amazon"
        if "flipkart" in url:
            retailer = "flipkart"
        elif "myntra" in url:
            retailer = "myntra"

        coupons = MOCK_COUPONS.get(retailer, MOCK_COUPONS["amazon"])
        return jsonify({"coupons": coupons, "retailer": retailer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@workspace_bp.route('/api/alerts', methods=['GET', 'POST', 'DELETE'])
def manage_alerts():
    global price_alerts
    try:
        if request.method == 'GET':
            return jsonify({"alerts": price_alerts})

        elif request.method == 'POST':
            data = get_json_payload()
            if not data or not data.get('url') or not data.get('email') or not data.get('target_price'):
                return jsonify({"error": "Missing required fields"}), 400

            target_price = parse_number(data.get('target_price'), "Target price", positive=True)
            current_price = parse_number(data.get('current_price', 0), "Current price", non_negative=True)

            alert = {
                "id": next_id(price_alerts),
                "title": str(data.get('title', 'Unknown Product'))[:300],
                "url": data.get('url'),
                "email": str(data.get('email'))[:254],
                "current_price": current_price,
                "target_price": target_price,
                "currency": data.get('currency', 'INR'),
                "date_created": datetime.utcnow().strftime("%Y-%m-%d"),
                "status": "Active"
            }
            price_alerts.append(alert)
            return jsonify({"message": "Alert created successfully", "alert": alert})

        elif request.method == 'DELETE':
            data = get_json_payload()
            alert_id = data.get('id')
            if not alert_id:
                return jsonify({"error": "Alert ID required"}), 400

            price_alerts[:] = [a for a in price_alerts if a["id"] != int(alert_id)]
            return jsonify({"message": "Alert deleted successfully"})

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@workspace_bp.route('/api/inbox', methods=['GET', 'POST'])
def manage_inbox():
    try:
        if request.method == 'GET':
            return jsonify({"inbox": inbox_emails})

        elif request.method == 'POST':
            data = get_json_payload()
            if not data or not data.get('title') or data.get('price') is None:
                return jsonify({"error": "Product title and price required"}), 400

            title = str(data.get('title'))[:300]
            price = parse_number(data.get('price'), "Price", positive=True)
            url = str(data.get('url', ''))
            currency = data.get('currency', 'INR')
            currency = currency if currency in {"INR", "USD", "EUR", "GBP"} else "INR"
            safe_title = escape(title)
            safe_currency = escape(currency)

            retailer = "Amazon"
            if "flipkart" in url.lower():
                retailer = "Flipkart"
            elif "myntra" in url.lower():
                retailer = "Myntra"

            order_id = f"ORDER-{datetime.utcnow().strftime('%M%S%f')[:9]}"
            cashback_amount = round(price * 0.05, 2)
            coins_earned = int(price * 0.02)

            email_body = f"""
                <div style="font-family: sans-serif; max-width: 600px; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff; color: #1e293b;">
                    <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f1f5f9; padding-bottom: 15px; margin-bottom: 20px;">
                        <h2 style="color: #2563eb; margin: 0; font-size: 20px;">{retailer}</h2>
                        <span style="font-size: 12px; color: #64748b; font-weight: bold; background: #f1f5f9; padding: 4px 8px; border-radius: 999px;">{order_id}</span>
                    </div>
                    <p>Hello Shopper,</p>
                    <p>Your Pricevana assistant successfully captured and verified your order! Congratulations on earning cashbacks and coins.</p>
                    <div style="background: #eff6ff; border: 1px solid #bfdbfe; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <strong style="display: block; margin-bottom: 8px; color: #1e40af;">🎉 Cashback Verified!</strong>
                        <p style="margin: 0; font-size: 14px; color: #1e3a8a;">
                            A cash value of <strong>{safe_currency} {cashback_amount}</strong> (5% cashback) has been instantly credited to your Pricevana Wallet!
                        </p>
                    </div>
                    <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <strong style="display: block; margin-bottom: 8px; color: #0f172a;">Order Summary:</strong>
                        <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                            <tr style="border-bottom: 1px solid #e2e8f0;">
                                <td style="padding: 8px 0;">{safe_title}</td>
                                <td style="text-align: right; padding: 8px 0;">{safe_currency} {price}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px 0; font-weight: bold;">Grand Total:</td>
                                <td style="text-align: right; padding: 8px 0; font-weight: bold; color: #2563eb;">{safe_currency} {price}</td>
                            </tr>
                        </table>
                    </div>
                    <p style="font-size: 14px; color: #64748b;">Thanks for shopping smarter with Pricevana!<br>Smart Delivery Team</p>
                </div>
            """

            new_email = {
                "id": next_id(inbox_emails),
                "sender": f"{retailer} Smart Tracker",
                "sender_email": f"tracker@{retailer.lower()}.com",
                "subject": f"Verified Order & Cashback Alert! {order_id} 💰",
                "date": "Just now",
                "body": email_body,
                "status": "In Transit",
                "retailer": retailer,
                "amount": price,
                "cashback": cashback_amount,
                "read": False
            }

            inbox_emails.insert(0, new_email)

            wallet["balance"] = round(wallet["balance"] + cashback_amount, 2)
            wallet["coins"] += coins_earned
            wallet["transactions"].insert(0, {
                "id": next_id(wallet["transactions"]),
                "type": "Cashback",
                "amount": cashback_amount,
                "details": f"{retailer} Order {order_id}",
                "date": "Today",
                "status": "Credited"
            })

            return jsonify({
                "message": "Order captured & simulated email delivered successfully!",
                "order_id": order_id,
                "cashback": cashback_amount,
                "coins": coins_earned,
                "email": new_email
            })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@workspace_bp.route('/api/wallet', methods=['GET', 'POST'])
def manage_wallet():
    try:
        if request.method == 'GET':
            return jsonify(wallet)

        elif request.method == 'POST':
            # UPI withdrawal simulation
            data = get_json_payload()
            if not data or data.get('amount') is None or not data.get('upi'):
                return jsonify({"error": "Amount and UPI ID required"}), 400

            amount = parse_number(data.get('amount'), "Amount", positive=True)
            upi = str(data.get('upi'))[:100]

            if amount > wallet["balance"]:
                return jsonify({"error": "Insufficient balance"}), 400

            wallet["balance"] = round(wallet["balance"] - amount, 2)
            wallet["transactions"].insert(0, {
                "id": next_id(wallet["transactions"]),
                "type": "Withdrawal",
                "amount": -amount,
                "details": f"UPI payout to {upi}",
                "date": "Today",
                "status": "Completed"
            })

            return jsonify({
                "message": "Withdrawal processed successfully via UPI!",
                "new_balance": wallet["balance"],
                "amount_withdrawn": amount
            })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@workspace_bp.route('/api/giftcards', methods=['GET'])
def get_giftcards():
    return jsonify(MOCK_GIFT_CARDS)


@workspace_bp.route('/api/giftcards/buy', methods=['POST'])
def buy_giftcard():
    try:
        data = get_json_payload()
        if not data or not data.get('brand') or data.get('value') is None:
            return jsonify({"error": "Brand and card value required"}), 400

        brand_id = data.get('brand')
        value = parse_number(data.get('value'), "Card value", positive=True)

        card = MOCK_GIFT_CARDS.get(brand_id)
        if not card:
            return jsonify({"error": "Invalid Brand selected"}), 400

        cashback_rate = card["cashback_rate"]
        cashback_earned = round(value * (cashback_rate / 100), 2)

        voucher_code = f"PV-{brand_id.upper()}-{datetime.utcnow().strftime('%f%H%M')[:10]}"
        provider = card["provider"]

        payment_source = "External Gateway (Card/UPI)"
        if wallet["balance"] >= value:
            wallet["balance"] = round(wallet["balance"] - value, 2)
            payment_source = "Cashback Wallet Balance"
            wallet["transactions"].insert(0, {
                "id": next_id(wallet["transactions"]),
                "type": "Voucher Purchase",
                "amount": -value,
                "details": f"Bought {card['name']} Voucher",
                "date": "Today",
                "status": "Completed"
            })

        wallet["balance"] = round(wallet["balance"] + cashback_earned, 2)
        wallet["coins"] += int(value * 0.05)

        wallet["transactions"].insert(0, {
            "id": next_id(wallet["transactions"]),
            "type": "Voucher Cashback",
            "amount": cashback_earned,
            "details": f"{cashback_rate}% Flat Reward for {card['name']}",
            "date": "Today",
            "status": "Credited"
        })

        email_body = f"""
            <div style="font-family: sans-serif; max-width: 600px; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff; color: #1e293b;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #f8fafc; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="color: #6366f1; margin: 0; font-size: 20px;">Pricevana Voucher Hub</h2>
                    <span style="font-size: 12px; color: #64748b; font-weight: bold; background: #f1f5f9; padding: 4px 8px; border-radius: 999px;">CODE INSTANTLY ACTIVE</span>
                </div>
                <p>Hello Shopper,</p>
                <p>Here is your digital gift card voucher code for <strong>{card['name']}</strong>, issued directly through {provider}.</p>
                <div style="background: #fdf4ff; border: 2px dashed #d946ef; padding: 18px; border-radius: 8px; text-align: center; margin: 20px 0;">
                    <span style="font-size: 13px; color: #86198f; font-weight: bold; text-transform: uppercase;">Your Voucher Claim Code:</span>
                    <h1 style="color: #701a75; font-size: 26px; letter-spacing: 2px; margin: 8px 0;">{voucher_code}</h1>
                    <p style="margin: 0; font-size: 13px; color: #a21caf;">Value: ₹{value} | Paid via {payment_source}</p>
                </div>
                <div style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 12px 16px; border-radius: 8px; margin-bottom: 15px;">
                    <span style="font-size: 14px; color: #15803d; font-weight: bold;">
                        🎁 Cashback Earned: ₹{cashback_earned} credited to your Pricevana Wallet!
                    </span>
                </div>
                <p style="font-size: 13px; color: #64748b;">Paste this code during checkout at {card['name']}.<br>Thank you for choosing Pricevana Rewards.</p>
            </div>
        """

        new_email = {
            "id": next_id(inbox_emails),
            "sender": "Pricevana Voucher Hub",
            "sender_email": "vouchers@pricevana.co",
            "subject": f"Voucher Delivered! ₹{value} {card['name']} Code Inside 🎁",
            "date": "Just now",
            "body": email_body,
            "status": "Delivered",
            "retailer": provider,
            "amount": value,
            "cashback": cashback_earned,
            "read": False
        }

        inbox_emails.insert(0, new_email)

        return jsonify({
            "success": True,
            "message": "Gift card purchased successfully!",
            "cashback_earned": cashback_earned,
            "voucher_code": voucher_code,
            "voucher": voucher_code,
            "new_balance": wallet["balance"],
            "email": new_email
        })

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@workspace_bp.route('/api/spend-lens', methods=['GET'])
def get_spend_lens():
    try:
        retailer_breakdown = [
            {"store": "Amazon", "amount": 44990, "color": "#ff9900", "percentage": 67},
            {"store": "Flipkart", "amount": 19999, "color": "#2563eb", "percentage": 30},
            {"store": "Myntra", "amount": 1899, "color": "#ff3f6c", "percentage": 3}
        ]

        calculated_spent = sum(item["amount"] for item in inbox_emails if item.get("status") != "Delivered") + 66888

        data = {
            "total_spent": calculated_spent,
            "total_cashback_earned": wallet["balance"],
            "efficiency_rate": round((wallet["balance"] / calculated_spent) * 100, 2) if calculated_spent > 0 else 5.0,
            "missed_savings": 4820,
            "retailer_breakdown": retailer_breakdown,
            "monthly_savings_trend": [1200, 1500, 900, 1820, 2400, 1900]
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@workspace_bp.route('/api/basket/compare', methods=['POST'])
def compare_grocery_basket():
    try:
        data = get_json_payload()
        selected_items = data.get('items', [])

        if not selected_items:
            return jsonify({"bigbasket": 0, "blinkit": 0, "zepto": 0, "cheapest": "bigbasket", "breakdown": {}})

        bb_total = 0
        bl_total = 0
        zp_total = 0
        breakdown = {}

        for raw_item in selected_items:
            if isinstance(raw_item, dict):
                item_key = raw_item.get("key") or raw_item.get("id") or raw_item.get("name")
            else:
                item_key = str(raw_item) if raw_item is not None else None

            if not item_key:
                continue

            item = GROCERY_ITEMS_PRICES.get(item_key)
            if item:
                bb_total += item["bigbasket"]
                bl_total += item["blinkit"]
                zp_total += item["zepto"]
                breakdown[item_key] = {
                    "name": item["name"],
                    "bigbasket": item["bigbasket"],
                    "blinkit": item["blinkit"],
                    "zepto": item["zepto"]
                }

        totals = {"bigbasket": bb_total, "blinkit": bl_total, "zepto": zp_total}
        cheapest_store = min(totals, key=totals.get)

        return jsonify({
            "bigbasket": bb_total,
            "blinkit": bl_total,
            "zepto": zp_total,
            "cheapest": cheapest_store,
            "breakdown": breakdown
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
