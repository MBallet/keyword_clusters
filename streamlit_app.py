import streamlit as st
import pandas as pd
import openai
import matplotlib.pyplot as plt
from io import StringIO

# Retrieve the OpenAI API Key from Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key is retrieved successfully
if api_key:
    openai.api_key = api_key
else:
    st.error("OpenAI API key not found. Please check your Streamlit secrets configuration.")

def identify_themes(keywords):
    prompt = f"Identify common themes in the following list of keywords: {', '.join(keywords)}"
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    themes = response.choices[0].text.strip().split(',')
    return [theme.strip() for theme in themes]

def process_csv(file):
    df = pd.read_csv(file)
    keywords = df['keywords'].tolist()
    themes = identify_themes(keywords)
    theme_count = pd.Series(themes).value_counts()
    return theme_count, themes

st.title("Keyword Theme Identifier")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    theme_count, themes = process_csv(uploaded_file)
    
    st.subheader("Top Themes by Keyword")
    fig, ax = plt.subplots()
    theme_count.plot(kind='bar', ax=ax)
    st.pyplot(fig)
    
    st.subheader("Themes")
    st.write(theme_count)
    
    # Adding an option to download the data as a CSV
    csv = StringIO()
    theme_count.to_csv(csv)
    csv.seek(0)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='themes.csv',
        mime='text/csv',
    )
