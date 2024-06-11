from telethon.sync import TelegramClient
import pandas as pd
import time
import random

API_ID = 20138314
API_HASH = '29ccf1c152698f24be15493b75fae14c'


def send_message(handle, message):
    with TelegramClient('session_name', API_ID, API_HASH) as client:
        try:
            client.send_message(handle, message)
            print(f"Message sent successfully to {handle}!")
            return True
        except Exception as e:
            print(f'The message to {handle} could not be sent: {e}')
            return False


def main():
    # files reading
    df = pd.read_csv('students_data/students.csv', sep=',', skipinitialspace=True)
    df['success'] = df.apply(lambda _: 1, axis=1)
    message_dict = {
        False: ''.join(open('txt_files/messages/bad_message_prompt.txt').readlines()),
        True: ''.join(open('txt_files/messages/good_message_prompt.txt').readlines()),
    }

    # message sending
    for i, row in df.iterrows():
        message_text = message_dict.get(row['homework'] != 0).replace('__name__', row['first_name']).replace(
            '__homework__', str(row['homework']))
        success = int(send_message(row['handle'], message_text))
        df.loc[i, 'success'] = success
        time.sleep(random.randint(20000, 40000) / 1000)

    unsuccessful_df = df[df['success'] == 0]
    # save students who could not be messaged to csv file for further consideration
    unsuccessful_df.to_csv('manual.csv', index=False)


if __name__ == "__main__":
    main()
