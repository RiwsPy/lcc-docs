from scripts.cleaner.utils import ModCleaner


class Tp2Cleaner(ModCleaner):
    def clean_languages(self) -> list[str]:
        if not self.data.get("languages"):
            return list()

        languages = set()
        for lang_name, lang_dir_name in zip(
            self.data["languages"][::2], self.data["languages"][1::2], strict=True
        ):
            cleaned_lang = self._clean_lang(lang_dir_name)
            if not cleaned_lang:
                cleaned_lang = self._clean_lang(lang_name)
            if cleaned_lang:
                languages.add(cleaned_lang)

        return sorted(languages)
