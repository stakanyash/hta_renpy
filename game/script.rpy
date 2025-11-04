default temp_name = ""
default player_name = "Игрок"
default difficulty = "normal"
default difficulty_base_multiplier = 0.03
default selected_shop_item = None

# --- PlayerConfig класс ---
init python:
    from dataclasses import dataclass, field
    import random

    @dataclass
    class PlayerConfig:
        # Основное состояние
        current_gun: str = "Hornet"
        second_gun: str = None
        money: int = 100
        car: str = "Van"
        current_region: str = "r1m1"
        gun_type: str = "Firearm"

        # Город
        town_type: str = None
        town_name: str = None
        group_logo: str = None

        # Инвентарь и квесты
        inventory: list = field(default_factory=list)
        farm_enabled: bool = False
        big_gun_install: str = None
        r1m3_farm_count: int = 0
        r1m4_side_quest: str = "CanBeGiven"

        # --- Методы для работы с состоянием ---
        def update_town_info(self, town_type, town_name, group_logo):
            self.town_type = town_type
            self.town_name = town_name
            self.group_logo = group_logo

        def try_add_item(self, item, limit_map=None):
            if limit_map is None:
                limit_map = CarInventoryLimits
            limit = limit_map.get(self.car, 4)
            if len(self.inventory) < limit:
                self.inventory.append(item)
                return True
            return False

        def spend_money(self, amount):
            if self.money >= amount:
                self.money -= amount
                return True
            renpy.notify("Недостаточно денег!")
            return False

        def add_money(self, amount):
            self.money += amount

        def format_money(self, val=None):
            val = val if val is not None else self.money
            if val >= 1_000_000:
                return f"{val / 1_000_000:.1f} млн"
            return str(val)

        def region_allowed(self, required):
            region_order = ["r1m1", "r1m2", "r1m3", "r1m4"]
            try:
                return region_order.index(self.current_region) >= region_order.index(required)
            except ValueError:
                return False

        def get_random_drops(self):
            if self.current_region in ("r1m1",):
                drop_dict = R1M1DropNames
                drop_count = random.randint(1, 2)
            elif self.current_region in ("r1m2", "r1m3"):
                drop_dict = R1DropNames
                drop_count = random.randint(1, 2)
            elif self.current_region in ("r1m4",):
                drop_dict = R1M4DropNames
                drop_count = random.randint(1, 3)
            else:
                drop_dict = DropNames
                drop_count = random.randint(1, 2)

            keys = list(drop_dict.keys())
            drop_ids = random.sample(keys, drop_count)
            return [(item_id, drop_dict[item_id]) for item_id in drop_ids]

# --- Создаем глобальный объект игрока ---
default player_config = PlayerConfig()

# --- Настройка каналов звука ---
init python:
    renpy.music.register_channel("sfx2", mixer="sfx", loop=True, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("shoot", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("damage", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("missshot", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("bossattack", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("sellitem", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")

# --- Константы и базы данных ---
init python:
    # --- Цены оружия ---
    smallweapon_prices = {
        "Hornet": 280, "Specter": 590, "PKT": 1670, "Kord": 3680, "Storm": 3450,
    }

    bigweapon_prices = {
        "Vector": 5520, "Vulcan": 5630, "KPVT": 6400, "Bumblebee": 13310,
        "Hurricane": 14910, "Flag": 17860, "Rapier": 20400, "Rainmetal": 24580,
        "Omega": 42000, "Elephant": 50500,
    }

    # --- Ограничения и инвентарь ---
    CarInventoryLimits = {
        "Van": 4, "Molokovoz": 8, "Ural": 12, "Belaz": 18, "Mirotvorec": 12,
    }

    # --- Имена и отображение ---
    car_names = {
        "Van": "Вэн",
        "Molokovoz": "Молоковоз",
        "Ural": "Урал",
        "Belaz": "Белаз",
        "Mirotvorec": "Миротворец"
    }

    region_names = {
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

    gun_names = {
        "Hornet": "Шершень", "Specter": "Спектр", "Storm": "Шторм", "PKT": "ПКТ",
        "Kord": "Корд", "Vector": "Вектор", "Vulcan": "Вулкан", "KPVT": "КПВТ",
        "Bumblebee": "Шмель", "Hurricane": "Ураган", "Flag": "Флаг",
        "Rapier": "Рапира", "Rainmetal": "Рейнметалл", "Omega": "Омега",
        "Elephant": "Слон", "None": "-"
    }

    gun_stats = {
        "Hornet": (4, 7), "Specter": (6, 11), "PKT": (8, 14), "Kord": (11, 18),
        "Storm": (20, 55), "Vector": (18, 30), "Vulcan": (12, 20), "KPVT": (16, 26),
        "Rainmetal": (28, 48), "Bumblebee": (35, 90), "Hurricane": (22, 50),
        "Flag": (45, 100), "Rapier": (50, 85), "Omega": (55, 130), "Elephant": (700, 800),
    }

    # --- Дропы ---
    R1M1DropNames = {"Hornet": "Шершень", "Potato": "Картофель", "Wood": "Дрова"}
    R1DropNames = {"Hornet": "Шершень", "Potato": "Картофель", "ScrapMetal": "Металлолом", "Wood": "Дрова"}
    R1M4DropNames = {"ScrapMetal": "Металлолом", "Oil": "Нефть", "Fuel": "Топливо"}
    DropNames = {"Hornet": "Шершень", "Potato": "Картофель", "ScrapMetal": "Металлолом", "Wood": "Дрова"}

    # --- Базы данных ---
    GunDatabase = {
        "Hornet": {"name": "Шершень", "desc": "Пулемёт калибра 5,45 - пожалуй, самое слабое автоматическое оружие, которым можно оборудовать грузовик.", "type": "Firearm"},
        "Specter": {"name": "Спектр", "desc": "Спаренный пулемёт калибра 5,45. Два ствола и малое время перезарядки позволяют вести почти непрерывный огонь.", "type": "Firearm"},
        "PKT": {"name": "ПКТ", "desc": "Пулемёт калибра 7,62 - с ним уже можно не бояться отправляться в недалёкое путешествие.", "type": "Firearm"},
        "Kord": {"name": "Корд", "desc": "Пулемёт калибра 12,7 - достойное оружие для борца с бандитами.", "type": "Firearm"},
        "Storm": {"name": "Шторм", "desc": "Дробовик наносит значительные повреждения на близком расстоянии.", "type": "Shotgun"},
        "Vector": {"name": "Вектор", "desc": "Мелкокалиберная пушка - хороший выбор для начинающего путешественника.", "type": "Firearm"},
        "Vulcan": {"name": "Вулкан", "desc": "Многоствольный пулемёт калибра 5,56 посылает во врага море свинца. Правда, мощная отдача может даже перевернуть небольшой автомобиль.", "type": "Firearm"},
        "KPVT": {"name": "КПВТ", "desc": "Пулемёт калибра 14,5 - настоящий монстр, прошивающий тонкую броню, как бумагу.", "type": "Firearm"},
        "Bumblebee": {"name": "Шмель", "desc": "Поражение значительной площади с большой скоростью - это то, что нужно честному торговцу в борьбе с шайкой бандитов.", "type": "Firearm"},
        "Hurricane": {"name": "Ураган", "desc": "Это ракетница выстреливает ракеты с небольшим зарядом, но она выпускает очень много таких ракет.", "type": "Firearm"},
        "Flag": {"name": "Флаг", "desc": "Тяжёлый дробовик - это веский аргумент для врагов, чтобы не подходить к вашей машине вплотную.", "type": "Shotgun"},
        "Rapier": {"name": "Рапира", "desc": "Дальнобойная пушка калибра 23 мм является серьёзным оружием в умелых руках.", "type": "Firearm"},
        "Rainmetal": {"name": "Рейнметалл", "desc": "Скорострельная пушка калибра 20 мм - прекрасный выбор для охоты на двуногого зверя.", "type": "Firearm"},
        "Omega": {"name": "Омега", "desc": "Если враг пытается взять вас не умением, а числом, то эта пушка как раз для такого случая.", "type": "Firearm"},
        "Elephant": {"name": "Слон", "desc": "Весьма достойный плазмомёт. Во всяком случае, никто из противников не жаловался.", "type": "Plasma"},
    }


    GunTypeName = {
        "Firearm": "Огнестрельное",
        "Shotgun": "Дробовик",
        "Plasma": "Плазма",
    }

    DifficultyNames = { 
        "easy": "Новичок", 
        "normal": "Бывалый", 
        "hard": "Профессионал", 
        "expert": "Мастер", 
    }

    CarHP = { 
        "Van": 850, 
        "Molokovoz": 1500, 
        "Ural": 2000, 
        "Belaz": 2500, 
        "Mirotvorec": 3500 
    }

    ItemDatabase = {
        "Hornet": {
            "name": "Шершень",
            "desc": "Пулемёт калибра 5,45 - пожалуй, самое слабое автоматическое оружие, которым можно оборудовать грузовик.",
            "icon": "gui/townmenu/items/hornet.png",
        },
        "Specter": {
            "name": "Спектр",
            "desc": "Спаренный пулемёт калибра 5,45. Два ствола и малое время перезарядки позволяют вести почти непрерывный огонь.",
            "icon": "gui/townmenu/items/Specter.png",
        },
        "PKT": {
            "name": "ПКТ",
            "desc": "Пулемёт калибра 7,62 - с ним уже можно не бояться отправляться в недалёкое путешествие.",
            "icon": "gui/townmenu/items/PKT.png",
        },
        "Kord": {
            "name": "Корд",
            "desc": "Пулемёт калибра 12,7 - достойное оружие для борца с бандитами.",
            "icon": "gui/townmenu/items/Kord.png",
        },
        "Storm": {
            "name": "Шторм",
            "desc": "Дробовик наносит значительные повреждения на близком расстоянии.",
            "icon": "gui/townmenu/items/Storm.png",
        },
        "Vector": {
            "name": "Вектор",
            "desc": "Мелкокалиберная пушка - хороший выбор для начинающего путешественника.",
            "icon": "gui/townmenu/items/Vector.png",
        },
        "Vulcan": {
            "name": "Вулкан",
            "desc": "Многоствольный пулемёт калибра 5,56 посылает во врага море свинца. Правда, мощная отдача может даже перевернуть небольшой автомобиль.",
            "icon": "gui/townmenu/items/Vulcan.png",
        },
        "KPVT": {
            "name": "КПВТ",
            "desc": "Пулемёт калибра 14,5 - настоящий монстр, прошивающий тонкую броню, как бумагу.",
            "icon": "gui/townmenu/items/KPVT.png",
        },
        "Bumblebee": {
            "name": "Шмель",
            "desc": "Поражение значительной площади с большой скоростью - это то, что нужно честному торговцу в борьбе с шайкой бандитов.",
            "icon": "gui/townmenu/items/Bumblebee.png",
        },
        "Hurricane": {
            "name": "Ураган",
            "desc": "Это ракетница выстреливает ракеты с небольшим зарядом, но она выпускает очень много таких ракет.",
            "icon": "gui/townmenu/items/Hurricane.png",
        },
        "Flag": {
            "name": "Флаг",
            "desc": "Тяжёлый дробовик - это веский аргумент для врагов, чтобы не подходить к вашей машине вплотную.",
            "icon": "gui/townmenu/items/Flag.png",
        },
        "Rapier": {
            "name": "Рапира",
            "desc": "Дальнобойная пушка калибра 23 мм является серьёзным оружием в умелых руках.",
            "icon": "gui/townmenu/items/Rapier.png",
        },
        "Rainmetal": {
            "name": "Рейнметалл",
            "desc": "Скорострельная пушка калибра 20 мм - прекрасный выбор для охоты на двуногого зверя.",
            "icon": "gui/townmenu/items/Rainmetal.png",
        },
        "Omega": {
            "name": "Омега",
            "desc": "Если враг пытается взять вас не умением, а числом, то эта пушка как раз для такого случая.",
            "icon": "gui/townmenu/items/Omega.png",
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

    ItemPricesCity = {
        "Hornet": 140,
        "Specter": 295,
        "PKT": 835,
        "Kord": 1840,
        "Storm": 1725,
        "Vector": 2760,
        "Vulcan": 2815,
        "KPVT": 3200,
        "Bumblebee": 6655,
        "Hurricane": 7455,
        "Flag": 8930,
        "Rapier": 10200,
        "Rainmetal": 12290,
        "Omega": 21000,
        "Elephant": 25250,
        "Potato": 200,
        "ScrapMetal": 400,
        "Wood": 50,
        "Oil": 200,
        "Fuel": 1850,
    }

    ItemPricesVillage = {
        "Hornet": 140,
        "Specter": 295,
        "PKT": 835,
        "Kord": 1840,
        "Storm": 1725,
        "Vector": 2760,
        "Vulcan": 2815,
        "KPVT": 3200,
        "Bumblebee": 6655,
        "Hurricane": 7455,
        "Flag": 8930,
        "Rapier": 10200,
        "Rainmetal": 12290,
        "Omega": 21000,
        "Elephant": 25250,
        "Potato": 30,
        "ScrapMetal": 450,
        "Wood": 285,
        "Oil": 1100,
        "Fuel": 900,
    }

    def buy_weapon_with_old_handling(weapon_name):
        # Проверяем цену
        if weapon_name in smallweapon_prices:
            price = smallweapon_prices[weapon_name]
        elif weapon_name in bigweapon_prices:
            price = bigweapon_prices[weapon_name]
        else:
            renpy.notify("Ошибка: цена оружия не найдена.")
            return

        if player_config.money >= price:
            player_config.money -= price

            # Старое оружие добавляем в инвентарь
            if player_config.current_gun not in player_config.inventory:
                player_config.inventory.append(player_config.current_gun)

            # Ставим новое оружие текущим
            player_config.current_gun = weapon_name

            weapon_data = GunDatabase.get(weapon_name)
            if weapon_data:
                player_config.gun_type = weapon_data.get("type")
            else:
                player_config.gun_type = None

            renpy.sound.play("audio/sfx/coins.wav", channel="sellitem")
            renpy.notify(f"Вы купили {gun_names.get(weapon_name, weapon_name)} за {price} монет.")
        else:
            renpy.notify("Недостаточно денег!")

# --- Трансформа для анимации ---
transform stretch_in:
    yzoom 0.95
    linear 0.1 yzoom 1.0

label start:
    if not config.developer:
        $ _window_hide()
        $ _game_menu_screen = None
        $ _menu = False
        $ config.keymap['save'] = []
        $ config.keymap['load'] = []
        $ config.keymap['game_menu'] = []
        $ persistent._in_battle = True

    jump tutorial_check

label show_loading(load_slides):
    python:
        import random

        total_time = random.uniform(4.0, 7.0)
        num_slides = len(load_slides)

        weights = [random.random() for _ in range(num_slides)]
        weight_sum = sum(weights)
        pauses = [total_time * w / weight_sum for w in weights]

        for i, slide in enumerate(load_slides):
            renpy.show(slide, at_list=[truecenter])
            renpy.pause(pauses[i], hard=True)
            renpy.hide(slide)

    return

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
    $ player_hp = CarHP.get(player_config.car, CarHP["Van"])
    $ player_max_hp = player_hp

    if player_config.current_region == "r1m1":
        $ enemy_hp = random.randint(80, 150)
    elif player_config.current_region in ("r1m2", "r1m3"):
        $ enemy_hp = random.randint(120, 200)
    elif player_config.current_region == "r1m4":
        $ enemy_hp = random.randint(180, 300)

    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = 20
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ bgname = f"bg_{player_config.current_region}_randomfight"
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
        $ renpy.sound.stop(channel="shoot")
        
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
        $ renpy.sound.stop(channel="shoot")

        play sound "sfx/explosion04.wav"
        $ renpy.hide(enemy_image) 
        with dissolve

        $ drops = player_config.get_random_drops()

        if drops:
            python:
                drop_names_text = []
                dropped_something = False
                items_not_added = 0

                for drop_id, drop_name in drops:
                    if player_config.try_add_item(drop_id):
                        drop_names_text.append(drop_name)
                        dropped_something = True
                    else:
                        items_not_added += 1

                if player_config.current_region == "r1m1":
                    money_drop = random.randint(50, 150)
                elif player_config.current_region == "r1m2":
                    money_drop = random.randint(100, 250)
                elif player_config.current_region == "r1m3":
                    money_drop = random.randint(150, 350)
                elif player_config.current_region == "r1m4":
                    money_drop = random.randint(300, 600)

                if items_not_added > 0:
                    compensation = items_not_added * random.randint(100, 200)
                    money_drop += compensation
                    renpy.say(None, f"В вашем инвентаре не хватает места! Получено: {compensation} монет")
                
                player_config.add_money(money_drop)

                if dropped_something:
                    drop_names_str = ", ".join(drop_names_text)
                    renpy.say(None, f"Найдены следующие предметы: {drop_names_str}.\nТак-же получено {money_drop} монет.")
                else:
                    renpy.say(None, f"Найдено: {money_drop} монет.")
                
        return

label titles:

    $ renpy.movie_cutscene("movies/titles.mp4")

    return

label fightlost:
    scene black with fade
    stop music fadeout 1.0

    $ dead_msgs = [
        "{cps=7}Я не смог... увернуться...{/cps}",
        "{cps=7}Это конец...{/cps}",
        "{cps=7}Нееет! Нее...{/cps}",
        "{cps=7}Прощайте, братцы!{/cps}"
    ]

    $ renpy.say(mc, random.choice(dead_msgs))
    
    return

label carshop:
    $ oldcarsell_value = CarSellPrices.get(player_config.car, 0)

    python:
        affordable_cars = [
            car_names[name]
            for name, price in CarPrices.items()
            if price <= player_config.money
            and (name != player_config.car or CarPrices[name] < CarPrices.get(player_config.car, 0))
            and player_config.region_allowed(CarMinRegion.get(name, "r1m1"))
        ]

        car_text = ", ".join(affordable_cars)

    "Ваших средств достаточно на: [car_text]."

    menu:
        "Купить Вэн" if player_config.money >= 1401 and player_config.car != "Van" and player_config.region_allowed("r1m1"):
            $ sellprice = 1401 - oldcarsell_value
            $ player_config.spend_money(sellprice)
            $ player_config.car = "Van"
            if sellprice > 0:
                $ renpy.notify(f"Вы отдали {sellprice} монет.")
                "Вы купили Вэн и отдали [sellprice] монет."
            elif sellprice < 0:
                $ renpy.notify(f"Вы получили {abs(sellprice)} монет.")
                "Вы купили Вэн и получили [abs(sellprice)] монет из-за того, что ваш старый автомобиль дороже нового."

        "Купить Молоковоз" if player_config.money >= 6501 and player_config.car != "Molokovoz" and player_config.region_allowed("r1m2"):
            $ sellprice = 6501 - oldcarsell_value
            $ player_config.spend_money(sellprice)
            $ player_config.car = "Molokovoz"
            if sellprice > 0:
                $ renpy.notify(f"Вы отдали {sellprice} монет.")
                "Вы купили Молоковоз и отдали [sellprice] монет."
            elif sellprice < 0:
                $ renpy.notify(f"Вы получили {abs(sellprice)} монет.")
                "Вы купили Молоковоз и получили [abs(sellprice)] монет из-за того, что ваш старый автомобиль дороже нового."

        "Купить Урал" if player_config.money >= 31001 and player_config.car != "Ural" and player_config.region_allowed("r1m4"):
            $ sellprice = 31001 - oldcarsell_value
            $ player_config.spend_money(sellprice)
            $ player_config.car = "Ural"
            if sellprice > 0:
                $ renpy.notify(f"Вы отдали {sellprice} монет.")
                "Вы купили Урал и отдали [sellprice] монет."
            elif sellprice < 0:
                $ renpy.notify(f"Вы получили {abs(sellprice)} монет.")
                "Вы купили Урал и получили [abs(sellprice)] монет из-за того, что ваш старый автомобиль дороже нового."

        "Не покупать новую машину":
            "Вы решили не покупать новую машину.\nНа вашем балансе: [player_config.money] монет."
            return

    return
