from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import time

# Prompt template for parsing HTML content
template = ( 
    "You are tasked with extracting specific information from the following HTML content:\n\n"
    "{dom_content}\n\n"
    "Please follow these instructions precisely:\n\n"
    "1. **Targeted Extraction:** Extract only the information that directly matches the following description:\n"
    "   {parse_description}\n"
    "2. **No Commentary:** Do not include any explanations, summaries, or extra text.\n"
    "3. **Empty Response Rule:** If no matching information is found, return an empty string (`''`).\n"
    "4. **Output Format:** Respond with only the extracted data—no markdown, no labels, no formatting.\n"
)

model = OllamaLLM(model="mistral")

# Safely invokes the model with 3 retries and  120 second timeout
def safe_invoke(chain, inputs, retries=2, max_duration=120, delay=0.5):
    """
    Attempts to invoke the model up to 3 times (1 initial + 2 retries),
    but aborts if total time exceeds max_duration (in seconds).
    """
    start_time = time.time()

    for attempt in range(retries + 1):
        elapsed = time.time() - start_time
        if elapsed > max_duration:
            print(f"⏱️ Timeout: Exceeded {max_duration} seconds after {attempt} attempts.")
            return "[Parsing aborted due to timeout]"

        try:
            print(f"🧠 Attempt {attempt + 1}: Sending to model...")
            response = chain.invoke(inputs)
            print(f"✅ Model response: {response}")
            return response
        except Exception as e:
            print(f"⚠️ Error on attempt {attempt + 1}: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                print("❌ Max retries reached. Returning empty response.")
                return "❌ Max retries reached. Returning empty response."


# Function to parse DOM content using Ollama LLM
start = time.time()
def parse_with_ollama(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    for i, chunk_data in enumerate(dom_chunks, start=1):
        try:
            response = safe_invoke(
                chain,
                {
                    "dom_content": chunk_data["dom_content"],
                    "parse_description": parse_description
                },
                retries=1
            )
            parsed_output = response.strip()

            # ✅ Add user-friendly fallback message
            if not parsed_output or parsed_output == "''":
                parsed_output = "[No matching information found in this chunk.]"

            print(f"✅ Parsed chunk {i}/{len(dom_chunks)} from {chunk_data['source_url']}")
            parsed_results.append({
                "source_url": chunk_data["source_url"],
                "timestamp": chunk_data["timestamp"],
                "parsed_output": parsed_output
            })
        # ❌ Detailed error logging
        except Exception as e:
            print(f"❌ Error parsing chunk {i} from {chunk_data['source_url']}: {e}")
            print(f"🔍 Raw HTML snippet:\n{chunk_data['dom_content'][:300]}...\n")
            parsed_results.append({
                "source_url": chunk_data["source_url"],
                "timestamp": chunk_data["timestamp"],
                "parsed_output": "[Error during parsing]"
            })

    elapsed = time.time() - start
    print(f"⏱️ Total parse time: {elapsed:.2f} seconds")

    return parsed_results
