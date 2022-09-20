from __future__ import annotations
from abc import ABC, abstractmethod
from project.equipment import Weapon, Armor
from project.classes import UnitClass
from random import randint
from typing import Optional


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit использует свойства класса UnitClass
        """
        self.name = name
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self._is_skill_used = False

    @property
    def health_points(self):
        """
        Возвращает аттрибут hp в красивом виде
        """
        return round(self.hp, 1)

    @property
    def stamina_points(self):
        """
        Возвращает аттрибут stamina в красивом виде
        """
        return round(self.stamina, 1)

    def equip_weapon(self, weapon: Weapon):
        """
        Присваивает нашему герою новое оружие
        """
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor):
        """
        Присваивает герою новую броню
        """
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> int:
        """
        Расчитывает урон игрока, брони цели, уменьшение выносливости атакующего и защищающегося,
        и возвращает итоговый урон для последующего вывода пользователю в текстовом виде
        """
        self.stamina -= self.weapon.stamina_per_hit * self.unit_class.stamina
        damage = self.weapon.damage * self.unit_class.attack
        if target.stamina > target.armor.stamina_per_turn * target.unit_class.stamina:
            target.stamina -= target.armor.stamina_per_turn * target.unit_class.stamina
            damage -= target.armor.defence * target.unit_class.armor
        return target.get_damage(damage)

    def get_damage(self, damage: int) -> Optional[int]:
        """
        Рассчитывает получение урона персонажем
        """
        self.hp = round(self.hp - damage, 1)
        if self.hp < 0:
            self.hp = 0
        return self.hp

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        Этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        Метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self._is_skill_used:
            return "Навык уже был использован"
        else:
            if self.unit_class.skill._is_stamina_enough:
                self._is_skill_used = True
            return self.unit_class.skill.use(user=self, target=target)


class PlayerUnit(BaseUnit):
    """
    Класс игрок
    """
    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina * self.unit_class.stamina >= self.weapon.stamina_per_hit:
            damage = self._count_damage(target)
            if damage > 0:
                return f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
            else:
                return f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."
        else:
            f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."


class EnemyUnit(BaseUnit):
    """
    Класс соперник
    """
    def hit(self, target: BaseUnit) -> str:
        """
        Функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Для этих целей используется функция randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target)
        """
        if not self._is_skill_used and self.stamina >= self.unit_class.skill.stamina and randint(0, 100) < 10:
            return self.use_skill(target)

        if self.stamina * self.unit_class.stamina < self.weapon.stamina_per_hit:
            return f"\n {self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target)
        if damage > 0:
            return f"\n{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона. "

        return f"\n{self.name} используя {self.weapon.name} наносит удар, но Ваш {target.armor.name}  его  останавливает."
