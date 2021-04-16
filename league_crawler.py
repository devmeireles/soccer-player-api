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
    leagues_collection = 'leagues'

    database = Database(mongo_address, db_name)

    items = database.find(leagues_collection)

    for item in items:
        league_id = item['league_id']

        url = f'https://www.transfermarkt.com/premier-league/startseite/wettbewerb/{league_id}'

        html = Crawler.get_data(url)

        data = Parser.get_club_dict(html, league_id)

        for club in data:
            print(url)
            print(club)
            exists = database.find_by_key(club['club_id'], collection, 'club_id')

            if type(exists) != type({}):
                database.save_data(club, collection)
                print(f"Saving {club['club']} - {club['club_id']}")
            else:
                print(f"{club['club']} - {club['club_id']} already saved")

        time.sleep(60)

    print("All leagues saved with success")


except Exception as e:
    print('ERROR')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)