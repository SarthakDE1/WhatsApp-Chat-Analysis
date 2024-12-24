import re
import pandas as pd
import matplotlib.pyplot as plt

def preprocess(data):
    # pattern definition
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    # Split messages and find dates
    messages = re.split(pattern, data)[1:]  # Getting the messages after splitting
    dates = re.findall(pattern, data)  # Extracting the date part

    # Creating a DataFrame
    df = pd.DataFrame({"User Message": messages, "Message Date": dates})

    # Converting the 'Message Date' column to datetime
    df["Message Date"] = pd.to_datetime(df["Message Date"], format="%d/%m/%y, %H:%M - ", errors='coerce')

    # Handling errors: 'coerce' will convert problematic date strings to NaT (Not a Time)
    if df["Message Date"].isnull().any():
        print("Some dates couldn't be parsed. Check the date format consistency.")

    # Renaming the column
    df.rename(columns = {"Message Date": "Date"}, inplace=True)

    # Separating users and messages
    users = []
    messages = []

    for message in df["User Message"]:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])  # User name
            messages.append("".join(entry[2:]))  # Actual message
        else:
            users.append("group notification")
            messages.append(entry[0])  # Message from group notification

    # Adding new columns to the DataFrame
    df['user'] = users
    df['message'] = messages

    # Dropping the original 'User Message' column
    df.drop(columns=["User Message"], inplace=True)

    # Extracting date components
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df["Day"] = df['Date'].dt.day
    df['Month_Num'] = df['Date'].dt.month
    df['Only_Date'] = df["Date"].dt.date
    df['Day Name'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute

    period = []

    for hour in df[['Day Name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str("00"))
        elif hour == 0:
            period.append(str("00") + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df["period"] = period

    return df
