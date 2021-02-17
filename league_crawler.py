from helpers.crawler import Crawler
from helpers.parser import Parser
import pprint
from bs4 import BeautifulSoup as bs
import time
import os
from helpers.database import Database


pp = pprint.PrettyPrinter(depth=4)

try:
    mongo_address = os.getenv('MONGO_ADDRESS')
    db_name = os.getenv('DATABASE_NAME')
    collection = 'leagues'

    database = Database(mongo_address, db_name)

    url = 'https://www.transfermarkt.com/wettbewerbe/europa/wettbewerbe?plus=1'

    # html = Crawler.get_data(url)

    # Loads the dict from url
    html = bs(open('./html/europe.html'), "html.parser")
    data = Parser.get_league_dict(html)

    test = {
        'name': 'Gabriel Meireles'
    }

    database.save_data(test, collection)

    # loop the dict to add some data and save in database
    # for key in data:
    #     key['created_at'] = time.time()
    #     key['status'] = 'created'

    #     # item = database.find_by_key(key['league_id'], collection, 'league_id')
    #     temp = database.save_data(key, collection)

    #     print(key)

    #     if type(item) != type({}):
    #         database.save_data(key, collection)


    # pp.pprint(data)
except Exception as e:
    print(e)