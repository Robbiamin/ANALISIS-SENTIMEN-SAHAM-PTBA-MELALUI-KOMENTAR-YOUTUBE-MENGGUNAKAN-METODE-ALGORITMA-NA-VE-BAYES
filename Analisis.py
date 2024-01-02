import pandas as pd
from googleapiclient.discovery import build

# api_key
api_key = "AIzaSyDTlGmeA0iOnD9x1WufQiWeGosOhgmiBL0"

def video_comments(video_id):
    # empty list for storing reply
    all_comments = []

    # creating youtube resource object
    youtube = build('youtube', 'v3', developerKey=api_key)

    # maximum number of comments to retrieve
    max_comments = 500

    # retrieve youtube video results
    video_response = youtube.commentThreads().list(
        part='snippet,replies', videoId=video_id).execute()

    # iterate video response
    while video_response:

        # extracting required info from each result object
        for item in video_response['items']:
            # Extracting comments
            published = item['snippet']['topLevelComment']['snippet']['publishedAt']
            user = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']

            all_comments.append([published, user, comment])

            # counting number of reply of comment
            replycount = item['snippet']['totalReplyCount']

            # if reply is there
            if replycount > 0:
                # iterate through all reply
                for reply in item['replies']['comments']:
                    # Extract reply
                    published = reply['snippet']['publishedAt']
                    user = reply['snippet']['authorDisplayName']
                    repl = reply['snippet']['textDisplay']

                    # Store reply in list
                    all_comments.append([published, user, repl])

        # Check if the total number of comments exceeds the limit
        if len(all_comments) >= max_comments:
            break

        # Again repeat
        if 'nextPageToken' in video_response:
            video_response = youtube.commentThreads().list(
                part='snippet,replies',
                pageToken=video_response['nextPageToken'],
                videoId=video_id
            ).execute()
        else:
            break

    # Trim the list to the maximum number of comments
    all_comments = all_comments[:max_comments]

    return all_comments

# Enter video id
#url video = https://www.youtube.com/watch?v=hC8YSP3rG4A

video_id = "hC8YSP3rG4A"

# Call function
comments = video_comments(video_id)

df = pd.DataFrame(comments, columns=['publishedAt', 'authorDisplayName', 'textDisplay'])
df.to_csv('youtube-comments-data1.csv',index=False)