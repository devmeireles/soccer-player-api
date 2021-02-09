import os
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv
from datetime import datetime
from helpers.crawler import Crawler
from helpers.parser import Parser
from helpers.database import Database

load_dotenv(verbose=True)

class Data():

    @staticmethod
    def build_player_stats(id):
        url = f"https://www.transfermarkt.com/ronaldinho/leistungsdatendetails/spieler/{id}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1"

        mongo_address = os.getenv('MONGO_ADDRESS')
        db_name = os.getenv('DATABASE_NAME')
        collection = 'players'

        database = Database(mongo_address, db_name)

        player = database.find_item(id, collection)

        soup = Crawler.get_data(url)
        # soup = bs(open('./html/zlatan.html'), "html.parser")

        if type(player) != type({}):
            head = Parser.player_head(soup)
            overall = Parser.stats(soup, head['position'])
            stats_by_club = Parser.stats_by_club(overall)
            stats_by_league = Parser.stats_by_league(overall)
            stats_by_season = Parser.stats_by_season(overall)
            played_clubs = Parser.played_clubs(overall)
            played_leagues = Parser.played_leagues(overall)

            stats_by_club = Parser.add_badge_club(stats_by_club, played_clubs)
            stats_by_league = Parser.add_badge_league(stats_by_league, played_leagues)

            if 'player_status' in head:
                current_club = Parser.current_club(overall[0], head['player_status'])
            else:
                current_club = {}

            data =  {
                'id': id,
                'player_bio': head,
                'current_club': current_club,
                'played_clubs': played_clubs,
                'overall': overall,
                'stats_by_club': stats_by_club,
                'stats_by_league': stats_by_league,
                'stats_by_season': stats_by_season
            }

            if head['player_status'] == 'Retired':
                now = datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S")
                data['created_at'] = now

                database.save_data(data, collection)

            return data
        
        return player