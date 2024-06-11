import data_cleaner
from parser import google_sheet_parser
import warnings

warnings.filterwarnings('ignore')


def main():
    # 'Матграм', 'Финал_матграм_отписки', 'Финал_матем'
    google_sheet_parser.make_csv(sheet_names=['Финал_матграм_отписки', 'Матграм'])
    dataset = data_cleaner.clean_data('students_data/students.csv')

    message_dict = {
            False: ''.join(open('txt_files/messages/bad_message_prompt.txt').readlines()),
            True: ''.join(open('txt_files/messages/good_message_prompt.txt').readlines()),
    }
    for i, row in dataset.iterrows():
        message_text = message_dict.get(row['homework'] != 0).replace('__name__', row['first_name']).replace(
            '__homework__', str(row['homework'])).replace('__handle__', str(row['handle']))
        directory = 'named_messages'

        with open(f'txt_files/{directory}/{row["first_name"]}_{row["last_name"]}.txt', 'w') as f:
            f.write(message_text)


if __name__ == '__main__':
    main()
