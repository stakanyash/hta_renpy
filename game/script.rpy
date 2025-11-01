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
        buy_weapon_with_old_handling(weapon_name)
        renpy.set_screen_variable("selected_shop_item", None)

    def UpdateTownInfo(town_type, town_name, group_logo):
        global TownType, TownName, GroupLogo
        TownType = town_type
        TownName = town_name
        GroupLogo = group_logo

    def buy_weapon_with_old_handling(weapon_name):
        price = smallweapon_prices.get(weapon_name) or bigweapon_prices.get(weapon_name)
        
        if CurrentMoney >= price:
            old_weapon = CurrentGun
            
            store.CurrentGun = weapon_name
            store.CurrentMoney -= price
            
            message = f"Куплено: {gun_names.get(weapon_name, weapon_name)}"
            
            if old_weapon and old_weapon != "None":
                if not try_add_item(old_weapon):
                    if TownType == "City":
                        sell_price = ItemPricesCity.get(old_weapon, 0)
                    else:
                        sell_price = ItemPricesVillage.get(old_weapon, 0)
                    
                    store.CurrentMoney += sell_price
                    message += f"\nИнвентарь полон! Старое оружие продано за {sell_price} монет"
                else:
                    message += "\nСтарое оружие добавлено в инвентарь"
            
            renpy.notify(message)
            renpy.restart_interaction()
        else:
            renpy.notify("Недостаточно денег!")

transform stretch_in:
    yzoom 0.95
    linear 0.1 yzoom 1.0

label start:

    $ CurrentGun = "Hornet"
    $ CurrentSecondGun = None
    $ CurrentMoney = 100
    $ CurrentCar = "Van"
    $ CurrentRegion = "r1m1"

    $ TownType = None
    $ TownName = None
    $ GroupLogo = None
    
    $ FarmEnabled = None

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
        "Storm": (30, 80),
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
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    if CurrentRegion == "r1m1":
        $ enemy_hp = random.randint(80, 150)
    elif CurrentRegion == "r1m2" or CurrentRegion == "r1m3":
        $ enemy_hp = random.randint(120, 200)
    elif CurrentRegion == "r1m4":
        $ enemy_hp = random.randint(180, 300)
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
                not_added_items = []
                dropped_something = False

                for drop_id, drop_name in drops:
                    if try_add_item(drop_id) == True:
                        drop_names_text.append(drop_name)
                        dropped_something = True
                    else:
                        not_added_items.append(drop_name)

                if dropped_something:
                    drop_names_str = ", ".join(drop_names_text)
                    renpy.say(None, f"Найдены следующие предметы: {drop_names_str}")
                elif not_added_items:
                    renpy.say(None, "В вашем инвентаре не хватает места!")
                
        return

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