from helpers.crawler import Crawler
from helpers.parser import Parser
from bs4 import BeautifulSoup as bs


class Data():

    @staticmethod
    def build_player_stats(id):
        url = f"https://www.transfermarkt.com/ronaldinho/leistungsdatendetails/spieler/{id}/saison//verein/0/liga/0/wettbewerb//pos/0/trainer_id/0/plus/1"

        soup = Crawler.get_data(url)

        # soup = bs(open('./html/eusebio.html'), "html.parser")

        head = Parser.player_head(soup)
        overall = Parser.stats(soup, head['position'])
        stats_by_club = Parser.stats_by_club(overall)
        stats_by_league = Parser.stats_by_league(overall)
        stats_by_season = Parser.stats_by_season(overall)

        return {
            'player_bio': head,
            'overall': overall,
            'stats_by_club': stats_by_club,
            'stats_by_league': stats_by_league,
            'stats_by_season': stats_by_season
        }