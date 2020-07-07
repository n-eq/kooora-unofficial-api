from enum import Enum

import requests
from datetime import datetime

from .utils import get_tz, KAPI_BASE_URL

class SearchType(Enum):
    TOURNAMENT = 0
    TEAM = 1
    PLAYER = 3
    PHOTO = 11
    NEWS = 20
    VIDEO = 25

class Kooora:
    def get_feed(self):
        print("TODO")

    def search(self, keyword, *search_types):
        req = KAPI_BASE_URL + "/search?keyWord=%s" % keyword
        for t in search_types:
            req += "&type=%d" % t.value
        j = requests.get(req).json()

        res = {}
        for key in j['Entries'].keys():
            if key == 'Team':
                res['teams'] = []
                for t in j['Entries']['Team']['Data']:
                    res['teams'].append(Team.from_search_json(t))
            if key == 'Player':
                res['players'] = []
                for p in j['Entries']['Player']['Data']:
                    res['players'].append(Player.from_search_json(p))
            if key == 'Album':
                res['photos'] = []
                for p in j['Entries']['Album']['Data']:
                    res['photos'].append(Album.from_search_json(p))
            if key == 'League':
                res['leagues'] = []
                for p in j['Entries']['League']['Data']:
                    res['leagues'].append(League.from_search_json(p))
        return res

    def search_team(self, keyword):
        return self.search(keyword, SearchType.TEAM)['teams']

    def search_league(self, keyword):
        return self.search(keyword, SearchType.TOURNAMENT)['leagues']

    def search_player(self, keyword):
        return self.search(keyword, SearchType.PLAYER)['players']

    def search_photo(self, keyword):
        return self.search(keyword, SearchType.PHOTO)['photos']

#     def search_news(self, keyword):
#         return self.search(keyword, [SearchType.NEWS])
# 
#     def search_video(self, keyword):
#         return self.search(keyword, [SearchType.VIDEO])

class Album:
    def __init__(self, id = None, album_id = None, url = None,
                 added_on = None, title = None, description = None):
        self.id = id
        self.album_id = album_id
        self.url = url
        self.added_on = added_on
        self.title = title
        self.description = description

    @staticmethod
    def from_search_json(j):
        return Album(j['Id'], j['AlbumId'], j['Url'], j['AddedOn'], j['Title'], j['Description'])

    def to_dict(self):
        return {
            'id': self.id,
            'album_id': self.album_id,
            'url': self.url,
            'added_on': added_on,
            'title': self.title,
            'description': self.description
        }

class Sport:
    def __init__(self, id = None, has_teams = None, name = None):
        self.id = id
        self.has_teams = has_teams or True
        self.name = name or ''

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def __str__(self):
        return "Sport {%s (%d), has teams: %s}" % (self.name, self.id, "yes" if self.has_teams else "no")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'has_teams': "yes" if self.has_teams else "no"
        }

class Player:
    # TODO : add support for other sports and national teams integration
    def __init__(self, id = None, flags = None, name = None, nationality = None,
                 position = None, team_id = None, number = None, national_number = None):
        self.id = id
        self.flags = flags
        self.name = name
        self.nationality = nationality
        self.position = position
        self.team = Team(team_id)
        self.number = number
        self.national_number = national_number

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    @staticmethod
    def from_id(id):
        res = requests.get(KAPI_BASE_URL + "/players?id=%s" % str(id)).json()
        if res:
            p = Player(res['Id'], res['Flags'], res['Name'], res['Nationality']['Value'], 
                    res['Position'], res['Team']['Id'], res['Number'])
            return p
        else:
            print("Could not find player id %d" % id)
            return None

    @staticmethod
    def from_search_json(j):
        # There are no 'Position' and 'Team ID' fields in the search results
        return Player(j['Id'], j['Flags'], j['Name'], j['Nationality']['Value'], 
                   0, -1, j['Number'], j['NationalNumber'])

    def __str__(self):
        return "[%d] %s" % (self.id, self.name)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'flags': self.flags,
            'nationality': self.nationality,
            'team': self.team.get_id(),
            'number': self.number
        }

class Team:
    def __init__(self, id = None, name = None, country = None, sport_id = None, players = []):
        self.name = name
        self.id = id
        self.country = country
        self.sport = Sport(sport_id)
        self.players = players

    def get_players(self):
        return self.players

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def set_players(self, l):
        self.players = l

    # date format : %Y-%m-%d
    def get_matches(self, date = 'null'):
        tz = get_tz()

        # TODO : check correct date format (d = datetime.strptime(date, '%Y-%m-%d'))
        req = KAPI_BASE_URL + "/teamMatches?tz=%.1f&date=%s&id=%d" % (tz, date, self.id)
        r = requests.get(req).json()

        matches = []
        for elt in r:
            matches.append(Match.from_json_search(elt['Matches'][0]))
        return matches

    def next_match(self):
        now = datetime.now()
        matches = self.get_matches()
        for m in matches:
            if datetime.strptime(m.get_kickoff(), '%Y-%m-%dT%H:%M:%S') > now:
                return m
        print("No match was found")
        return None

    def next_matches(self):
        res = []
        now = datetime.now()
        matches = self.get_matches()
        for m in matches:
            if datetime.strptime(m.get_kickoff(), '%Y-%m-%dT%H:%M:%S') > now:
                res.append(m)
        return res

    def add_player(self, player):
        if player in self.players:
            pass
        self.players.append(player)

    def get_news(self):
        return requests.get(KAPI_BASE_URL + "/teamNews?id=%s" % str(self.id)).json()

    @staticmethod
    def from_id(id):
        res = requests.get(KAPI_BASE_URL + "/teams?id=%s" % str(id))
        res_json = res.json()
        if res_json:
            t = Team()
            t.init_from_json(res_json)
            return t
        else:
            print("Team %s was not found" % id)
            return None

    def read_players_from_json(self, j):
        for elt in j:
            player = Player.from_id(elt['Id'])
            if player:
                self.add_player(player)

    def init_from_json(self, j):
        try:
            self.id = j['Id']
            self.logo = j['Logo']
            self.name = j['Name']
            self.sport = Sport(j['Sport']['Id'])
            self.country = j['Country']['Value']
            self.cls = j['Class']
            self.temp_team = j['TempTeam']
            self.established = j['Established']
            self.group_photo = j['GroupPhoto']
            self.type = j['Type']
            self.flags = j['Flags']
            self.read_players_from_json(j['Players'])
        except Exception as e:
            print("There was an exception initializing team from json: %s" % e)

    @staticmethod
    def from_search_json(j):
        # This is a reduced version, no players are included
        t = Team(j['Id'], j['Name'], j['Country']['Value'], j['Sport']['Id'])
        return t

    def to_dict(self):
        d = {
            'id': self.id,
            'name': self.name,
            'country': self.country or "",
            'sport': self.sport.to_dict()
        }
        d['players'] = [p.to_dict() for p in self.players]

        return d

    def __str__(self):
        return "%s(%d)" % (self.name, self.id)

class Match:
    def __init__(self, id = None, kickoff = None, league_id = None, team1 = None, team2 = None):
        self.id = id
        self.kickoff = kickoff
        self.league_id = league_id
        self.team1 = Team.from_id(team1)
        self.team2 = Team.from_id(team2)

    def __init__(self):
        self.id = -1

    # TODO : produce a better output
    def get_stats(self):
        req = KAPI_BASE_URL + "/matchStats?id=%s" % str(self.id)
        r = requests.get(req)
        return r.json()

    def get_kickoff(self):
        return self.kickoff

    @staticmethod
    def from_id(id):
        r = KAPI_BASE_URL + "/matches?id=%d" % id
        res = requests.get(r).json()
        return Match.from_json_search(res)

    @staticmethod
    def from_json_search(j):
        m = Match()
        m.id = j['Id']
        m.league_id = j['League']['Id']
        m.team1 = Team.from_search_json(j['Team1'])
        m.team2 = Team.from_search_json(j['Team2'])
        m.kickoff = j['Kickoff']
        m.status = j['Status']
        m.scores = [j['Score1'], j['Score2']]
        m.period = j['Period']
        m.period_scores = j['PeriodScores']
        m.curr_min = j['CurrentMinute']
        return m

    def to_dict(self):
        return {
            "id": self.id,
            "league": self.league_id,
            "kickoff": self.kickoff,
            "team1": self.team1.to_dict(),
            "team2": self.team2.to_dict(),
            "status": self.status,
            "scores": self.scores,
            "period": self.period,
            "period_scores": self.period_scores,
            "current_minute": self.curr_min
        }

    def __str__(self):
        return "(%d) %s vs %s %s" % (self.id, self.kickoff, self.team1, self.team2)

class League:
    def __init__(self, id = None, title = '', flags = None, sport = None, years = None):
        self.id = id
        self.title = title
        self.flags = flags
        self.sport = sport
        self.years = years or []

    def __init__(self):
        self.id = -1

    def get_title(self):
        return self.title

    def get_years(self):
        return self.years

    def get_sport(self):
        return self.sport

    def get_teams(self):
        r = requests.get(KAPI_BASE_URL + "/teams?league=%s" % str(self.id)).json()

        teams = []
        for e in r['Data']:
            # TODO : rename from_search_json to init_from_league[search?]
            teams.append(Team.from_search_json(e))

        return teams

    # TODO : implement paging
    def get_news(self):
        r = requests.get(KAPI_BASE_URL + "/leagueNews?id=%d" % self.id).json()
        return r

    @staticmethod
    def from_search_json(j):
        l = League()
        l.id = j['Id']
        l.logo = j['Logo']
        l.title = j['Title']
        l.flags = j['Flags']
        l.years = [j['Year'], j['Year2']]
        l.country = j['Country']
        l.archived = j['IsArchived']
        l.sport = j['Sport']

        return l

    @staticmethod
    def from_id(id):
        r = requests.get(KAPI_BASE_URL + "/leagues?id=%d" % id).json()
        return League.from_search_json(r)


    def get_matches(self, date = 'null', by_stage = True):
        req = KAPI_BASE_URL + "/LeagueMatches/%d/?date=%s&bystage=%s" % (self.id, date, "true" if by_stage else "false")
        r = requests.get(req).json()

        # For League matches, the resulting json is structured as follows:
        # every elemnent of the 'root' list consists of a 'day' date regrouping
        # all the matches played/due to be played that day.
        res = []
        for elt in r:
            for stage in elt['Stages']:
                for match in stage['Matches']:
                    m = Match.from_json_search(match)
                    res.append(m)
        return res

    def get_next_matches(self):
        # TODO : use get_matches and keep 'future' matches only
        return []

    def get_table(self):
        req = KAPI_BASE_URL + "/LeagueTable/%d" % self.id
        r = requests.get(req).json()

        res = []
        for elt in r['Entries']:
            res.append(elt)
        return res

    def get_top_scorers(self):
        req = KAPI_BASE_URL + "/scorers/%d" % self.id
        r = requests.get(req).json()

        res = []
        for elt in r['Scorers']:
            res.append({'goals': elt['Goals'], 'player': Player.from_search_json(elt['Player'])})
        return res

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'years': '%d/%d' % (self.years[0], self.years[1]),
            'country': self.country,
            'sport': self.sport
        }

    def __str__(self):
        return "(%d) %s %d/%d" % (self.id, self.title, self.years[0], self.years[1])

