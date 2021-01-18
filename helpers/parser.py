from bs4 import BeautifulSoup as bs
import re

class Parser():
    @staticmethod
    def format_text(text):
        regex = re.compile(r'[\n\r\t]')
        text = regex.sub('', text)

        splited = text.split(":")
        key = splited[0]
        value = splited[1]

        if key == 'Current international':
            key = 'current_international'
        elif key == 'Place of birth':
            key = 'birth_place'
        elif key == 'Citizenship':
            key = 'citizenship'
        elif key == 'Position':
            key = 'position'
        elif key == 'Citizenship':
            key = 'citizenship'
        elif key == 'Agent':
            key = 'agent'
        elif key == 'Contract expires':
            key = 'contract_expires'
        elif key == 'Height':
            key = 'height'
        elif key == 'Former International':
            key = 'former_international'


        return key, value.strip()
    
    @staticmethod
    def player_head(soup):
        try:
            data = {}
            profile = soup.select('.dataContent > .dataBottom > .dataDaten')
            profile_size = range(len(profile))

            for profile_index in range(len(profile_size)):
                if profile_index == 0:
                    items_flag = profile[profile_index].find_all(True, {"class": re.compile("^(flaggenrahmen)$")})
                    for index in range(len(items_flag)):
                        if index == 0:
                            data.update({'birth_country': items_flag[index]['title']})
                for p in profile[profile_index].find_all('p'):
                    formated_text = Parser.format_text(p.text)
                    data.update({formated_text[0]: formated_text[1]})
        except IndexError:
            pass

        return data



    @staticmethod
    def overal_ballance(soup, position):
        data = []
        try:
            player = soup.select('.dataMain > .dataTop > .dataName > h1')[0].text
            
            overall_table = soup.select('.responsive-table > .grid-view > .items > tbody')[0]
            
            if position == "Goalkeeper":
                return Parser.goalkeeper_overall(soup)
            else:
                return Parser.line_overall(soup)

        except IndexError:
            pass

    @staticmethod
    def line_overall(soup):
        data = []
        try:            
            overall_table = soup.select('.responsive-table > .grid-view > .items > tbody')[0]
            
            for cells in overall_table.find_all(True, {"class": re.compile("^(even|odd)$")}):
                league = cells.find_all('td')[1].text
                apps = cells.find_all('td')[2].text
                goals = cells.find_all('td')[3].text
                assists = cells.find_all('td')[4].text
                own_goals = cells.find_all('td')[5].text
                substitutions_on = cells.find_all('td')[6].text
                substitutions_off = cells.find_all('td')[7].text
                yellow_card = cells.find_all('td')[8].text
                second_yellow_card = cells.find_all('td')[9].text
                red_card = cells.find_all('td')[10].text
                penalty_goal = cells.find_all('td')[11].text
                minutes_per_goal = cells.find_all('td')[12].text
                minutes_played = cells.find_all('td')[13].text
                

                player_overall =  {
                    'league': league,
                    'apps': 0 if apps == '-' else apps,
                    'goals': 0 if goals == '-' else goals,
                    'assists': 0 if assists == '-' else assists,
                    'own_goals': 0 if own_goals == '-' else own_goals,
                    'substitutions_on': 0 if substitutions_on == '-' else substitutions_on,
                    'substitutions_off': 0 if substitutions_off == '-' else substitutions_off,
                    'yellow_card': 0 if yellow_card == '-' else yellow_card,
                    'second_yellow_card': 0 if second_yellow_card == '-' else second_yellow_card,
                    'red_card': 0 if red_card == '-' else red_card,
                    'penalty_goal': 0 if penalty_goal == '-' else penalty_goal,
                    'minutes_per_goal': 0 if minutes_per_goal == '-' else minutes_per_goal,
                    'minutes_played': 0 if minutes_played == '-' else minutes_played,
                }

                data.append(player_overall)
        except IndexError:
            pass

        return data

    @staticmethod
    def goalkeeper_overall(soup):
        data = []
        try:            
            overall_table = soup.select('.responsive-table > .grid-view > .items > tbody')[0]
            
            for cells in overall_table.find_all(True, {"class": re.compile("^(even|odd)$")}):
                league = cells.find_all('td')[1].text
                apps = cells.find_all('td')[2].text
                goals = cells.find_all('td')[3].text
                own_goals = cells.find_all('td')[4].text
                substitutions_on = cells.find_all('td')[5].text
                substitutions_off = cells.find_all('td')[6].text
                yellow_card = cells.find_all('td')[7].text
                second_yellow_card = cells.find_all('td')[8].text
                red_card = cells.find_all('td')[9].text
                goals_conceded = cells.find_all('td')[10].text
                clean_sheets = cells.find_all('td')[11].text
                minutes_played = cells.find_all('td')[12].text
                

                player_overall =  {
                    'league': league,
                    'apps': 0 if apps == '-' else apps,
                    'goals': 0 if goals == '-' else goals,
                    'own_goals': 0 if own_goals == '-' else own_goals,
                    'substitutions_on': 0 if substitutions_on == '-' else substitutions_on,
                    'substitutions_off': 0 if substitutions_off == '-' else substitutions_off,
                    'yellow_card': 0 if yellow_card == '-' else yellow_card,
                    'second_yellow_card': 0 if second_yellow_card == '-' else second_yellow_card,
                    'red_card': 0 if red_card == '-' else red_card,
                    'goals_conceded': 0 if goals_conceded == '-' else goals_conceded,
                    'clean_sheets': 0 if clean_sheets == '-' else clean_sheets,
                    'minutes_played': 0 if minutes_played == '-' else minutes_played,
                }

                data.append(player_overall)
        except IndexError:
            pass

        return data