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

# def get_random_wikipedia_page():
#     """Fetches a truly random Wikipedia article and adjusts content length based on article size."""

#     for _ in range(10):  # Try multiple times to find a valid, unseen article
#         random_url = "https://en.wikipedia.org/wiki/Special:Random"
#         response = requests.get(random_url, allow_redirects=True)

#         if response.status_code == 200:
#             article_title = response.url.split("/wiki/")[-1]

#             # Skip articles already shown
#             if article_title in st.session_state.seen_articles:
#                 continue

#             page = wiki_wiki.page(article_title)
#             if page.exists():
#                 # Store article title in session to avoid repeats
#                 st.session_state.seen_articles.add(article_title)

#                 # Extract content and filter out empty lines or section headers
#                 paragraphs = [p.strip() for p in page.text.split("\n") if p.strip() and len(p.split()) > 5]

#                 if len(paragraphs) < 5:
#                     # If the article is very short, show the entire content
#                     return page.title, "\n\n".join(paragraphs)
#                 else:
#                     # If the article is long, show 3–4 paragraphs
#                     return page.title, "\n\n".join(paragraphs[:4])

#     return "No content found.", ""


def get_random_paragraph():
    """Fetches a truly random paragraph from Wikipedia, Trivia APIs, or Quote/Joke/Poetry APIs."""
    
    sources = ["wikipedia", "trivia", "quote", "joke", "poetry"]
    selected_source = random.choice(sources)

    if selected_source == "wikipedia":
        return get_random_wikipedia_page() + ("Source: Wikipedia",)

    elif selected_source == "trivia":
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if response.status_code == 200:
            fact = response.json().get("text", "No fact found.")
            return "Random Fact", fact, "Source: Useless Facts API"

    elif selected_source == "quote":
        response = requests.get("https://api.quotable.io/random")
        if response.status_code == 200:
            data = response.json()
            quote = f'"{data.get("content", "No quote found.")}" - {data.get("author", "Unknown")}'
            return "Inspiration", quote, "Source: Quotable API"

    elif selected_source == "joke":
        response = requests.get("https://v2.jokeapi.dev/joke/Any")
        if response.status_code == 200:
            data = response.json()
            if "joke" in data:  
                return "Random Joke", data["joke"], "Source: JokeAPI"
            elif "setup" in data and "delivery" in data:  
                return "Random Joke", f'{data["setup"]}\n\n{data["delivery"]}', "Source: JokeAPI"

    elif selected_source == "poetry":
        response = requests.get("https://poetrydb.org/random")
        if response.status_code == 200:
            poems = response.json()
            if poems and isinstance(poems, list):
                poem = poems[0]
                title = poem.get("title", "Untitled")
                author = poem.get("author", "Unknown")
                lines = "\n".join(poem.get("lines", []))  # Show full poem
                return title, f"{lines}\n\n— {author}", "Source: PoetryDB API"

    # Fallback to Wikipedia if nothing else works
    return get_random_wikipedia_page() + ("Source: Wikipedia",)

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
