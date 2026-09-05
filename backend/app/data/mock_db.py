# ================== MOCK DATA & IN-MEMORY STORE ==================

price_alerts = []

MOCK_COUPONS = {
    "amazon": [
        {"code": "AMZFREE", "discount": "Free Shipping", "description": "Get free shipping on your entire cart", "success_rate": "92%"},
        {"code": "SAVE10", "discount": "10% OFF", "description": "10% discount up to ₹1,000 on electronic appliances", "success_rate": "78%"},
        {"code": "FESTIVE500", "discount": "₹500 OFF", "description": "Flat ₹500 off on order above ₹5,000", "success_rate": "65%"},
        {"code": "AMZBLOCK", "discount": "15% OFF", "description": "15% off on Amazon Brands", "success_rate": "42%"}
    ],
    "flipkart": [
        {"code": "FKWELCOME10", "discount": "10% OFF", "description": "10% off for your first shopping order", "success_rate": "95%"},
        {"code": "SUPERCOIN5", "discount": "5% OFF", "description": "Additional 5% discount on using Flipkart SuperCoins", "success_rate": "89%"},
        {"code": "FLAT1200", "discount": "₹1,200 OFF", "description": "Flat ₹1,200 off on select Mobiles & Electronics", "success_rate": "54%"},
        {"code": "FKDEAL", "discount": "15% OFF", "description": "15% off on electronic accessories", "success_rate": "38%"}
    ],
    "myntra": [
        {"code": "MYNTRA200", "discount": "₹200 OFF", "description": "Flat ₹200 off on your first order above ₹999", "success_rate": "98%"},
        {"code": "STYLE30", "discount": "30% OFF", "description": "30% off on premium fashion labels", "success_rate": "82%"},
        {"code": "FREEGIFT", "discount": "Free Accessory", "description": "Get a free card holder on orders above ₹2,499", "success_rate": "67%"},
        {"code": "TRENDING15", "discount": "15% OFF", "description": "Extra 15% discount on trending casual wear", "success_rate": "50%"}
    ]
}

wallet = {
    "balance": 2846.95,
    "pending": 450.00,
    "lifetime": 7820.50,
    "coins": 1420,
    "transactions": [
        {"id": 1, "type": "Cashback", "amount": 1000.00, "details": "Flipkart Order #FP981273912", "date": "Today, 08:30 AM", "status": "Credited"},
        {"id": 2, "type": "Cashback", "amount": 2249.50, "details": "Amazon Order #408-9812739-11029", "date": "Yesterday, 04:15 PM", "status": "Credited"},
        {"id": 3, "type": "Cashback", "amount": 85.45, "details": "Myntra Order #MY-918237918", "date": "May 24, 2026", "status": "Credited"}
    ]
}

inbox_emails = [
    {
        "id": 1,
        "sender": "Flipkart Delivery",
        "sender_email": "delivery@flipkart.com",
        "subject": "Your package is out for delivery! 🚚",
        "date": "Today, 08:30 AM",
        "body": """
            <div style="font-family: sans-serif; max-width: 600px; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff; color: #1e293b;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #eff6ff; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="color: #2563eb; margin: 0; font-size: 20px;">Flipkart</h2>
                    <span style="font-size: 12px; color: #64748b; font-weight: bold; background: #eff6ff; padding: 4px 8px; border-radius: 999px;">ORDER #FP981273912</span>
                </div>
                <p>Hi Customer,</p>
                <p>Great news! Your package is currently out for delivery with our delivery partner and will reach you today by 9:00 PM.</p>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <strong style="display: block; margin-bottom: 8px; color: #0f172a;">Shipping Details:</strong>
                    <div style="font-size: 14px; line-height: 1.5;">
                        <strong>Product:</strong> Sony WH-1000XM4 Noise Cancelling Headphones<br>
                        <strong>Quantity:</strong> 1<br>
                        <strong>Delivery Address:</strong> 104, Green Meadows, Sector 45, Gurgaon, Haryana - 122003
                    </div>
                </div>
                <p style="font-size: 14px; color: #64748b;">Thanks for shopping with us!<br>Team Flipkart</p>
            </div>
        """,
        "status": "Out for Delivery",
        "retailer": "Flipkart",
        "amount": 19999,
        "cashback": 1000,
        "read": False
    },
    {
        "id": 2,
        "sender": "Amazon.in Orders",
        "sender_email": "auto-confirm@amazon.in",
        "subject": "Order Confirmation for Sony PlayStation 5 🎮",
        "date": "Yesterday, 04:15 PM",
        "body": """
            <div style="font-family: sans-serif; max-width: 600px; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff; color: #1e293b;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #fff7ed; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="color: #ff9900; margin: 0; font-size: 20px;">Amazon.in</h2>
                    <span style="font-size: 12px; color: #64748b; font-weight: bold; background: #fff7ed; padding: 4px 8px; border-radius: 999px;">ORDER #408-9812739-11029</span>
                </div>
                <p>Hello,</p>
                <p>Thank you for shopping with us. We'll send a confirmation when your items ship. Your estimated delivery date is in 2 days.</p>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <strong style="display: block; margin-bottom: 8px; color: #0f172a;">Order Summary:</strong>
                    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
                        <tr style="border-bottom: 1px solid #e2e8f0;">
                            <td style="padding: 8px 0;">Sony PlayStation 5 Console (Slim)</td>
                            <td style="text-align: right; padding: 8px 0;">₹44,990.00</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0; font-weight: bold;">Grand Total:</td>
                            <td style="text-align: right; padding: 8px 0; font-weight: bold; color: #ff9900;">₹44,990.00</td>
                        </tr>
                    </table>
                </div>
                <p style="font-size: 14px; color: #64748b;">Visit Your Orders to check tracking details.<br>Amazon.in Support</p>
            </div>
        """,
        "status": "Shipped",
        "retailer": "Amazon",
        "amount": 44990,
        "cashback": 2249.50,
        "read": True
    },
    {
        "id": 3,
        "sender": "Myntra Delivery",
        "sender_email": "orders@myntra.com",
        "subject": "Your Myntra package has been delivered! 🎉",
        "date": "May 24, 2026",
        "body": """
            <div style="font-family: sans-serif; max-width: 600px; padding: 20px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff; color: #1e293b;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #fdf2f8; padding-bottom: 15px; margin-bottom: 20px;">
                    <h2 style="color: #ff3f6c; margin: 0; font-size: 20px;">Myntra</h2>
                    <span style="font-size: 12px; color: #64748b; font-weight: bold; background: #fdf2f8; padding: 4px 8px; border-radius: 999px;">ORDER #MY-918237918</span>
                </div>
                <p>Hello Shopper,</p>
                <p>Your order containing 1 item has been handed over safely at your address.</p>
                <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <strong style="display: block; margin-bottom: 8px; color: #0f172a;">Order Summary:</strong>
                    <div style="font-size: 14px; line-height: 1.5;">
                        <strong>Product:</strong> Roadster Men Solid Denim Jacket<br>
                        <strong>Total Amount Paid:</strong> ₹1,899.00<br>
                        <strong>Cashback Status:</strong> ₹85.45 Credited to Flash Wallet
                    </div>
                </div>
                <p style="font-size: 14px; color: #64748b;">Enjoy your purchase!<br>Team Myntra</p>
            </div>
        """,
        "status": "Delivered",
        "retailer": "Myntra",
        "amount": 1899,
        "cashback": 85.45,
        "read": True
    }
]

MOCK_GIFT_CARDS = {
    "amazon": {"name": "Amazon Pay Gift Card", "cashback_rate": 0.5, "badge": "FLAT 0.5% CASHBACK", "provider": "Amazon"},
    "flipkart": {"name": "Flipkart Gift Card", "cashback_rate": 1.0, "badge": "FLAT 1.0% OFF", "provider": "Flipkart"},
    "myntra": {"name": "Myntra Gift Card", "cashback_rate": 4.5, "badge": "FLAT 4.5% OFF", "provider": "Myntra"},
    "dominos": {"name": "Dominos Voucher Card", "cashback_rate": 12.0, "badge": "FLAT 12.0% OFF", "provider": "Dominos"},
    "blinkit": {"name": "Blinkit E-Voucher", "cashback_rate": 3.0, "badge": "FLAT 3.0% OFF", "provider": "Blinkit"},
    "pvr": {"name": "PVR Cinemas Voucher", "cashback_rate": 18.0, "badge": "FLAT 18.0% OFF", "provider": "PVR"}
}

MOCK_BUDGET_DEALS = {
    "99": [
        {"title": "USB-C OTG Sync Adapter", "store": "Flipkart", "price": 79, "original_price": 299, "discount": "73% OFF", "rating": 4.2, "url": "https://www.flipkart.com/search?q=usb-c+otg+adapter"},
        {"title": "Laptop Webcam Slider Cover (3 Pack)", "store": "Amazon", "price": 49, "original_price": 199, "discount": "75% OFF", "rating": 4.5, "url": "https://www.amazon.in/s?k=laptop+webcam+cover"},
        {"title": "Premium Matte Metal Carabiner Keyring", "store": "Amazon", "price": 89, "original_price": 399, "discount": "77% OFF", "rating": 3.9, "url": "https://www.amazon.in/s?k=matte+metal+carabiner"}
    ],
    "199": [
        {"title": "Dual-Port 18W Fast Car Charger", "store": "Amazon", "price": 149, "original_price": 499, "discount": "70% OFF", "rating": 4.3, "url": "https://www.amazon.in/s?k=fast+car+charger"},
        {"title": "Fine Point Capacitive Stylus Pen", "store": "Flipkart", "price": 129, "original_price": 399, "discount": "67% OFF", "rating": 4.0, "url": "https://www.flipkart.com/search?q=capacitive+stylus+pen"},
        {"title": "Anti-Static Screen Cleaning Microfiber Cloth", "store": "Myntra", "price": 119, "original_price": 249, "discount": "52% OFF", "rating": 4.6, "url": "https://www.myntra.com/screen-clean-cloth"}
    ],
    "299": [
        {"title": "Ergonomic Silent USB Wired Mouse", "store": "Flipkart", "price": 249, "original_price": 799, "discount": "68% OFF", "rating": 4.1, "url": "https://www.flipkart.com/search?q=wired+mouse"},
        {"title": "Unisex Cotton Cushion Cushion Socks (3 Pair)", "store": "Myntra", "price": 229, "original_price": 599, "discount": "61% OFF", "rating": 4.4, "url": "https://www.myntra.com/socks"},
        {"title": "Flexible 360 Mini Tripod for Phone", "store": "Amazon", "price": 279, "original_price": 899, "discount": "69% OFF", "rating": 4.2, "url": "https://www.amazon.in/s?k=mini+tripod+phone"}
    ],
    "399": [
        {"title": "Smart LED Bulb 9W (Wi-Fi, Multi-Color)", "store": "Amazon", "price": 349, "original_price": 999, "discount": "65% OFF", "rating": 4.5, "url": "https://www.amazon.in/s?k=smart+led+bulb+9w"},
        {"title": "Comfy Lounge Cotton Pajama Shorts", "store": "Myntra", "price": 399, "original_price": 999, "discount": "60% OFF", "rating": 4.3, "url": "https://www.myntra.com/pajama-shorts"},
        {"title": "Anti-Glare Blue Light Filtering Glasses", "store": "Flipkart", "price": 379, "original_price": 1299, "discount": "70% OFF", "rating": 4.0, "url": "https://www.flipkart.com/search?q=blue+light+glasses"}
    ]
}

MOCK_CATEGORY_DEALS = {
    "smartphones": [
        {"title": "Apple iPhone 15 Pro Max (256GB, Blue)", "store": "Amazon", "price": 139900, "original_price": 159900, "discount": "12% OFF", "rating": 4.8, "url": "https://www.amazon.in/s?k=iphone+15+pro+max"},
        {"title": "Samsung Galaxy S24 Ultra (5G, 12GB RAM)", "store": "Flipkart", "price": 119999, "original_price": 129999, "discount": "7% OFF", "rating": 4.7, "url": "https://www.flipkart.com/search?q=samsung+s24+ultra"},
        {"title": "OnePlus 12R (5G, 8GB RAM, 256GB)", "store": "Amazon", "price": 39999, "original_price": 45999, "discount": "13% OFF", "rating": 4.5, "url": "https://www.amazon.in/s?k=oneplus+12r"}
    ],
    "laptops": [
        {"title": "Apple MacBook Air M2 (16GB, 512GB SSD)", "store": "Amazon", "price": 94999, "original_price": 114999, "discount": "17% OFF", "rating": 4.8, "url": "https://www.amazon.in/s?k=macbook+air+m2"},
        {"title": "HP Pavilion 15 (Ryzen 5, 16GB, 512GB)", "store": "Flipkart", "price": 44999, "original_price": 54999, "discount": "18% OFF", "rating": 4.2, "url": "https://www.flipkart.com/search?q=hp+pavilion+15"},
        {"title": "Lenovo IdeaPad Slim 3 (Intel Core i3)", "store": "Amazon", "price": 32900, "original_price": 48999, "discount": "32% OFF", "rating": 4.1, "url": "https://www.amazon.in/s?k=lenovo+ideapad+slim+3"}
    ],
    "televisions": [
        {"title": "Xiaomi Smart TV X Pro (55 Inch, 4K Dolby)", "store": "Flipkart", "price": 34999, "original_price": 49999, "discount": "30% OFF", "rating": 4.4, "url": "https://www.flipkart.com/search?q=xiaomi+tv+55"},
        {"title": "Sony BRAVIA 4K Ultra HD (65 Inch, Smart TV)", "store": "Amazon", "price": 79999, "original_price": 119900, "discount": "33% OFF", "rating": 4.7, "url": "https://www.amazon.in/s?k=sony+tv+65"},
        {"title": "Samsung Crystal 4K Smart TV (43 Inch)", "store": "Amazon", "price": 28990, "original_price": 44900, "discount": "35% OFF", "rating": 4.3, "url": "https://www.amazon.in/s?k=samsung+tv+43"}
    ],
    "appliances": [
        {"title": "Samsung 236L Double Door Refrigerator", "store": "Flipkart", "price": 22490, "original_price": 28999, "discount": "22% OFF", "rating": 4.4, "url": "https://www.flipkart.com/search?q=samsung+double+door+refrigerator"},
        {"title": "LG 7kg 5-Star Front Load Washing Machine", "store": "Amazon", "price": 29490, "original_price": 38999, "discount": "24% OFF", "rating": 4.6, "url": "https://www.amazon.in/s?k=lg+washing+machine"},
        {"title": "Haier 190L Single Door Refrigerator", "store": "Flipkart", "price": 14790, "original_price": 19999, "discount": "26% OFF", "rating": 4.3, "url": "https://www.flipkart.com/search?q=haier+single+door+refrigerator"}
    ]
}

SEARCH_PRODUCTS = [
    {"title": "SMOWKLY Women Korean Cotton Shorts Pajama Set", "store": "Amazon", "price": 498, "original_price": 999, "discount": "50% OFF", "rating": 3.8, "url": "https://www.amazon.in/s?k=smowkly+shorts+pajama+set"},
    {"title": "Korean Style Women Night Suit Cute Printed Pajamas", "store": "Flipkart", "price": 649, "original_price": 1299, "discount": "50% OFF", "rating": 3.8, "url": "https://www.flipkart.com/search?q=korean+style+women+night+suit"},
    {"title": "Women Korean Striped Shorts Pajama Set", "store": "Amazon", "price": 498, "original_price": 999, "discount": "50% OFF", "rating": 3.9, "url": "https://www.amazon.in/s?k=striped+shorts+pajama+set"},
    {"title": "Women Korean Hearts Print Pajama Set", "store": "Amazon", "price": 493.9, "original_price": 999, "discount": "51% OFF", "rating": 3.9, "url": "https://www.amazon.in/s?k=hearts+print+pajama+set"},
    {"title": "Celary Korean Style Night Suit Cute Printed Sleepwear", "store": "Amazon", "price": 649, "original_price": 1499, "discount": "57% OFF", "rating": 3.8, "url": "https://www.amazon.in/s?k=celary+night+suit"},
    {"title": "Sony WH-1000XM4 Noise Cancellation Bluetooth Headphones", "store": "Amazon", "price": 19999, "original_price": 29990, "discount": "33% OFF", "rating": 4.6, "url": "https://www.amazon.in/Sony-WH-1000XM4-Bluetooth-Cancellation-Resistance/dp/B0863TXGM3"},
    {"title": "Puma Unisex Solid Classic Retro Sneakers", "store": "Myntra", "price": 2499, "original_price": 4999, "discount": "50% OFF", "rating": 4.2, "url": "https://www.myntra.com/sneakers"},
    {"title": "Adidas Running Ultraboost Sports Shoes", "store": "Myntra", "price": 9899, "original_price": 17999, "discount": "45% OFF", "rating": 4.7, "url": "https://www.myntra.com/adidas-ultraboost"}
]

for tier_items in MOCK_BUDGET_DEALS.values():
    SEARCH_PRODUCTS.extend(tier_items)
for cat_items in MOCK_CATEGORY_DEALS.values():
    SEARCH_PRODUCTS.extend(cat_items)

GROCERY_ITEMS_PRICES = {
    "milk": {"name": "Organic Whole Milk (1L)", "bigbasket": 68, "blinkit": 72, "zepto": 70},
    "coffee": {"name": "Premium Roast Coffee (200g)", "bigbasket": 340, "blinkit": 360, "zepto": 350},
    "almonds": {"name": "California Almonds (500g)", "bigbasket": 420, "blinkit": 450, "zepto": 440},
    "bread": {"name": "Whole Wheat Bread (400g)", "bigbasket": 45, "blinkit": 48, "zepto": 46},
    "eggs": {"name": "Farm Fresh Eggs (12 Pack)", "bigbasket": 90, "blinkit": 95, "zepto": 92},
    "butter": {"name": "Premium Salted Butter (500g)", "bigbasket": 265, "blinkit": 275, "zepto": 270}
}


def get_catalog_product(url):
    for product in SEARCH_PRODUCTS:
        if product["url"] == url:
            return {
                "title": product["title"],
                "price": product["price"],
                "currency": "INR",
                "price_source": "demo_catalog",
                "image_url": product.get("image_url")
            }
    return None
