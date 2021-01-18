import requests
from bs4 import BeautifulSoup as bs


class Crawler():

    @staticmethod
    def get_data(url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}

            resp = requests.get(url, headers=headers)

            if resp.status_code == 200:
                soup = bs(resp.content, "html.parser")

                return soup
                
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)

        