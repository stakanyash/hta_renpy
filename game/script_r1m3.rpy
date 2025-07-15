# TODO: Make a video cutscene when leaving to r1m2 (high priority) and r1m1 (middle priority)

# Default start-up

label vaterlandfirst:
    if LisaAgreed == "True":
        jump r1m3withlisa
    elif LisaAgreed == "False":
        jump r1m3nolisa

# Without Lisa route

label r1m3nolisa:

    play music "music/driving1.ogg" fadeout 1.0
    scene bg_m3nolisa with fade

    "Оказавшись в Фатерлянде вы продолжили ехать в сторону Пешта."

    scene bg_pesht with dissolve

    "Однако около ворот Пешта вас останавливают..."

    show pguard at left with dissolve

    unknown "Куда едешь? Не видишь: закрыто!"

    show mchar at right with dissolve

    mc "Что здесь происходит? Почему все носятся как угорелые? Пожара вроде не видно? И кто вы такой?"

    pguard "Я охранник Пешта. Бандиты, наконец, вскрыли нижние этажи военной базы и добыли себе мощное оружие."
    pguard "Мы думали, они просто пугали нас этой базой, чтобы увеличить поборы, а теперь даже убежать не успеем. Если ничего не предпринять, они захватят наш славный город."

    mc "Да, непросто вам приходится…"
    mc "Кстати, не подскажете, как проехать на северо-восток?"

    pguard "Туда только две дороги: через наш город или через само логово бандитов!"

    "Вы понимаете, что ситуация безысходная, но пытаете \"счастья\" ещё раз."

    mc "Так пропустите меня?"

    pguard "Нет. Сейчас город закрыт. Мы переходим в глухую оборону. Пока не решится проблема с бандитами, город находится на военном положении."

    mc "Что же делать?"

    hide pguard
    show pguard at left, stretch_in

    pguard "Взорви мост."

    "Вы ошарашены от услышанного."

    hide mchar
    show mcsurp at right, stretch_in

    mc "Чего?! Какой ещё мост?"

    pguard "Тот, через который идёт дорога на военную базу. Если мост взорвать, то до нашего города врагу не добраться."

    mc "И как же я могу это сделать?"

    pguard "Прежде всего, нужно найти взрывчатку. В Асгарде должно быть что-то похожее. Они же всё-таки горняки."
    pguard "А потом придётся заложить заряд на мосту. Он, конечно охраняется… Но ты справишься!"

    hide pguard with dissolve

    mc "А у самих-то что, ноги отсохли? Трусы…"

    hide mcsurp with dissolve

    jump asgardboom

label asgardboom:

    play music "music/town1.ogg" fadeout 1.0
    scene bg_asgard with fade

    "Приехав в Асгард вы быстро находите магазин взрывчатки."

    show seller at left with dissolve

    seller "Добро пожаловать в Асгард!"

    show mc5 at right, stretch_in

    mc "Срочно нужна взрывчатка! Вопрос жизни и смерти!"

    seller "В принципе, Вы пришли в правильное место, чтобы купить взрывчатые вещества."
    seller "Это специальность нашего магазина, как видно по его названию. Люди со всего света приезжают сюда, чтобы приобрести наш замечательный продукт."
    hide seller
    show seller at left, stretch_in
    seller "Но в данный момент мы испытываем некоторые производственные трудности."
    seller "Так что в течение следующих 12 дней мы не сможем предоставить даже самое небольшое количество продукта. Взрывчатка пользуется бешеной популярностью в последнее время."

    hide mc5
    show mcsurp at right, stretch_in

    mc "Но мне очень нужно!"

    "Продавец явно задумался."

    seller "Исключительно из соображений человеколюбия я сообщу Вам, что продукт гораздо худшего качества, чем наш, можно приобрести в шахтёрском посёлке. Похоже, они нашли старый склад."

    mc "Спасибо!"

    hide seller
    hide mcsurp

    jump mvillage

label mvillage:

    play music "music/bar.ogg" fadeout 1.0
    scene bg_mvillage with fade

    "Не успели вы приехать, как вас сразу встречают."

    show miner at left with dissolve

    miner "Какими судьбами?"

    show mc5 at right with dissolve

    mc "Мне сказали, что у вас есть запас взрывчатки."

    miner "Не тебе одному она нужна."
    miner "..."
    hide miner
    show miner at left, stretch_in
    miner "Опять эти бандиты нападают!"

    hide mc5
    show mcsurp at right, stretch_in

    mc "Где?"

    miner "Все на стены. Враг не пройдёт! Слушай, если тебе нужна взрывчатка, помогай её защищать!"

    hide miner with dissolve

    mc "Опять двадцать пять. Ни дня без боя, что за жизнь!"

    hide mcsurp

    play music "music/battle1.ogg"

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ boss_image = "minerattackers"
    $ player_hp = 1500
    $ player_max_hp = player_hp
    $ boss_hp = 2000


    # Amount of heals increased because high enemy HP
    if CurrentGun == "Storm":
        $ damage_range = (0.005, 0.02)
        $ max_heals = 15
    elif CurrentGun == "PKT":
        $ damage_range = (0.005, 0.0188)
        $ max_heals = 25
    elif CurrentGun == "Kord":
        $ damage_range = (0.005, 0.0195)
        $ max_heals = 20
    else:
        $ damage_range = (0.005, 0.0175)
        $ max_heals = 25
    
    $ turn_count = 0
    $ boss_max_hp = boss_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ boss_name = "Бандиты"
    $ bgname = "bg_mvillage_fight"
    scene bg_mvillage_fight
    show minerattackers at center

    while boss_hp > 0 and player_hp > 0:
        call screen boss_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide minerattackers
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
        hide minerattackers with dissolve

        jump mvillageafterfight

label mvillageafterfight:

    scene bg_mvillage with dissolve
    play music "music/bar.ogg" fadeout 1.0

    show miner at left with dissolve
    show mchar at right with dissolve

    miner "Спасибо за помощь! После такого отпора они долго к нам не сунутся."
    miner "Что тебе нужно было? Взрывчатка?"
    miner "Да бери сколько нужно! Для хорошего человека не жалко."

    mc "Вот и хорошо…"

    hide miner with dissolve
    hide mchar with dissolve

    jump brigdedestroy

label brigdedestroy:

    scene bg_nearbridgeenemy with fade
    play music "music/alarm2.ogg" fadeout 1.0

    "Подъехав к мосту вы заметили бандитские машины."
    mc "Видимо, чтобы осуществить свою задачу нужно их уничтожить, но куда деваться..."

    play music "music/battle2.ogg"

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ boss_image = "brigde_defender"
    $ player_hp = 1500
    $ player_max_hp = player_hp
    $ boss_hp = player_hp


    if CurrentGun == "Storm":
        $ damage_range = (0.005, 0.02)
        $ max_heals = 10
    elif CurrentGun == "PKT":
        $ damage_range = (0.005, 0.0188)
        $ max_heals = 20
    elif CurrentGun == "Kord":
        $ damage_range = (0.005, 0.0195)
        $ max_heals = 15
    else:
        $ damage_range = (0.005, 0.0175)
        $ max_heals = 20
    
    $ turn_count = 0
    $ boss_max_hp = boss_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ boss_name = "Бандиты"
    $ bgname = "bg_nearbridge"

    scene bg_nearbridge
    show brigde_defender at center

    while boss_hp > 0 and player_hp > 0:
        call screen boss_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide brigde_defender
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
        hide brigde_defender with dissolve

        stop music fadeout 1.0
        jump BOOOM


label BOOOM:
    scene bg_bandbridge with fade

    mc "Ну что-же пора браться за дело..."

    stop sound

    $ renpy.movie_cutscene("movies/r1m3/bridge_destroy.mp4")

    scene bg_bandbridge_down

    play music "music/driving2.ogg"

    mc "Мост взорван. Можно возвращаться."

    "Вы выдвинулись обратно в сторону Пешта."

    jump peshtallow

label peshtallow:

    scene bg_pesht with fade

    show pguard at left with dissolve

    pguard "Справился?"

    show mc5 at right with dissolve

    mc "Больше бандиты этой дорогой не пройдут."

    "Вам открыли ворота и вы проехали через Пешт."

    hide pguard
    hide mc5

    jump minin1st_nl

label minin1st_nl:

    scene bg_minin with fade

    "..."

    # Temporary return
    return

# With Lisa route