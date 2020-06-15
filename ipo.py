from common import *

def find_player(player):
    for player_name in player_data:
                if(player_name.startswith(player.lower())):
                    return player_name
    return ''

def lock_players():
    locked_players = []
    for i in range(7):
        player_list = input('Locked players of team '+team_name[i]+': ').split()
        for player in player_list:
            player_name = find_player(player)
            if(player_name!=''):
                locked_players.append(player_name)
    return locked_players

def distribute(player,buyers,sheet):
    share = round(0.5/len(buyers),2)
    player_team_sheet = player_data[player][0]
    player_ind = player_data[player][1]
    
    player_val_fetch = sheet.values().get(spreadsheetId=spreadsheet_id,range=player_team_sheet+'!B'+player_ind).execute()
    player_val = float(player_val_fetch.get('values',[])[0][0])
    
    ownerupdate = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_team_sheet+'!'+team_ind[player_team_sheet]+player_ind,valueInputOption='RAW',body={'values':[[1-(share*len(buyers))]]}).execute()
    
    ownercurrentbal_fetch = sheet.values().get(spreadsheetId=spreadsheet_id,range=player_team_sheet+'!B2').execute()
    ownercurrentbal = float(ownercurrentbal_fetch.get('values',[])[0][0])
    ownerbalupdate = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_team_sheet+'!B2',valueInputOption='RAW',body={'values':[[ownercurrentbal+(share*len(buyers)*player_val)]]}).execute()
    
    for buyer in buyers:
        buyerupdate = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_team_sheet+'!'+team_ind[buyer]+player_ind,valueInputOption='RAW',body={'values':[[share]]}).execute()
        
        buyercurrentbal_fetch = sheet.values().get(spreadsheetId=spreadsheet_id,range=buyer+'!B2').execute()
        buyercurrentbal = float(buyercurrentbal_fetch.get('values',[])[0][0])
        buyerbalupdate = sheet.values().update(spreadsheetId=spreadsheet_id,range=buyer+'!B2',valueInputOption='RAW',body={'values':[[buyercurrentbal-(share*player_val)]]}).execute()
    
def main():
    creds = auth()
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    locked_players = lock_players()

    print('\nLocked Players:')
    for player_det in locked_players:
        print(player_det)
    print()

    portfolio = []
    for i in range(7):
        player_list=input('Portfolio for team '+team_name[i]+':\n').split()
        portfolio.append([find_player(player) for player in player_list][:7]+['']*(7-len([find_player(player) for player in player_list][:7])))

    for i in range(7):
        lot = [portfolio[j][i] for j in range(7)]
        uniques = list(set(lot))
        if '' in uniques:
            uniques.remove('')
        for locked_player in locked_players:
            if locked_player in uniques:
                uniques.remove(locked_player)
        
        buyer_dict = {}
        for unique in uniques:
            buyer_dict[unique]=[]
        
        for j in range(7):
            if(portfolio[j][i] in uniques):
                buyer_dict[portfolio[j][i]].append(team_name[j])
        
        print(buyer_dict)

        for key in buyer_dict.keys():
            locked_players.append(key)

        for player,buyers in buyer_dict.items():
            distribute(player,buyers,sheet)

if __name__ == '__main__':
    main()
