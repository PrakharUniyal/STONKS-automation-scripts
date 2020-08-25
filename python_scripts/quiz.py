from common import *
import random

def find_player(player):
    for player_name in player_data:
                if(player_name.startswith(player)):
                    return player_name
    return ''

def update(player,response,answered,sheet):
    currentval = float(sheet.values().get(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!C'+player_data[player][1]).execute().get('values',[])[0][0])

    firstcorrect = 1.15
    penalty = 0.90
    correct = 1.05

    if(response==0):
        if (currentval>500):
            valupdate = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!C'+player_data[player][1],valueInputOption='RAW',body={'values':[[currentval*penalty]]}).execute()
    else:
        if (currentval>500):
            if(answered==False):
                valupdate = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!C'+player_data[player][1],valueInputOption='RAW',body={'values':[[currentval*firstcorrect]]}).execute()
            else:
                valupdate = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!C'+player_data[player][1],valueInputOption='RAW',body={'values':[[currentval*correct]]}).execute()
        else:
            valupdate = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!C'+player_data[player][1],valueInputOption='RAW',body={'values':[[currentval+250]]}).execute()
    
def main():
    creds = auth()

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    participants = []
    for i in range(7):
        team_group = input(team_name[i]+': ').split()
        group = [find_player(player) for player in team_group]
        participants.append(group[:3])
    
    print('And the round begins..')

    while 1:
        players = []
        for i in range(7):
            players.append(participants[i][int(random.random()*3)])

        print(players)

        answered=False
        for i in range(7):
            play = input().split()
            if play[0]!='rest':
                player=find_player(play[0])
                response = int(play[1]) #0 or 1
                update(player,response,answered,sheet)
                players.remove(player)
                if(response): answered=True
            else:
                answered=True
                response=int(play[1])
                for player in players:
                    update(player,response,answered,sheet)
                break


        exit = input('end?')
        if(exit=='y'): break

if __name__ == '__main__':
    main()
