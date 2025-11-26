default temp_name = ""
default player_name = "Игрок"
default difficulty = "normal"
default difficulty_base_multiplier = 0.03
default selected_shop_item = None
default battle_tracks = [
    "audio/music/battle01.ogg",
    "audio/music/battle1.ogg",
    "audio/music/battle02.ogg",
    "audio/music/battle2.ogg",
    "audio/music/battle7.ogg"
]
default driving_tracks_by_region = {
    "r1m1": ["driving1", "driving2"],
    "r1m2": ["driving1", "driving2"],
    "r1m3": ["driving1", "driving2"],
    "r1m4": ["driving1", "driving2", "driving7"],
}

init python:
    from dataclasses import dataclass, field
    import random

    @dataclass
    class PlayerConfig:
        current_gun: str = "Hornet"
        second_gun: str = None
        money: int = 100
        car: str = "Van"
        current_region: str = "r1m1"
        gun_type: str = "Firearm"
        max_hp: int = 0
        hp: int = 0
        max_heals: int = 0
        heals: int = 0

        town_type: str = None
        town_name: str = None
        group_logo: str = None

        inventory: list = field(default_factory=list)
        farm_enabled: bool = False
        big_gun_install: str = None
        r1m3_farm_count: int = 0
        r1m4_side_quest: str = "CanBeGiven"

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

    renpy.music.register_channel("sfx2", mixer="sfx", loop=True, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("shoot", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("damage", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("missshot", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("bossattack", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("sellitem", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("boss_charge", mixer="sfx", loop=True, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")

    smallweapon_prices = {
        "Hornet": 280, "Specter": 590, "PKT": 1670, "Kord": 3680, "Storm": 3450, "Maxim": 26600, "Fagot": 25500
    }

    bigweapon_prices = {
        "Vector": 5520, "Vulcan": 5630, "KPVT": 6400, "Bumblebee": 13310,
        "Hurricane": 14910, "Flag": 17860, "Rapier": 20400, "Rainmetal": 24580,
        "Omega": 42000, "Elephant": 50500,
    }

    CarInventoryLimits = {
        "Van": 4, "Molokovoz": 8, "Ural": 12, "Belaz": 18, "Mirotvorec": 12,
    }

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
        "Elephant": "Слон", "Maxim": "Максим", "Fagot": "Фагот", "None": "-"
    }

    gun_stats = {
        "Hornet": (4, 7), "Specter": (6, 11), "PKT": (8, 14), "Kord": (11, 18),
        "Storm": (20, 55), "Vector": (18, 30), "Vulcan": (12, 20), "KPVT": (16, 26),
        "Rainmetal": (28, 48), "Bumblebee": (35, 90), "Hurricane": (22, 50),
        "Flag": (45, 100), "Rapier": (50, 85), "Omega": (55, 130), "Elephant": (700, 800),
        "Maxim": (32, 45), "Fagot": (60, 110),
    }

    R1M1DropNames = {"Hornet": "Шершень", "Potato": "Картофель", "Wood": "Дрова"}
    R1DropNames = {"Hornet": "Шершень", "Potato": "Картофель", "ScrapMetal": "Металлолом", "Wood": "Дрова"}
    R1M4DropNames = {"ScrapMetal": "Металлолом", "Oil": "Нефть", "Fuel": "Топливо"}
    DropNames = {"Hornet": "Шершень", "Potato": "Картофель", "ScrapMetal": "Металлолом", "Wood": "Дрова"}

    GunDatabase = {
        "Hornet": {"name": "Шершень", "desc": "Пулемёт калибра 5,45 - пожалуй, самое слабое автоматическое оружие, которым можно оборудовать грузовик.", "type": "Firearm", "size": "Small"},
        "Specter": {"name": "Спектр", "desc": "Спаренный пулемёт калибра 5,45. Два ствола и малое время перезарядки позволяют вести почти непрерывный огонь.", "type": "Firearm", "size": "Small"},
        "PKT": {"name": "ПКТ", "desc": "Пулемёт калибра 7,62 - с ним уже можно не бояться отправляться в недалёкое путешествие.", "type": "Firearm", "size": "Small"},
        "Kord": {"name": "Корд", "desc": "Пулемёт калибра 12,7 - достойное оружие для борца с бандитами.", "type": "Firearm", "size": "Small"},
        "Storm": {"name": "Шторм", "desc": "Дробовик наносит значительные повреждения на близком расстоянии.", "type": "Shotgun", "size": "Small"},
        "Maxim": {"name": "Максим", "desc": "Малый импульсный лазер, несмотря на небольшую мощность, прожигает насквозь почти любую броню.", "type": "Energy", "size": "Small"},
        "Fagot": {"name": "Фагот", "desc": "Заряд плазмы, посылаемый этим оружием, летит с небольшой скоростью, но при удачном попадании может буквально испепелить противника.", "type": "Plasma", "size": "Small"},

        "Vector": {"name": "Вектор", "desc": "Мелкокалиберная пушка - хороший выбор для начинающего путешественника.", "type": "Firearm", "size": "Big"},
        "Vulcan": {"name": "Вулкан", "desc": "Многоствольный пулемёт калибра 5,56 посылает во врага море свинца. Правда, мощная отдача может даже перевернуть небольшой автомобиль.", "type": "Firearm", "size": "Big"},
        "KPVT": {"name": "КПВТ", "desc": "Пулемёт калибра 14,5 - настоящий монстр, прошивающий тонкую броню, как бумагу.", "type": "Firearm", "size": "Big"},
        "Bumblebee": {"name": "Шмель", "desc": "Поражение значительной площади с большой скоростью - это то, что нужно честному торговцу в борьбе с шайкой бандитов.", "type": "Artillery", "size": "Big"},
        "Hurricane": {"name": "Ураган", "desc": "Это ракетница выстреливает ракеты с небольшим зарядом, но она выпускает очень много таких ракет.", "type": "Rocket", "size": "Big"},
        "Flag": {"name": "Флаг", "desc": "Тяжёлый дробовик - это веский аргумент для врагов, чтобы не подходить к вашей машине вплотную.", "type": "Shotgun", "size": "Big"},
        "Rapier": {"name": "Рапира", "desc": "Дальнобойная пушка калибра 23 мм является серьёзным оружием в умелых руках.", "type": "Explosive", "size": "Big"},
        "Rainmetal": {"name": "Рейнметалл", "desc": "Скорострельная пушка калибра 20 мм - прекрасный выбор для охоты на двуногого зверя.", "type": "Firearm", "size": "Big"},
        "Omega": {"name": "Омега", "desc": "Если враг пытается взять вас не умением, а числом, то эта пушка как раз для такого случая.", "type": "Artillery", "size": "Big"},
        "Elephant": {"name": "Слон", "desc": "Весьма достойный плазмомёт. Во всяком случае, никто из противников не жаловался.", "type": "Plasma", "size": "Big"},
    }

    GunTypeName = {
        "Firearm": "Огнестрельное",
        "Shotgun": "Дробовик",
        "Plasma": "Плазма",
        "Energy": "Энергетическое",
        "Artillery": "Артиллерия",
        "Rocket": "Ракетница",
        "Explosive": "Взрывное",
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

    CarMaxHeals = { 
        "Van": 15, 
        "Molokovoz": 20, 
        "Ural": 25, 
        "Belaz": 30, 
        "Mirotvorec": 35 
    }

    battle_heal_prices = {
        "Van": 48,
        "Molokovoz": 84,
        "Ural": 113,
        "Belaz": 141,      
        "Mirotvorec": 197 
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
        "Maxim": {
            "name": "Максим",
            "desc": "Малый импульсный лазер, несмотря на небольшую мощность, прожигает насквозь почти любую броню.",
            "icon": "gui/townmenu/items/maxim.png",
        },
        "Fagot": {
            "name": "Фагот",
            "desc": "Заряд плазмы, посылаемый этим оружием, летит с небольшой скоростью, но при удачном попадании может буквально испепелить противника.",
            "icon": "gui/townmenu/items/fagot.png",
        },
    }

    car_descriptions = {
        "Van": "Только самые беспечные или отчаянные торговцы рискуют отправляться в рейс на такой машине. Всего одна слабая пушка и почти полное отсутствие брони лишь частично компенсируются высокой мобильностью.",
        "Molokovoz": "Легкий грузовик, любимый богатыми фермерами и скупыми торговцами за прекрасное соотношение цены и качества. Однако профессионалы недолюбливают эту недостаточно безопасную модель.",
        "Ural": "Те, кто преуспел – выбирают Урал за отличный баланс грузоподъемности и вооружения. Самый быстрый из тяжелых грузовиков вывезет вас из любой передряги."
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
        "Maxim": 13300,
        "Fagot": 12750,
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
        "Maxim": 13300,
        "Fagot": 12750,
    }

    CarPrices = {
        "Van": 1401,
        "Molokovoz": 6501,
        "Ural": 31001,
        "Belaz": 170001,
        "Mirotvorec": 360001,
    }

    CarSellPrices = {
        "Van": 701,
        "Molokovoz": 3251,
        "Ural": 15501,
        "Belaz": 47405,
        "Mirotvorec": 180001,
    }

    def buy_weapon_with_old_handling(weapon_name):
        addedg = None
        sell_price = 0

        if weapon_name in smallweapon_prices:
            price = smallweapon_prices[weapon_name]
        elif weapon_name in bigweapon_prices:
            price = bigweapon_prices[weapon_name]
        else:
            renpy.notify("Ошибка: цена оружия не найдена.")
            return

        if player_config.money >= price:
            player_config.money -= price

            if player_config.current_gun not in player_config.inventory:
                addedg = player_config.try_add_item(player_config.current_gun)
            
                if not addedg:
                    if player_config.town_type == "City":
                        sell_price = ItemPricesCity.get(player_config.current_gun, 0)
                    else:
                        sell_price = ItemPricesVillage.get(player_config.current_gun, 0)

                    player_config.add_money(sell_price)

            player_config.current_gun = weapon_name

            weapon_data = GunDatabase.get(weapon_name)
            if weapon_data:
                player_config.gun_type = weapon_data.get("type")
            else:
                player_config.gun_type = None

            renpy.sound.play("audio/sfx/coins.wav", channel="sellitem")
            if not addedg:
                renpy.notify(f"Вы купили {gun_names.get(weapon_name, weapon_name)} за {price} монет.\nИнвентарь полон. Старое оружие было продано за {sell_price} монет.")
            else:
                renpy.notify(f"Вы купили {gun_names.get(weapon_name, weapon_name)} за {price} монет.")
        else:
            renpy.notify("Недостаточно денег!")

    def buy_car_with_exchange(car_name):
        car_price = CarPrices.get(car_name, 0)
        sell_price = CarSellPrices.get(player_config.car, 0) if player_config.car else 0
        actual_cost = car_price - sell_price

        if actual_cost > 0:
            if not player_config.spend_money(actual_cost):
                renpy.notify("Недостаточно денег!")
                return
        elif actual_cost < 0:
            player_config.add_money(-actual_cost)

        if car_name in ["Molokovoz", "Van"]:
            if player_config.current_gun and player_config.current_gun in bigweapon_prices:
                weapon_to_handle = player_config.current_gun
                
                if player_config.try_add_item(weapon_to_handle):
                    player_config.current_gun = "Hornet"
                else:
                    if player_config.town_type == "City":
                        sell_price_weapon = ItemPricesCity.get(weapon_to_handle, 0)
                    else:
                        sell_price_weapon = ItemPricesVillage.get(weapon_to_handle, 0)
                    
                    player_config.add_money(sell_price_weapon)
                    player_config.current_gun = "Hornet"
                    renpy.notify(f"{gun_names.get(weapon_to_handle, weapon_to_handle)} было продано за {sell_price_weapon} монет (нет места в инвентаре).")

        player_config.car = car_name
        new_max_hp = CarHP.get(car_name, 850)

        player_config.max_hp = new_max_hp
        player_config.hp = new_max_hp

        new_max_heal = CarMaxHeals.get(car_name, 15)
        player_config.max_heals = new_max_heal
        player_config.heals = new_max_heal
        
        if car_name == "Ural":
            player_config.big_gun_install = "Possible"
        elif car_name in ["Molokovoz", "Van"]:
            player_config.big_gun_install = "NotPossible"
            
        if actual_cost > 0:
            renpy.notify(
                f"Куплена машина: {car_names.get(car_name, car_name)} "
                f"за {actual_cost} монет."
            )
        else:
            renpy.notify(
                f"Куплена машина: {car_names.get(car_name, car_name)} "
                f"(получено {-actual_cost} монет сверху)."
            )
        
        renpy.sound.play("audio/sfx/coins.wav", channel="sellitem")

    def repair_car():
        if player_config.hp < player_config.max_hp:
            hp_to_repair = player_config.max_hp - player_config.hp
            repair_cost = int(hp_to_repair * 0.75)

            if player_config.money >= repair_cost:
                player_config.spend_money(repair_cost)
                player_config.hp = player_config.max_hp
                renpy.notify(f"Вы отдали {repair_cost} монет")
                renpy.sound.play("audio/sfx/coins.wav", channel="sellitem")
            else:
                renpy.notify("Недостаточно денег для ремонта!")
        else:
            renpy.notify("Машина не нуждается в ремонте")

    def buy_heals():
        heals_needed = player_config.max_heals - player_config.heals

        if heals_needed <= 0:
            renpy.notify("У вас уже максимум лечений.")
            return

        price_per_heal = battle_heal_prices.get(player_config.car, 48)
        heal_cost = heals_needed * price_per_heal

        if player_config.money < heal_cost:
            renpy.notify("Недостаточно денег!")
            return

        player_config.spend_money(heal_cost)
        renpy.notify(f"Вы отдали {heal_cost} монет")
        player_config.heals = player_config.max_heals
        renpy.sound.play("audio/sfx/coins.wav", channel="sellitem")

    def get_lowhealincs():
        percent = player_config.hp / float(player_config.max_hp)
        if percent < 0.15:
            return "gui/bossbar/redlight_hp.png"
        else:
            return "gui/bossbar/redlight_blank.png"

    def get_lowhealamountincs():
        percent = player_config.heals / player_config.max_heals
        if percent < 0.30:
            return "gui/bossbar/redlight_fuel.png"
        else:
            return "gui/bossbar/redlight_blank.png"

    def get_region_driving_tracks():
        region = player_config.current_region
        return driving_tracks_by_region.get(region, ["driving1", "driving2"])

    def generate_random_weapons():
        global shop_random_weapons, shop_random_city, shop_random_big_gun_state

        current_city = player_config.town_name
        current_big_gun_state = player_config.big_gun_install

        if (shop_random_city == current_city and 
            shop_random_weapons is not None and 
            shop_random_big_gun_state == current_big_gun_state):
            return

        all_weapons = list(smallweapon_prices.keys())
        if player_config.big_gun_install == "Possible":
            all_weapons += list(bigweapon_prices.keys())

        if current_city not in ["Мидгард", "Ольм"]:
            all_weapons = [w for w in all_weapons if w not in ["Fagot", "Maxim"]]

        if len(all_weapons) == 0:
            shop_random_weapons = []
            return

        count = random.randint(2, len(all_weapons))

        shop_random_weapons = random.sample(all_weapons, count)

        shop_random_city = current_city
        shop_random_big_gun_state = current_big_gun_state

    def process_battle_loot(drops):
        drop_names_text = []
        dropped_something = False
        items_not_added = 0

        for drop_id, drop_name in drops:
            if player_config.try_add_item(drop_id):
                drop_names_text.append(drop_name)
                dropped_something = True
            else:
                items_not_added += 1

        region = player_config.current_region
        if region == "r1m1":
            money_drop = random.randint(50, 150)
        elif region == "r1m2":
            money_drop = random.randint(100, 250)
        elif region == "r1m3":
            money_drop = random.randint(150, 350)
        elif region == "r1m4":
            money_drop = random.randint(300, 600)
        else:
            money_drop = random.randint(50, 150)

        if items_not_added > 0:
            compensation = items_not_added * random.randint(100, 200)
            money_drop += compensation
            renpy.say(None, f"В вашем инвентаре не хватает места! Получено: {compensation} монет")

        player_config.add_money(money_drop)

        if dropped_something:
            drop_list = ", ".join(drop_names_text)
            renpy.say(None, f"Найдены следующие предметы: {drop_list}.\nТакже получено {money_drop} монет.")
        else:
            renpy.say(None, f"Найдено: {money_drop} монет.")


default player_config = PlayerConfig()

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

    $ player_config.max_hp = CarHP.get(player_config.car, CarHP["Van"])

    if player_config.hp is None:
        $ player_config.hp = player_config.max_hp

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = f"randomenemy{enemyint}"
    $ player_hp = player_config.hp
    $ player_max_hp = player_config.max_hp
    $ enemy_damage_multiplier = 1.0

    if player_config.current_region == "r1m1":
        $ enemy_hp = random.randint(80, 150)
    elif player_config.current_region in ("r1m2", "r1m3"):
        $ enemy_hp = random.randint(120, 200)
    elif player_config.current_region == "r1m4":
        $ enemy_hp = random.randint(180, 300)

    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = player_config.heals
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ bgname = f"bg_{player_config.current_region}_randomfight"
    $ EnemyType = "Regular"

    $ renpy.scene()
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
        $ player_config.hp = player_hp
        $ player_config.heals = remainheals

        play sound "sfx/explosion04.wav"
        $ renpy.hide(enemy_image) 
        with dissolve

        $ drops = player_config.get_random_drops()

        if drops:
            python:
                process_battle_loot(drops)

            if persistent._prebattle_music:
                $ renpy.music.play(persistent._prebattle_music, channel="music", fadeout=1.0)
            else:
                $ allowed_tracks = get_region_driving_tracks()
                $ renpy.music.play(renpy.random.choice(allowed_tracks), channel="music", fadeout=1.0)
                
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

label demofinished:
    call screen onebuttonpopup("Демо-версия завершена.\nСпасибо за игру!")

    if not config.developer:
        pause 1.0

        $ slides = ["loading_1", "loading_2", "loading_3", "loading_4", "loading_5", "loading_6"]
        python:
            for i in range(len(slides)):
                renpy.show(slides[i])
                renpy.pause(pauses[i], hard=True)
                renpy.hide(slides[i])

    return