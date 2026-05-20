from scripts.cleaner.utils import ModCleaner


class ReadmeCleaner(ModCleaner):
    shield_game_mapping = {
        "BGII": "BG2",
        "BG1": "BG",
        "IWD1": "IWD",
        "BG2ToB": "BG2",
        "EasyTutu": "Tutu",
        "BG2-ToB": "BG2",
        "IWD-in-BG2": "",
        "PsT": "PST",
        "PsTEE": "PSTEE",
        "BG1EE": "BGEE",
    }

    def clean_authors(self):
        return [
            cleaned_author
            for author in super().clean_authors()
            if (cleaned_author := author.strip("*"))
        ]

    def clean_games(self):
        self.data["games"] = [
            self.shield_game_mapping.get(game, game) for game in self.data["games"]
        ]
        return super().clean_games()
