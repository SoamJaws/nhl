import os
import json
from datetime import date
import calendar
import operator

class Player:

    MAIN_CMP_FACTOR = "wlr"

    def __init__(self, name):
        self.name = name
        self.gp = 0
        self.w = 0
        self.l = 0
        self.otw = 0
        self.otl = 0
        self.gf = 0
        self.ga = 0
        self.win_counts = {}
        self.loss_counts = {}

    def __cmp__(self, other):
        for prop in [ Player.MAIN_CMP_FACTOR , "diff" , "gp" , "ot" ]:
            result = cmp(getattr(self, prop), getattr(other, prop))
            if result != 0:
                return result
        return 0

    @property
    def wlr(self):
        wins = (self.w - self.otw) + self.otw * 0.5
        return wins/float(self.l) if self.l > 0 else float('inf')

    @property
    def ppg(self):
        totalgames = self.w + self.l
        return (self.w * 2 + self.otl) / float(totalgames)

    @property
    def diff(self):
        return self.gf - self.ga

    @property
    def match_counts(self):
        return dict(self.win_counts.items() + self.loss_counts.items() + [(k, self.win_counts[k] + self.loss_counts[k]) for k in set(self.loss_counts) & set(self.win_counts)])


class Model:

    def __init__(self):
        today = date.today()
        self.games_file = "games.json" 
        self.current_season = "%d_%s" % (today.year, calendar.month_abbr[today.month])

        if os.path.exists(self.games_file):
            with open(self.games_file) as data_file:
                    self.data = json.load(data_file)
        else:
            self.data = []

        if not self.current_season in self.data:
            self.data[self.current_season] = []

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
        self.player_dicts = {}
        self.player_wlr_lists = {}
        self.player_ppg_lists = {}
        for season, data in self.data.iteritems():
            self.player_dicts[season] = {}
            self.player_wlr_lists[season] = []
            self.player_ppg_lists[season] = []
            for entry in self.data[season]:
                home = entry["home"]
                away = entry["away"]
                home_score = entry[home]
                away_score = entry[away]
                OT = entry["OT"]

                if not home in self.player_dicts[season]:
                    self.player_dicts[season][home] = Player(home)
                if not away in self.player_dicts[season]:
                    self.player_dicts[season][away] = Player(away)

                home_player = self.player_dicts[season][home]
                away_player = self.player_dicts[season][away]

                home_player.gp += 1
                home_player.gf += home_score
                home_player.ga += away_score

                away_player.gp += 1
                away_player.gf += away_score
                away_player.ga += home_score

                if home_score > away_score:
                    away_player.l += 1
                    home_player.w += 1
                    if OT:
                        home_player.otw += 1
                        away_player.otl += 1
                    if not away in home_player.win_counts:
                        home_player.win_counts[away] = 1
                    else:
                        home_player.win_counts[away] += 1
                    if not home in away_player.loss_counts:
                        away_player.loss_counts[home] = 1
                    else:
                        away_player.loss_counts[home] += 1
                elif home_score < away_score:
                    home_player.l += 1
                    away_player.w += 1
                    if OT:
                        away_player.otw += 1
                        home_player.otl += 1
                    if not away in home_player.loss_counts:
                        home_player.loss_counts[away] = 1
                    else:
                        home_player.loss_counts[away] += 1
                    if not home in away_player.win_counts:
                        away_player.win_counts[home] = 1
                    else:
                        away_player.win_counts[home] += 1
            for name1, player in self.player_dicts[season].iteritems():
                for name2 in self.player_dicts[season]:
                    if not (name1 == name2 or name2 in player.win_counts):
                        player.win_counts[name2] = 0
                    if not (name1 == name2 or name2 in player.loss_counts):
                        player.loss_counts[name2] = 0

            Player.MAIN_CMP_FACTOR = "wlr"
            self.player_wlr_lists[season] = list(self.player_dicts[season].values())
            self.player_wlr_lists[season].sort(reverse=True)

            Player.MAIN_CMP_FACTOR = "ppg"
            self.player_ppg_lists[season] = list(self.player_dicts[season].values())
            self.player_ppg_lists[season].sort(reverse=True)

    def add(self, home, away, home_score, away_score, overtime):
        if not self.current_season in self.data:
            self.data[self.current_season] = []
        self.data[self.current_season].append({ "home" : home
                                      , "away" : away
                                      , home   : home_score
                                      , away   : away_score
                                      , "OT"   : overtime
                                      })

    def get_player(self, player_name, season=None):
        if not season:
            season = self.current_season
        return self.player_dicts[season][player_name]

    def get_least_played_player(self, player_name, excluded_players=[], season=None):
        if not season:
            season = self.current_season
        player = self.player_dicts[season][player_name]
        filtered_match_counts = { pn: mc for (pn, mc) in player.match_counts.iteritems() if pn not in excluded_players }
        least_played_player_name = min(filtered_match_counts.iteritems(), key=operator.itemgetter(1))[0]
        return self.player_dicts[season][least_played_player_name]

    def get_player_least_played_games(self, excluded_players, season=None):
        if not season:
            season = self.current_season
        filtered_players = { pn: p for (pn, p) in self.player_dicts[season].iteritems() if pn not in excluded_players }
        player_least_played_games_name = min(filtered_players.values(), key=operator.attrgetter('gp')).name
        return self.player_dicts[season][player_least_played_games_name]

    def get_wlr_leader(self, excluded_players=[], season=None):
        Player.MAIN_CMP_FACTOR = "wlr"
        return self._get_leader(excluded_players, season)

    def get_ppg_leader(self, excluded_players=[], season=None):
        Player.MAIN_CMP_FACTOR = "ppg"
        return self._get_leader(excluded_players, season)

    def _get_leader(self, excluded_players, season):
        if not season:
            season = self.current_season
        filtered_players = { pn: p for (pn, p) in self.player_dicts[season].iteritems() if pn not in excluded_players }
        leader_name = max(filtered_players.values()).name
        return self.player_dicts[season][leader_name]

    def save(self):
        with open(self.games_file, 'w') as data_file:
            json.dump(self.data, data_file, indent=4, separators=(',', ': '))

    @property
    def player_dict(self):
        return self.player_dicts[self.current_season]

    @property
    def player_wlr_list(self):
        return self.player_wlr_lists[self.current_season]

    @property
    def player_ppg_list(self):
        return self.player_ppg_lists[self.current_season]

    @property
    def seasons(self):
        return [ season for season, data in self.data.iteritems() ]
