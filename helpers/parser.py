from bs4 import BeautifulSoup as bs
import re
import itertools
import operator
from collections import defaultdict
import pandas as pd
import numpy as np
import calendar
from datetime import datetime

class Parser():
    @staticmethod
    def format_text(text):
        regex = re.compile(r'[\n\r\t]')
        text = regex.sub('', text)

        splited = text.split(":")
        key = splited[0]
        value = splited[1]
        value = value.strip()

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
        elif key == 'Caps/Goals':
            key = 'international_performance'
            splited_value = value.split("/")
            value = {
                "apps": splited_value[0],
                "goals": splited_value[1],
            }
        elif key == 'Date of death':
            key = 'data_death'
            value = Parser.format_date(value)
        elif key == 'Date of birth/Age':
            key = 'birth'
            value = Parser.format_date(value)


        return key, value
    
    @staticmethod
    def player_head(soup):
        try:
            data = {}
            profile = soup.select('.dataContent > .dataBottom > .dataDaten')
            profile_image = soup.select('.dataBild > img')[0]['src']
            player = soup.select('.dataMain > .dataTop > .dataName > h1')[0].text
            profile_size = range(len(profile))

            data.update({'name': player})
            data.update({'profile_image': profile_image})

            for profile_index in range(len(profile_size)):
                if profile_index == 0:
                    items_flag = profile[profile_index].find_all(True, {"class": re.compile("^(flaggenrahmen)$")})
                    for index in range(len(items_flag)):
                        if index == 0:
                            data.update({'birth_country': items_flag[index]['title']})
                for p in profile[profile_index].find_all('p'):
                    formated_text = Parser.format_text(p.text)
                    data.update({formated_text[0]: formated_text[1]})

            player_status = soup.select('.dataZusatzDaten > .hauptpunkt')[0]
            if player_status:
                data.update({'player_status': player_status.text})
        except IndexError:
            pass


        if 'contract_expires' in data:
            data['contract_expires_days'] = Parser.format_contract(data['contract_expires'])

        return data


    @staticmethod
    def stats(soup, position):
        data = []
        try:
            if position == "Goalkeeper":
                return Parser.stats_goalkeeper(soup)
            else:
                return Parser.stats_line(soup)

        except IndexError:
            pass

    @staticmethod
    def stats_line(soup):
        data = []
        try:
            table = soup.select('.items > tbody')[0]

            for cells in table.find_all(True, {"class": re.compile("^(even|odd)$")}):
                season = cells.find_all('td')[0].text
                league = cells.find_all('td')[1].img['title']
                league_badge = cells.find_all('td')[1].img['src']
                club = cells.find_all('td')[3].a.img['alt']
                club_badge = cells.find_all('td')[3].a.img['src']
                squads = cells.find_all('td')[4].text
                apps = cells.find_all('td')[5].text
                ppg = cells.find_all('td')[6].text
                goals = cells.find_all('td')[7].text
                assists = cells.find_all('td')[8].text
                own_goal = cells.find_all('td')[9].text
                substitutions_on = cells.find_all('td')[10].text
                substitutions_off = cells.find_all('td')[11].text
                yellow_card = cells.find_all('td')[12].text
                second_yellow_card = cells.find_all('td')[13].text
                red_card = cells.find_all('td')[14].text
                penalty_goal = cells.find_all('td')[15].text
                minutes_goal = cells.find_all('td')[16].text
                minutes_played = cells.find_all('td')[17].text

                club_badge = Parser.format_badge(club_badge)
                
                stats = {
                    'season': season,
                    'league': league,
                    'league_badge': league_badge,
                    'club': club,
                    'club_badge': club_badge,
                    'squads': 0 if squads == '-' else int(squads),
                    'apps': 0 if apps == '-' else int(apps),
                    'ppg': 0 if ppg == '-' else ppg,
                    'goals': 0 if goals == '-' else int(goals),
                    'assists': 0 if assists == '-' else int(assists),
                    'own_goal': 0 if own_goal == '-' else int(own_goal),
                    'substitutions_on': 0 if substitutions_on == '-' else int(substitutions_on),
                    'substitutions_off': 0 if substitutions_off == '-' else int(substitutions_off),
                    'yellow_card': 0 if yellow_card == '-' else int(yellow_card),
                    'second_yellow_card': 0 if second_yellow_card == '-' else int(second_yellow_card),
                    'red_card': 0 if red_card == '-' else int(red_card),
                    'penalty_goal': 0 if penalty_goal == '-' else int(penalty_goal),
                    'minutes_goal': 0 if minutes_goal == '-' else Parser.format_minutes(minutes_goal),
                    'minutes_played': 0 if minutes_played == '-' else Parser.format_minutes(minutes_played),
                }

                data.append(stats)
        except IndexError as e:
            pass

        return data

    @staticmethod
    def stats_goalkeeper(soup):
        data = []
        try:
            table = soup.select('.items > tbody')[0]

            for cells in table.find_all(True, {"class": re.compile("^(even|odd)$")}):
                season = cells.find_all('td')[0].text
                league = cells.find_all('td')[1].img['title']
                league_badge = cells.find_all('td')[1].img['src']
                club = cells.find_all('td')[3].a.img['alt']
                club_badge = cells.find_all('td')[3].a.img['src']
                squads = cells.find_all('td')[4].text
                apps = cells.find_all('td')[5].text
                ppg = cells.find_all('td')[6].text
                goals = cells.find_all('td')[7].text
                assists = cells.find_all('td')[8].text
                substitutions_on = cells.find_all('td')[9].text
                substitutions_off = cells.find_all('td')[10].text
                yellow_card = cells.find_all('td')[11].text
                second_yellow_card = cells.find_all('td')[12].text
                red_card = cells.find_all('td')[13].text
                goals_conceded = cells.find_all('td')[14].text
                clean_sheets = cells.find_all('td')[15].text
                minutes_played = cells.find_all('td')[16].text

                club_badge = Parser.format_badge(club_badge)

                stats = {
                    'season': season,
                    'league': league,
                    'league_badge': league_badge,
                    'club': club,
                    'club_badge': club_badge,
                    'squads': 0 if squads == '-' else int(squads),
                    'apps': 0 if apps == '-' else int(apps),
                    'ppg': 0 if ppg == '-' else ppg,
                    'goals': 0 if goals == '-' else int(goals),
                    'assists': 0 if assists == '-' else int(assists),
                    'substitutions_on': 0 if substitutions_on == '-' else int(substitutions_on),
                    'substitutions_off': 0 if substitutions_off == '-' else int(substitutions_off),
                    'yellow_card': 0 if yellow_card == '-' else int(yellow_card),
                    'second_yellow_card': 0 if second_yellow_card == '-' else int(second_yellow_card),
                    'red_card': 0 if red_card == '-' else int(red_card),
                    'goals_conceded': 0 if goals_conceded == '-' else int(goals_conceded),
                    'clean_sheets': 0 if clean_sheets == '-' else int(clean_sheets),
                    'minutes_played': 0 if minutes_played == '-' else Parser.format_minutes(minutes_played),
                }

                data.append(stats)
        except IndexError as e:
            pass

        return data

    @staticmethod
    def stats_by_club(data):
        stats = Parser.group_sum(['club'], data)

        return stats

    @staticmethod
    def stats_by_league(data):

        stats = Parser.group_sum(['league'], data)

        return stats

    @staticmethod
    def stats_by_season(data):

        stats = Parser.group_sum(['season'], data)

        return stats

    @staticmethod
    def current_club(current, status):
        if status == 'Retired':
            data = {}
        else:
            data = {
                'club': current['club'],
                'club_badge': current['club_badge'],
            }

        return data

    @staticmethod
    def played_clubs(clubs):
        played_clubs = []
        
        for item in clubs:
            data = {
                'club': item['club'],
                'club_badge': item['club_badge'],
            }

            played_clubs.append(data)

        return Parser.remove_dupe_dicts(played_clubs)

    def group_sum(filter_key, data):
        df = pd.DataFrame.from_dict(data)

        df = df.groupby(filter_key).sum(numeric_only=True).reset_index()

        dd = defaultdict(list)
        response = df.to_dict('records', into=dd)
        
        return response

    def format_minutes(minutes):
        minutes_played = minutes.replace("'", "")
        minutes_played = minutes_played.replace(".", "")
        minutes_played = int(minutes_played)

        return minutes_played

    def alphabet_position(text):
        nums = [str(ord(x) - 96) for x in text.lower() if x >= 'a' and x <= 'z']
        return "".join(nums)

    def format_date(value):
        if re.match("[a-zA-Z][a-z][a-z][\s][0-9][,][\s][0-9][0-9][0-9][0-9][(][0-9][0-9][)]+", value):
            return value[: -4]
        elif re.match("[a-zA-Z][a-z][a-z][\s][0-9][0-9][,][\s][0-9][0-9][0-9][0-9][(][0-9][0-9][)]+", value):
            return value[: -4]
        elif re.match("[0-9][0-9][.][0-9][0-9].[0-9][0-9][0-9][0-9][\W][(][0-9][0-9][)]+", value):
            value = value[: -5]
            splited_value = value.split(".")
            month = int(splited_value[1])
            month = calendar.month_abbr[month]

            date = f"{month} {splited_value[1]}, {splited_value[2]}"
            
            return date

        return value

    def format_contract(date):
        formated_date = datetime.strptime(date, '%b %d, %Y')
        today = datetime.today()

        remaining_days = formated_date - today

        return remaining_days.days


    def remove_dupe_dicts(data):
        try:
            aux = []
            b = []
            for item in data:
                if item['club'] not in aux:
                    b.append({
                        "club": item['club'],
                        "club_badge": item['club_badge']
                    })
                    aux.append(item['club'])
        except:
            pass
        return b

    def add_badge(stats, clubs):
        for item in range(0, len(stats)):
            for club in clubs:
                if stats[item]['club'] == club['club']:
                    stats[item]['club_badge'] = club['club_badge']
                    

        return stats

    def format_badge(badge):
        club_badge = badge.replace('tiny', 'normal')
        splited_club_badge = club_badge.split('_')

        return splited_club_badge[0] + '.png'