import streamlit as st
import requests

# Function to fetch data from the API
def fetch_data():
    url = 'https://catalog.prod.learnapp.com/catalog/discover?type=courses'
    headers = {
        'accept': '*/*',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3Mjc1ODI3MjgsImV4cCI6MTcyODE4NzUyOCwiYXVkIjoibGVhcm5hcHAiLCJpc3MiOiJoeWRyYTowLjAuMSJ9.0qOdLOLcH_N4GrmOhSyRB82QNW5eizBX5G4-MkHEd3Q',
        'x-api-key': 'ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Streamlit app
st.title("Course Catalog")

# Button to fetch data
if st.button("Fetch Courses"):
    data = fetch_data()
    
    if data:
        # Display the fetched data
        st.write(data)  # Display the raw JSON response
        # If you want to display it in a table, convert to a DataFrame first
        # df = pd.DataFrame(data)
        # st.dataframe(df)  # Uncomment if data is suitable for a DataFrame

