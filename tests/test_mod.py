from pydantic import ValidationError
import pytest

from i18n import LanguageConfig
from models.mod import Mod, ModStatus
from settings import TranslationStateEnum

mod_kwargs = {
    "id": 1,
    "name": "mod name",
    "categories": [],
    "urls": ["https://toto.com"],
    "description": "description",
    "team": [],
    "languages": [],
    "games": [],
    "notes": [],
    "compatibilities": dict(),
    "safe": 2,
    "translation_state": TranslationStateEnum.AUTO,
    "status": ModStatus.ACTIVE,
    "authors": [],
    "last_update": "",
    "tp2": "",
}


def create_mod_instance(**kwargs):
    return Mod(**(mod_kwargs | kwargs))


@pytest.fixture
def mod(**kwargs):
    return create_mod_instance(**kwargs)


class TestMod:
    def test_mod_base(self):
        create_mod_instance()

    def test_mod_last_update_validator_format(self):
        with pytest.raises(ValidationError):
            create_mod_instance(last_update="25-12")

    def test_mod_last_update_validator_date(self):
        with pytest.raises(ValidationError):
            create_mod_instance(last_update="2025-24")

    def test_mod_translation_state_auto1(self):
        mod = create_mod_instance(translation_state=TranslationStateEnum.AUTO, languages=list())
        expected_value = TranslationStateEnum.TODO

        assert mod.translation_state_auto == expected_value

    def test_mod_translation_state_auto2(self):
        mod = create_mod_instance(translation_state=TranslationStateEnum.AUTO, languages=["en"])
        expected_value = TranslationStateEnum.NO

        assert mod.translation_state_auto == expected_value

        expected_value = TranslationStateEnum.YES

        with LanguageConfig().switch_language("en"):
            assert mod.translation_state_auto == expected_value

    def test_mod_translation_state_auto3(self):
        mod = create_mod_instance(translation_state=TranslationStateEnum.YES)
        expected_value = TranslationStateEnum.YES

        assert mod.translation_state_auto == expected_value

    def test_mod_is_weidu(self):
        mod = create_mod_instance(tp2="toto")
        expected_value = True

        assert mod.is_weidu is expected_value

    def test_mod_is_weidu2(self):
        mod = create_mod_instance(tp2="non-weidu")
        expected_value = False

        assert mod.is_weidu is expected_value

    def test_mod_get_urls(self, mod):
        expected_value = mod.urls

        assert mod.get_urls() == expected_value

    def test_mod_get_urls_missing(self):
        mod = create_mod_instance(urls=["http://toto.com"], status=ModStatus.MISSING)
        expected_value = list()

        assert mod.get_urls() == expected_value

    def test_mod__convert_quote_base(self, mod):
        source_value = "Convert nothing."

        assert mod._convert_quote(source_value) == source_value

    def test_mod__convert_quote_convert(self, mod):
        source_value = "Convert `quote`."
        expected_value = 'Convert <span class="quote">quote</span>.'

        assert mod._convert_quote(source_value) == expected_value

    def test_mod__convert_pipe_convert(self, mod):
        source_value = "Pipe|Pipe"
        expected_value = "Pipe<br/>Pipe"

        assert mod._convert_pipe(source_value) == expected_value

    def test_mod_internal_link(self):
        mod = create_mod_instance(id=1, name="Toto")
        source_value = "[[1]]"
        expected_value = '<a href="#m1">Toto</a>'

        assert mod._convert_link(source_value, mod_id_to_name={1: "Toto"}) == expected_value

    def test_mod_internal_link_str_type(self):
        mod = create_mod_instance(id=1, name="Toto")
        source_value = "[[Toto]]"
        expected_value = "[[Toto]]"

        assert mod._convert_link(source_value) == expected_value

    def test_mod_internal_link_multiple(self):
        mod = create_mod_instance(id=1, name="Toto")
        source_value = "[[1]] some text [[1]]."
        expected_value = '<a href="#m1">Toto</a> some text <a href="#m1">Toto</a>.'

        assert mod._convert_link(source_value, mod_id_to_name={1: "Toto"}) == expected_value

    def test_mod_internal_link_no_mod_id_to_name(self):
        mod = create_mod_instance(id=1, name="Toto")
        source_value = "[[1]]"
        expected_value = '<a href="#m1">1</a>'

        assert mod._convert_link(source_value, mod_id_to_name=dict()) == expected_value

    def test_mod_internal_link_one_bracket(self):
        mod = create_mod_instance(id=1, name="Toto")
        source_value = "[[1]"
        expected_value = "[[1]"

        assert mod._convert_link(source_value) == expected_value

    def test_mod_external_link(self):
        mod = create_mod_instance(id=1, name="Toto")
        source_value = "[Toto](toto.com)"
        expected_value = '<a href="toto.com" target="_blank">Toto</a>'

        assert mod._convert_link(source_value) == expected_value

    def test_mod_get_internal_link(self, mod):
        source_value = 1
        expected_value = '<a href="#m1">Toto</a>'

        assert mod.get_internal_link(source_value, mod_id_to_name={1: "Toto"}) == expected_value

    def test_mod_get_internal_link_no_mod_id_to_name(self, mod):
        source_value = 1
        expected_value = '<a href="#m1">1</a>'

        assert mod.get_internal_link(source_value, mod_id_to_name=dict()) == expected_value

    def test_mod_get_internal_link_str(self, mod):
        source_value = "ToB"
        expected_value = "ToB"

        assert mod.get_internal_link(source_value) == expected_value

    # TODO: others
