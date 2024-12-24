import streamlit as st
from PIL.ImageColor import colormap
from streamlit import columns

import Preprocessor
import Helper
import matplotlib.pyplot as plt
import emoji

import seaborn as sns

from Helper import daily_timeline

st.sidebar.title("WhatsApp Chat Analysis")

# File uploader in the sidebar
uploaded_file = st.sidebar.file_uploader("Choose a WhatsApp chat file")

if uploaded_file is not None:
    # Reading and decoding the uploaded file
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")

    # Preprocessing the data
    try:
        df = Preprocessor.preprocess(data)
    except Exception as e:
        st.error(f"Error during preprocessing: {e}")
        st.stop()

    # Displaying the DataFrame
    st.dataframe(df)

    # Fetch unique users excluding group notifications
    user_list = df['user'].unique().tolist()
    if 'group notification' in user_list:
        user_list.remove('group notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    # Sidebar selectbox for user selection
    selected_user = st.sidebar.selectbox("Show Analysis About", user_list)

    if st.sidebar.button("Show Analysis"):
        # Fetching statistics for the selected user
        num_messages, words, num_media_messages, links = Helper.fetch_stats(selected_user, df)

        # Creating columns to display statistics
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Message")
            st.title(num_messages)

        with col2:
            st.header("Total Words")
            st.title(words)

        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)

        with col4:
            st.header("Total Links")
            st.title(links)

        if selected_user == "Overall":
            st.title("Most Busy Users")
            # Fetch the most busy users and the corresponding DataFrame
            x, new_df = Helper.most_busy_user(df)

            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)
            with col1:
                # Bar chart of top users
                ax.bar(x.index, x.values, color="green")
                st.pyplot(fig)

            with col2:
                # Displaying the DataFrame with message counts
                st.dataframe(new_df)

        # Fetching the most common words for the selected user
        most_common_df = Helper.most_common_words(selected_user, df)

        st.title("Most Common Words")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(most_common_df)

        with col2:
            # Creating a new figure for this plot
            fig, ax = plt.subplots()
            ax.bar(most_common_df[0], most_common_df[1], color="Red")
            plt.xticks(rotation="vertical")
            st.pyplot(fig)

        emoji_df = Helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)

    st.title("Monthly Timeline Analysis")
    timeline = Helper.monthly_timeline(selected_user, df)

    fig, ax = plt.subplots()

    ax.plot(timeline['time'], timeline['message'],color = "Green")
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    st.title("Daily Timeline Analysis")
    daily_timeline = Helper.daily_timeline(selected_user, df)

    fig, ax = plt.subplots()  # Set the figure size here

    ax.plot(daily_timeline['Only_Date'], daily_timeline['message'], color='blue')
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    st.title("Activity Map")
    col1, col2 = st.columns(2)

    with col1:
        st.header("Most Busy Day")
        busy_day = Helper.week_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        plt.bar(busy_day.index,busy_day.values,color = "Purple")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

    with col2:
        st.header("Most Busy Month")
        busy_month = Helper.month_activity_map(selected_user, df)

        fig, ax = plt.subplots()
        plt.bar(busy_month.index,busy_month.values,color = "green")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)


    st.title("Online Activity Map")
    user_heatmap = Helper.activity_heatmap(selected_user, df)

    fig, ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    plt.yticks(rotation = 'horizontal')
    st.pyplot(fig)