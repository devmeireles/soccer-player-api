from helpers.crawler import Crawler
from helpers.parser import Parser
from bs4 import BeautifulSoup


class Data():

    @staticmethod
    def build(id):
        url = f"https://www.transfermarkt.com/andriy-shevchenko/leistungsdaten/spieler/{id}/saison//plus/1#gesamt"

        # soup = Crawler.get_data(url)

        soup = BeautifulSoup(open('kahn.html'), "html.parser")
        head = Parser.player_head(soup)
        overall = Parser.overal_ballance(soup, head['position'])
        

        return {
            'player_bio': head,
            'player_data': overall
        }