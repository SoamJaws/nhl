class ConsoleView:

    def __init__(self, model):
        self.model = model
        self.pos_w    = max(1, len(str(len(self.model.player_list)))) if self.model.player_list else 0
        self.player_w = max([ len(p.name) for p in self.model.player_list ]) if self.model.player_list else 0
        self.wlr_w    = max(2, max([ len("%.2f" % round(p.wlr, 2)) for p in self.model.player_list ])) if self.model.player_list else 0
        self.ppg_w    = max(2, max([ len("%.2f" % round(p.ppg, 2)) for p in self.model.player_list ])) if self.model.player_list else 0
        self.gp_w     = max(2, max([ len(str(p.gp))   for p in self.model.player_list ])) if self.model.player_list else 0
        self.w_w      = max(1, max([ len(str(p.w))    for p in self.model.player_list ])) if self.model.player_list else 0
        self.l_w      = max(1, max([ len(str(p.l))    for p in self.model.player_list ])) if self.model.player_list else 0
        self.otw_w    = max(3, max([ len(str(p.otw))  for p in self.model.player_list ])) if self.model.player_list else 0
        self.otl_w    = max(3, max([ len(str(p.otl))  for p in self.model.player_list ])) if self.model.player_list else 0
        self.gf_w     = max(2, max([ len(str(p.gf))   for p in self.model.player_list ])) if self.model.player_list else 0
        self.ga_w     = max(2, max([ len(str(p.ga))   for p in self.model.player_list ])) if self.model.player_list else 0
        self.diff_w   = max(4, max([ len(str(p.diff)) for p in self.model.player_list ])) if self.model.player_list else 0
        self.total_w  = self.pos_w + self.player_w + self.wlr_w + self.ppg_w + self.gp_w + self.w_w + self.l_w + self.otw_w + self.otl_w + self.gf_w + self.ga_w + self.diff_w + 35

    def _get_filled_line(self, c):
        return self.format_string_line % ( c * self.pos_w
                                         , c * self.player_w
                                         , c * self.wlr_w
                                         , c * self.ppg_w
                                         , c * self.gp_w
                                         , c * self.w_w
                                         , c * self.l_w
                                         , c * self.otw_w
                                         , c * self.otl_w
                                         , c * self.gf_w
                                         , c * self.ga_w
                                         , c * self.diff_w
                                         )

    def _get_header(self):
        rows = []
        rows.append(self._get_filled_line("-"))
        rows.append("|" + self.model.current_season.replace("_", " ").upper().center(self.total_w) + "|")
        rows.append(self._get_filled_line("-"))
        rows.append(self.format_string_row % ( "#"
                                             , "Player"
                                             , "WLR"
                                             , "PPG"
                                             , "GP"
                                             , "W"
                                             , "L"
                                             , "OTW"
                                             , "OTL"
                                             , "GF"
                                             , "GA"
                                             , "DIFF"
                                             ))
        rows.append(self._get_filled_line("-"))
        return rows

    def _get_rows(self):
        self.format_string_row = (("| %%-%ds " + "| %%-%ds " * 11 + "|")) % ( self.pos_w
                                                                            , self.player_w
                                                                            , self.wlr_w
                                                                            , self.ppg_w
                                                                            , self.gp_w
                                                                            , self.w_w
                                                                            , self.l_w
                                                                            , self.otw_w
                                                                            , self.otl_w
                                                                            , self.gf_w
                                                                            , self.ga_w
                                                                            , self.diff_w
                                                                            )
        self.format_string_line = ("|" + self.format_string_row[1:-1].replace(" ", "-").replace("|", "-") + "|")

        rows = []
        rows.extend(self._get_header())

        position = 0
        for player in self.model.player_list:
            position += 1
            rows.append(self.format_string_row % ( position
                                                 , player.name
                                                 , "%.2f" % player.wlr
                                                 , "%.2f" % player.ppg
                                                 , player.gp
                                                 , player.w - player.otw
                                                 , player.l - player.otl
                                                 , player.otw
                                                 , player.otl
                                                 , player.gf
                                                 , player.ga
                                                 , player.diff
                                                 ))

        rows.append(self._get_filled_line("-"))
        return rows

    def print_stats(self):
        for row in self._get_rows():
            print row

    def print_suggestions(self, player_name, excluded_players):
        excluded_players.append(player_name)
        least_played_player = self.model.get_least_played_player(player_name, excluded_players)
        player_least_played_games = self.model.get_player_least_played_games(excluded_players)
        leader = self.model.get_leader(excluded_players)
        player = self.model.get_player(player_name)

        print "Least played player            - %s, %s" % (least_played_player.name, "away" if least_played_player > player else "home")
        print "Player with least played games - %s, %s" % (player_least_played_games.name, "away" if player_least_played_games > player else "home")
        print "Season leader                  - %s, away" % leader.name

    def print_game_addition(self, home, away, home_score, away_score, overtime):
        overtime_print = ", OT" if overtime else ""
        print "Successfully added game \"%s @ %s: %d-%d%s\"" % ( away
                                                               , home
                                                               , away_score
                                                               , home_score
                                                               , overtime_print
                                                               )

class HtmlView():

    def __init__(self, model):
        self.model = model

    def _print_stats_table(self):
        print "<table>"
        print "<caption>%s</caption>" % self.model.current_season.replace("_", " ").upper()
        print "<tr class=\"header\">"
        print "<th>#</th>"
        print "<th>Player</th>"
        print "<th style=\"cursor:pointer;\" title=\"Win loss ratio\">WLR</th>"
        print "<th style=\"cursor:pointer;\" title=\"Points per game\">PPG</th>"
        print "<th style=\"cursor:pointer;\" title=\"Games played\">GP</th>"
        print "<th style=\"cursor:pointer;\" title=\"Wins\">W</th>"
        print "<th style=\"cursor:pointer;\" title=\"Losses\">L</th>"
        print "<th style=\"cursor:pointer;\" title=\"Overtime wins\">OTW</th>"
        print "<th style=\"cursor:pointer;\" title=\"Overtime losses\">OTL</th>"
        print "<th style=\"cursor:pointer;\" title=\"Goals for\">GF</th>"
        print "<th style=\"cursor:pointer;\" title=\"Goals against\">GA</th>"
        print "<th style=\"cursor:pointer;\" title=\"Goal difference\">DIFF</th>"
        print "</tr>"

        position = 0
        for player in self.model.player_list:
            position += 1
            print "<tr class=\"player\">"
            print "<th>%d</th>"   % position
            print "<th>%s</th>"   % player.name
            print "<th>%.2f</th>" % player.wlr
            print "<th>%.2f</th>" % player.ppg
            print "<th>%d</th>"   % player.gp
            print "<th>%d</th>"   % (player.w - player.otw)
            print "<th>%d</th>"   % (player.l - player.otl)
            print "<th>%d</th>"   % player.otw
            print "<th>%d</th>"   % player.otl
            print "<th>%d</th>"   % player.gf
            print "<th>%d</th>"   % player.ga
            print "<th>%d</th>"   % player.diff
            print "</tr>"
        print "</table>"

    def _print_champions_table(self):
        print "<table>"
        print "<caption>CHAMPIONS</caption>"
        print "<tr class=\"header\">"
        print "<th>Season</th>"
        print "<th>Player</th>"
        print "<th style=\"cursor:pointer;\" title=\"Win loss ratio\">WLR</th>"
        print "<th style=\"cursor:pointer;\" title=\"Points per game\">PPG</th>"
        print "<th style=\"cursor:pointer;\" title=\"Games played\">GP</th>"
        print "<th style=\"cursor:pointer;\" title=\"Wins\">W</th>"
        print "<th style=\"cursor:pointer;\" title=\"Losses\">L</th>"
        print "<th style=\"cursor:pointer;\" title=\"Overtime wins\">OTW</th>"
        print "<th style=\"cursor:pointer;\" title=\"Overtime losses\">OTL</th>"
        print "<th style=\"cursor:pointer;\" title=\"Goals for\">GF</th>"
        print "<th style=\"cursor:pointer;\" title=\"Goals against\">GA</th>"
        print "<th style=\"cursor:pointer;\" title=\"Goal difference\">DIFF</th>"
        print "</tr>"

        for season in [ season for season in self.model.seasons if season != self.model.current_season ]:
            player = self.model.get_leader(season=season)
            print "<tr class=\"player\">"
            print "<th>%s</th>"   % season.replace("_", " ").upper()
            print "<th>%s</th>"   % player.name
            print "<th>%.2f</th>" % player.wlr
            print "<th>%.2f</th>" % player.ppg
            print "<th>%d</th>"   % player.gp
            print "<th>%d</th>"   % (player.w - player.otw)
            print "<th>%d</th>"   % (player.l - player.otl)
            print "<th>%d</th>"   % player.otw
            print "<th>%d</th>"   % player.otl
            print "<th>%d</th>"   % player.gf
            print "<th>%d</th>"   % player.ga
            print "<th>%d</th>"   % player.diff
            print "</tr>"
        print "</table>"

    def _print_match_count_table(self):
        print "<table>"
        print "<caption>GAMES PLAYED</caption>"
        print "<tr class=\"header\">"
        print "<th>Player</th>"
        print "<th>Player</th>"
        print "<th>Games played</th>"
        print "</tr>"

        printed = {}
        for player in self.model.player_list:
            printed[player.name] = []
            for away_player, count in player.match_counts.iteritems():
                if away_player in printed and not player.name in printed[away_player]:
                    print "<tr class=\"player\">"
                    print "<th>%s</th>" % player.name
                    print "<th>%s</th>" % away_player
                    print "<th>%d</th>" % count
                    print "</tr>"
                    printed[player.name].append(away_player)
        print "</table>"

    def _print_suggestions_table(self):
        print "<table>"
        print "<caption>MATCH SUGGESTIONS</caption>"
        print "<tr class=\"header\">"
        print "<th>Player</th>"
        print "<th style=\"cursor:pointer;\" title=\"Least played player\">LPP</th>"
        print "<th style=\"cursor:pointer;\" title=\"Least played games\">LPG</th>"
        print "<th>Leader</th>"
        print "</tr>"

        printed = {}
        for player_name, player in self.model.player_dict.iteritems():
            least_played_player = self.model.get_least_played_player(player_name)
            player_least_played_games = self.model.get_player_least_played_games([player_name])
            leader = self.model.get_leader([player_name])
            print "<tr class=\"player\">"
            print "<th>%s</th>" % player.name
            print "<th>%s</th>" % least_played_player.name
            print "<th>%s</th>" % player_least_played_games.name
            print "<th>%s</th>" % leader.name
            print "</tr>"
        print "</table>"

    def print_html(self):
        print "<!DOCTYPE html>"
        print "<html>"
        print "<head><title>NHL STEGEN 3.0</title><link rel=\"stylesheet\" href=\"styles.css\"></head>"
        print "<body>"
        self._print_stats_table()
        print "<br>"
        self._print_match_count_table()
        print "<br>"
        self._print_suggestions_table()
        print "<br>"
        self._print_champions_table()
        print "</body>"
        print "</html>"
