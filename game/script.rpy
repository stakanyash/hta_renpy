default temp_name = ""
default player_name = "Вы"

init python:
    renpy.music.register_channel("sfx2", mixer="sfx", loop=True, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("shoot", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("damage", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("missshot", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")

    def try_add_item(item):
        limit = CarInventoryLimits.get(CurrentCar, 4)
        if len(Inventory) < limit:
            Inventory.append(item)
            return True
        return False

    def get_random_drops():
        if CurrentRegion in ("r1m1"):
            keys = list(R1M1DropNames.keys())
            drop_count = random.randint(1, 2)
        elif CurrentRegion in ("r1m2", "r1m3", "r1m4"):
            keys = list(R1DropNames.keys())
            drop_count = random.randint(1, 2)
        else:
            keys = list(DropNames.keys())
            drop_count = random.randint(1, 2)

        drop_ids = random.sample(keys, drop_count)
        return [(item_id, DropNames[item_id]) for item_id in drop_ids]

transform stretch_in:
    yzoom 0.95
    linear 0.1 yzoom 1.0

label start:

    $ player_name = "Вы"

    $ CurrentGun = "Hornet"
    $ CurrentMoney = 0
    $ CurrentCar = "Van"
    $ CurrentRegion = "r1m1"

    $ TownType = "None"

    $ Inventory = []
    $ R1M3FarmCount = 0

    $ r1m4SideQuest = "CanBeGiven"

    $ car_names = {
        "Van": "Вэн",
        "Molokovoz": "Молоковоз",
        "Ural": "Урал",
        "Belaz": "Белаз",
        "Mirotvorec": "Миротворец"
    }

    $ region_names = {
        "r1m1": "Край",
        "r1m2": "Риджин",
        "r1m3": "Фатерлянд",
        "r1m4": "Хель",
        "r2m1": "Либриум",
        "r2m2": "Аржан",
        "r3m1": "Роща Друидов",
        "r3m2": "Игнотт",
        "r4m1": "Вахат",
        "r4m2": "Зармек",
    }

    $ gun_names = {
        "Hornet": "Шершень",
        "Storm": "Шторм",
        "PKT": "ПКТ",
        "Kord": "Корд",
        "Vulcan": "Вулкан",
        "KPVT": "КПВТ",
        "Bumblebee": "Шмель",
        "Hurricane": "Ураган",
        "Flag": "Флаг",
        "None": "-"
    }

    $ gun_stats = {
        "Hornet": (0.0060, 0.0140),
        "Specter": (0.0070, 0.0164),
        "Storm": (0.0071, 0.0167),
        "PKT": (0.0076, 0.0178),
        "Kord": (0.0082, 0.0190),
        "Hurricane": (0.0082, 0.0190),
        "Flag": (0.0120, 0.0280),
        "Vulcan": (0.0089, 0.0207),
        "KPVT": (0.0090, 0.0210),
        "Bumblebee": (0.0100, 0.0232),
        "Vector": (0.0102, 0.0238)
    }

    $ CarHP = {
        "Van": 850,
        "Molokovoz": 1500,
        "Ural": 2000,
        "Belaz": 2500,
        "Mirotvorec": 3500
    }

    $ ItemPricesCity = {
        "Hornet": 260,
        "Specter": 50,
        "PKT": 200,
        "Storm": 30,
        "Potato": 200,
        "ScrapMetal": 400,
        "Wood": 50,
    }

    $ ItemPricesVillage = {
        "Hornet": 260,
        "Specter": 50,
        "PKT": 200,
        "Storm": 30,
        "Potato": 30,
        "ScrapMetal": 450,
        "Wood": 285,
    }

    $ ItemNames = {
        "Hornet": "Шершень",
        "Specter": "Спектр",
        "PKT": "ПКТ",
        "Storm": "Шторм",
        "Potato": "Картофель",
        "ScrapMetal": "Металлолом",
        "Wood": "Дрова",
    }

    $ R1M1DropNames = {
        "Hornet": "Шершень",
        "Potato": "Картофель",
        "Wood": "Дрова",
    }

    $ R1DropNames = {
        "Hornet": "Шершень",
        "Potato": "Картофель",
        "ScrapMetal": "Металлолом",
        "Wood": "Дрова",
    }

    $ DropNames = {
        "Hornet": "Шершень",
        "Potato": "Картофель",
        "ScrapMetal": "Металлолом",
        "Wood": "Дрова",
    }

    $ CarInventoryLimits = {
        "Van": 4,
        "Molokovoz": 8,
        "Ural": 12,
        "Belaz": 18,
        "Mirotvorec": 12,
    }

    call screen name_input_screen

label selling:
    if TownType == "City":
        $ current_prices = ItemPricesCity
    elif TownType == "Village":
        $ current_prices = ItemPricesVillage

    $ sale_list = [f"{ItemNames[item]}" for item in Inventory if item in current_prices and item in ItemNames]
    $ sale_text = ", ".join(sale_list)
    $ total_value = sum([current_prices[item] for item in Inventory if item in current_prices])

    "В вашем инвентаре есть: [sale_text]."
    "Хотите продать всё и получить [total_value] монет?"

    menu:
        "Продать":
            $ CurrentMoney += total_value
            $ Inventory.clear()
            "Вы продали все предметы и получили [total_value] монет.\nВаш баланс: [CurrentMoney] монет."
        "Оставить":
            "Вы решили не продавать предметы."

    return

label tutorial_check:
    init python:
        import os

        def tutorial_file_exists():
            return os.path.exists("htafirstrun")

        def create_tutorial_flag():
            with open("htafirstrun", "w") as f:
                f.write("V2FybSBsZWdzLg==")

    if not tutorial_file_exists():
        $ need_tutorial = renpy.call_screen("tutorial_prompt_call")
        $ create_tutorial_flag()

        if need_tutorial:
            jump tutorial
        
    jump main_game

label tutorial:

    play music "music/bio06.ogg" fadeout 1.0

    scene bg_glukhoe with fade

    show mc3 at center

    "Добро пожаловать в Ex Machina/Hard Truck Apocalypse RenPy."
    "Данная игра является фанатским переносом сюжета оригинальной Ex Machina/Hard Truck Apocalypse на движок RenPy."

    "Данная игра очень сильно отличается от оригинальной Ex Machina/Hard Truck Apocalypse. Так что есть с чем ознакомиться."

    "Начнём с того, что в данной игре вы не управляете грузовиком, а лишь следуете по сюжету игры."
    "Текст, который вы сейчас читаете - расположен на диалоговом окне. Все разговоры, мысли и описания происходящего будут появляться именно здесь."
    mc "Сейчас появилось окно с именем персонажа. Так вы будете знать, с кем говорите."
    unknown "Незнакомцы будут помечены следующим именем."

    "В данной игре есть выборы, которые могут влиять на события игры."
    "Выглядеть они будут примерно так:"

    menu:
        "Вариант 1":
            jump tutorial_continue

        "Вариант 2":
            jump tutorial_continue

label tutorial_continue:
    "Поэтому обдумывайте каждый свой выбор, ведь он может повлиять на доступ к событиям или концовку."

    "Так-же в данной игре реализована система боёв."
    scene tr_fight with fade
    pause 2.0
    "Перед вами пример интерфейса игры в состоянии боя."
    scene tr_fight_hp with dissolve
    pause 0.5
    "В левом верхнем углу отображается ваше здоровье."
    scene tr_fight_heal with dissolve
    pause 0.5
    "В правом верхнем углу количество оставшихся единиц лечения."
    scene tr_fight_action with dissolve
    pause 0.5
    "Кнопки атаки и лечения расположены в левом нижнем углу."
    scene tr_fight_enemyhp with dissolve
    pause 0.5
    "В правом нижнем углу - здоровье противника и его имя."
    scene tr_fight_attack with dissolve
    pause 0.5
    "Для атаки нажмайте кнопку \"Атаковать\"."
    scene tr_fight_healbtn with dissolve
    pause 0.5
    "Для лечения нажимайте кнопку \"Лечиться\"."
    scene tr_fight with dissolve
    pause 0.5
    "Атака имеет 70%% шанс нанесения урона по противнику. Урон варьируется в зависимости от оружия, которое установлено на вашем грузовике. Оружие можно улучшить по сюжету."
    "Например: стандартное оружие \"Шершень\" имеет случайный урон от 0.5%% до 1.75%% от максимального здоровья противника."
    "Лечение случайным образом восстанавливает вам от 2%% до 10%% от вашего максимального здоровья."

    scene tr_fight at Shake(None, 1.0, dist=7)
    $ renpy.show("damage", at_list=[fadeout_damage, Shake(None, 2.0, dist=7)])
    $ renpy.sound.play(f"audio/sfx/tutorial_damage.ogg", channel="damage")

    "Получение урона отнимает у вас 3%% от вашего максимального здоровья за каждый промах. Урон наносится после 5 попыток атаковать противника при наличии промаха."
    "Т.е. если вы за 5 атак промажете 2 раза, то урон будет 6%%. Если же вам повезёт не промахнуться 10 раз подряд, то будет нанесён фиксированный урон в 7%% от вашего максимального здоровья."
    "Поэтому победить противника без лечения - не получится."
    "На время боя отключена возможность сохранения, загрузки сохранений и выхода в меню. Но об этом далее..."

    scene tr_checkpoints with fade

    "В игре реализована механика \"чекпоинтов\", которые заменяют собой встроенные в движок автосохранения."
    "Чекпоинты создаются в критически важные моменты игры. Например: после выбора или перед боем."
    "Для чекпоинтов имеется всего 6 слотов, которые будут перезаписываться, так что не забывайте делать ручные сохранения."
    "Сделать это можно как в главном меню, так и с помощью нижних кнопок в окне диалога."
    "Делать ручные сохранения во вкладку \"чекпоинтов\" нельзя."

    scene bg_glukhoe with fade
    show mc3 at center

    "Теперь вы готовы. Осталось одно - выжить в этом мире."
    "Удачи. Она вам пригодится."

    jump main_game


label titles:

    $ renpy.movie_cutscene("movies/titles.mp4")

    return

label fightlost:
    scene black with fade
    stop music fadeout 1.0
    $ randomdeadmsg = random.randint(1, 4)
    if randomdeadmsg == "1":
        mc "{cps=7}Я не смог... увернуться...{/cps}"
    elif randomdeadmsg == "2":
        mc "{cps=7}Это конец...{/cps}"
    elif randomdeadmsg == "3":
        mc "{cps=7}Нееет! Нее...{/cps}"
    else:
        mc "{cps=7}Прощайте, братцы!{/cps}"
    
    return