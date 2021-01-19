from helpers.crawler import Crawler
from helpers.parser import Parser
from helpers.data import Data
import pprint
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(depth=4)

temp = Data.build_player_stats(206)

pp.pprint(temp)