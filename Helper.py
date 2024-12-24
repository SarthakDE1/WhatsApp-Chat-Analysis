from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import seaborn as sns


extractor = URLExtract()

# Fetching statistics for selected user or overall
def fetch_stats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]

    # Fetching words
    words = df['message'].str.split().explode().tolist()

    # Counting media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # Extracting links
    links = df['message'].apply(extractor.find_urls).explode().dropna().tolist()

    return num_messages, len(words), num_media_messages, len(links)

# Function to get most busy users and their percentage
def most_busy_user(df):
    user_message_count = df['user'].value_counts().head()
    user_percentage_df = (df['user']
                          .value_counts(normalize=True)
                          .mul(100)
                          .round(2)
                          .reset_index()
                          .rename(columns={'index': 'Name', 'user': 'Percentage'}))
    return user_message_count, user_percentage_df

# Function to get most common words
def most_common_words(selected_user, df):
    with open("stop_hinglish.txt", 'r') as f:
        stop_words = f.read().splitlines()  # Reading stop words into a list

    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Exclude 'group notification' and media messages
    temp = df[(df['user'] != 'group notification') & (df['message'] != '<Media omitted>\n')]

    words = []
    for message in temp['message']:
        words.extend([word for word in message.lower().split() if word not in stop_words])

    most_common_df = pd.DataFrame(Counter(words).most_common(25))
    return most_common_df

# Function to help with emoji analysis
def emoji_helper(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    emojis = [c for message in df['message'] for c in message if c in emoji.EMOJI_DATA]

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

# Function to create monthly timeline for messages
def monthly_timeline(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    df['Month_Num'] = df['Date'].dt.month
    timeline = df.groupby(['Year', 'Month', 'Month_Num']).count()['message'].reset_index()

    # Creating time column in 'Month-Year' format
    timeline['time'] = timeline['Month'] + "-" + timeline['Year'].astype(str)
    return timeline

def daily_timeline(selected_user, df):
    # Filter the DataFrame for the selected user if not "Overall"
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    # Create a new column with just the date (without time)
    df['Only_Date'] = df["Date"].dt.date

    # Group by the date and count the number of messages per day
    daily_timeline = df.groupby("Only_Date").count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user,df):
    # Filter the DataFrame for the selected user if not "Overall"
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df.groupby("Day Name").count()['message'].sort_values(ascending = False)

def month_activity_map(selected_user,df):
    # Filter the DataFrame for the selected user if not "Overall"
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    return df.groupby("Month").count()['message']

def activity_heatmap(selected_user, df):
    # Filter the DataFrame for the selected user if not "Overall"
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index="Day Name", columns="period", values='message', aggfunc='count').fillna(0)

    return user_heatmap