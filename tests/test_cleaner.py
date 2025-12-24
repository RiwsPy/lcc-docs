from datetime import datetime

from scripts.cleaner.ini import IniCleaner
from scripts.cleaner.readme import ReadmeCleaner
from scripts.cleaner.utils import ModCleaner


class TestModCleaner:
    def test_name(self):
        data = {"name": "Name"}
        expected_value = "Name"

        assert ModCleaner(data).clean_name() == expected_value

    def test_name_with_arobase(self):
        data = {"name": "@mail.fr"}
        expected_value = ""

        assert ModCleaner(data).clean_name() == expected_value

    def test_name_with_bracket(self):
        data = {"name": "toto (coco)"}
        expected_value = "toto"

        assert ModCleaner(data).clean_name() == expected_value

    def test_name_with_bracket2(self):
        data = {"name": "toto [coco]"}
        expected_value = "toto"

        assert ModCleaner(data).clean_name() == expected_value

    def test_games(self):
        # TODO: mock
        data = {"games": ["eet"]}
        expected_value = ["EET"]

        assert ModCleaner(data).clean_games() == expected_value

    def test_games_duplicate(self):
        # TODO: mock
        data = {"games": ["eet", "Eet", "eet"]}
        expected_value = ["EET"]

        assert ModCleaner(data).clean_games() == expected_value

    def test_games_unknown(self):
        # TODO: mock
        data = {"games": ["_"]}
        expected_value = list()

        assert ModCleaner(data).clean_games() == expected_value

    def test_authors(self):
        data = {"authors": ["Toto"]}
        expected_value = ["Toto"]

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_team(self):
        data = {"authors": ["Toto & Titi"]}
        expected_value = ["Toto", "Titi"]

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_team2(self):
        data = {"authors": ["Toto and Titi"]}
        expected_value = ["Toto", "Titi"]

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_team3(self):
        data = {"authors": ["Toto et Titi"]}
        expected_value = ["Toto", "Titi"]

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_team4(self):
        data = {"authors": ["Toto, Titi"]}
        expected_value = ["Toto", "Titi"]

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_email(self):
        data = {"authors": ["to.to@mail.com"]}
        expected_value = ["to.to"]

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_with_email(self):
        data = {"authors": ["Toto (to.to@mail.com)"]}
        expected_value = ["Toto"]

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_url(self):
        data = {"authors": ["http://to.com"]}
        expected_value = list()

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_at(self):
        data = {"authors": ["Toto, at https://toto.com"]}
        expected_value = ["Toto"]

        assert ModCleaner(data).clean_authors() == expected_value

    def test_authors_exclude_others(self):
        data = {"authors": ["others"]}
        expected_value = list()

        assert ModCleaner(data).clean_authors() == expected_value

    def test_clean_languages(self):
        data = {"languages": ["english"]}
        expected_value = ["en"]

        assert ModCleaner(data).clean_languages() == expected_value

    def test_clean_languages_iso(self):
        data = {"languages": ["en_US"]}
        expected_value = ["en"]

        assert ModCleaner(data).clean_languages() == expected_value

    def test_clean_languages_with_translator(self):
        data = {"languages": ["english (by Toto)"]}
        expected_value = ["en"]

        assert ModCleaner(data).clean_languages() == expected_value

    def test_clean_languages_with_path(self):
        data = {"languages": ["lang/brazilian"]}
        expected_value = ["br"]

        assert ModCleaner(data).clean_languages() == expected_value

    def test_clean_languages_with_tra_path(self):
        data = {"languages": ["mod/tra"]}
        expected_value = list()

        assert ModCleaner(data).clean_languages() == expected_value

    def test_clean_languages_sorted(self):
        data = {"languages": ["en", "br"]}
        expected_value = ["br", "en"]

        assert ModCleaner(data).clean_languages() == expected_value

    def test_clean_languages_duplicate(self):
        data = {"languages": ["en", "en_US"]}
        expected_value = ["en"]

        assert ModCleaner(data).clean_languages() == expected_value

    def test_clean_last_update(self):
        data = {"last_update": datetime(2042, 12, 1)}
        expected_value = "2042-12"

        assert ModCleaner(data).clean_last_update() == expected_value

    def test_clean_last_update_error(self):
        data = {"last_update": ""}
        expected_value = ""

        assert ModCleaner(data).clean_last_update() == expected_value

    def test_clean_tp2(self):
        data = {"tp2": "toto"}
        expected_value = "toto"

        assert ModCleaner(data).clean_tp2() == expected_value

    def test_clean_tp2_with_tp2(self):
        data = {"tp2": "toto.tp2"}
        expected_value = "toto"

        assert ModCleaner(data).clean_tp2() == expected_value

    def test_clean_tp2_with_setup(self):
        data = {"tp2": "setup-toto.tp2"}
        expected_value = "toto"
        assert ModCleaner(data).clean_tp2() == expected_value

    def test_clean_tp2_with_setup_case(self):
        data = {"tp2": "SetuP-toto.tP2"}
        expected_value = "toto"
        assert ModCleaner(data).clean_tp2() == expected_value


class TestIniCleaner:
    def test_categories(self):
        data = {"categories": ["Category"]}
        expected_value = ["Category"]

        assert IniCleaner(data).clean_categories() == expected_value

    def test_categories_map(self, mocker):
        mocker.patch.object(
            IniCleaner,
            "category_mapping",
            {"Category": "OtherCategory"},
        )

        data = {"categories": ["Category"]}
        expected_value = ["OtherCategory"]

        assert IniCleaner(data).clean_categories() == expected_value

    def test_categories_empty(self):
        data = {"categories": [""]}
        expected_value = list()

        assert IniCleaner(data).clean_categories() == expected_value

    def test_categories_overwrite(self):
        data = {"categories": ["Overwrite"]}
        expected_value = list()

        assert IniCleaner(data).clean_categories() == expected_value


class TestReadmeCleaner:
    def test_authors(self):
        data = {"authors": ["Plop"]}
        expected_value = ["Plop"]

        assert ReadmeCleaner(data).clean_authors() == expected_value

    def test_authors_splat(self):
        data = {"authors": ["Plop**"]}
        expected_value = ["Plop"]

        assert ReadmeCleaner(data).clean_authors() == expected_value

    def test_authors_fullsplat(self):
        data = {"authors": ["***"]}
        expected_value = list()

        assert ReadmeCleaner(data).clean_authors() == expected_value

    def test_games(self):
        data = {"games": ["BGEE"]}
        expected_value = ["BGEE"]

        assert ReadmeCleaner(data).clean_games() == expected_value

    def test_games_unknown(self):
        data = {"games": ["_"]}
        expected_value = list()

        assert ReadmeCleaner(data).clean_games() == expected_value

    def test_games_map(self, mocker):
        mocker.patch.object(
            ReadmeCleaner,
            "shield_game_mapping",
            {"Game1": "BG2EE"},
        )

        data = {"games": ["Game1"]}
        expected_value = ["BG2EE"]

        assert ReadmeCleaner(data).clean_games() == expected_value
