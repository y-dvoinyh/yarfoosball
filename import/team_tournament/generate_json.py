import csv
from datetime import datetime
import json

tournament_dict = {
    "_id": "d148379f-b750-4ca8-b285-09fae971dd14",
    "name": "Тензор лига (осень-зима 2023)",
    "date_start": "2023-09-01",
    "date_end": "2024-03-15",
    "players": [],
    "teams": [],
    "competitions": []
}

# Игроки
with open(f'players.csv', 'r', encoding='utf-8') as players_file:
    reader = csv.reader(players_file, delimiter=' ', quotechar='|')
    for num, row in enumerate(reader):
        if num == 0:
            continue
        _id, first_name, last_name = row[0].split(',')
        tournament_dict["players"].append({
            "_id": _id,
            "name": f'{first_name} {last_name}'
        })

# Команды
with open(f'teams.csv', 'r', encoding='utf-8') as teams_file:
    reader = csv.reader(teams_file, delimiter=',', quotechar='|')
    for num, row in enumerate(reader):
        if num == 0:
            continue
        _id, name, *players = row
        tournament_dict['teams'].append({
            "_id": _id,
            "name": name,
            "players": players
        })

# Матчи
with open(f'matches.csv', 'r', encoding='utf-8') as matches_file:
    reader = csv.reader(matches_file, delimiter=',', quotechar='|')
    competitions_dict = dict()
    for num, row in enumerate(reader):
        if num == 0:
            continue
        (
            competition_uuid,
            competition_date,
            competition_name,
            team1_name,
            team1_uuid,
            team2_name,
            team2_uuid,
            match_uuid,
            match_team1_uuid,
            match_team1_players,
            match_team2_uuid,
            match_team2_players,
            set_uuid,
            first_team_scope,
            second_team_scope
        ) = row

        competition = competitions_dict.get(competition_uuid)
        if competition is None:
            competition = {
                '_id': competition_uuid,
                'name': competition_name,
                'start_datetime': int(datetime.strptime(competition_date, "%Y-%m-%d").timestamp()),
                'table_name': None,
                'ferst_team': match_team1_uuid,
                'second_team': match_team2_uuid,
                'video_lincs': [],
                'matches': []
            }
            competitions_dict[competition_uuid] = competition
            tournament_dict['competitions'].append(competition)

        players1 = match_team1_players.split(';')
        players2 = match_team2_players.split(';')

        num_match = len(competition['matches']) + 1
        name = 'S' if len(players1) == 1 else 'D'

        len_matches = len([m for m in competition['matches'] if name in m['name']])

        name += str(len_matches + 1)

        match = {
            '_id': match_uuid,
            'name': name,
            'first_team': {
                '_id': match_team1_uuid,
                'players': players1
            },
            'second_team': {
                '_id': match_team2_uuid,
                'players': players2
            },
            'sets': [
                {
                    '_id': set_uuid,
                    'score': [first_team_scope, second_team_scope]
                }
            ]
        }
        competition['matches'].append(match)

with open('tensor_2023_export_team_tournament.json', 'w', encoding='utf-8') as file:
    json.dump(tournament_dict, file, ensure_ascii=False)