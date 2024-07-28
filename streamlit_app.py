import streamlit as st
import pandas as pd
from collections import Counter
import itertools
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def preprocess_keywords(keywords):
    """Split keywords into individual words."""
    return [word.lower().split() for word in keywords]

def get_word_combinations(words, n):
    """Generate word combinations of length n."""
    return [' '.join(combo) for combo in itertools.combinations(words, n)]

def get_top_combinations(keywords, n, top_n=10):
    """Get the top n word combinations."""
    all_combinations = []
    for words in keywords:
        if len(words) >= n:
            all_combinations.extend(get_word_combinations(words, n))
    combination_counts = Counter(all_combinations)
    return combination_counts.most_common(top_n)

def plot_wordcloud(data, title):
    """Plot a wordcloud of the data."""
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(dict(data))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(title)
    plt.axis('off')
    st.pyplot(plt)

# Streamlit app
st.title("Keyword Combination Visualizer")

uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'keywords' not in df.columns or 'volume' not in df.columns:
        st.error("CSV file must contain 'keywords' and 'volume' columns.")
    else:
        keywords = df['keywords'].tolist()
        keywords_processed = preprocess_keywords(keywords)
        
        st.subheader("Top 2-word Combinations")
        top_2_combinations = get_top_combinations(keywords_processed, 2)
        st.write(pd.DataFrame(top_2_combinations, columns=['Combination', 'Count']))
        plot_wordcloud(top_2_combinations, "Top 2-word Combinations")
        
        st.subheader("Top 3-word Combinations")
        top_3_combinations = get_top_combinations(keywords_processed, 3)
        st.write(pd.DataFrame(top_3_combinations, columns=['Combination', 'Count']))
        plot_wordcloud(top_3_combinations, "Top 3-word Combinations")
