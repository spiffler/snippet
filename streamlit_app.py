import streamlit as st
import wikipediaapi
import openai
import random

# OpenAI API Key (store in an environment variable instead for security)
OPENAI_API_KEY = "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"

# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia('en')

def get_random_wikipedia_page():
    """Fetches a random Wikipedia page title and its first paragraph."""
    random_titles = ["History of Mathematics", "Quantum Mechanics", "Artificial Intelligence",
                     "World War II", "Philosophy", "Ancient Rome", "Computer Science",
                     "Space Exploration", "Economics", "Biology", "Psychology"]

    random_title = random.choice(random_titles)
    page = wiki_wiki.page(random_title)

    if page.exists():
        return page.title, page.summary.split(".")[0] + "."  # First sentence only
    return None, None

def get_ai_insights(paragraph):
    """Uses OpenAI to provide more context on the paragraph."""
    openai.api_key = OPENAI_API_KEY
    prompt = f"Explain this paragraph in more detail: {paragraph}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Streamlit UI
st.title("📖 Random Paragraph Explorer")

# Get a random Wikipedia paragraph
if "current_paragraph" not in st.session_state:
    st.session_state.current_title, st.session_state.current_paragraph = get_random_wikipedia_page()

st.subheader(st.session_state.current_title)
st.write(st.session_state.current_paragraph)

# Buttons for user actions
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Next"):
        st.session_state.current_title, st.session_state.current_paragraph = get_random_wikipedia_page()
        st.experimental_rerun()

with col2:
    if st.button("💡 Engage More"):
        if "ai_response" not in st.session_state or not st.session_state.ai_response:
            st.session_state.ai_response = get_ai_insights(st.session_state.current_paragraph)
        st.write(st.session_state.ai_response)
