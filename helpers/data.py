from helpers.crawler import Crawler
from helpers.parser import Parser
from bs4 import BeautifulSoup as bs


class Data():

    @staticmethod
    def build_player_stats(id):
        url = f"https://www.transfermarkt.com/ronaldinho/leistungsdatendetails/spieler/{id}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1"

        soup = Crawler.get_data(url)

        # soup = bs(open('./html/zlatan.html'), "html.parser")

        head = Parser.player_head(soup)
        overall = Parser.stats(soup, head['position'])
        stats_by_club = Parser.stats_by_club(overall)
        stats_by_league = Parser.stats_by_league(overall)
        stats_by_season = Parser.stats_by_season(overall)
        played_clubs = Parser.played_clubs(overall)

        stats_by_club = Parser.add_badge(stats_by_club, played_clubs)

        if 'player_status' in head:
            current_club = Parser.current_club(overall[0], head['player_status'])
        else:
            current_club = {}

        data =  {
            'player_bio': head,
            'current_club': current_club,
            'played_clubs': played_clubs,
            'overall': overall,
            'stats_by_club': stats_by_club,
            'stats_by_league': stats_by_league,
            'stats_by_season': stats_by_season
        }

        return data