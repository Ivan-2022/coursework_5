from dataclasses import dataclass
from typing import List, Optional
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: float
    stamina_per_turn: float


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        """
        Рассчитывает конечный урон, исходя из минимального и максимального значения
        """
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: List[Weapon]
    armors: List[Armor]


class Equipment:
    """
    Класс Экипировка - интерфейс для взаимодействия с классом BaseUnit.
    """

    def __init__(self):
        self._equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Optional[Weapon]:
        """
        Возвращает объект оружия по имени
        """
        for item in self._equipment.weapons:
            if weapon_name == item.name:
                return item
        return None

    def get_armor(self, armor_name: str) -> Optional[Armor]:
        """
        Возвращает объект брони по имени
        """
        for item in self._equipment.armors:
            if armor_name == item.name:
                return item
        return None

    def get_weapons_names(self) -> list:
        """
        Возвращает список оружия
        """
        return [item.name for item in self._equipment.weapons]

    def get_armors_names(self) -> list:
        """
        Возвращает список брони
        """
        return [item.name for item in self._equipment.armors]

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        """
        загружает json в переменную EquipmentData
        """
        equipment_file = open("./data/equipment.json", encoding='utf-8')
        data = json.load(equipment_file)
        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
