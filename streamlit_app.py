import streamlit as st
import wikipediaapi
import requests
import random
import time

# Wikipedia API Setup
wiki_wiki = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="snippet (anonymous@example.com)"
)


# Store seen articles to prevent repeats
if "seen_articles" not in st.session_state:
    st.session_state.seen_articles = set()

def get_random_wikipedia_page():
    """Fetches a truly random Wikipedia article and adjusts content length based on article size."""

    for _ in range(10):  # Try multiple times to find a valid, unseen article
        random_url = "https://en.wikipedia.org/wiki/Special:Random"
        response = requests.get(random_url, allow_redirects=True)

        if response.status_code == 200:
            article_title = response.url.split("/wiki/")[-1]

            # Skip articles already shown
            if article_title in st.session_state.seen_articles:
                continue

            page = wiki_wiki.page(article_title)
            if page.exists():
                # Store article title in session to avoid repeats
                st.session_state.seen_articles.add(article_title)

                # Extract content and filter out empty lines or section headers
                paragraphs = [p.strip() for p in page.text.split("\n") if p.strip() and len(p.split()) > 5]

                if len(paragraphs) < 5:
                    # If the article is very short, show the entire content
                    return page.title, "\n\n".join(paragraphs)
                else:
                    # If the article is long, show 3–4 paragraphs
                    return page.title, "\n\n".join(paragraphs[:4])

    return "No content found.", ""

# Streamlit UI
st.title("📖 Snippet!")

# Get a Wikipedia article based on the selected topic
if "current_title" not in st.session_state:
    st.session_state.current_title, st.session_state.current_paragraph = get_random_wikipedia_page()

st.subheader(st.session_state.current_title)
st.write(st.session_state.current_paragraph)

# Buttons for user actions
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Next"):
        st.session_state.current_title, st.session_state.current_paragraph = get_random_wikipedia_page()
        st.rerun()
