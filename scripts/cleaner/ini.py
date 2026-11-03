from models import CategoryEnum
from scripts.cleaner.utils import ModCleaner


class IniCleaner(ModCleaner):
    # TODO
    category_mapping: dict[str, str] = {
        "Quest": CategoryEnum.QUEST.value,
        "Quests": CategoryEnum.QUEST.value,
        "NPC": CategoryEnum.NPC.value,
        "NPC-Related": CategoryEnum.NPC_OTHER.value,
        "Early_Tweak": "",
        "Tweak": CategoryEnum.TWEAK.value,
        "Tweaks": CategoryEnum.TWEAK.value,
        "Tweak_Early": "",
        "Tweak_early": "",
        "Late_Tweak": "",
        "Items": CategoryEnum.SPELL_ITEM.value,
        "Kits": CategoryEnum.KIT.value,
        "Story, Quest": CategoryEnum.QUEST.value,
        "Quest and NPC": CategoryEnum.QUEST.value,
        "NPC,Quests": CategoryEnum.NPC_OTHER.value,
    }

    def clean_categories(self) -> list[str]:
        new_categories = list()
        for category in super().clean_categories():
            if category not in self.category_mapping:
                print(f"{category} not found in {self.__class__.__name__}.category_mapping")
            category = self.category_mapping.get(category) or category
            if category and category not in ("Overwrite",):
                new_categories.append(category)
        return new_categories
