import streamlit as st
import validators
from scrape import (
    scrape_website,
    split_dom_content,
    extract_body_content, 
    clean_body_content
)
import time
from parse import parse_with_ollama 

# Streamlit App Configuration
st.set_page_config(page_title="AI Web Scraper", layout="centered")

# Load custom CSS
with open("styles/app.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Initialize session state variables
st.markdown(
    """
    <link rel="icon" href="https://ramseyjordan.site/favicon.ico" type="image/x-icon">
    <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet">
    """,
    unsafe_allow_html=True
)

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
                    chunks = split_dom_content(cleaned_content, max_length=1000)

                    # Store chunks with metadata
                    st.session_state.dom_chunks = [
                        {
                            "source_url": url,
                            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
                            "dom_content": chunk
                        }
                        for chunk in chunks
                    ]
                    st.session_state.page_index = 0 #Start on the first page

                    with st.expander("View Cleaned Body Content"):
                        st.text_area("Cleaned Body Content", cleaned_content, height=300)

                    st.success("✅ Website scraped successfully!")

                    # Using st.code(result, language="html") to display raw HTML made a large slow page so I used st.markdown with a scrollable div instead
                    st.markdown(
                        f"""
                        <div class="scrollable-div">
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
        value=st.session_state.dom_chunks[page_index]["dom_content"],
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
    st.header("🧠 AI Web Parser")

    if 'dom_chunks' in st.session_state:
        parse_description = st.text_area(
            "Enter a description of what to parse from the content:",
            height=100,
            value="The page title from the HTML"
        )

        if st.button("Parse Content"):
            if parse_description:
                with st.spinner("⏳ Parsing in progress... This may take a few minutes. Thank you for your patience!"):
                    progress_bar = st.progress(0)
                    total_chunks = len(st.session_state.dom_chunks)
                    parsed_results = []
                    
                    for i, chunk_data in enumerate(st.session_state.dom_chunks, start=1):
                        result = parse_with_ollama([chunk_data], parse_description)[0]
                        parsed_results.append(result)
                        progress_bar.progress(i / total_chunks)

                        # 🔍 Show result immediately with divider
                        st.markdown(f"**Chunk {i} — Source:** {result['source_url']}")
                        output = result["parsed_output"]

                        if "[Error" in output:
                            st.error(output)
                        elif "[No matching" in output:
                            st.info(output)
                        else:
                            st.success(output)

                        st.markdown("---")  # Divider between chunks

                    st.session_state.parsed_results = parsed_results

                st.success("✅ Parsing completed!")

                # Summary Metrics
                total_chunks = len(parsed_results)
                successful_parses = sum(1 for r in parsed_results if "[No matching" not in r["parsed_output"] and "[Error" not in r["parsed_output"])
                no_match = sum(1 for r in parsed_results if "[No matching" in r["parsed_output"])
                errors = sum(1 for r in parsed_results if "[Error" in r["parsed_output"])

                st.markdown("### 📊 Parsing Summary")
                st.table({
                    "Total Chunks": total_chunks,
                    "Successful Parses": successful_parses,
                    "No Match Found": no_match,
                    "Errors": errors
                })

                # Scroll to results
                st.markdown('<a name="results"></a>', unsafe_allow_html=True)
                st.markdown("""
                    <script>
                        setTimeout(function() {
                            document.querySelector("a[name='results']").scrollIntoView({ behavior: 'smooth' });
                        }, 500);
                    </script>
                """, unsafe_allow_html=True)

                # 🔍 Display Results with Color Coding
                st.markdown("### 🔍 Parsed Results")
                for result in parsed_results:
                    st.markdown(f"**Source:** {result['source_url']}")
                    output = result["parsed_output"]

                    if "[Error" in output:
                        st.error(output)
                    elif "[No matching" in output:
                        st.info(output)
                    else:
                        st.success(output)

            else:
                st.warning("Please enter a description before parsing.")
    else:
        st.info("Please scrape a site first in Tab 1 to generate content.")

# Custom Footer
st.markdown(
    """
    <div class="footer">
        &copy; Ramsey Jordan 2025. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
