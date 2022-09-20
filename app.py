from flask import Flask, render_template, request, redirect, url_for
from project.base import Arena
from project.classes import unit_classes
from project.equipment import Equipment
from project.unit import PlayerUnit, EnemyUnit

app = Flask(__name__)

heroes = {}

arena = Arena()
equipment = Equipment()


@app.route("/")
def menu_page():
    """
    Начальная страница, меню
    """
    return render_template('index.html')


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """
    Выбор героя
    """
    if request.method == 'GET':
        result = {
            "header": "Выберите героя",
            "classes": unit_classes,
            "weapons": equipment.get_weapons_names(),
            "armors": equipment.get_armors_names(),
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form["name"]
        choose_unit_class = request.form["unit_class"]
        weapon_name = request.form["weapon"]
        armor_name = request.form["armor"]
        player = PlayerUnit(name=name, unit_class=unit_classes.get(choose_unit_class))
        player.equip_weapon(equipment.get_weapon(weapon_name))
        player.equip_armor(equipment.get_armor(armor_name))
        heroes["player"] = player
        return redirect(url_for('choose_enemy'))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    """
    Выбор противника
    """
    if request.method == 'GET':
        result = {
            "header": "Выберите противника",
            "classes": unit_classes,
            "weapons": equipment.get_weapons_names(),
            "armors": equipment.get_armors_names(),
        }
        return render_template('hero_choosing.html', result=result)

    if request.method == 'POST':
        name = request.form["name"]
        choose_unit_class = request.form["unit_class"]
        weapon_name = request.form["weapon"]
        armor_name = request.form["armor"]
        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(choose_unit_class))
        enemy.equip_weapon(equipment.get_weapon(weapon_name))
        enemy.equip_armor(equipment.get_armor(armor_name))
        heroes["enemy"] = enemy
        return redirect(url_for('start_fight'))


@app.route("/fight/")
def start_fight():
    """
    Выполняет функцию start_game экземпляра класса арена и передаем ему необходимые аргументы
    """
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template('fight.html', heroes=heroes)


@app.route("/fight/hit")
def hit():
    """
    Если игра идет - вызывает метод player_hit() экземпляра класса Арена.
    Если игра не идет - пропускает срабатывание метода
    """
    if arena.game_is_running:
        result = arena.player_hit()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/use-skill")
def use_skill():
    """
    Использование скилла. Если игра идет - вызывает метод player_use_skill() экземпляра класса Арена
    """
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/pass-turn")
def pass_turn():
    """
    Пропуск хода. Если игра идет - вызывает метод next_turn() экземпляра класса Арена
    """
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result
    return render_template('fight.html', heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """
    Кнопка завершить игру
    """
    arena._end_game()
    return render_template('index.html', heroes=heroes)


if __name__ == "__main__":
    app.run()
