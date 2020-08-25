from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from player_data import player_data
from spreadsheets import *
# If modifying these scopes, delete the file token.pickle. Append '.readonly' if don't want to update the sheet
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

team_name = ['FoduLassans','TaareZameenPar','TwelveThirtyFive','2020','RedZoneEmpire','TheKewlSquad','FlossAsia']
team_ind = {'FoduLassans':'D','TaareZameenPar':'E','TwelveThirtyFive':'F','2020':'G','RedZoneEmpire':'H','TheKewlSquad':'I','FlossAsia':'J'}

# Spreadsheet ID is present in its URL. It's the long string after ../d/ and before /edit..
# dev:
# spreadsheet_id = spreadsheet_dev
# prod:
spreadsheet_id = spreadsheet_prod

# NameRange is a string in the format: SheetName!TopLeftCell:BottomRightCell
range_name = [i+'!A1:K12' for  i in team_name]

    # Don't worry about this. It's for taking care of access creds and stuff.
def auth():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

"""
Common indices:
Leader Index: teamname!B1
Currency Balance: teamname!B2
Player Row: teamname!Ax:Kx (3<x<12)
Team Shares: teamname!x4:x11 (x=D,E,..,J)
"""

"""
Common commands:
update = sheet.values().update(spreadsheetId=spreadsheet_id,range='',valueInputOption='RAW',body={'values':[['']]}).execute()
getvalue = sheet.values().get(spreadsheetId=spreadsheet_id,range='').execute().get('values',[])[0][0])
"""