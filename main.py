import streamlit as st
import validators
from scrape import (
    scrape_website,
    split_dom_content,
    extract_body_content, 
    clean_body_content
)
import time

# Streamlit App Configuration
st.set_page_config(page_title="AI Web Scraper", layout="wide")
st.title("AI Web Scraper")
tab1, tab2, tab3 = st.tabs(["🔍 Scrape", "📄 View Chunks", "🧠 Parse with AI"])

# Scrape Button Logic
with tab1:
    url = st.text_input("Enter the URL of the Website to scrape:")
    headless_mode = st.checkbox("Run in headless mode", value=True, key="headless_mode", help="Headless mode runs the browser invisibly in the background. It's faster and cleaner, but you won't see the browser window.")

    if st.button("Scrape Site"):
        if not url.strip():
            st.error("Please enter a valid URL.")
        elif not validators.url(url):
            st.error("Please enter a valid URL.")
        else:
            status_placeholder = st.empty()
            with st.spinner("Scraping website... please wait ⏳"):
                status_placeholder.text("Starting the scraping process...")
                start_time = time.time()

                result = scrape_website(url, headless=headless_mode, max_duration=30)
                elapsed = time.time() - start_time

                # Timeout Handling
                if "<!-- Scraping timed out -->" in result:
                    status_placeholder.warning("Scraping timed out after 30 seconds. This site may use infinite scroll or dynamic loading.")
                else: # Successful scrape
                    status_placeholder.text(f"Scraping completed in {elapsed:.2f} seconds.")
                    body_content = extract_body_content(result)
                    cleaned_content = clean_body_content(body_content)
                    st.write(f"🧪 Cleaned content length: {len(cleaned_content)} characters")
                    st.session_state.dom_content = cleaned_content

                    # Store cleaned content and prepare for pagination
                    st.session_state.dom_content = cleaned_content
                    st.session_state.dom_chunks = split_dom_content(cleaned_content)
                    st.session_state.page_index = 0 #Start on the first page

                    with st.expander("View Cleaned Body Content"):
                        st.text_area("Cleaned Body Content", cleaned_content, height=300)

                    st.success("✅ Website scraped successfully!")

                    # Using st.code(result, language="html") to display raw HTML made a large slow page so I used st.markdown with a scrollable div instead
                    st.markdown(
                        f"""
                        <div style="height:250px; overflow:auto; border:1px solid #ccc; padding:10px; background-color:#f9f9f9;">
                            <pre>{result}</pre>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

# Paginated viewer for parsed content
with tab2:
    if 'dom_chunks' in st.session_state:
        total_pages = len(st.session_state.dom_chunks)
        page_index = st.session_state.get("page_index", 0)

        st.markdown(f"### Parsed Content - Page {page_index + 1} of {total_pages}")
        st.text_area(
        label="Chunked Content",
        value=st.session_state.dom_chunks[page_index],
        height=300
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Previous Page") and page_index > 0:
                st.session_state.page_index = page_index - 1
        with col2:
            if st.button("Next Page") and page_index < total_pages - 1:
                st.session_state.page_index = page_index + 1

# Parsing Section
with tab3:
    if 'dom_content' in st.session_state:
        parse_description = st.text_area(
        "Enter a description of what to parse from the content:",
        height=100
        )

        if st.button("Parse Content"):
            if parse_description:
                st.write("Parsing DOM content...")
                dom_chunks = split_dom_content(st.session_state.dom_content)
                # You can now pass dom_chunks to an AI model or parsing logic
            else:
                st.warning("Please enter a description before parsing.")
