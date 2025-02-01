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


def get_random_paragraph():
    """Fetches a truly random paragraph from Wikipedia, Trivia APIs, or Quote/Joke/Poetry APIs."""
    
    sources = ["wikipedia", "trivia", "sports_trivia", "entertainment_trivia", "quote", "joke", "poetry"]
    selected_source = random.choice(sources)

    if selected_source == "wikipedia":
        return get_random_wikipedia_page() + ("Source: Wikipedia",)

    elif selected_source == "trivia":
        try:
            response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
            if response.status_code == 200:
                fact = response.json().get("text", "No fact found.")
                return "Random Fact", fact, "Source: Useless Facts API"
        except requests.exceptions.RequestException:
            pass

    elif selected_source == "sports_trivia":
        try:
            response = requests.get("https://opentdb.com/api.php?amount=1&category=21&type=multiple")
            if response.status_code == 200:
                data = response.json().get("results", [{}])[0]
                question = data.get("question", "No trivia found.")
                return "Sports Trivia", question, "Source: OpenTDB Sports API"
        except requests.exceptions.RequestException:
            pass

    elif selected_source == "entertainment_trivia":
        try:
            response = requests.get("https://opentdb.com/api.php?amount=1&category=11&type=multiple")
            if response.status_code == 200:
                data = response.json().get("results", [{}])[0]
                question = data.get("question", "No trivia found.")
                return "Entertainment Trivia", question, "Source: OpenTDB Entertainment API"
        except requests.exceptions.RequestException:
            pass

    elif selected_source == "quote":
        try:
            response = requests.get("https://zenquotes.io/api/random")
            if response.status_code == 200:
                data = response.json()
                quote = f'"{data[0]["q"]}" - {data[0]["a"]}'
                return "Inspiration", quote, "Source: ZenQuotes API"
        except requests.exceptions.RequestException:
            pass

    elif selected_source == "joke":
        try:
            response = requests.get("https://v2.jokeapi.dev/joke/Any")
            if response.status_code == 200:
                data = response.json()
                if "joke" in data:  
                    return "Random Joke", data["joke"], "Source: JokeAPI"
                elif "setup" in data and "delivery" in data:  
                    return "Random Joke", f'{data["setup"]}\n\n{data["delivery"]}', "Source: JokeAPI"
        except requests.exceptions.RequestException:
            pass

    elif selected_source == "poetry":
        try:
            response = requests.get("https://poetrydb.org/random")
            if response.status_code == 200:
                poems = response.json()
                if poems and isinstance(poems, list):
                    poem = poems[0]
                    title = poem.get("title", "Untitled")
                    author = poem.get("author", "Unknown")
                    lines = "\n".join(poem.get("lines", []))  # Show full poem
                    return title, f"{lines}\n\n— {author}", "Source: PoetryDB API"
        except requests.exceptions.RequestException:
            pass

    # Fallback to Wikipedia if nothing else works
    return get_random_wikipedia_page() + ("Source: Wikipedia",)

# Streamlit UI
st.title("📖 Snippet!")

# Get a Wikipedia article based on the selected topic
if "current_title" not in st.session_state:
    st.session_state.current_title, st.session_state.current_paragraph, st.session_state.current_source = get_random_paragraph()

st.subheader(st.session_state.current_title)
st.write(st.session_state.current_paragraph)

# Display the source with a smaller font
if "current_source" in st.session_state:
    st.markdown(f"<p style='font-size:12px; color:gray;'>📌 {st.session_state.current_source}</p>", unsafe_allow_html=True)

# Buttons for user actions
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Next"):
        st.session_state.current_title, st.session_state.current_paragraph, st.session_state.current_source = get_random_paragraph()
        st.rerun()


# Let users toggle button position for better mobile UX
if "button_side" not in st.session_state:
    st.session_state.button_side = "right"  # Default is right-handed

toggle_side = st.toggle("Switch Button Side (for mobile)", value=(st.session_state.button_side == "left"))
st.session_state.button_side = "left" if toggle_side else "right"

# Improve mobile tap accessibility with adaptive positioning
st.markdown(
    f"""
    <style>
    @media (max-width: 768px) {{
        div.stButton button {{
            position: fixed;
            bottom: 20px;
            {"left: 20px;" if st.session_state.button_side == "left" else "right: 20px;"}
            font-size: 18px;
            padding: 12px 24px;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns([2, 1, 2])  # Centered on desktop

with col2:  # Centered for desktop, dynamic for mobile
    if st.button("➡️ Next", use_container_width=True):
        st.session_state.current_title, st.session_state.current_paragraph, st.session_state.current_source = get_random_paragraph()
        st.rerun()
