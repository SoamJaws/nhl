import os
import json
from datetime import date
import calendar
import operator

class Player:

    def __init__(self, name):
        self.name = name
        self.gp = 0
        self.w = 0
        self.l = 0
        self.ot = 0
        self.gf = 0
        self.ga = 0
        self.match_counts = {}

    def __cmp__(self, other):
        for prop in [ "wlr" , "diff" , "gp" , "ot" ]:
            result = cmp(getattr(self, prop), getattr(other, prop))
            if result != 0:
                return result
        return 0

    @property
    def wlr(self):
        wins = self.w + self.ot * 0.5
        return wins/float(self.l) if self.l > 0 else float('inf')

    @property
    def diff(self):
        return self.gf - self.ga


class Model:

    def __init__(self):
        today = date.today()
        self.games_file = "games.json" 
        self.season = "%d_%s" % (today.year, calendar.month_abbr[today.month])

        if os.path.exists(self.games_file):
            with open(self.games_file) as data_file:
                    self.data = json.load(data_file)
        else:
            self.data = []
        self._load_players()

    def _load_players(self):
        # "GP"   : Games played
        # "WLR"  : Win/lose ratio
        # "W"    : Wins
        # "L"    : Losses
        # "OT"   : OT/Shootout wins
        # "GF"   : Goals for
        # "GA"   : Goals against
        # "DIFF" : Goal difference
        self.player_dict = {}
        for entry in self.data[self.season]:
            home = entry["home"]
            away = entry["away"]
            home_score = entry[home]
            away_score = entry[away]
            OT = entry["OT"]

            if not home in self.player_dict:
                self.player_dict[home] = Player(home)
            if not away in self.player_dict:
                self.player_dict[away] = Player(away)

            home_player = self.player_dict[home]
            away_player = self.player_dict[away]

            home_player.gp += 1
            home_player.gf += home_score
            home_player.ga += away_score

            away_player.gp += 1
            away_player.gf += away_score
            away_player.ga += home_score

            if not away in home_player.match_counts:
                home_player.match_counts[away] = 1
            else:
                home_player.match_counts[away] += 1
            if not home in away_player.match_counts:
                away_player.match_counts[home] = 1
            else:
                away_player.match_counts[home] += 1

            if home_score > away_score:
                away_player.l += 1
                if OT:
                    home_player.ot += 1
                else:
                    home_player.w += 1
            elif home_score < away_score:
                home_player.l += 1
                if OT:
                    away_player.ot += 1
                else:
                    away_player.w += 1
        for name1, player in self.player_dict.iteritems():
            for name2 in self.player_dict:
                if not (name1 == name2 or name2 in player.match_counts):
                    player.match_counts[name2] = 0
        self.player_list = list(self.player_dict.values())
        self.player_list.sort(reverse=True)

    def add(self, home, away, home_score, away_score, overtime):
        if not self.season in self.data:
            self.data[self.season] = []
        self.data[self.season].append({ "home" : home
                                      , "away" : away
                                      , home   : home_score
                                      , away   : away_score
                                      , "OT"   : overtime
                                      })

    def get_player(self, player_name):
        return self.player_dict[player_name]

    def get_least_played_player(self, player_name, excluded_players=[]):
        player = self.player_dict[player_name]
        filtered_match_counts = { pn: mc for (pn, mc) in player.match_counts.iteritems() if pn not in excluded_players }
        least_played_player_name = min(filtered_match_counts.iteritems(), key=operator.itemgetter(1))[0]
        return self.player_dict[least_played_player_name]

    def get_player_least_played_games(self, excluded_players=[]):
        filtered_players = { pn: p for (pn, p) in self.player_dict.iteritems() if pn not in excluded_players }
        player_least_played_games_name = min(filtered_players.values(), key=operator.attrgetter('gp')).name
        return self.player_dict[player_least_played_games_name]

    def get_leader(self, excluded_players=[]):
        filtered_players = { pn: p for (pn, p) in self.player_dict.iteritems() if pn not in excluded_players }
        leader_name = max(filtered_players.values()).name
        return self.player_dict[leader_name]

    def save(self):
        with open(self.games_file, 'w') as data_file:
            json.dump(self.data, data_file, indent=4, separators=(',', ': '))