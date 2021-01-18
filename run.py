from helpers.crawler import Crawler
from helpers.parser import Parser
from helpers.data import Data
import pprint
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(depth=4)

# url = f"https://www.transfermarkt.com/andriy-shevchenko/leistungsdaten/spieler/206/saison//plus/1#gesamt"

# # soup = Crawler.get_data(url)


# soup = BeautifulSoup(open('data.html'), "html.parser")
# item = Parser.player_head(soup)


# print(item['position'])
# pp.pprint(item)


temp = Data.build(206)

pp.pprint(temp)