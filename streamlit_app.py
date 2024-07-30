import streamlit as st
import pandas as pd
import openai

# Set up OpenAI API
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to get themes using OpenAI API
def get_keyword_themes(keywords):
    try:
        prompt = f"Identify the main themes from the following list of keywords:\n\n{', '.join(keywords)}\n\nReturn the themes and the number of keywords under each theme."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use a valid model like gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return None

# Streamlit UI
st.title("Keyword Theme Analyzer")

uploaded_file = st.file_uploader("Upload a CSV file with keywords", type="csv")

if uploaded_file:
    try:
        keywords_df = pd.read_csv(uploaded_file)
        st.write("Keywords from the uploaded file:")
        st.write(keywords_df)
        
        if 'Keyword' not in keywords_df.columns:
            st.error("CSV must contain a column named 'Keyword'")
        else:
            keywords = keywords_df['Keyword'].tolist()
            themes = get_keyword_themes(keywords)
            
            if themes:
                st.write("Keyword Themes and Counts:")
                st.write(themes)
            else:
                st.write("No themes were returned from the API.")
    except Exception as e:
        st.error(f"Error processing the uploaded file: {e}")
