import pandas as pd


def clean_data(file_location):
    df = pd.read_csv(file_location, sep=',', skipinitialspace=True)
    df['first_name'] = df['ФИО'].map(lambda x: x.split()[0])
    df['last_name'] = df['ФИО'].map(lambda x: x.split()[1])
    df.drop(columns=['ФИО', 'Телефон', 'Продукт', 'Заметки', 'Куда планирует поступать'], inplace=True)
    df.rename(columns={'US ID': 'id', 'ТГ': 'handle', 'Почта': 'email', 'Формат': 'format', 'Домашки': 'homework',
                       'Дата рождения': 'birthday'}, inplace=True)
    df['handle'].fillna('@', inplace=True)
    df['handle'] = df['handle'].map(lambda x: x.lstrip('@'))
    df['homework'].fillna(0, inplace=True)
    df['homework'] = df['homework'].map(lambda x: int(x))
    # df.to_csv('students_to_db.csv', index=False)
    return df
