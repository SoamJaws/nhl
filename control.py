class Control:

    def __init__(self, model, console_view, html_view):
        self.model = model
        self.console_view = console_view
        self.html_view = html_view

    def run_command(self, command, args):
        getattr(self, command)(args)

    def add(self, args):
        self.model.add(args.home, args.away, args.home_score, args.away_score, args.overtime)
        self.console_view.print_game_addition(args.home, args.away, args.home_score, args.away_score, args.overtime)

    def suggest(self, args):
        self.console_view.print_suggestions(args.player, args.exclude)

    def stats(self, args):
        self.console_view.print_stats()

    def html(self, args):
        self.html_view.print_html()
