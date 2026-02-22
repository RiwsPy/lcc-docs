from scripts.manager import IniManager, ReadmeManager, Tp2Manager


class TestIniManager:
    def test_metadata_header(self):
        content = """
# ini section header is required to avoid false detection
[Metadata]
test_is_ok"""

        expected_value = "test_is_ok"

        assert IniManager(content).content_clean == expected_value

    def test_clean_comment(self):
        content = """
# ini section header is required to avoid false detection
test_is_ok"""

        expected_value = "\ntest_is_ok"

        assert IniManager.clean_comments(content) == expected_value

    def test_empty_data(self):
        content = ""
        expected_value = dict()

        assert IniManager(content).json == expected_value

    def test_json(self):
        content = """
        Key1 = Value1
        Key2 = Value2
        Key3 = Value3
        """
        expected_value = {
            "Key1": "Value1",
            "Key2": "Value2",
            "Key3": "Value3",
        }

        assert IniManager(content).json == expected_value

    def test_key_with_one_space(self):
        key_name = "Key"
        content = f"{key_name} = Value"
        expected_value = "Value"

        assert IniManager(content).json[key_name] == expected_value

    def test_key_with_spaces(self):
        key_name = "Key"
        content = f"{key_name}   =  Value"
        expected_value = "Value"

        assert IniManager(content).json[key_name] == expected_value

    def test_key_without_space(self):
        key_name = "Key"
        content = f"{key_name}=Value"
        expected_value = "Value"

        assert IniManager(content).json[key_name] == expected_value

    def test_authors(self):
        content = "Author = toto"
        expected_value = ["toto"]

        assert IniManager(content).get_authors() == expected_value

    def test_urls1(self):
        content = "Homepage = https://1.com"
        expected_value = ["https://1.com"]

        assert IniManager(content).get_urls() == expected_value

    def test_urls2(self):
        content = "Forum = https://1.com"
        expected_value = ["https://1.com"]

        assert IniManager(content).get_urls() == expected_value

    def test_urls3(self):
        content = "Download = https://1.com"
        expected_value = ["https://1.com"]

        assert IniManager(content).get_urls() == expected_value

    def test_urls4(self):
        content = """
        Homepage = https://2.com
        Forum = https://3.com
        Download = https://1.com
        """
        expected_value = ["https://1.com", "https://2.com", "https://3.com"]
        value = IniManager(content).get_urls()

        assert set(value) == set(expected_value)
        assert len(value) == len(expected_value)

    def test_name(self):
        content = "Name = Mod name"
        expected_value = "Mod name"

        assert IniManager(content).get_name() == expected_value

    def test_name_with_space(self):
        content = "Name =  Mod name  "
        expected_value = "Mod name"

        assert IniManager(content).get_name() == expected_value

    def test_tp2(self):
        content = "Tp2 = Toto"
        expected_value = ""

        assert IniManager(content).get_tp2() == expected_value

    def test_tp2_overwrite(self):
        content = "Type = Overwrite"
        expected_value = "non-weidu"

        assert IniManager(content).get_tp2() == expected_value

    def test_categories(self):
        content = "Type = Type"
        expected_value = ["Type"]

        assert IniManager(content).get_categories() == expected_value

    def test_after(self):
        content = "After = ab, ac, DC"
        expected_value = ["ab", "ac", "dc"]

        assert IniManager(content).get_after() == expected_value

    def test_after_with_empty(self):
        content = "After = ab, ac, DC, "
        expected_value = ["ab", "ac", "dc"]

        assert IniManager(content).get_after() == expected_value


class TestReadmeManager:
    def test_is_html(self):
        content = "# Plop"
        expected_value = False

        assert ReadmeManager(content).is_html is expected_value

    def test_is_html_and_it_is(self):
        content = "<!DOCTYPE html>Plop"
        expected_value = True

        assert ReadmeManager(content).is_html is expected_value

    def test_name_md(self):
        content = "# Plop"
        expected_value = "Plop"

        assert ReadmeManager(content).get_name() == expected_value

    def test_name_md2(self):
        content = "## Plop"
        expected_value = ""

        assert ReadmeManager(content).get_name() == expected_value

    def test_name_bad_md1(self):
        content = "#Plop"
        expected_value = ""

        assert ReadmeManager(content).get_name() == expected_value

    def test_name_html(self):
        content = "<!DOCTYPE html><h1>Plop</h1>"
        expected_value = "Plop"

        assert ReadmeManager(content).get_name() == expected_value

    def test_name_hybrid(self):
        content = "<h1>Plop</h1>"
        expected_value = "Plop"

        assert ReadmeManager(content).get_name() == expected_value

    def test_name_html_multiline(self):
        content = """<h1>Plop
</h1>"""
        expected_value = "Plop\n"

        assert ReadmeManager(content).get_name() == expected_value

    def test_name_false_md(self):
        content = "<!DOCTYPE html># Plop"
        expected_value = ""

        assert ReadmeManager(content).get_name() == expected_value

    def test_authors_md(self):
        content = "**Autor**: Toto"
        expected_value = ["Toto"]
        assert ReadmeManager(content).get_authors() == expected_value

    def test_authors_md_with_splat(self):
        content = "**Author**: **Toto**"
        expected_value = ["Toto"]
        assert ReadmeManager(content).get_authors() == expected_value

    def test_authors_md_original(self):
        content = "Original Autor: Toto"
        expected_value = ["Toto"]
        assert ReadmeManager(content).get_authors() == expected_value

    def test_authors_html_original(self):
        content = "<!DOCTYPE html><strong>Autor: Toto</strong>"
        expected_value = ["Toto"]
        assert ReadmeManager(content).get_authors() == expected_value

    def test_authors_empty(self):
        content = ""
        expected_value = []
        assert ReadmeManager(content).get_authors() == expected_value

    def test_languages_static(self):
        content = "![Language](https://img.shields.io/static/v1?label=language&message=msg&color=limegreen)"
        expected_value = ["msg"]

        assert sorted(ReadmeManager(content).get_languages()) == sorted(expected_value)

    def test_languages_badge(self):
        # TODO: cas concret à trouver
        content = "![Language](https://img.shields.io/badge/language-aa|ab-)"
        expected_value = ["aa", "ab"]

        assert sorted(ReadmeManager(content).get_languages()) == sorted(expected_value)

    def test_games_static(self):
        content = "![Language](https://img.shields.io/static/v1?label=supported games&message=msg&color=limegreen)"
        expected_value = ["msg"]

        assert sorted(ReadmeManager(content).get_games()) == sorted(expected_value)

    def test_games_badge(self):
        # TODO: cas concret à trouver
        content = "![Language](https://img.shields.io/badge/games-aa|ab-)"
        expected_value = ["aa", "ab"]

        assert sorted(ReadmeManager(content).get_games()) == sorted(expected_value)


class TestTp2Manager:
    def test_comment_line(self):
        content = "toto // comment"
        expected_value = "toto"

        assert Tp2Manager.clean_comments(content) == expected_value

    def test_comment_line_multi(self):
        content = """// comment1
toto
// comment2"""
        expected_value = "\ntoto"

        assert Tp2Manager.clean_comments(content) == expected_value

    def test_comment_block(self):
        content = """/* comment1
toto
comment2 */"""
        expected_value = ""

        assert Tp2Manager.clean_comments(content) == expected_value

    def test_comment_url(self):
        content = "toto https://comment.com"
        expected_value = content

        assert Tp2Manager.clean_comments(content) == expected_value

    def test_authors(self):
        content = "AUTHOR ~Toto~"
        expected_value = ["Toto"]

        assert Tp2Manager(content).get_authors() == expected_value

    def test_authors2(self):
        content = 'AUTHOR "Toto"'
        expected_value = ["Toto"]

        assert Tp2Manager(content).get_authors() == expected_value

    def test_authors_typo(self):
        content = "VAUTHOR ~Toto~"
        expected_value = []

        assert Tp2Manager(content).get_authors() == expected_value

    def test_languages(self):
        content = """
LANGUAGE ~English~
~en_US~
~Modname/lang/en_US/setup.tra~
"""
        expected_value = ["English", "en_US"]

        assert Tp2Manager(content).get_languages() == expected_value

    # FIXME
    #     def test_languages_multiline(self):
    #         content = """
    # LANGUAGE ~English
    # (oupsy)~
    # ~en_US~
    # ~Modname/lang/en_US/setup.tra~
    # """
    #         expected_value = ["English", "en_US"]

    #         assert Tp2Manager(content).get_languages() == expected_value

    def test_games(self):
        content = "ACTION_IF GAME_INCLUDES ~SoD~ BEGIN"
        expected_value = ["SoD"]

        assert Tp2Manager(content).get_games() == expected_value

    def test_games_multiple(self):
        content = "ACTION_IF GAME_INCLUDES ~SoD bgee~ BEGIN"
        expected_value = ["SoD", "bgee"]

        assert Tp2Manager(content).get_games() == expected_value

    def test_games_not(self):
        content = "ACTION_IF NOT GAME_INCLUDES ~SoD~ BEGIN"
        expected_value = []

        assert Tp2Manager(content).get_games() == expected_value

    def test_games_not2(self):
        content = "ACTION_IF !GAME_INCLUDES ~SoD~ BEGIN"
        expected_value = []

        assert Tp2Manager(content).get_games() == expected_value

    def test_version(self):
        content = "VERSION ~1.2.3~"
        expected_value = "1.2.3"

        assert Tp2Manager(content).get_version() == expected_value

    def test_version2(self):
        content = 'VERSION "v1.2"'
        expected_value = "v1.2"

        assert Tp2Manager(content).get_version() == expected_value

    def test_translator(self):
        content = """
LANGUAGE ~English~
~en_US (Toto)~
~Modname/lang/en_US/setup.tra~
"""
        expected_value = ["en_US (Toto)"]

        assert Tp2Manager(content).get_translators() == expected_value

    def test_translator_without_brackets(self):
        content = """
LANGUAGE ~English~
~en_US by Toto~
~Modname/lang/en_US/setup.tra~
"""
        expected_value = ["en_US by Toto"]

        assert Tp2Manager(content).get_translators() == expected_value

    def test_translator_incorrect(self):
        content = """
LANGUAGE ~English~
~en_US Toto~
~Modname/lang/en_US/setup.tra~
"""
        expected_value = []

        assert Tp2Manager(content).get_translators() == expected_value
