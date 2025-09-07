#python3.7
import re
import pandas as pd

# Open file
f = open(r"C:\Users\Renukaraj\OneDrive\Desktop\whatsapp chat analyser\me\WhatsApp Chat with Rithish Kushallappa.txt", 'r', encoding='utf-8')

data = f.read()
print(data)

# ✅ Regex updated for dd/mm/yy and am/pm
pattern = r'\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s'

messages = re.split(pattern, data)[1:]
print(messages)

dates = re.findall(pattern, data)
print(dates)

df = pd.DataFrame({'user_message': messages, 'message_date': dates})

# ✅ Correct datetime parsing for 2-digit year + 12h clock with am/pm
df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ', errors='coerce')

df.rename(columns={'message_date': 'date'}, inplace=True)
print(df.head())
print(df.shape)

users = []
messages = []
for message in df['user_message']:
    entry = re.split('([\w\W]+?):\s', message)
    if entry[1:]:
        users.append(entry[1])
        messages.append(entry[2])
    else:
        users.append('group_notification')
        messages.append(entry[0])

df['user'] = users
df['message'] = messages
df.drop(columns=['user_message'], inplace=True)
print(df.head())

df['year'] = df['date'].dt.year
print(df.head())

df['month'] = df['date'].dt.month_name()
df['day'] = df['date'].dt.day
df['hour'] = df['date'].dt.hour
df['minute'] = df['date'].dt.minute
print(df.head())

words = []
for message in df['message']:
    words.extend(message.split())