import streamlit as st
import wikipediaapi
import requests
import random

# Wikipedia API Setup
wiki_wiki = wikipediaapi.Wikipedia(
    language="en",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="snippet (anonymous@example.com)"
)

# List of topic categories
TOPIC_CATEGORIES = ["Random", "Sports", "Economics", "Science", "History", "Technology", "Art", "Politics", "Medicine"]

def get_wikipedia_article(topic):
    """Fetches a Wikipedia article from a broader category instead of strict search terms."""
    
    # Mapping each topic to a relevant Wikipedia category
    CATEGORY_MAPPING = {
        "Sports": "Category:Sports",
        "Economics": "Category:Economics",
        "Science": "Category:Science",
        "History": "Category:History",
        "Technology": "Category:Technology",
        "Art": "Category:Art",
        "Politics": "Category:Politics"
    }

    if topic == "Random":
        # Get a truly random Wikipedia article
        random_url = "https://en.wikipedia.org/wiki/Special:Random"
        response = requests.get(random_url, allow_redirects=True)
        if response.status_code == 200:
            article_title = response.url.split("/wiki/")[-1]
    else:
        # Fetch articles from the broader category
        category_name = CATEGORY_MAPPING.get(topic, None)  # No default fallback
        if not category_name:
            return "No category found.", ""

        category_page = wiki_wiki.page(category_name)

        if category_page.exists():
            subpages = category_page.categorymembers
            article_titles = [title for title in subpages if ":" not in title]  # Ignore subcategories

            if not article_titles:
                return "No articles found for this topic.", ""

            # Pick a truly random article from the category
            article_title = random.choice(article_titles)
        else:
            return "No category found.", ""

    # Fetch Wikipedia page
    page = wiki_wiki.page(article_title)

    if page.exists():
        # Extract at least two paragraphs
        paragraphs = page.text.split("\n")
        selected_paragraphs = [p for p in paragraphs if p.strip()]
        
        return page.title, "\n\n".join(selected_paragraphs[:2])  # First two paragraphs

    return "No content found.", ""

# Streamlit UI
st.title("📖 Snippet!")

# Dropdown for topic selection
selected_topic = st.selectbox("Choose a topic:", TOPIC_CATEGORIES)

# Get a Wikipedia article based on the selected topic
if "current_topic" not in st.session_state or st.session_state.current_topic != selected_topic:
    st.session_state.current_topic = selected_topic
    st.session_state.current_title, st.session_state.current_paragraph = get_wikipedia_article(selected_topic)

st.subheader(st.session_state.current_title)
st.write(st.session_state.current_paragraph)

# Buttons for user actions
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Next"):
        st.session_state.current_title, st.session_state.current_paragraph = get_wikipedia_article(selected_topic)
        st.rerun()
