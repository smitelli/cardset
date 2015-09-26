import gspread
import json
from oauth2client.client import SignedJwtAssertionCredentials
from render import render_plot, render_trope

DOC_NAME = 'Plot Twist - Print and Play Card List - v0.1'
PLOT_NAME = 'Plot Cards'
TROPE_NAME = 'Trope Cards'

json_key = json.load(open('credentials.json'))
credentials = SignedJwtAssertionCredentials(
    json_key['client_email'], json_key['private_key'],
    ['https://spreadsheets.google.com/feeds'])
gc = gspread.authorize(credentials)

doc = gc.open(DOC_NAME)
for sheet in doc.worksheets():
    data = sheet.get_all_values()

    if sheet.title == PLOT_NAME:
        card_data = [{'text': r[0], 'size': r[1]} for r in data]
        render_plot(card_data)

    elif sheet.title == TROPE_NAME:
        card_data = [{'top': r[0], 'mid': r[1], 'bot': r[2]} for r in data]
        render_trope(card_data)
