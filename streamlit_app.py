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
    """Fetches a Wikipedia article based on the selected topic or a random one if 'Random' is chosen."""
    
    if topic == "Random":
        # Get a truly random Wikipedia article
        random_url = "https://en.wikipedia.org/wiki/Special:Random"
        response = requests.get(random_url, allow_redirects=True)
        if response.status_code == 200:
            article_title = response.url.split("/wiki/")[-1]
    else:
        # Search Wikipedia for articles related to the selected topic
        search_url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={topic}&format=json"
        search_response = requests.get(search_url).json()
        search_results = search_response.get("query", {}).get("search", [])

        if not search_results:
            return "No articles found for this topic.", ""

        # Pick a random article from the search results
        article_title = search_results[random.randint(0, len(search_results) - 1)]["title"]
    
    # Get Wikipedia page
    page = wiki_wiki.page(article_title)

    if page.exists():
        # Extract at least two paragraphs
        paragraphs = page.text.split("\n")
        selected_paragraphs = [p for p in paragraphs if p.strip()]
        
        return page.title, "\n\n".join(selected_paragraphs[:3])  # First two paragraphs

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
