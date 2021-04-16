from helpers.crawler import Crawler
from helpers.parser import Parser
import pprint
from bs4 import BeautifulSoup as bs
import time
from dotenv import load_dotenv
import sys, os
from helpers.database import Database


pp = pprint.PrettyPrinter(depth=4)
load_dotenv()

try:
    mongo_address = os.getenv('MONGO_ADDRESS')
    db_name = os.getenv('DATABASE_NAME')
    collection = 'clubs'
    clubs_collection = 'clubs'
    players_collection = 'players'

    database = Database(mongo_address, db_name)

    items = database.find(collection)

    # print(items)

    for item in items:
        club_id = item['club_id']
        club_data = {
            'club': item['club'],
            'club_badge': item['club_badge'],
            'club_id': club_id
        }

        print(club_data)
        url = f'https://www.transfermarkt.com/fc-paris-saint-germain/startseite/verein/{club_id}'

        html = Crawler.get_data(url)

        data = Parser.get_players_dict(html, club_data)

        update_data = {"$set": {'updated_at': time.time()}}
        query = {"club_id": club_id}
        database.update(update_data, query, clubs_collection)

        for player in data:
            print(url)
            print(player)
            exists = database.find_by_key(player['id'], players_collection, 'id')

            if type(exists) != type({}):
                database.save_data(player, players_collection)
                print(f"Saving {player['name']} - {player['id']}")
            else:
                print(f"{player['name']} - {player['id']} already saved")

        time.sleep(60)

    print("All leagues saved with success")

except Exception as e:
    print('ERROR')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)