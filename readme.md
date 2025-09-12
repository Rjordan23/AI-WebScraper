# 🧠 AI Web Scraper

**Built by Ramsey Jordan**  
A modern, tabbed Streamlit app for scraping, chunking, and parsing website content—with a sleek dark theme and future-ready architecture for LLM integration.

---

## 🚀 Features

- 🔍 **Scrape websites** with headless browser support and timeout handling  
- 📄 **View chunked content** with pagination and diagnostics  
- 🧠 **Prepare for AI parsing** with a clean interface and semantic chunking  
- 🎨 **Dark theme** with custom Inter font and responsive layout  
- 🖼️ **Branded footer** and polished UI components  
- ⚙️ **Modular architecture** for easy expansion and LLM integration

---

## 🖼️ App Screenshot

![AI Web Scraper UI](assets/screenshot.png?raw=true "AI Web Scraper - Tabbed Interface with Dark Theme")

---

## 📋 Usage

1. **Launch the app**  
   Run `streamlit run main.py` from your terminal.

2. **Scrape a website**  
   - Go to the **🔍 Scrape** tab  
   - Enter a valid URL (e.g. `https://en.uesp.net/wiki/Oblivion:Oblivion`)  
   - Toggle **headless mode** if desired  
   - Click **Scrape Site**

3. **View chunked content**  
   - Switch to the **📄 View Chunks** tab  
   - Use **Previous/Next** buttons to navigate chunks  
   - Inspect each chunk in a scrollable text area

4. **Prepare for parsing**  
   - Go to the **🧠 Parse with AI** tab  
   - Enter a description of what to extract  
   - Click **Parse Content** (LLM support coming soon)

---

## 🛠️ Tech Stack

- Python 3.11+
- Streamlit
- Selenium
- BeautifulSoup
- Custom CSS (`styles/app.css`)

---

## 📦 Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-web-scraper.git
cd ai-web-scraper

# Create and activate a virtual environment
# Requires Python 3.11+
python -m venv venv           # Use python3 if needed
source venv/bin/activate      # Mac/Linux
venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Optional: Install manually if requirements.txt is missing
pip install streamlit selenium beautifulsoup4 validators

# Launch the app
streamlit run main.py         
# Or use:
python3 -m streamlit run main.py

```
---

## 📁 File Structure

├── main.py              # Streamlit app logic
├── scrape.py            # Scraping and chunking functions
├── styles/
│   └── app.css          # Custom theme and layout styles
├── assets/
│   └── screenshot.png   # UI screenshot for README
├── requirements.txt

---

## 🧠 Coming Soon: LLM Integration

AI-powered parsing of chunked content
Summarization, tagging, and structured extraction
Persistent output across sessions
Export options for parsed results

---

## 📜 License

MIT License — feel free to fork, remix, and build on it.

---

## 🙌 Acknowledgments

Thanks to the open-source tools and libraries that make this possible. Stay tuned for LLM-powered parsing and more UX enhancements.