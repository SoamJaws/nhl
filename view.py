class View:

    def __init__(self, model):
        self.model = model
        self.pos_w    = max(1, len(str(len(self.model.player_list))))
        self.player_w = max([ len(p.name) for p in self.model.player_list ])
        self.wlr_w    = max(2, max([ len("%.2f" % round(p.wlr, 2)) for p in self.model.player_list ]))
        self.gp_w     = max(2, max([ len(str(p.gp))   for p in self.model.player_list ]))
        self.w_w      = max(1, max([ len(str(p.w))    for p in self.model.player_list ]))
        self.l_w      = max(1, max([ len(str(p.l))    for p in self.model.player_list ]))
        self.ot_w     = max(2, max([ len(str(p.ot))   for p in self.model.player_list ]))
        self.gf_w     = max(2, max([ len(str(p.gf))   for p in self.model.player_list ]))
        self.ga_w     = max(2, max([ len(str(p.ga))   for p in self.model.player_list ]))
        self.diff_w   = max(4, max([ len(str(p.diff)) for p in self.model.player_list ]))
        self.total_w  = self.pos_w + self.player_w + self.wlr_w + self.gp_w + self.w_w + self.l_w + self.ot_w + self.gf_w + self.ga_w + self.diff_w + 29

    def _get_filled_line(self, c):
        return self.format_string_line % ( c * self.pos_w
                                         , c * self.player_w
                                         , c * self.wlr_w
                                         , c * self.gp_w
                                         , c * self.w_w
                                         , c * self.l_w
                                         , c * self.ot_w
                                         , c * self.gf_w
                                         , c * self.ga_w
                                         , c * self.diff_w
                                         )

    def _get_header(self):
        rows = []
        rows.append(self._get_filled_line("-"))
        rows.append("|" + self.model.season.replace("_", " ").upper().center(self.total_w) + "|")
        rows.append(self._get_filled_line("-"))
        rows.append(self.format_string_row % ( "#"
                                             , "Player"
                                             , "WLR"
                                             , "GP"
                                             , "W"
                                             , "L"
                                             , "OT"
                                             , "GF"
                                             , "GA"
                                             , "DIFF"
                                             ))
        rows.append(self._get_filled_line("-"))
        return rows

    def _get_rows(self):
        self.format_string_row = (("| %%-%ds " + "| %%-%ds " * 9 + "|")) % ( self.pos_w
                                                                           , self.player_w
                                                                           , self.wlr_w
                                                                           , self.gp_w
                                                                           , self.w_w
                                                                           , self.l_w
                                                                           , self.ot_w
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
                                                 , player.gp
                                                 , player.w
                                                 , player.l
                                                 , player.ot
                                                 , player.gf
                                                 , player.ga
                                                 , player.diff
                                                 ))

        rows.append(self._get_filled_line("-"))
        return rows

    def print_stats(self):
        for row in self._get_rows():
            print row

    def _print_stats_html_table(self):
        print "<table>"
        print "<caption>%s</caption>" % self.model.season.replace("_", " ").upper()
        print "<tr class=\"header\">"
        print "<th>#</th>"
        print "<th>Player</th>"
        print "<th style=\"cursor:pointer;\" title=\"Win loss ratio\">WLR</th>"
        print "<th style=\"cursor:pointer;\" title=\"Games played\">GP</th>"
        print "<th style=\"cursor:pointer;\" title=\"Wins\">W</th>"
        print "<th style=\"cursor:pointer;\" title=\"Losses\">L</th>"
        print "<th style=\"cursor:pointer;\" title=\"Overtime wins\">OT</th>"
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
            print "<th>%d</th>"   % player.gp
            print "<th>%d</th>"   % player.w
            print "<th>%d</th>"   % player.l
            print "<th>%d</th>"   % player.ot
            print "<th>%d</th>"   % player.gf
            print "<th>%d</th>"   % player.ga
            print "<th>%d</th>"   % player.diff
            print "</tr>"
        print "</table>"

    def _print_match_count_html_table(self):
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

    def _print_suggestions_html_table(self):
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
            least_played_player, player_least_played_games, leader = self._suggest_matches(player, [])
            print "<tr class=\"player\">"
            print "<th>%s</th>" % player.name
            print "<th>%s</th>" % least_played_player
            print "<th>%s</th>" % player_least_played_games
            print "<th>%s</th>" % leader
            print "</tr>"
        print "</table>"

    def print_html(self):
        print "<!DOCTYPE html>"
        print "<html>"
        print "<head><title>NHL STEGEN 3.0</title><link rel=\"stylesheet\" href=\"styles.css\"></head>"
        print "<body>"
        self._print_stats_html_table()
        print "<br>"
        self._print_match_count_html_table()
        print "<br>"
        self._print_suggestions_html_table()
        print "</body>"
        print "</html>"
