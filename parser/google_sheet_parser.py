import csv
import gspread
from google.oauth2.service_account import Credentials
import secret


CREDENTIALS = secret.CREDENTIALS
SHEET_URL = secret.SHEET_URL
# Google Sheets API setup
scopes = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file(CREDENTIALS, scopes=scopes)
client = gspread.authorize(creds)


def read_google_sheet(sheet_url, sheet_name):
    sheet_id = sheet_url.split('/')[-2]
    sheet = client.open_by_key(sheet_id).worksheet(sheet_name)
    return sheet.get_all_records(head=1, default_blank='')


def make_csv(sheet_names):
    sheet_url = SHEET_URL
    directory = 'students_data'
    students = []

    for sheet_name in sheet_names:
        students += read_google_sheet(sheet_url, sheet_name)

    with open(f'{directory}/students.csv', 'w', newline='') as csvfile:
        fieldnames = students[0].keys() if students else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for student in students:
            writer.writerow(student)
