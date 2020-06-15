from common import *

def find_player(player):
    for player_name in player_data:
                if(player_name.startswith(player)):
                    return player_name
    return ''

def find_team(team):
    for team_ in team_name:
        if(team_.lower().startswith(team.lower())):
            return team_
    return ''

def main():
    creds = auth()
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()

    arg = input('Enter: playername seller shares buyer price\n').split()
    
    player = find_player(arg[0])
    seller = find_team(arg[1])
    shares = float(arg[2])
    buyer = find_team(arg[3])
    price = float(arg[4])

    print(player,seller,shares,buyer,price)

    seller_share = float(sheet.values().get(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!'+team_ind[seller]+player_data[player][1]).execute().get('values', [])[0][0])
    seller_currency = float(sheet.values().get(spreadsheetId=spreadsheet_id,range=seller+'!B2').execute().get('values', [])[0][0])
    buyer_share = float(sheet.values().get(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!'+team_ind[buyer]+player_data[player][1]).execute().get('values', [])[0][0])
    buyer_currency = float(sheet.values().get(spreadsheetId=spreadsheet_id,range=buyer+'!B2').execute().get('values', [])[0][0])

    if(buyer_currency<price or seller_share<shares or (seller==player_data[player][0] and seller_share-shares<min(0.5,seller_share) or (buyer_share+shares>1))):
        print("Invalid trade.")
        return
 
    ss = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!'+team_ind[seller]+player_data[player][1],valueInputOption='RAW',body={'values':[[seller_share-shares]]}).execute()
    bs = sheet.values().update(spreadsheetId=spreadsheet_id,range=player_data[player][0]+'!'+team_ind[buyer]+player_data[player][1],valueInputOption='RAW',body={'values':[[buyer_share+shares]]}).execute()
    sc = sheet.values().update(spreadsheetId=spreadsheet_id,range=seller+'!B2',valueInputOption='RAW',body={'values':[[seller_currency+price]]}).execute()
    bc = sheet.values().update(spreadsheetId=spreadsheet_id,range=buyer+'!B2',valueInputOption='RAW',body={'values':[[buyer_currency-price]]}).execute()

if __name__ == '__main__':
    main()
