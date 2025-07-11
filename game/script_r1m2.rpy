label arrivetor1m2:
    
    scene bg_ridzin with fade

    "Приехав в соседний регион вы оказались в замешательстве."
    mc "А где тут вообще находится Восточное?.."
    mc "Поеду дальше по дороге, надеюсь сориентируюсь."
    scene bg_razvyazka with dissolve
    "Вы доехали до первой развязки и вновь задумались."
    mc "Так. А здесь то куда?"
    mc "Прямо вроде \"тупик\". Значит нужно поехать направо."
    scene bg_loot with dissolve
    play music "music/alarm2.ogg"
    "Однако впереди вы замечаете лежащий в развалинах ящик."
    mc "Там может быть что-то полезное..."
    mc "Однако он охраняется..."

    menu:
        "Атаковать охранника":
            $ renpy.save("checkpoint-6")
            $ AttackForLoot = "True"
            jump attackforloot

        "Двигаться дальше в Восточное":
            $ renpy.save("checkpoint-6")
            $ AttackForLoot = "False"
            jump movetovostochnoe

label attackforloot:
    play music "music/battle2.ogg"
    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ boss_image = "lootdefender"
    $ player_hp = 850
    $ player_max_hp = player_hp
    $ boss_hp = 400
    if TakeGunFromZaimka == "True":
        $ damage_range = (0.005, 0.02)
        $ max_heals = 10
    else:
        $ damage_range = (0.005, 0.0175)
        $ max_heals = 20
    $ turn_count = 0
    $ boss_max_hp = boss_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ boss_name = "Бандит"
    scene bg_fightforloot
    show lootdefender at center

    while boss_hp > 0 and player_hp > 0:
        call screen boss_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide lootdefender
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
        hide lootdefender with dissolve

        jump defeateddefender

label defeateddefender:

    mc "Посмотрим, что в этом ящике..."
    $ randomgun = random.randint(1, 3)

    if randomgun == "1":
        "Вы нашли оружие \"Корд\"!"
        $ CurrentGun = "Kord"
    elif randomgun == "2":
        "Вы нашли оружие \"ПКТ\"!"
        $ CurrentGun = "PKT"
    else:
        "Вы нашли оружие \"Шторм\"!"
        $ CurrentGun = "Shtorm"

    mc "О, то что нужно!"
    mc "Пора таки двигаться в Восточное."

    jump movetovostochnoe

label movetovostochnoe:

    "Больше пока ничего нет. Терпим."

    return