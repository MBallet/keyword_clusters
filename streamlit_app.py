import streamlit as st
import pandas as pd
from openai import OpenAI

# Set up OpenAI API
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Function to get themes using OpenAI API
def get_keyword_themes(keywords):
    try:
        prompt = f"Identify the main themes from the following list of keywords:\n\n{', '.join(keywords)}\n\nReturn the themes and the number of keywords under each theme in markdown format with category names in H2."
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an SEO expert skilled at finding keyword topic clusters"},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"OpenAI API error: {e}")
        return None

# Streamlit UI
# Set the page configuration
st.set_page_config(page_title="Keyword Theme Analyzer", page_icon=":bucket:")
st.image('https://djeholdingscom.cachefly.net/sites/g/files/aatuss516/files/styles/holding_logo_original/public/2024-03/DXI-new-logo.png?itok=xaoiwJJ7', width=200)
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
