import streamlit as st
import pandas as pd
import requests
import json

# Function to fetch data from the API
def fetch_data():
    url = 'https://catalog.prod.learnapp.com/catalog/discover?type=courses'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE3Mjc1ODI3MjgsImV4cCI6MTcyODE4NzUyOCwiYXVkIjoibGVhcm5hcHAiLCJpc3MiOiJoeWRyYTowLjAuMSJ9.0qOdLOLcH_N4GrmOhSyRB82QNW5eizBX5G4-MkHEd3Q',
        'content-type': 'application/json',
        'dnt': '1',
        'origin': 'https://learnapp.com',
        'priority': 'u=1, i',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'x-api-key': 'ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu'
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to fetch data: {response.status_code}")
        return None

# Function to normalize JSON and flatten all keys
def json_to_dataframe(data):
    items = data.get('items', [])
    records = []
    
    for item in items:
        # Handle multiple mentors and credentials
        for mentor in item.get('mentors', [{}]):
            for credential in item.get('content', {}).get('mentorCredentials', [{}]):
                record = {
                    "subject": data.get('subject', None),
                    "subjectId": data.get('subjectId', None),
                    "item_id": item.get('id', None),
                    "type": item.get('type', None),
                    "contentType": item.get('contentType', None),
                    "title": item.get('title', None),
                    "canonicalTitle": item.get('canonicalTitle', None),
                    "difficulty": item.get('difficulty', None),
                    "totalPlaybackTime": item.get('totalPlaybackTime', None),
                    "language": ', '.join(item.get('language', [])),
                    "features": ', '.join(item.get('features', [])),
                    "isFree": item.get('isFree', None),
                    "isReleased": item.get('isReleased', None),
                    "isFeatured": item.get('isFeatured', None),
                    "isSecret": item.get('isSecret', None),
                    "releaseDate": item.get('releaseDate', None),
                    "createdAt": item.get('createdAt', None),
                    "updatedAt": item.get('updatedAt', None),
                    "mentorId": mentor.get('mentorId', None),
                    "mentorName": mentor.get('name', None),
                    "mentorTitle": mentor.get('title', None),
                    "mentorCompany": mentor.get('company', None),
                    "mentorAvatar": mentor.get('avatar', None),
                    "description": item.get('content', {}).get('description', None),
                    "watchedUser": item.get('content', {}).get('watchedUser', None),
                    "tags": ', '.join(item.get('content', {}).get('tags', [])),
                    "learningItems": ', '.join([li.get('title', '') for li in item.get('content', {}).get('learningItems', [])]),
                    "seo_metaDescription": item.get('content', {}).get('seo', {}).get('metaDescription', None),
                    "seo_metaTitle": item.get('content', {}).get('seo', {}).get('metaTitle', None),
                    "mentorCredentialTitle": credential.get('title', None),
                    "asset_card_270x350_webp_url": item.get('assets', {}).get('card-270x350-webp', {}).get('url', None),
                    "trailerVideoId": item.get('assets', {}).get('trailerVideoId', None),
                    "asset_card_500x275_jpg_url": item.get('assets', {}).get('card-500x275-jpg', {}).get('url', None)
                }
                records.append(record)
    
    df = pd.DataFrame(records)
    return df

# Fetch the data from the API
data = fetch_data()

if data:
    # Convert JSON data to DataFrame
    df = json_to_dataframe(data)

    # Streamlit app to display and query the data
    st.title('Business Event Analysis')

    # Display the dataframe in the app
    st.dataframe(df)

    # Allow user to filter by title or mentor
    title_filter = st.text_input('Filter by Course Title')
    mentor_filter = st.text_input('Filter by Mentor Name')

    # Filter the dataframe based on the filters
    if title_filter:
        df = df[df['title'].str.contains(title_filter, case=False, na=False)]

    if mentor_filter:
        df = df[df['mentorName'].str.contains(mentor_filter, case=False, na=False)]

    # Display the filtered dataframe
    st.write(f"Filtered Data ({len(df)} results):")
    st.dataframe(df)
