import unittest
import sys
import os

# Ensure backend directory is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app import app


class PricevanaApiTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_index_route(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("service"), "Pricevana REST API")
        self.assertEqual(data.get("status"), "running")

    def test_health_route(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data.get("status"), "healthy")
        self.assertIn("timestamp", data)

    def test_predict_requires_url(self):
        response = self.client.post("/predict", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_predict_rejects_unsupported_domain(self):
        response = self.client.post("/predict", json={"url": "https://malicious-site.com/item"})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("error", data)

    def test_predict_success_catalog(self):
        response = self.client.post(
            "/predict",
            json={"url": "https://www.amazon.in/Sony-WH-1000XM4-Bluetooth-Cancellation-Resistance/dp/B0863TXGM3"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("currentPrice", data)
        self.assertIn("predictedLowest", data)
        self.assertIn("advice", data)
        self.assertIn("history", data)
        self.assertIn("future_predictions", data)

    def test_compare_endpoint_with_title(self):
        response = self.client.post(
            "/compare",
            json={"title": "Sony WH-1000XM4 Noise Cancelling Headphones", "current_price": 22990}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("platforms", data)
        self.assertGreater(len(data["platforms"]), 0)

    def test_compare_endpoint_with_product_alias(self):
        response = self.client.post(
            "/compare",
            json={"product": "Apple MacBook Air M1", "current_price": 75000}
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("platforms", data)

    def test_compare_endpoint_missing_title(self):
        response = self.client.post("/compare", json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn("Title required", data["error"])

    def test_search_endpoint(self):
        response = self.client.post("/api/search", json={"query": "laptop"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)

    def test_deals_endpoint_with_tier(self):
        response = self.client.get("/api/deals?tier=99")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("deals", data)
        self.assertGreater(len(data["deals"]), 0)

    def test_deals_endpoint_with_category(self):
        response = self.client.get("/api/deals?category=smartphones")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("deals", data)
        self.assertGreater(len(data["deals"]), 0)

    def test_deals_endpoint_default_without_params(self):
        response = self.client.get("/api/deals")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("deals", data)
        self.assertGreater(len(data["deals"]), 0)

    def test_giftcards_get_and_buy(self):
        response = self.client.get("/api/giftcards")
        self.assertEqual(response.status_code, 200)
        cards = response.get_json()
        self.assertIn("amazon", cards)

        buy_resp = self.client.post(
            "/api/giftcards/buy",
            json={"brand": "amazon", "value": 500}
        )
        self.assertEqual(buy_resp.status_code, 200)
        data = buy_resp.get_json()
        self.assertTrue(data.get("success"))
        self.assertIn("voucher", data)

    def test_alerts_routes(self):
        get_resp = self.client.get("/api/alerts")
        self.assertEqual(get_resp.status_code, 200)
        alerts_data = get_resp.get_json()
        self.assertIn("alerts", alerts_data)

        add_resp = self.client.post(
            "/api/alerts",
            json={
                "title": "Test Alert Product",
                "url": "https://www.amazon.in/dp/test",
                "email": "test@example.com",
                "target_price": 500,
                "current_price": 800
            }
        )
        self.assertEqual(add_resp.status_code, 200)
        created = add_resp.get_json().get("alert")
        self.assertIsNotNone(created)

        del_resp = self.client.delete("/api/alerts", json={"id": created["id"]})
        self.assertEqual(del_resp.status_code, 200)

    def test_coupons_routes(self):
        resp = self.client.post(
            "/api/coupons",
            json={"url": "https://www.amazon.in/dp/test"}
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.get_json()
        self.assertIn("coupons", data)
        self.assertEqual(data.get("retailer"), "amazon")

    def test_wallet_routes(self):
        get_resp = self.client.get("/api/wallet")
        self.assertEqual(get_resp.status_code, 200)
        wallet = get_resp.get_json()
        self.assertIn("balance", wallet)

        # Test withdraw with missing upi
        bad_resp = self.client.post("/api/wallet", json={"amount": 100})
        self.assertEqual(bad_resp.status_code, 400)

        # Test successful withdraw
        ok_resp = self.client.post("/api/wallet", json={"amount": 10, "upi": "test@upi"})
        self.assertEqual(ok_resp.status_code, 200)

    def test_inbox_route(self):
        response = self.client.get("/api/inbox")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("inbox", data)

    def test_spend_lens_route(self):
        response = self.client.get("/api/spend-lens")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("total_spent", data)
        self.assertIn("total_cashback_earned", data)
        self.assertIn("retailer_breakdown", data)

    def test_basket_compare_strings_and_dicts(self):
        # Test empty basket
        empty_resp = self.client.post("/api/basket/compare", json={"items": []})
        self.assertEqual(empty_resp.status_code, 200)
        self.assertEqual(empty_resp.get_json()["cheapest"], "bigbasket")

        # Test with string keys
        str_resp = self.client.post("/api/basket/compare", json={"items": ["milk", "bread"]})
        self.assertEqual(str_resp.status_code, 200)
        str_data = str_resp.get_json()
        self.assertIn("bigbasket", str_data)
        self.assertIn("blinkit", str_data)
        self.assertIn("zepto", str_data)

        # Test with dictionary items (prevents unhashable type error)
        dict_resp = self.client.post("/api/basket/compare", json={"items": [{"key": "milk"}, {"name": "bread"}]})
        self.assertEqual(dict_resp.status_code, 200)
        dict_data = dict_resp.get_json()
        self.assertIn("bigbasket", dict_data)
        self.assertIn("blinkit", dict_data)
        self.assertIn("zepto", dict_data)

    def test_similar_products(self):
        response = self.client.post("/api/similar", json={"title": "Sony WH-1000XM4 headphones"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("results", data)
        self.assertGreater(len(data["results"]), 0)


if __name__ == "__main__":
    unittest.main()
