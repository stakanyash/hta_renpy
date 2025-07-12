label arrivetor1m2:

    $ persistent.current_script = "r1m2"
    
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
            $ CurrentGun = "Hornet"
            jump attackforloot

        "Двигаться дальше в Восточное":
            $ renpy.save("checkpoint-6")
            $ CurrentGun = "Hornet"
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
    if CurrentGun == "Storm":
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

    play music "music/bar.ogg" fadeout 1.0

    scene bg_vostochnoe with fade

    "Приехав в Восточное вы не знаете к кому обратиться."
    show hose at left with dissolve
    "Однако замечаете человека, похожего на фермера и решаете подойти к нему."
    "Но он с ходу на вас бросается..."

    unknown "Сразу видать, нездешний."

    "Поняв, что \"дружеского\" приветствия не получится вы решаете сразу перейти к делу."

    show mchar at right with dissolve

    mc "Мне нужен Бен Дроссель!"

    hide hose
    show hose at left, stretch_in

    hose "Я Хосе, а не Бен Дроссель. Мне какое дело?"

    hide mchar
    show mcsurp at right, stretch_in

    mc "Прости, ты всем так хамишь или у меня просто внешность располагающая?"
    mc "Ты не смотри, что я хлипкий, драться мне приходилось, и не раз!"

    "Хосе немного успокаивается."

    hose "Не кипятись. Просто столько всякого сброда вокруг… Кто этот твой друг?"

    mc "Бен Дроссель, исследователь."

    hose "То-то я гляжу, ты странный какой-то. С колдунами якшаться."

    mc "С колдунами?"

    hide hose
    show hose at left, stretch_in

    hose "Не прикидывайся. Все знают, что исследователи твои с нечистым водятся и черти им помогают. Потому-то они селятся на отшибе."

    mc "Значит, знаешь, где искать!"

    hose "Этих-то у нас в округе давно не видно было. А вот ведьма одна живет в одной из дальних деревень. Может, она подскажет. Ты уж не серчай на меня."

    mc "Ладно, не бойся. Не стану на тебя чертей натравливать."
    mc "На этот раз!"

    hide hose with dissolve
    hide mcsurp with dissolve

    jump tolocus

label tolocus:

    scene bg_locus with fade
    play music "music/town2.ogg" fadeout 1.0

    "Приехав в Локус и узнав о том, где искать загадочную женщину вы подходите к её двери и стучите."
    "Спустя несколько секунд дверь открывается."

    show oldwoman at right with dissolve
    oldwoman "Чую нерусский дух!"

    "Вы в замешательстве и с языка слетает лишь..."

    show mc6 at left with dissolve

    mc "Ты ведьма?"

    "Старуха явно рассердилась от такого вопроса..."

    hide oldwoman
    show oldwoman at right, stretch_in

    oldwoman "Ах ты невежа!"
    oldwoman "Сказок наслушался!"

    "Вы пытаетесь уладить ситуацию."

    mc "Простите, бабушка, я не со зла. Я ищу Бена Дро…"

    hide oldwoman
    show oldwoman at right, stretch_in

    oldwoman "Теперь ещё и бабушка!"
    oldwoman "Почему я вообще с тобой разговариваю?"
    oldwoman "Бена он ищет. Не знаю мерзавца и знать не желаю!"
    oldwoman "..."
    oldwoman "Хотя ладно. Сколько воды утекло…"
    oldwoman "В последний раз я его видела в Мидгарде. Там и ищи. В музее."

    mc "Спасибо огромное..."
    hide oldwoman with dissolve

    mc "Странная она какая-то... Ладно, надо ехать в Мидгард."

    hide mc6 with dissolve

    jump tomidgard

label tomidgard:

    scene bg_midgard with fade
    play music "music/town3.ogg" fadeout 1.0

    "Терпим."

    # Temporary
    return