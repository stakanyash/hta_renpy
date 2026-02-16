label arrivetor2m1:
    if not config.developer:
        pause 0.5

        show bg_r2m1load at truecenter

        $ level_slides = ["loadinglvl0","loadinglvl1","loadinglvl2","loadinglvl3","loadinglvl4","loadinglvl5","loadinglvl6"]

        call show_loading(level_slides) from _call_show_loading_1

        scene black

    $ _game_menu_screen = "save_screen"
    $ _menu = True
    $ config.keymap['save'] = ['save']
    $ config.keymap['load'] = ['load']
    $ config.keymap['game_menu'] = ['game_menu']
    $ persistent._in_battle = False

    $ renpy.notify("Игра сохранена в слот 2.")
    $ renpy.save("checkpoint-2")

    play music "music/QuietDialogue02.ogg" fadeout 0.5

    $ player_config.current_region = "r2m1"

    scene bg_librium with fade

    if LisaAgreed == True:
        mc "Далеко же я забрался..."
        mc "Не время любоваться красотами! Надо скорее связаться с местными."
        mc "А вот и они."

        mc "День добрый. Я ищу Акселя. Вы не слышали про такого?"
        unknown "Аксель - это величайший из живущих, наш вождь и кормилец, альфа и омега! Он ведет нас к победе добра и справедливости во всем мире!"
        mc "Ничего себе... Сразу видно – большой человек."
        mc "Могу ли я повстречаться с этим «кормильцем»?"

        unknown "Так ты что, не агитатор?"
        unknown "Черт, я уж подумал, что тебя к нам подослали проверить боевой дух. Хотя мне бояться нечего. Я честный вояка!"
        mc "Я много наслышан о вашем лидере. И очень хотел бы пожать его мужественную руку."
        unknown "Кто попало не может с ним встретиться. Только тот, кто совершит подвиг, будет допущен в его тайное жилище. Но тебе это явно не грозит."
        mc "Пожалуй, я все-таки попытаюсь попасть туда. Раз вы ничего не знаете, поищу тех, кто может мне помочь."
        
        unknown "Постой, а кто ты вообще такой? Как ты проехал через тоннель?"
        mc "А твое какое дело? Я свободный бродяга: куда хочу, туда лечу!"
        unknown "Я защищаю свой народ от таких, как ты: шпионов и провокаторов!"

        $ randommus = random.choice([6, 3])
        $ renpy.music.play(f"audio/music/battle{randommus}.ogg", channel='music')

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
        $ enemy_image = "r2m1tunnelfirste"
        $ player_hp = player_config.hp
        $ player_max_hp = player_config.max_hp
        $ enemy_hp = 850
        $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
        $ max_heals = player_config.heals
        $ turn_count = 0
        $ enemy_max_hp = enemy_hp
        $ heal_count = 0
        $ remainheals = max_heals - heal_count
        $ attack_locked = False
        $ enemy_name = "???"
        $ bgname = "bg_librium"
        $ EnemyType = "Regular"
        $ enemy_damage_multiplier = 1.0

        scene bg_librium
        show r2m1tunnelfirste at center

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
            
            hide r2m1tunnelfirste
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

            hide r2m1tunnelfirste with dissolve

            mc "Эти бандиты больше не будут мешать торговцам."
            mc "Осталось сообщить в Ольм об освобождении склада."

            jump r1m4SideQuest_finish