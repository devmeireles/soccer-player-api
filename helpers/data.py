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
    def get_players(id):
        data = []
        player_data = []

        mongo_address = os.getenv('MONGO_ADDRESS')
        db_name = os.getenv('DATABASE_NAME')
        players_collection = 'players'

        database = Database(mongo_address, db_name)

        query = { "current_club.club_id": id }
        players = database.find_multiple_by_query(query, players_collection)

        for player in players:
            del player['_id']
            player_data.append(player)

        return player_data

    @staticmethod
    def get_clubs(id):
        data = []
        club_data = []

        mongo_address = os.getenv('MONGO_ADDRESS')
        db_name = os.getenv('DATABASE_NAME')
        clubs_collection = 'clubs'

        database = Database(mongo_address, db_name)

        # clubs = database.find(clubs_collection)
        clubs = database.find_multiple_by_key(str(id), clubs_collection, 'league_id')

        for club in clubs:
            del club['_id']
            club['club_badge'] = club['club_badge'].replace('tiny', 'head')
            club_data.append(club)

        return club_data

    @staticmethod
    def get_leagues():
        data = []
        league_data = []

        mongo_address = os.getenv('MONGO_ADDRESS')
        db_name = os.getenv('DATABASE_NAME')
        leagues_collection = 'leagues'

        database = Database(mongo_address, db_name)

        leagues = database.find(leagues_collection)

        for league in leagues:
            del league['_id']
            league['league_badge'] = league['league_badge'].replace('tiny', 'normal')
            league['country_flag'] = league['country_flag'].replace('tiny', 'medium')
            league_data.append(league)

        return league_data

    @staticmethod
    def get_configs():
        data = []
        league_data = []
        mongo_address = os.getenv('MONGO_ADDRESS')
        db_name = os.getenv('DATABASE_NAME')
        leagues_collection = 'leagues'
        clubs_collection = 'clubs'
        players_collection = 'players'

        database = Database(mongo_address, db_name)

        leagues = database.count_collection(leagues_collection)
        clubs = database.count_collection(clubs_collection)
        players = database.count_collection(players_collection)

        data.append(
            {
                'leagues': leagues,
                'clubs': clubs,
                'players': players,
            }
        )

        return data

    @staticmethod
    def search_top():
        data = []
        mongo_address = os.getenv('MONGO_ADDRESS')
        db_name = os.getenv('DATABASE_NAME')
        collection = 'players'

        database = Database(mongo_address, db_name)

        items = database.find_top(collection)

        for item in items:
            del item['_id']
            data.append(item)

        return data

    @staticmethod
    def search_player(keyword):
        data = []
        mongo_address = os.getenv('MONGO_ADDRESS')
        db_name = os.getenv('DATABASE_NAME')
        collection = 'players'

        database = Database(mongo_address, db_name)

        items = database.find_player(keyword, collection)

        for item in items:
            del item['_id']
            data.append(item)

        return data

    @staticmethod
    def build_player_stats(id):
        id = int(id)
        url = f"https://www.transfermarkt.com/ronaldinho/leistungsdatendetails/spieler/{id}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1"

        mongo_address = os.getenv('MONGO_ADDRESS')
        db_name = os.getenv('DATABASE_NAME')
        collection = 'players'

        database = Database(mongo_address, db_name)

        soup = Crawler.get_data(url)
        # soup = bs(open('./html/eusebio.html'), "html.parser")

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

        item = database.find_item(id, collection)

        if type(item) != type({}):
            player_data = {
                'name': head['name'],
                'profile_image': head['profile_image'],
                'current_club': current_club,
                'id': id,
                'hit': 1
            }

            database.save_data(player_data, collection)
        else:
            update_data = {"$inc": {'hit': 1}}
            query = {"id": id}
            database.update(update_data, query, collection)


        return data