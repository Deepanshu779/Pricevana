from flask import Blueprint, jsonify, request
from ..services.validator import get_json_payload
from ..data.mock_db import SEARCH_PRODUCTS, MOCK_BUDGET_DEALS, MOCK_CATEGORY_DEALS

deals_bp = Blueprint('deals', __name__)


@deals_bp.route('/api/search', methods=['POST'])
def search_deals():
    try:
        data = get_json_payload()
        query = data.get('query', '').lower().strip()

        if not query:
            return jsonify({"results": SEARCH_PRODUCTS[:6]})

        matches = []
        for p in SEARCH_PRODUCTS:
            if query in p["title"].lower() or query in p["store"].lower():
                matches.append(p)

        return jsonify({"results": matches})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@deals_bp.route('/api/deals', methods=['GET'])
def get_deals():
    try:
        tier = request.args.get('tier')
        category = request.args.get('category')

        if tier:
            deals = MOCK_BUDGET_DEALS.get(tier, [])
            return jsonify({"deals": deals})
        elif category:
            deals = MOCK_CATEGORY_DEALS.get(category, [])
            return jsonify({"deals": deals})

        all_deals = []
        for deals_list in MOCK_BUDGET_DEALS.values():
            all_deals.extend(deals_list)
        return jsonify({"deals": all_deals})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
