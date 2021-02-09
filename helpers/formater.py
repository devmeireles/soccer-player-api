import re
from datetime import datetime
import pandas as pd
from collections import defaultdict

class Formater():
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
            value = Formater.format_date(value)
        elif key == 'Date of birth/Age':
            key = 'birth'
            value = Formater.format_date(value)


        return key, value

    @staticmethod
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

    @staticmethod
    def format_badge(badge):
        club_badge = badge.replace('tiny', 'normal')
        splited_club_badge = club_badge.split('_')

        return splited_club_badge[0] + '.png'

    @staticmethod
    def format_contract(date):
        formated_date = datetime.strptime(date, '%b %d, %Y')
        today = datetime.today()

        remaining_days = formated_date - today

        return remaining_days.days

    @staticmethod
    def format_minutes(minutes):
        minutes_played = minutes.replace("'", "")
        minutes_played = minutes_played.replace(".", "")
        minutes_played = int(minutes_played)

        return minutes_played

    @staticmethod
    def remove_dupe_league(data):
        try:
            aux = []
            b = []
            for item in data:
                if item['league'] not in aux:
                    b.append({
                        "league": item['league'],
                        "league_badge": item['league_badge']
                    })
                    aux.append(item['league'])
        except:
            pass
        return b

    @staticmethod
    def remove_dupe_clubs(data):
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

    @staticmethod
    def group_sum(filter_key, data):
        df = pd.DataFrame.from_dict(data)

        df = df.groupby(filter_key).sum(numeric_only=True).reset_index()

        dd = defaultdict(list)
        response = df.to_dict('records', into=dd)
        
        return response