from project.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    """
    Класс для организации взаимодействие между двумя персонажами
    """
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False
    battle_result = None

    def start_game(self, player: BaseUnit, enemy: BaseUnit):
        """
        Присваивает экземпляру класса аттрибуты "игрок" и "противник",
        а также выставляем True для свойства "началась ли игра"
        """
        self.player = player
        self.enemy = enemy
        self.game_is_running = True

    def _check_players_hp(self):
        """
        Проверка здоровья игрока и врага, с возвращением результата строкой
        """
        if self.player.hp <= 0 and self.enemy.hp <= 0:
            self.battle_result = "Ничья"
        elif self.enemy.hp <= 0:
            self.battle_result = "Вы выиграли"
        elif self.player.hp <= 0:
            self.battle_result = "Вы проиграли"
        else:
            return None
        return self._end_game()

    def _stamina_regeneration(self):
        """
        Регенерация здоровья и стамины для игрока и врага за ход
        """
        units = (self.player, self.enemy)
        for  unit in units:
            if unit.stamina + self.STAMINA_PER_ROUND > unit.unit_class.max_stamina:
                unit.stamina = unit.unit_class.max_stamina
            else:
                unit.stamina += self.STAMINA_PER_ROUND

    def next_turn(self):
        """
        Проверяет что вернется в результате функции self._check_players_hp. Если result -> возвращаем его,
        если же результата пока нет и после завершения хода игра продолжается с запуском регенерации
        стамины, здоровья и ответного хода противника
        """
        result = self._check_players_hp()
        if result:
            return result
        self._stamina_regeneration()
        return self.enemy.hit(self.player)

    def _end_game(self):
        """
        Завершает игру
        """
        self._instances = {}
        self.game_is_running = False
        return self.battle_result

    def player_hit(self):
        """
        Удар игрока. Получает результат от функции self.player.hit, запускает следующий ход,
        возвращает результат удара
        """
        result = self.player.hit(self.enemy)
        self.next_turn()
        return result

    def player_use_skill(self):
        """
        Игрок использует умение. Получает результат от функции self.player.use_skill, запускает следующий ход,
        возвращает результат удара
        """
        result = self.player.use_skill(self.enemy)
        self.next_turn()
        return result
