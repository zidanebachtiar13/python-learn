import pandas as pd
import smtplib
from datetime import datetime
import random

data = pd.read_csv('birthdays.csv')
account = open('account.txt', 'r')
my_account = []

for acc in account:
    my_account.append(acc)

email = my_account[0][:-1]
password = my_account[1][:-1]

today = datetime.now()
today_tuple = (today.month, today.day)

birthdays_dict = {(data_row['month'], data_row['day']): data_row for (index, data_row) in data.iterrows()}

if today_tuple in birthdays_dict:
    birthday_person = birthdays_dict[today_tuple]
    file_path = 'letter_templates/letter_' + str(random.randint(1,3)) + '.txt'
    with open(file_path) as letter_file:
        contents = letter_file.read()
        contents = contents.replace('[NAME]', birthday_person['name'])

with smtplib.SMTP('smtp.gmail.com') as connection:
    connection.starttls()
    connection.login(user=email, password=password)
    connection.sendmail(
            from_addr=email,
            to_addrs=birthday_person['email'],
            msg='Subject:Happy Birthday!\n\n' + contents
            )
