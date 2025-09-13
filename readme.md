# 🧠 AI Web Scraper & Parser

This Streamlit-powered app scrapes any public website, cleans and chunks its HTML content, and uses a locally hosted LLM (via Ollama) to extract targeted information—live, chunk-by-chunk.

---

## 🚀 Features

- 🔍 Headless Web Scraping with Selenium  
- 🧼 DOM Cleaning & Chunking using BeautifulSoup  
- 🧠 LLM Parsing via LangChain + Ollama (Mistral model)  
- 📊 Real-Time Feedback with progress bar and live result rendering  
- ✅ Color-Coded Results for success, empty matches, and errors  
- 📈 Summary Metrics for total chunks, successful parses, and failures  
- 🧭 Tabbed UI for scraping, chunk viewing, and parsing  
- 🎨 Custom Styling with CSS and Google Fonts

---

## 🛠️ Technologies

- Python, Streamlit, Selenium, BeautifulSoup  
- LangChain + Ollama  
- Modular architecture: `scrape.py`, `parse.py`, `main.py`

---

## 📦 Installation

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Install Ollama locally
# Visit https://ollama.com/download and follow instructions for your OS
# Once installed, run:
ollama run mistral

# 3. Launch the app
streamlit run main.py
```
---

## 💡 Note: 

This app uses the Mistral model via Ollama. You must have Ollama installed and running locally before parsing will work.
- https://ollama.com/download
- https://github.com/ollama/ollama
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

## 📄 Example Parse Descriptions

- "The page title from the HTML"
- "Names of featured projects"
-"Any mention of awards or recognitions"

---

## 📊 Output Format

![AI Web Parser Screenshot](assets/ai-web-parser-screenshot-2.png?raw=true "AI Web Scraper - Tabbed Interface with Dark Theme")
Each chunk is parsed individually. Results are displayed live with:
- Output Type	Display Method:
- Valid Match	st.success() ✅
- No Match Found	st.info() ⚠️
- Parsing Error	st.error() ❌

---

## 🧠 Prompt Template

Strict instructions ensure clean output:
- No commentary
- Empty string if no match
- Raw data only—no formatting or labels

---

## 🧹 Cleanup & Resilience

![Real Time Terminal Output](assets/ai-web-parser-screenshot-3.png?raw=true "AI Web Scraper - Tabbed Interface with Dark Theme")
- Retry logic with timeout
- Fallback messages for empty/error chunks
- Scroll-to-results for smooth UX
- Chunk-by-chunk rendering for real-time feedback

---

## 🛠️ Tech Stack

- Python 3.11+
- Streamlit
- Selenium
- BeautifulSoup
- Custom CSS (`styles/app.css`)

---

## 📁 File Structure

<details>
<summary>📁 Click to view folder structure</summary>

```plaintext
AI-WEBSCRAPER/
├── __pycache__/                 # Compiled Python cache files
│   ├── parse.cpython-312.pyc
│   └── scrape.cpython-312.pyc
├── ai/                          # Optional virtual environment (if used)
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   └── pyvenv.cfg
├── assets/                      # Screenshots and media for documentation
├── styles/
│   └── app.css                  # Custom CSS for Streamlit UI
├── venv/                        # Python virtual environment
│   ├── Include/
│   ├── Lib/
│   ├── Scripts/
│   ├── etc/
│   ├── share/
│   └── pyvenv.cfg
├── chromedriver.exe            # Chrome WebDriver for Selenium
├── main.py                     # Streamlit app entry point
├── parse.py                    # LLM parsing logic via LangChain + Ollama
├── scrape.py                   # Web scraping and DOM chunking logic
├── requirements.txt            # Python dependencies
└── readme.md                   # Project documentation
```
</details>

---

## 🧪 Troubleshooting

If parsing fails or hangs:
```Bash
ollama list
```

You should see mistral listed and active. If not, run:

```Bash
ollama run mistral
```

---

## 📜 License

MIT License — feel free to fork, remix, and build on it.

---

## 🙌 Acknowledgments

Thanks to the open-source tools and libraries that make this possible. Stay tuned for LLM-powered parsing and more UX enhancements.