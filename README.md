# 💰 Pricevana

> **An intelligent price-tracking and product-discovery platform that helps shoppers decide when and where to buy.**

🌐 **Live Demo:** https://pricevana.vercel.app/

Pricevana combines web scraping, historical price analytics, machine learning, and coupon discovery into a single shopping-assistant experience. Paste a product URL from supported marketplaces and Pricevana analyzes pricing signals, estimates near-term movement, and helps identify better times to purchase.

---

## 🖼️ Project Preview

### Smart Price Tracking
![Pricevana Price Tracker](./frontend/static/images/hero-price-tracker.webp)

### Smart Savings
![Pricevana Smart Savings](./frontend/static/images/smart-savings.webp)

### Browser Assistant
![Pricevana Browser Assistant](./frontend/static/images/browser-assistant.webp)

---

## ✨ Key Features

| Feature | Description |
| --- | --- |
| 🌗 Dark & Light Themes | Native W3C color-scheme toggle with Sun/Moon icons, system preference detection, and zero FOUC |
| 🔎 Product URL Analysis | Analyze product links from Amazon India, Flipkart, and Myntra |
| 📈 Price History | Visualize historical price movement and identify previous lows |
| 🤖 ML Price Prediction | Uses linear regression to estimate a product's near-term 7-day price trajectory |
| 🎯 Buy-Timing Score | Dynamic gauge communicates whether the current price looks bad, stable, or good |
| 🏷️ Coupon Discovery | Scans available promotional codes and evaluates potential savings |
| 🖼️ Product Image Extraction | Reads product metadata such as OpenGraph/Twitter images for fast visual previews |
| 💸 Savings Workspace | Track discounts, cashback information, notifications, and price-drop alerts |
| 🌍 Multi-Environment Frontend | Seamlessly switches between local Flask development and production cloud endpoints |

---

## 🧠 How It Works

```text
Product URL
    ↓
Pricevana Frontend (Light / Dark Theme)
    ↓
Flask Modular REST API (Blueprints Architecture)
    ├── Validator & Security (SSRF protection)
    ├── Scraper Service (Selenium + Mock fallback)
    ├── ML Engine (Linear regression forecasting)
    └── Data Layer (Deals, coupons, gift cards, grocery index)
    ↓
Dynamic interactive analytics shown in dashboard
```

### Price prediction
The backend fits a lightweight **linear regression model** to available pricing data and uses it to estimate the next **7 days** of price movement.

> **Important:** Predictions are estimates based on the available scraped/historical data and should not be treated as guaranteed future prices.

---

## 🏗️ Technical Architecture

### Frontend
- Semantic HTML5 with anti-FOUC inline theme bootstrap
- Modular CSS design system (`variables.css`, `navigation.css`, `style.css`)
- Light & Dark mode controller with `localStorage` persistence and OS media sync
- Responsive SaaS dashboard with glassmorphism aesthetics
- Canvas-based Chart.js graphs adaptive to dark/light color schemes
- CSS conic-gradient speed gauge visualization

### Backend (Modular Blueprint Pattern)
- Flask Application Factory (`create_app`)
- REST Blueprints:
  - `predictor_bp`: `/predict`, `/compare`, `/ai-advice`, `/api/similar`
  - `deals_bp`: `/api/deals`, `/api/search`
  - `workspace_bp`: `/api/wallet`, `/api/inbox`, `/api/alerts`, `/api/coupons`, `/api/giftcards`, `/api/spend-lens`, `/api/basket/compare`
- Core Services:
  - `validator.py`: SSRF prevention and URL validation
  - `ml_engine.py`: Scikit-learn regression models
  - `scraper.py`: Headless browser scraping and demo fallback
- Data Layer:
  - `mock_db.py`: In-memory state and curated store catalogs

---

## 📂 Repository Structure

```text
Pricevana/
├── backend/
│   ├── app/                    # Modular Flask Application Package
│   │   ├── __init__.py         # Application Factory & Blueprint Registration
│   │   ├── config.py           # Configuration & Environment Settings
│   │   ├── api/                # Modular REST API Blueprints
│   │   │   ├── predictor.py    # Price prediction, comparisons & AI advice
│   │   │   ├── deals.py        # Flash deals & keyword search
│   │   │   └── workspace.py    # Wallet, inbox, alerts, coupons, grocery basket
│   │   ├── services/           # Core Business Logic & Processing
│   │   │   ├── ml_engine.py    # Linear regression forecasting
│   │   │   ├── scraper.py      # E-commerce scrapers & fallback generator
│   │   │   └── validator.py    # URL safety & SSRF defense
│   │   └── data/               # Catalogs & In-Memory Store
│   │       └── mock_db.py      # Products, coupons, gift cards & prices
│   ├── app.py                  # Entrypoint runner (supports `python app.py`)
│   ├── requirements.txt        # Python dependencies
│   └── Procfile                # PaaS process configuration (Render/Railway)
│
├── frontend/
│   ├── index.html              # Main web application dashboard
│   └── static/
│       ├── css/                # Modular Design System
│       │   ├── variables.css   # Light & Dark theme tokens, design system variables
│       │   └── navigation.css  # Header, navbar tabs, theme toggle switch
│       ├── js/                 # Modular Frontend Architecture
│       │   ├── config.js       # Dynamic API_BASE resolution & global config
│       │   └── theme.js        # Professional Dark / Light theme controller
│       ├── style.css           # Master stylesheet (imports modular CSS)
│       ├── script.js           # Client-side application logic & API client
│       ├── logo.jpg            # Brand logo & favicon
│       └── images/             # Visual previews & marketplace store logos
│           ├── hero-price-tracker.webp
│           ├── smart-savings.webp
│           ├── browser-assistant.webp
│           └── stores/          # Retailer / partner logos
│
├── tests/
│   ├── __init__.py
│   └── test_app.py             # Automated unit tests for all REST API routes
│
├── .env.example                # Template for environment variables
├── .gitignore                  # Git ignore rules for Python, IDE, and OS artifacts
├── Procfile                    # Root deployment process definition
├── vercel.json                 # Vercel deployment configuration
└── README.md                   # Project documentation
```

---

## 🚀 Run Locally

### 1. Clone

```bash
git clone https://github.com/Deepanshu779/Pricevana.git
cd Pricevana
```

### 2. Start the backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The Flask API runs locally on:

`http://127.0.0.1:5000`

### 3. Start the frontend

Open a second terminal:

```bash
cd frontend
python -m http.server 8000
```

Open:

`http://localhost:8000`

### 4. Run Automated Tests

Run the backend test suite:

```bash
python -m unittest tests/test_app.py -v
```

---

## 🌐 Deployment

| Layer | Platform | URL |
| --- | --- | --- |
| Frontend | Vercel | https://pricevana.vercel.app/ |
| Backend | Render | https://pricevana.onrender.com |

---

## 📊 Product Decision Flow

```text
Check Product
      ↓
Current Price
      ↓
Historical Trend ─────┐
      ↓               │
ML 7-Day Forecast     │
      ↓               │
Buy-Timing Score ←────┘
      ↓
Coupon / Savings Check
      ↓
Suggested Purchase Decision
```

---

## 🔧 Supported Shopping Signals

Pricevana is designed around several signals that can be combined before buying:

- Current listed price
- Historical price behavior
- Estimated short-term trend
- Previous low price
- Discount/coupon opportunities
- Store/product metadata

---

## 🔮 Future Improvements

- Add richer historical-price storage instead of generated/simulated history where applicable
- Introduce stronger time-series forecasting models
- Expand marketplace coverage
- Add user accounts with persistent watchlists
- Add browser-extension integration for one-click analysis
- Add scheduled price monitoring and notifications
- Improve scraping resilience against marketplace markup changes
- Add automated backend/frontend tests and CI

---

## 👨‍💻 Author

**Deepanshu Kumar Pandit**

GitHub: [@Deepanshu779](https://github.com/Deepanshu779)

---

## ⭐ Support

If Pricevana helps you make better buying decisions, consider giving the repository a ⭐ on GitHub.

**Live Demo:** https://pricevana.vercel.app/