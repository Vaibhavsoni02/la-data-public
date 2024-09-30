import streamlit as st
import pandas as pd
import requests

# Function to refresh the access token
def refresh_access_token():
    url = 'https://hydra.prod.learnapp.com/auth/refresh'
    headers = {
        'accept': '*/*',
        'content-type': 'application/json',
        'x-api-key': 'u36jbrsUjD8v5hx2zHdZNwqGA6Kz7gsm'
    }
    payload = '{"grantType":"refresh_token"}'
    
    response = requests.post(url, headers=headers, data=payload)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data['accessToken'], token_data['refreshToken']
    else:
        print(f"Failed to refresh token: {response.status_code} - {response.text}")
        return None, None

# Function to fetch data from the API
def fetch_data(access_token):
    url = 'https://catalog.prod.learnapp.com/catalog/discover?type=courses'
    headers = {
        'accept': '*/*',
        'authorization': f'Bearer {access_token}',
        'x-api-key': 'ZmtFWfKS9aXK3NZQ2dY8Fbd6KqjF8PDu'
    }

    try:
        response = requests.get(url, headers=headers)

        # Debugging: Check status code and raw response
        # st.write(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                # Parse the response to JSON
                data = response.json()
                # st.write("Raw Data from API (limited to 1000 characters):", str(data)[:1000])
                return data
            except ValueError as e:
                st.error(f"Failed to parse response as JSON: {e}")
                return None
        else:
            st.error(f"Failed to fetch data: {response.status_code}")
            return None
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Function to normalize JSON and flatten all keys, including the assets and mentor avatars
def json_to_dataframe(data):
    base_asset_url = "https://assets.learnapp.com/"
    video_asset_url = "https://www.youtube.com/watch?v="
    google_avatar_base_urls = [
        "https://lh3.googleusercontent.com/",
        "https://lh4.googleusercontent.com/"
    ]
    records = []
    
    # Navigate into 'courses' key
    courses = data.get('courses', [])
    
    # Ensure the 'courses' key exists and process it
    if isinstance(courses, list) and len(courses) > 0:
        # Iterate through each course subject
        for course in courses:
            subject = course.get('subject', None)
            subject_id = course.get('subjectId', None)
            items = course.get('items', [])
            
            # Process each item within the course
            for item in items:
                # Handle multiple mentors and flatten content
                for mentor in item.get('mentors', [{}]):
                    # Ensure the mentor avatar has the correct base URL
                    mentor_avatar = mentor.get('avatar', None)
                    if mentor_avatar:
                        # Check if avatar URL starts with known Google URLs
                        if not any(mentor_avatar.startswith(url) for url in google_avatar_base_urls):
                            # If it's a relative path, prepend base_asset_url
                            mentor_avatar = base_asset_url + mentor_avatar
                    
                    # Extract the content fields if available
                    content = item.get('content', {})
                    
                    # Flatten content fields
                    description = content.get('description', None)
                    main_resources = ', '.join([resource.get('title', '') for resource in content.get('mainResources', [])])
                    learning_items = ', '.join([item.get('title', '') for item in content.get('learningItems', [])])
                    mentor_credentials = ', '.join([cred.get('title', '') for cred in content.get('mentorCredentials', [])])
                    tags = ', '.join(content.get('tags', []))
                    
                    # Extract and flatten the assets with full URLs
                    assets = item.get('assets', {})
                    asset_columns = {
                        "asset_card_270x350_webp_url": base_asset_url + assets.get('card-270x350-webp', {}).get('url', '') if assets.get('card-270x350-webp') else None,
                        "asset_card_238x330_webp_url": base_asset_url + assets.get('card-238x330-webp', {}).get('url', '') if assets.get('card-238x330-webp') else None,
                        "asset_card_256x256_jpg_url": base_asset_url + assets.get('card-256x256-jpg', {}).get('url', '') if assets.get('card-256x256-jpg') else None,
                        "asset_card_50x50_jpg_url": base_asset_url + assets.get('card-50x50-jpg', {}).get('url', '') if assets.get('card-50x50-jpg') else None,
                        "asset_card_290x201_jpg_url": base_asset_url + assets.get('card-290x201-jpg', {}).get('url', '') if assets.get('card-290x201-jpg') else None,
                        "asset_card_500x275_webp_url": base_asset_url + assets.get('card-500x275-webp', {}).get('url', '') if assets.get('card-500x275-webp') else None,
                        "asset_card_256x256_webp_url": base_asset_url + assets.get('card-256x256-webp', {}).get('url', '') if assets.get('card-256x256-webp') else None,
                        "asset_card_640x645_webp_url": base_asset_url + assets.get('card-640x645-webp', {}).get('url', '') if assets.get('card-640x645-webp') else None,
                        "asset_card_1536x645_webp_url": base_asset_url + assets.get('card-1536x645-webp', {}).get('url', '') if assets.get('card-1536x645-webp') else None,
                        "asset_card_640x645_jpg_url": base_asset_url + assets.get('card-640x645-jpg', {}).get('url', '') if assets.get('card-640x645-jpg') else None,
                        "asset_card_290x201_webp_url": base_asset_url + assets.get('card-290x201-webp', {}).get('url', '') if assets.get('card-290x201-webp') else None,
                        "asset_card_50x50_webp_url": base_asset_url + assets.get('card-50x50-webp', {}).get('url', '') if assets.get('card-50x50-webp') else None,
                        "asset_card_400x505_webp_url": base_asset_url + assets.get('card-400x505-webp', {}).get('url', '') if assets.get('card-400x505-webp') else None,
                        "asset_card_238x165_jpg_url": base_asset_url + assets.get('card-238x165-jpg', {}).get('url', '') if assets.get('card-238x165-jpg') else None,
                        "asset_card_1440x545_webp_url": base_asset_url + assets.get('card-1440x545-webp', {}).get('url', '') if assets.get('card-1440x545-webp') else None,
                        "asset_card_400x505_jpg_url": base_asset_url + assets.get('card-400x505-jpg', {}).get('url', '') if assets.get('card-400x505-jpg') else None,
                        "asset_card_650x350_jpg_url": base_asset_url + assets.get('card-650x350-jpg', {}).get('url', '') if assets.get('card-650x350-jpg') else None,
                        "asset_card_1536x645_jpg_url": base_asset_url + assets.get('card-1536x645-jpg', {}).get('url', '') if assets.get('card-1536x645-jpg') else None,
                        "asset_card_270x350_jpg_url": base_asset_url + assets.get('card-270x350-jpg', {}).get('url', '') if assets.get('card-270x350-jpg') else None,
                        "asset_card_238x330_jpg_url": base_asset_url + assets.get('card-238x330-jpg', {}).get('url', '') if assets.get('card-238x330-jpg') else None,
                        "asset_card_500x275_jpg_url": base_asset_url + assets.get('card-500x275-jpg', {}).get('url', '') if assets.get('card-500x275-jpg') else None,
                        "trailerVideoId": video_asset_url + assets.get('trailerVideoId', None),
                    }

                    record = {
                        "subject": subject,
                        "subjectId": subject_id,
                        "item_id": item.get('id', None),
                        "type": item.get('type', None),
                        "contentType": item.get('contentType', None),
                        "title": item.get('title', None),
                        "canonicalTitle": item.get('canonicalTitle', None),
                        "summary": item.get('summary', None),
                        "difficulty": item.get('difficulty', None),
                        "totalPlaybackTime": item.get('totalPlaybackTime', None),
                        "lessonCount": item.get('lessonCount', None),
                        "language": ', '.join(item.get('language', [])),
                        "features": ', '.join(item.get('features', [])),
                        "isFree": item.get('isFree', None),
                        "isReleased": item.get('isReleased', None),
                        "isFeatured": item.get('isFeatured', None),
                        "releaseDate": item.get('releaseDate', None),
                        "createdAt": item.get('createdAt', None),
                        "updatedAt": item.get('updatedAt', None),
                        "mentorId": mentor.get('mentorId', None),
                        "mentorName": mentor.get('name', None),
                        "mentorTitle": mentor.get('title', None),
                        "mentorAvatar": mentor_avatar,  # Avatar with correct base URL
                        "mentorAbout": mentor.get('about', None),
                        # Content fields
                        "description": description,
                        "mainResources": main_resources,
                        "learningItems": learning_items,
                        "mentorCredentials": mentor_credentials,
                        "tags": tags,
                    }
                    
                    # Add the asset columns to the record
                    record.update(asset_columns)
                    records.append(record)
    
    if records:
        return pd.DataFrame(records)
    else:
        st.warning("No records were created from the data.")
        return pd.DataFrame()

# Streamlit app
st.title("Course Catalog")

# Button to fetch data
if st.button("Fetch Courses"):
    # Replace with a valid access token for testing
    access_token = "your_access_token"
    data = fetch_data(access_token)
    
    if data:
        # Convert JSON data to DataFrame
        df = json_to_dataframe(data)

        # Display the DataFrame in the app
        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("The DataFrame is empty. No data to display.")

        # Display the raw JSON in a collapsed state
        with st.expander("View raw JSON data"):
            st.json(data)
