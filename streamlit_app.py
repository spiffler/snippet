import streamlit as st
import wikipediaapi
import openai
import random
import os

# OpenAI API Key (store in an environment variable instead for security)
#OPENAI_API_KEY = "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"
# Initialize Wikipedia API
wiki_wiki = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="snippet (anonymous@example.com)"
)

# def get_random_wikipedia_page():
#     """Fetches a random Wikipedia page title and its first paragraph."""
#     random_titles = ["History of Mathematics", "Quantum Mechanics", "Artificial Intelligence",
#                      "World War II", "Philosophy", "Ancient Rome", "Computer Science",
#                      "Space Exploration", "Economics", "Biology", "Psychology"]

#     random_title = random.choice(random_titles)
#     page = wiki_wiki.page(random_title)

#     if page.exists():
#         return page.title, page.summary.split(".")[0] + "."  # First sentence only
#     return None, None

def get_random_wikipedia_page():
    """Fetches a truly random Wikipedia article and returns the first two paragraphs."""

    # Get a truly random Wikipedia article title
    random_url = "https://en.wikipedia.org/wiki/Special:Random"
    response = requests.get(random_url, allow_redirects=True)

    if response.status_code == 200:
        article_title = response.url.split("/wiki/")[-1]
        page = wiki_wiki.page(article_title)

        if page.exists():
            # Split text into paragraphs
            paragraphs = page.text.split("\n")

            # Get at least two non-empty paragraphs
            selected_paragraphs = []
            for para in paragraphs:
                if para.strip():  # Avoid empty lines
                    selected_paragraphs.append(para)
                if len(selected_paragraphs) >= 2:  # Stop after two paragraphs
                    break

            return page.title, "\n\n".join(selected_paragraphs)
    
    return None, None

def get_ai_insights(paragraph):
    """Uses OpenAI API to provide more context on the paragraph."""
    
    client = openai.OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        organization="org-DdMb01W8dCtzx7RX4429W3iF"  # Replace with your OpenAI Org ID
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Explain this paragraph in detail: {paragraph}"}
        ]
    )

    return response.choices[0].message.content

# Streamlit UI
st.title("📖 Snippet!")

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
        st.rerun()

with col2:
    if st.button("💡 Engage More"):
        if "ai_response" not in st.session_state or not st.session_state.ai_response:
            st.session_state.ai_response = get_ai_insights(st.session_state.current_paragraph)
        st.write(st.session_state.ai_response)
