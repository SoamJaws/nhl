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
