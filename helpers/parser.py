import re
from bs4 import BeautifulSoup as bs
from helpers.formater import Formater

class Parser():
    @staticmethod
    def player_head(soup):
        '''
        player_head method receives a SOUP html content and returns a dict with the player heads content

        Parameters:
            soup - A SOUP html content
        '''
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
                    formated_text = Formater.format_text(p.text)
                    data.update({formated_text[0]: formated_text[1]})

            player_status = soup.select('.dataZusatzDaten > .hauptpunkt')[0]
            if player_status:
                data.update({'player_status': player_status.text})
        except IndexError:
            pass


        if 'contract_expires' in data:
            data['contract_expires_days'] = Formater.format_contract(data['contract_expires'])

        return data


    @staticmethod
    def stats(soup, position):
        '''
        stats method receives a SOUP html content and the player position to return a dict with the player stats content

        Parameters:
            soup - A SOUP html content
            position - A string with the player position
        '''
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
        '''
        stats_line method receives a SOUP html content and returns a dict with the player stats content

        Parameters:
            soup - A SOUP html content
        '''
        data = []
        try:
            table = soup.select('.items > tbody')[0]

            for cells in table.find_all(True, {"class": re.compile("^(even|odd)$")}):
                season = cells.find_all('td')[0].text
                league = cells.find_all('td')[1].img['title'] if cells.find_all('td')[1].img else ''
                league_badge = cells.find_all('td')[1].img['src'] if cells.find_all('td')[1].img else ''
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

                club_badge = Formater.format_badge(club_badge)
                league_badge = Formater.format_badge(league_badge)
                
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
                    'minutes_goal': 0 if minutes_goal == '-' else Formater.format_minutes(minutes_goal),
                    'minutes_played': 0 if minutes_played == '-' else Formater.format_minutes(minutes_played),
                }

                data.append(stats)
        except IndexError as e:
            pass

        return data

    @staticmethod
    def stats_goalkeeper(soup):
        '''
        stats_goalkeeper method receives a SOUP html content and returns a dict with the player stats content for goalkeeper

        Parameters:
            soup - A SOUP html content
        '''
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

                club_badge = Formater.format_badge(club_badge)
                league_badge = Formater.format_badge(league_badge)

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
                    'minutes_played': 0 if minutes_played == '-' else Formater.format_minutes(minutes_played),
                }

                data.append(stats)
        except IndexError as e:
            pass

        return data

    @staticmethod
    def stats_by_club(data):
        '''
        stats_by_club method receives a dict with the player stats and returns a dict with the stats content grouped by club

        Parameters:
            data - A dict with the player stats
        '''
        stats = Formater.group_sum(['club'], data)

        return stats

    @staticmethod
    def stats_by_league(data):
        '''
        stats_by_league method receives a dict with the player stats and returns a dict with the stats content grouped by league

        Parameters:
            data - A dict with the player stats
        '''

        stats = Formater.group_sum(['league'], data)

        return stats

    @staticmethod
    def stats_by_season(data):
        '''
        stats_by_season method receives a dict with the player stats and returns a dict with the stats content grouped by season

        Parameters:
            data - A dict with the player stats
        '''

        stats = Formater.group_sum(['season'], data)

        return stats

    @staticmethod
    def current_club(current, status):
        '''
        current_club method receives a dict with the player head data and the player status to return a dict with the current club

        Parameters:
            current - A dict with the player head data
            status - A string with the player status
        '''
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
        '''
        played_clubs method receives a dict with the player stats and returns a dict with the played clubs

        Parameters:
            clubs - A dict with the player stats
        '''
        played_clubs = []
        
        for item in clubs:
            data = {
                'club': item['club'],
                'club_badge': item['club_badge'],
            }

            played_clubs.append(data)

        return Formater.remove_dupe_clubs(played_clubs)

    @staticmethod
    def played_leagues(leagues):
        '''
        played_leagues method receives a dict with the player stats and returns a dict with the played leagues

        Parameters:
            leagues - A dict with the player stats
        '''
        played_leagues = []
        
        for item in leagues:
            data = {
                'league': item['league'],
                'league_badge': item['league_badge'],
            }

            played_leagues.append(data)

        return Formater.remove_dupe_league(played_leagues)

    def add_badge_club(stats, clubs):
        '''
        add_badge_club method receives a dict with the stats by club and an another dict with the played clubs to add and the badges to the clubs

        Parameters:
            stats - A dict with the player stats by club
            clubs - A dict with the played clubs
        '''
        for item in range(0, len(stats)):
            for club in clubs:
                if stats[item]['club'] == club['club']:
                    stats[item]['club_badge'] = club['club_badge']
                    

        return stats

    def add_badge_league(stats, leagues):
        '''
        add_badge_league method receives a dict with the stats by league and an another dict with the played leagues to add and return the badges to the leagues

        Parameters:
            stats - A dict with the player stats by league
            leagues - A dict with the played leagues
        '''
        for item in range(0, len(stats)):
            for league in leagues:
                if stats[item]['league'] == league['league']:
                    stats[item]['league_badge'] = league['league_badge']
                    

        return stats

    