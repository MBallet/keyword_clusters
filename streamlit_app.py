import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to get themes using OpenAI API
def get_keyword_themes(keywords):
    prompt = f"Identify the main themes from the following list of keywords:\n\n{', '.join(keywords)}\n\nReturn the themes and the number of keywords under each theme."
    response = openai.Completion.create(
        engine="gpt-4o-mini",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Streamlit UI
st.title("Keyword Theme Analyzer")

uploaded_file = st.file_uploader("Upload a CSV file with keywords", type="csv")

if uploaded_file:
    try:
        keywords_df = pd.read_csv(uploaded_file)
        st.write("Keywords from the uploaded file:")
        st.write(keywords_df)
        
        keywords = keywords_df['keyword'].tolist()  # Assuming 'keyword' is the column name
        themes = get_keyword_themes(keywords)
        
        st.write("Keyword Themes and Counts:")
        st.write(themes)
    except Exception as e:
        st.error(f"Error: {e}")
