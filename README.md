# ✈️ AI Travel Planner

> **An AI-powered travel planning dashboard built with Streamlit, Groq, and live travel APIs.**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red?logo=streamlit)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/AI-Groq%20Llama3-purple)](https://console.groq.com)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🌟 Features

| Feature | Description | API |
|---------|-------------|-----|
| 🌍 **Country Information** | Capital, population, languages, currencies, flag, map | REST Countries |
| 🌤️ **Live Weather** | Current conditions + 7-day forecast with icons | Open-Meteo |
| 💱 **Currency Conversion** | INR to any currency + 16 popular travel currencies | Open Exchange Rate |
| 📸 **Destination Gallery** | 6 high-quality destination photos | Unsplash / Picsum |
| 🤖 **AI Itinerary** | Day-by-day plan with costs and tips | Groq Llama 3 |
| 💰 **Budget Analyzer** | Assessment: tight / moderate / luxury | Groq Llama 3 |
| 🎒 **Packing List** | Weather-appropriate, categorized packing list | Groq Llama 3 |
| 🗺️ **Local Tips** | Phrases, safety, transport, cultural etiquette | Groq Llama 3 |

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit + Custom CSS (glassmorphism dark mode)
- **AI**: Groq API (Llama 3 8B) with OpenRouter fallback
- **APIs**: REST Countries, Open-Meteo, Open Exchange Rate, Unsplash
- **Testing**: Bruno API collection
- **Language**: Python 3.10+

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/travel-planner.git
cd travel-planner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
cp .env.example .env
```

Edit `.env` and add your keys:

```env
# Required for AI features
GROQ_API_KEY=your_groq_api_key_here

# Optional — enhances photo quality
UNSPLASH_ACCESS_KEY=your_unsplash_access_key_here
```

> **Free API Keys:**
> - **Groq**: [console.groq.com](https://console.groq.com) — Free tier, very fast
> - **Unsplash**: [unsplash.com/developers](https://unsplash.com/developers) — Free dev account
> - REST Countries, Open-Meteo, and Exchange Rate APIs are **completely free** with no registration needed.

### 4. Run the App

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📁 Project Structure

```
travel-planner/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .env.example              # API key template
├── .gitignore
├── README.md
│
├── services/                 # API integration layer
│   ├── country.py            # REST Countries API
│   ├── weather.py            # Open-Meteo API
│   ├── currency.py           # Open Exchange Rate API
│   ├── images.py             # Unsplash API
│   └── ai.py                 # Groq / OpenRouter AI
│
├── components/               # Streamlit UI components
│   ├── country_card.py       # Country information display
│   ├── weather_card.py       # Weather forecast display
│   ├── currency_card.py      # Currency converter UI
│   ├── image_gallery.py      # Photo grid gallery
│   └── itinerary_display.py  # AI content display
│
├── bruno/                    # Bruno API testing collection
│   ├── bruno.json
│   ├── get_country.bru
│   ├── get_weather.bru
│   ├── get_currency.bru
│   ├── get_images.bru
│   └── post_ai_itinerary.bru
│
└── assets/
    └── style.css             # Custom dark mode theme
```

---

## 🧪 Bruno API Collection

This project includes a [Bruno](https://www.usebruno.com/) API collection for testing all endpoints before integration.

### Setup Bruno

1. Install Bruno from [usebruno.com](https://www.usebruno.com)
2. Open Bruno → **Open Collection** → select the `bruno/` folder
3. Set environment variables:
   - `GROQ_API_KEY` → your Groq API key
   - `UNSPLASH_ACCESS_KEY` → your Unsplash access key
4. Run requests individually to verify each API

### Collection Contents

| File | Method | Endpoint | Description |
|------|--------|----------|-------------|
| `get_country.bru` | GET | `restcountries.com/v3.1/name/japan` | Country info |
| `get_weather.bru` | GET | `api.open-meteo.com/v1/forecast` | Weather forecast |
| `get_currency.bru` | GET | `open.er-api.com/v6/latest/INR` | Exchange rates |
| `get_images.bru` | GET | `api.unsplash.com/search/photos` | Destination photos |
| `post_ai_itinerary.bru` | POST | `api.groq.com/openai/v1/chat/completions` | AI itinerary |

---

## 🌐 APIs Used

### REST Countries API
- **URL**: `https://restcountries.com/v3.1/name/{name}`
- **Auth**: None
- **Returns**: Country details, coordinates, flags, currencies

### Open-Meteo API
- **URL**: `https://api.open-meteo.com/v1/forecast`
- **Auth**: None
- **Returns**: Current weather + 7-day forecast

### Open Exchange Rate API
- **URL**: `https://open.er-api.com/v6/latest/INR`
- **Auth**: None (free tier)
- **Returns**: Live exchange rates for 160+ currencies

### Unsplash API
- **URL**: `https://api.unsplash.com/search/photos`
- **Auth**: Client-ID header (free developer account)
- **Returns**: High-quality CC-licensed photos

### Groq API
- **URL**: `https://api.groq.com/openai/v1/chat/completions`
- **Auth**: Bearer token
- **Model**: `llama3-8b-8192`
- **Returns**: AI-generated travel content

---

## ☁️ Deployment

### Streamlit Community Cloud

1. Push your code to GitHub (ensure `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set **Secrets** in Streamlit dashboard:
   ```toml
   GROQ_API_KEY = "your_key_here"
   UNSPLASH_ACCESS_KEY = "your_key_here"
   ```
5. Click **Deploy**!

---

## 📝 Example Usage

1. Enter **"Japan"** in the destination field
2. Set budget to **₹50,000 INR**
3. Choose **5 days**
4. Select interests: **Anime & Pop Culture**, **Food & Cuisine**
5. Click **Plan My Trip**

You'll get:
- 🗾 Japan's capital (Tokyo), population (125M), flag, map link
- 🌤️ Current Tokyo weather + 7-day forecast
- 💱 ₹50,000 = ~84,000 JPY (live rate)
- 📸 6 stunning Japan travel photos
- 🤖 5-day AI itinerary with Akihabara, Shibuya, Kyoto temples, ramen restaurants

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License — feel free to use and modify for your projects.

---

*Built with ❤️ using Streamlit, Groq, and open travel APIs.*
