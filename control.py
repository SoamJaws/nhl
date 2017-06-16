class Control:

    def __init__(self, model, view):
        self.model = model
        self.view = view

    def run_command(self, command, args):
        getattr(self, command)(args)

    def add(self, args):
        model.add(args.home, args.away, args.home_score, args.away_score, args.overtime)
        view.print_game_addition(args.home, args.away, args.home_score, args.away_score, args.overtime)

    def suggest(self, args):
        self.view.print_suggestions(args.player, args.exclude)

    def stats(self, args):
        self.view.print_stats()

    def html(self, args):
        self.view.print_html()
