import streamlit as st
import requests

# Function to fetch data from the API
def fetch_data():
    url = 'https://catalog.prod.learnapp.com/catalog/discover?type=courses'
    headers = {
        'accept': '*/*',
        'authorization': 'Bearer YOUR_BEARER_TOKEN',  # Replace with your token
        'x-api-key': 'YOUR_API_KEY'  # Replace with your API key
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Streamlit app
st.title("Course Catalog")
data = fetch_data()

if data:
    st.write(data)
