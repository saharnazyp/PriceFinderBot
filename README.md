# PriceFinderBot
Telegram &amp; Bale bot that scrapes Iranian e-commerce sites for product prices and returns an Excel report
<div align="center">

# 🔎 price-finder-bot

**English · [فارسیPersian](README.fa.md)**

</div>

---

A bot for **Telegram** and **Bale** that takes a product name from the user, searches for it across multiple Iranian online stores, and delivers the results as a **clean Excel file** — sorted from cheapest to most expensive, with direct purchase links.

> User types: "oil" → the bot searches → user receives an Excel price-comparison file.

## ✨ Features

- Dual support for **Telegram** and **Bale** with shared core logic
- Automated search across Iranian e-commerce sites with human-like behavior simulation (Playwright)
- **Persian, right-to-left Excel output** including:
  - Price summary (min, max, average)
  - Product name, price, store name, stock availability, seller rating, purchase link
  - Sorted from cheapest to most expensive
- **Multi-provider LLM system** with fallback (for optional language processing)
- Modular structure: one module per store for easy maintenance

## 🏗️ Project Architecture

```
price-finder-bot/
│
├── app/
│   ├── bot/                    
│   │   ├── telegram_bot.py
│   │   ├── bale_bot.py
│   │   ├── handlers.py         
│   │   ├── keyboards.py         
│   │   └── messages.py           
│   │
│   ├── services/                 
│   │   ├── search_service.py     
│   │   ├── cache_service.py       
│   │   ├── user_service.py     
│   │   ├── history_service.py   
│   │   └── excel_service.py      
│   │
│   ├── scrapers/                 
│   │   ├── base.py              
│   │   ├── registry.py            
│   │   ├── torob.py
│   │   ├── digikala.py
│   │   ├── basalam.py
│   │   └── ...
│   │
│   ├── core/                     
│   │   ├── search_engine.py      
│   │   ├── aggregator.py         
│   │   ├── llm_router.py         
│   │   ├── browser_pool.py       
│   │   └── exceptions.py          
│   │
│   ├── db/                       
│   │   ├── database.py            
│   │   ├── models.py            
│   │   ├── repositories.py      
│   │   └── migrations/           
│   │
│   ├── tasks/                    
│   │   ├── celery_app.py         
│   │   ├── search_tasks.py       
│   │   └── worker.py             
│   │
│   ├── config/                  
│   │   ├── settings.py           
│   │   ├── sites.py              
│   │   └── logging_config.py     
│   │
│   └── utils/                    
│       ├── logger.py             
│       ├── validators.py         
│       └── helpers.py           
│
├── data/                         
│   ├── suppliers.xlsx           
│   └── outputs/                  
│
├── logs/                         
├── tests/                        
│
├── .env.example                   
├── .gitignore
├── docker-compose.yml           
├── Dockerfile
├── requirements.txt
├── README.md
└── main.py                      
```

## 🔄 Workflow

```
User message (product name)
        ↓
   Search engine (Playwright)
        ↓
   Per-store scraper
        ↓
   Aggregate & clean results
        ↓
   Build Excel file
        ↓
   Send to user
```

## 🛒 Target Stores

Prioritized by widest coverage and lowest complexity:

| Priority | Store | URL | Note |
|:---:|---|---|---|
| 1 | Torob | torob.com | Price comparison engine — covers hundreds of stores at once |
| 2 | Digikala | digikala.com | Large general marketplace |
| 3 | Basalam | basalam.com | Producer marketplace |
| 4 | Omde-Bazar | omde-bazar.ir | Wholesale |
| 5 | Okala | okala.com | Online supermarket (location-dependent pricing) |
| 6 | SnappShop | snappshop.ir | General store (app-first) |

A list of custom supplier stores is also supported.

## ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/USERNAME/price-finder-bot.git
cd price-finder-bot

# Create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

### Environment Variables

```env
TELEGRAM_BOT_TOKEN=your_telegram_token
BALE_BOT_TOKEN=your_bale_token

# Optional — only if using language processing
GROQ_API_KEY=your_groq_key
GEMINI_API_KEY=your_gemini_key
OPENROUTER_API_KEY=your_openrouter_key
```

### Run

```bash
python main.py
```

## 🧰 Tech Stack

- **Language:** Python
- **Scraping:** Playwright (real browser, human-like behavior)
- **Messengers:** Telegram Bot API, Bale API
- **Output:** Excel via openpyxl (Persian / RTL)
- **Language processing (optional):** Groq, Google Gemini, OpenRouter

## ⚠️ Notes

- Many stores have **anti-bot** systems; scrapers require periodic maintenance.
- Browser-based scraping is **slow**; a **task queue** is recommended to prevent the bot from locking up.
- **Server geolocation** directly affects access to both Iranian stores and AI services, and must be decided before final deployment.

## 🗺️ Roadmap

- [x] Project architecture design
- [x] Excel output template design
- [ ] Torob scraper implementation
- [ ] Other scrapers implementation
- [ ] Telegram bot setup
- [ ] Add Bale bot
- [ ] Task queue & error handling
- [ ] Server deployment

## 📄 License

Developed for internal use.
