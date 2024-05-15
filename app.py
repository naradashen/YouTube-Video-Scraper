import requests
from io import BytesIO
from datetime import datetime
from dateutil.relativedelta import relativedelta

def get_youtube_videos(query, api_key, num_pages=1):
    videos_data = []

    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "key": api_key,
        "maxResults": 50  # Maximum number of results per page (YouTube API allows up to 50)
    }

    for page in range(1, num_pages + 1):
        params["pageToken"] = None if page == 1 else next_page_token

        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            videos = data.get("items", [])

            for video in videos:
                video_title = video["snippet"]["title"]
                video_id = video["id"]["videoId"]
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                thumbnail_url = video["snippet"]["thumbnails"]["default"]["url"]
                upload_date = video["snippet"]["publishedAt"]

                # Download thumbnail image
                #response_thumbnail = requests.get(thumbnail_url)
                #thumbnail_image = Image.open(BytesIO(response_thumbnail.content))

                # Calculate time difference
                upload_datetime = datetime.strptime(upload_date, "%Y-%m-%dT%H:%M:%SZ")
                current_datetime = datetime.utcnow()
                time_difference = relativedelta(current_datetime, upload_datetime)

                # Format time since upload
                years_str = f"{time_difference.years} year{'s' if time_difference.years != 1 else ''}" if time_difference.years != 0 else ""
                months_str = f"{time_difference.months} month{'s' if time_difference.months != 1 else ''}" if time_difference.months != 0 else ""
                weeks_str = f"{time_difference.days // 7} week{'s' if time_difference.days // 7 != 1 else ''}" if time_difference.days >= 7 else ""
                days_str = f"{time_difference.days % 7} day{'s' if time_difference.days % 7 != 1 else ''}" if time_difference.days % 7 != 0 else ""
                hours_str = f"{time_difference.hours} hour{'s' if time_difference.hours != 1 else ''}" if time_difference.hours != 0 else ""

                time_since_upload = ", ".join(filter(None, [years_str, months_str, weeks_str, days_str, hours_str]))

                #videos_data.append({'title': video_title, 'url': video_url, 'thumbnail_image': thumbnail_image, 'upload_date': upload_date, 'time_since_upload': time_since_upload})
                videos_data.append({'title': video_title, 'url': video_url, 'upload_date': upload_date, 'time_since_upload': time_since_upload})

            next_page_token = data.get("nextPageToken")

        else:
            print(f"Failed to fetch data from YouTube API. Status code: {response.status_code}")
            break

    # Sort videos by upload date in descending order
    videos_data.sort(key=lambda x: x['upload_date'], reverse=True)

    return videos_data

def main():
    query = input("Enter your search query: ")
    num_pages = int(input("Enter the number of pages to scrape: "))
    api_key = input("Enter your YouTube API key: ")
    videos = get_youtube_videos(query, api_key, num_pages)

    if videos:
        for video in videos:
            print(f"Title: {video['title']}")
            print(f"URL: {video['url']}")
            print(f"Uploaded: {video['upload_date']}")
            print(f"Time since upload: {video['time_since_upload']}")
            # Display the thumbnail image
            #video['thumbnail_image'].show()
            print("\n")
    else:
        print("No videos found for the given query.")

if __name__ == "__main__":
    main()
