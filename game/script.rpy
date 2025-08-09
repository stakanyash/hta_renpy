default temp_name = ""
default player_name = "Игрок"
default difficulty = "normal"
default difficulty_base_multiplier = 0.03
default selected_shop_item = None

init python:
    renpy.music.register_channel("sfx2", mixer="sfx", loop=True, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("shoot", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("damage", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("missshot", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("bossattack", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("sellitem", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")

    def try_add_item(item):
        limit = CarInventoryLimits.get(CurrentCar, 4)
        if len(Inventory) < limit:
            Inventory.append(item)
            return True
        return False

    def get_random_drops():
        if CurrentRegion in ("r1m1"):
            drop_dict = R1M1DropNames
            drop_count = random.randint(1, 2)
        elif CurrentRegion in ("r1m2", "r1m3"):
            drop_dict = R1DropNames
            drop_count = random.randint(1, 2)
        elif CurrentRegion in ("r1m4"):
            drop_dict = R1M4DropNames
            drop_count = random.randint(1, 3)
        else:
            drop_dict = DropNames
            drop_count = random.randint(1, 2)

        keys = list(drop_dict.keys())
        drop_ids = random.sample(keys, drop_count)
        return [(item_id, drop_dict[item_id]) for item_id in drop_ids]

    def region_allowed(current, required):
        region_order = ["r1m1", "r1m2", "r1m3", "r1m4"]
        try:
            return region_order.index(current) >= region_order.index(required)
        except ValueError:
            return False

    def format_money(val):
        if val >= 1_000_000:
            return f"{val / 1_000_000:.1f} млн"
        else:
            return str(val)

    def buy_weapon(weapon_name):
        global CurrentMoney, CurrentGun, CurrentSecondGun

        if weapon_name in smallweapon_prices:
            price = smallweapon_prices[weapon_name]
            if CurrentMoney >= price:
                CurrentMoney -= price
                CurrentGun = weapon_name
                return True
            else:
                renpy.notify("Ваших средств недостаточно для покупки!")

        elif weapon_name in bigweapon_prices:
            price = bigweapon_prices[weapon_name]
            if CurrentMoney >= price:
                CurrentMoney -= price
                CurrentSecondGun = weapon_name
                return True
            else:
                renpy.notify("Ваших средств недостаточно для покупки!")

    def try_buy_weapon(weapon_name):
        if buy_weapon(weapon_name):
            return NullAction()
        else:
            return NullAction()
        return NullAction()

    def buy_and_clear(weapon_name):
        try_buy_weapon(weapon_name)
        store.selected_shop_item = None
        return None
        

transform stretch_in:
    yzoom 0.95
    linear 0.1 yzoom 1.0

label start:

    $ player_name = "Игрок"

    $ CurrentGun = "Hornet"
    $ CurrentSecondGun = None
    $ CurrentMoney = 0
    $ CurrentCar = "Van"
    $ CurrentRegion = "r1m1"

    $ TownType = None
    $ TownName = None
    $ GroupLogo = None

    $ BigGunInstall = None

    $ Inventory = []
    $ R1M3FarmCount = 0

    $ r1m4SideQuest = "CanBeGiven"

    $ smallweapon_prices = {
        "Hornet": 280,
        "Specter": 590,
        "PKT": 1670,
        "Kord": 3680,
        "Storm": 3450,
    }

    $ bigweapon_prices = {
        "Vector": 5520,
        "Vulcan": 5630,
        "KPVT": 6400,
        "Bumblebee": 13310,
        "Hurricane": 14910,
        "Flag": 17860,
        "Rapier": 20400,
        "Rainmetal": 24580,
        "Omega": 42000,
    }

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
        "Specter": "Спектр",
        "Storm": "Шторм",
        "PKT": "ПКТ",
        "Kord": "Корд",
        "Maxim": "Максим",
        "Fagot": "Фагот",
        "Vulcan": "Вулкан",
        "KPVT": "КПВТ",
        "Bumblebee": "Шмель",
        "Hurricane": "Ураган",
        "Flag": "Флаг",
        "Vector": "Вектор",
        "Rapier": "Рапира",
        "Rainmetal": "Рейнметалл",
        "Omega": "Омега",
        "None": "-"
    }

    $ gun_stats = {
        "Hornet": (4, 6),
        "Specter": (5, 8),
        "Storm": (30, 100),
        "PKT": (6, 10),
        "Vector": (10, 15),
        "Kord": (8, 12),
        "Hurricane": (20, 46),
        "Vulcan": (15, 20),
        "KPVT": (13, 18),
        "Bumblebee": (30, 130),
        "Flag": (50, 180),
        "Rainmetal": (25, 70),
        "Rapier": (25, 45),
        "Omega": (50, 150),
    }

    $ CarHP = {
        "Van": 850,
        "Molokovoz": 1500,
        "Ural": 2000,
        "Belaz": 2500,
        "Mirotvorec": 3500
    }

    $ ItemPricesCity = {
        "Hornet": 130,
        "Specter": 295,
        "PKT": 835,
        "Storm": 1725,
        "Potato": 200,
        "ScrapMetal": 400,
        "Wood": 50,
        "Oil": 200,
        "Fuel": 1850,
        "Elephant": 22250
    }

    $ ItemPricesVillage = {
        "Hornet": 130,
        "Specter": 295,
        "PKT": 835,
        "Storm": 1725,
        "Potato": 30,
        "ScrapMetal": 450,
        "Wood": 285,
        "Oil": 1100,
        "Fuel": 900,
        "Elephant": 22250
    }

    $ ItemNames = {
        "Hornet": "Шершень",
        "Specter": "Спектр",
        "PKT": "ПКТ",
        "Storm": "Шторм",
        "Potato": "Картофель",
        "ScrapMetal": "Металлолом",
        "Wood": "Дрова",
        "Oil": "Нефть",
        "Fuel": "Топливо",
        "Elephant": "Слон"
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

    $ R1M4DropNames = {
        "ScrapMetal": "Металлолом",
        "Oil": "Нефть",
        "Fuel": "Топливо"
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

    $ DifficultyNames = {
        "easy": "Новичок",
        "normal": "Бывалый",
        "hard": "Профессионал",
        "expert": "Мастер",
    }

    $ CarPrices = {
        "Van": 1401,
        "Molokovoz": 6501,
        "Ural": 31001,
        "Belaz": 170001,
        "Mirotvorec": 360001,
    }

    $ CarSellPrices = {
        "Van": 701,
        "Molokovoz": 3251,
        "Ural": 15501,
        "Belaz": 47405,
        "Mirotvorec": 180001,
    }

    $ CarMinRegion = {
        "Van": "r1m1",
        "Molokovoz": "r1m2",
        "Ural": "r1m4",
        "Belaz": "r3m1",
        "Mirotvorec": "r4m1"
    }

    $ GunDatabase = {
        "Hornet": {
            "name": "Шершень",
            "desc": "Пулемёт калибра 5,45 - пожалуй, самое слабое автоматическое оружие, которым можно оборудовать грузовик.",
        },

        "Specter": {
            "name": "Спектр",
            "desc": "Спаренный пулемёт калибра 5,45. Два ствола и малое время перезарядки позволяют вести почти непрерывный огонь.",
        },

        "PKT": {
            "name": "ПКТ",
            "desc": "Пулемёт калибра 7,62 - с ним уже можно не бояться отправляться в недалёкое путешествие.",
        },

        "Kord": {
            "name": "Корд",
            "desc": "Пулемёт калибра 12,7 - достойное оружие для борца с бандитами.",
        },

        "Storm": {
            "name": "Шторм",
            "desc": "Дробовик наносит значительные повреждения на близком расстоянии.",
        },

        "Vector": {
            "name": "Вектор",
            "desc": "Мелкокалиберная пушка - хороший выбор для начинающего путешественника.",
        },

        "Vulcan": {
            "name": "Вулкан",
            "desc": "Многоствольный пулемёт калибра 5,56 посылает во врага море свинца. Правда, мощная отдача может даже перевернуть небольшой автомобиль.",
        },

        "KPVT": {
            "name": "КПВТ",
            "desc": "Пулемёт калибра 14,5 - настоящий монстр, прошивающий тонкую броню, как бумагу.",
        },

        "Bumblebee": {
            "name": "Шмель",
            "desc": "Поражение значительной площади с большой скоростью - это то, что нужно честному торговцу в борьбе с шайкой бандитов.",
        },

        "Hurricane": {
            "name": "Ураган",
            "desc": "Это ракетница выстреливает ракеты с небольшим зарядом, но она выпускает очень много таких ракет.",
        },

        "Flag": {
            "name": "Флаг",
            "desc": "Тяжёлый дробовик - это веский аргумент для врагов, чтобы не подходить к вашей машине вплотную.",
        },

        "Rapier": {
            "name": "Рапира",
            "desc": "Дальнобойная пушка калибра 23 мм является серьёзным оружием в умелых руках.",
        },

        "Rainmetal": {
            "name": "Рейнметалл",
            "desc": "Скорострельная пушка калибра 20 мм - прекрасный выбор для охоты на двуногого зверя.",
        },

        "Omega": {
            "name": "Омега",
            "desc": "Если враг пытается взять вас не умением, а числом, то эта пушка как раз для такого случая.",
        },
    }

    $ ItemDatabase = {
        "Hornet": {
            "name": "Шершень",
            "desc": "Пулемёт калибра 5,45 - пожалуй, самое слабое автоматическое оружие, которым можно оборудовать грузовик.",
            "icon": "gui/townmenu/items/hornet.png",
        },
        "Potato": {
            "name": "Картошка",
            "desc": "Картошка - она и есть. Что тут добавишь. Основной источник пропитания для всех людей.",
            "icon": "gui/townmenu/items/potatoe.png",
        },
        "Wood": {
            "name": "Дрова",
            "desc": "Дерево всегда было источником тепла. Как в качестве топлива, так и в качестве дешёвого строительного материала.",
            "icon": "gui/townmenu/items/trees.png",
        },
        "ScrapMetal": {
            "name": "Металлолом",
            "desc": "Из обломков иногда удаётся сколотить неплохие детали для грузовика. Ещё говорят, что кто-то научился переплавлять ржавый металл в слитки.",
            "icon": "gui/townmenu/items/lom.png",
        },
        "Oil": {
            "name": "Нефть",
            "desc": "Тот, кто контролирует нефть, контролирует и грузоперевозки. Поэтому вокруг этого ценного товара часто плетутся интриги.",
            "icon": "gui/townmenu/items/oil.png",
        },
        "Fuel": {
            "name": "Топливо",
            "desc": "Высокооктановое горючее встречается очень редко и обладает немалой стоимостью.",
            "icon": "gui/townmenu/items/fuel.png",
        },
        "Elephant": {
            "name": "Слон",
            "desc": "Весьма достойный плазмомёт. Во всяком случае, никто из противников не жаловался.",
            "icon": "gui/townmenu/items/elephant.png",
        },
    }

    call screen name_input_screen
    call screen difficulty_select
    jump tutorial_check

label randomfight:
    $ renpy.music.play(f"audio/music/battle{randommus}.ogg", channel='music')

    $ enemyint = random.randint(1, 4)

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = f"randomenemy{enemyint}"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = random.randint(250, 1000)
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 20
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ bgname = f"bg_{CurrentRegion}_randomfight"
    $ EnemyType = "Regular"
    $ renpy.show(bgname, at_list=[center], what=None)
    $ renpy.show(enemy_image, at_list=[center], what=None)

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        $ renpy.hide(enemy_image)
        play sound "sfx/explosion04.wav"
        jump fightlost
    else:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False

        play sound "sfx/explosion04.wav"
        $ renpy.hide(enemy_image) 
        with dissolve

        $ drops = get_random_drops()

        if drops:
            python:
                drop_names_text = []
                dropped_something = False
                no_space_warning_shown = False

                for drop_id, drop_name in drops:
                    if try_add_item(drop_id) == True:
                        drop_names_text.append(drop_name)
                        dropped_something = True
                    else:
                        if not no_space_warning_shown:
                            renpy.say(None, "В вашем инвентаре не хватает места!")
                            no_space_warning_shown = True

                if dropped_something:
                    drop_names_str = ", ".join(drop_names_text)
                    renpy.say(None, f"Найдены следующие предметы: {drop_names_str}")
                
        return

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

label shopmenu:
    $ SelShopPoint = None

    python:
        available_cars = [
            name for name, price in CarPrices.items()
            if price <= CurrentMoney
            and name != CurrentCar
            and region_allowed(CurrentRegion, CarMinRegion.get(name, "r1m1"))
        ]

    menu:
        "Купить автомобиль" if available_cars:
            $ SelShopPoint = "car"
        
        "Купить оружие":
            $ SelShopPoint = "weapon"

        "Продать предметы из инвентаря" if Inventory:
            $ SelShopPoint = "selling"

    if SelShopPoint == "car":
        call carshop
    elif SelShopPoint == "weapon":
        call weaponshop
    elif SelShopPoint == "selling":
        call selling

    return

label carshop:
    $ oldcarsell_value = CarSellPrices.get(CurrentCar, 0)

    python:
        affordable_cars = [
            car_names[name]
            for name, price in CarPrices.items()
            if price <= CurrentMoney
            and (name != CurrentCar or CarPrices[name] < CarPrices.get(CurrentCar, 0))
            and region_allowed(CurrentRegion, CarMinRegion.get(name, "r1m1"))
        ]

        car_text = ", ".join(affordable_cars)

    "Ваших средств достаточно на: [car_text]."

    menu:
        "Купить Вэн" if CurrentMoney >= 1401 and CurrentCar != "Van" and region_allowed(CurrentRegion, "r1m1"):
            $ sellprice = 1401 - oldcarsell_value
            $ CurrentMoney -= sellprice
            $ CurrentCar = "Van"
            if sellprice > 0:
                $ renpy.notify(f"Вы отдали {sellprice} монет.")
                "Вы купили Вэн и отдали [sellprice] монет."
            elif sellprice < 0:
                $ renpy.notify(f"Вы получили {abs(sellprice)} монет.")
                "Вы купили Вэн и получили [abs(sellprice)] монет из-за того, что ваш старый автомобиль дороже нового."

        "Купить Молоковоз" if CurrentMoney >= 6501 and CurrentCar != "Molokovoz" and region_allowed(CurrentRegion, "r1m2"):
            $ sellprice = 6501 - oldcarsell_value
            $ CurrentMoney -= sellprice
            $ CurrentCar = "Molokovoz"
            if sellprice > 0:
                $ renpy.notify(f"Вы отдали {sellprice} монет.")
                "Вы купили Молоковоз и отдали [sellprice] монет."
            elif sellprice < 0:
                $ renpy.notify(f"Вы получили {abs(sellprice)} монет.")
                "Вы купили Молоковоз и получили [abs(sellprice)] монет из-за того, что ваш старый автомобиль дороже нового."

        "Купить Урал" if CurrentMoney >= 31001 and CurrentCar != "Ural" and region_allowed(CurrentRegion, "r1m4"):
            $ sellprice = 31001 - oldcarsell_value
            $ CurrentMoney -= sellprice
            $ CurrentCar = "Ural"
            if sellprice > 0:
                $ renpy.notify(f"Вы отдали {sellprice} монет.")
                "Вы купили Урал и отдали [sellprice] монет."
            elif sellprice < 0:
                $ renpy.notify(f"Вы получили {abs(sellprice)} монет.")
                "Вы купили Урал и получили [abs(sellprice)] монет из-за того, что ваш старый автомобиль дороже нового."

        "Не покупать новую машину":
            "Вы решили не покупать новую машину.\nНа вашем балансе: [CurrentMoney] монет."
            return

    return

label weaponshop:
    $ selweashop = None

    menu:
        "Магазин маленького оружия":
            $ selweashop = "small"

        "Магазин среднего оружия":
            $ selweashop = "big"

    if selweashop == "small":
        call smallgunweaponshop
    elif selweashop == "big":
        call biggunweaponshop

    return
    
label smallgunweaponshop:
    python:
        affordable_weapons = [name for name, price in smallweapon_prices.items() if price <= CurrentMoney]
        weapon_text = ", ".join(affordable_weapons)
    
    "Ваших средств достаточно на: [weapon_text]."

    menu:
        "Шершень" if CurrentMoney >= 280 and CurrentGun != "Hornet":
            $ CurrentMoney -= 280
            $ CurrentGun = "Hornet"
            "Вы установили оружие \"Шершень\" и отдали 280 монет.\nУ вас осталось [CurrentMoney] монет."

label biggunweaponshop:
    python:
        affordable_weapons = [name for name, price in bigweapon_prices.items() if price <= CurrentMoney]
        weapon_text = ", ".join(affordable_weapons)
    
    "Ваших средств достаточно на: [weapon_text]."

    menu:
        "Вектор" if CurrentMoney >= 5520 and CurrentGun != "Vector":
            $ CurrentMoney -= 5520
            $ CurrentGun = "Vector"
            "Вы установили оружие \"Вектор\" и отдали 5520 монет.\nУ вас осталось [CurrentMoney] монет."

        "Вулкан" if CurrentMoney >= 5630 and CurrentGun != "Vulcan":
            $ CurrentMoney -= 5630
            $ CurrentGun = "Vulcan"
            "Вы установили оружие \"Вулкан\" и отдали 5630 монет.\nУ вас осталось [CurrentMoney] монет."  

        "КПВТ" if CurrentMoney >= 6400 and CurrentGun != "KPVT":
            $ CurrentMoney -= 6400
            $ CurrentGun = "KPVT"
            "Вы установили оружие \"КПВТ\" и отдали 6400 монет.\nУ вас осталось [CurrentMoney] монет."  

        "Шмель" if CurrentMoney >= 13310 and CurrentGun != "Bumbleebee":
            $ CurrentMoney -= 13310
            $ CurrentGun = "Bumblebee"
            "Вы установили оружие \"Шмель\" и отдали 13310 монет.\nУ вас осталось [CurrentMoney] монет."

        "Ураган" if CurrentMoney >= 14910 and CurrentGun != "Hurricane":
            $ CurrentMoney -= 14910
            $ CurrentGun = "Hurricane"
            "Вы установили оружие \"Ураган\" и отдали 14910 монет.\nУ вас осталось [CurrentMoney] монет."

        "Флаг" if CurrentMoney >= 17860 and CurrentGun != "Flag":
            $ CurrentMoney -= 17860
            $ CurrentGun = "Flag"
            "Вы установили оружие \"Флаг\" и отдали 17860 монет.\nУ вас осталось [CurrentMoney] монет."
