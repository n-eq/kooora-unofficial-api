import requests
import json
import time
from pprint import pprint
from datetime import datetime

class Match:
    def __init__(self, id, date, league, team1, team2):
        self.id = id
        self.date = date
        self.league = league
        self.team1 = team1
        self.team2 = team2

    def __str__(self):
        return ""


# class Player:
#     def __init__(self, id, name, team, number, position, footedness, weigth, height, nationality, sport, national_team=None, national_number=0):
#         # TODO
#         self.id = id
#         self.name = name
#         self.team = team
#         self.national_team = national_team
#         self.number = number
#         self.national_number = national_number
#         self.position = position
#         self.footedness = footedness
#         self.weight = weight
#         self.height = height
#         self.nationality = nationality
#         self.sport = sport

class Sport:
    def __init__(self, id, has_teams = True, name = ""):
        self.id = id
        self.has_teams = has_teams
        self.name = name

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def __str__(self):
        return "Sport {%s (%d), has teams: %s}" % (self.name, self.id, "yes" if self.has_teams else "no")

class Team:
    def __init__(self, id, name, country, sport_id):
        self.name = name
        self.id = id
        self.name = name
        self.country_key = country
        self.sport = Sport(sport_id)

    def __str__(self):
        return "Team {name: \"%s\", id: %d, sport: %s}" % (self.name, self.id, self.sport)
    
    def get_players(self):
        # TODO
        pass

    def get_matches(self, date = None):
        # example w/ date http://kapi.kooora.ws/api/teamMatches?tz=1.0&date=2019-12-20&id=1291&rand=1581853560
        # curl -X GET -H "Host:kapi.kooora.ws" -H "Connection:Keep-Alive" 
        # -H "Accept-Encoding:gzip" -H "User-Agent:okhttp/3.12.1"
        # "http://kapi.kooora.ws/api/teamMatches?tz=2.0&date=null&id=895&rand=1585587150"
        if (date == None):
            date = "null"

        # move to a dedicated function (maybe even independent from the class)
        ts = time.time()
        tz = (datetime.fromtimestamp(ts) -
              datetime.utcfromtimestamp(ts)).total_seconds() / 3600

        req = "http://kapi.kooora.ws/api/teamMatches?tz=%.1f&date=%s&id=%d" % (tz, date, self.id)
        r = requests.get(req)

        res = []
        for elt in r.json():
            matches = elt["Matches"][0]
            t1 = Team(matches["Team1"]["Id"], matches["Team1"]["Name"], 
                    matches["Team1"]["Sport"]["Id"], matches["Team1"]["Country"]["Key"])
            t2 = Team(matches["Team2"]["Id"], matches["Team2"]["Name"], 
                    matches["Team2"]["Sport"]["Id"], matches["Team2"]["Country"]["Key"])
            res.append(Match(matches["Id"], elt["Date"], matches['League'], t1, t2))

        return res

    def get_news(self):
        # curl -X GET -H "Host:kapi.kooora.ws" -H "Connection:Keep-Alive" 
        # -H "Accept-Encoding:gzip" -H "User-Agent:okhttp/3.12.1" 
        # "http://kapi.kooora.ws/api/newsAfter?id=913678&sport=0&team=1291&rand=1585587150"
        pass

class Kooora:
    def get_search(self, keyword):
        """
        public enum SearchTabType {
        VIDEO(25),
        PHOTOS(11),
        PLAYERS(3),
        TEAMS(1),
        TOURNS(0),
        NEWS(20);

        TODO
        """
        return requests.get('http://kapi.kooora.ws/api/search?keyWord=' + keyword + '&type=1')


# tests
api = Kooora()
res = api.get_search('الكوكب المراكشي')
e = res.json()["Entries"]["Team"]["Data"][0]
t = Team(e['Id'], e['Name'], e['Country']['Key'], e['Sport']['Id'])
print(t)

matches = t.get_matches()
for match in matches:
    print([match.date, match.id])

## returns :
"""
{'Date': '2020-03-08T00:00:00',
  'Matches': [{'CurrentMinute': 0,
               'Id': 1894543,
               'Kickoff': '2020-03-08T15:01:00',
               'League': {'Country': 'MA',
                          'Flags': 0,
                          'Id': 17866,
                          'IsArchived': False,
                          'Logo': 'https://img.kooora.com/?i=kooora_logo/africa/maroc/botola2.gif',
                          'Sport': 0,
                          'StageTitles': None,
                          'Title': 'البطولة المغربية الإحترافية 2 (متوقفة '
                                   'حاليا لوقت غير محدد)',
                          'Year': 2019,
                          'Year2': 2020},
               'Period': 'f',
               'PeriodScores': {'HT': [1, 0]},
               'Score1': 1,
               'Score1InGame': 0,
               'Score2': 0,
               'Score2InGame': 0,
               'Seed1': 0,
               'Seed2': 0,
               'Serving': 0,
               'Stage': 1,
               'Status': 0,
               'Team1': {'Class': 0,
                         'Country': {'Key': 'MA', 'Value': 'المغرب'},
                         'Id': 1293,
                         'Logo': 'https://img.kooora.com/?i=omar_a/maroc/botola/2020-01-07_064235.jpg',
                         'Name': 'النادي القنيطري',
                         'Sport': {'HasTeams': True,
                                   'Id': 0,
                                   'Name': 'كرة القدم'},
                         'TempTeam': False},
               'Team2': {'Class': 0,
                         'Country': {'Key': 'MA', 'Value': 'المغرب'},
                         'Id': 1291,
                         'Logo': 'https://img.kooora.com/?i=00$mohammed/kawkab%20marrakech%20.jpg',
                         'Name': 'الكوكب المراكشي',
                         'Sport': {'HasTeams': True,
                                   'Id': 0,
                                   'Name': 'كرة القدم'},
                         'TempTeam': False}}],
  'Stages': None},
"""
