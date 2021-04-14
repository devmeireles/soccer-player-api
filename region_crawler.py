from helpers.crawler import Crawler
from helpers.parser import Parser
import pprint
from bs4 import BeautifulSoup as bs
import time
from dotenv import load_dotenv
import os
from helpers.database import Database


pp = pprint.PrettyPrinter(depth=4)
load_dotenv()

try:
    mongo_address = os.getenv('MONGO_ADDRESS')
    db_name = os.getenv('DATABASE_NAME')
    collection = 'leagues'

    database = Database(mongo_address, db_name)

    url = 'https://www.transfermarkt.com/wettbewerbe/europa/wettbewerbe?plus=1'

    # html = Crawler.get_data(url)

    # Loads the dict from url
    html = bs(open('./html/africa.html'), "html.parser")
    data = Parser.get_league_dict(html)


    # loop the dict to add some data and save in database
    for key in data:
        key['created_at'] = time.time()
        key['status'] = 'created'

        item = database.find_by_key(key['league_id'], collection, 'league_id')

        if type(item) != type({}):
            database.save_data(key, collection)
            print(f"Saving {key['league_id']}")
        else:
            print(f"{key['league_id']} already saved")


    print("All leagues saved with success")
except Exception as e:
    print(e)