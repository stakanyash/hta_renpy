# Without Lisa route

label firsthel_nl:

    $ CurrentRegion = "r1m4"

    scene bg_helfirst with fade
    play music "music/driving7.ogg" fadeout 1.0

    "Приехав в Хель вы сразу направились в Ольм."

    scene bg_olm with dissolve

    "В Ольме вы решили начать поиски Гомера."

    show olmeper at right with dissolve

    perchitto "Ещё один с большой земли пожаловал."

    show mc6 at left, stretch_in

    mc "Приветствую вас, труженики моря!"

    perchitto "И тебе того же. А причём тут море?"

    "Вы немного в недоумении."

    mc "Ну, это же рыбацкий поселок, так?"

    perchitto "Но-но, полегче. Ты находишься в столице свободного края! Оглянись, ты море видишь?"

    mc "Признаться, нет. Простите, если задел ваши патриотические чувства."
    mc "Я ищу старика Гомера. Не знаете такого?"

    perchitto "Кто же этого болтуна не знает. Вечно напьётся и пристаёт ко всем со своими байками."

    mc "Так где же мне его искать?"

    perchitto "Попробуй один из рыбацких поселков."
    perchitto "И не смотри так: все остальные здешние поселения, кроме нашего, - это именно рыбацкие поселки. Но мы не такие."

    mc "Конечно, ничего общего! Спасибо, поеду искать."

    hide olmeper with dissolve

    mc "Интересно получается. Все значит тут рыбаки, а они - нет? Странно."

    "Вы начали искать Гомера в рыбацких посёлках."

    scene bg_lauka with fade

    "В Лауке его нет."

    scene bg_kalis with fade

    "В Калисе тоже..."

    mc "Мне что, придётся весь регион объездить в его поисках?!"

    scene bg_kordan with fade

    "В Кордане его так-же не оказалось."

    mc "Да где его искать то?!"

    show matvey at left, stretch_in

    matvey "Кого ищешь?"

    show mcsurp at right with dissolve

    mc "Гомера."

    matvey "Ну это я не знаю. Он может быть где угодно. Лучше садись и выпей со мной рюмочку ананаги."

    mc "Если ты меня угостишь, то не откажусь."

    hide matvey
    show matvey at left, stretch_in

    matvey "Хех! Чего захотел. Плати сам, халявщик."

    mc "Ну и пей сам свою ананагу."

    hide matvey with dissolve

    mc "Осталось только одно место, где я ещё не был..."

    hide mcsurp
    
    play music "music/bar.ogg" fadeout 1.0
    scene bg_saliniom with fade

    "Приехав в Салиниом вы подходите к человеку, который подходит под описание Гомера."

    show homer at left with dissolve

    homer "Не каждый день видишь здесь новые лица."

    show mchar at right with dissolve

    mc "День добрый! Не подскажешь, где я могу найти Гомера?"

    homer "Ну, предположим, что я Гомер. Что тогда?"

    mc "Тогда я поставлю тебе стаканчик-другой и выслушаю одну из твоих знаменитых историй."

    homer "Это мне по душе! Что именно ты хочешь узнать?"

    hide mchar
    show mc7 at right, stretch_in

    mc "Бармен! Налей чего-нибудь покрепче моему другу!"
    hide mc7
    show mcsurp at right, stretch_in
    mc "Итак, Гомер, расскажи о том загадочном месте, в котором ты побывал, а больше никто так и не смог найти."

    hide homer
    show homer at left, stretch_in

    homer "Дело не в том, что найти никто не смог, а в том, что уйти живым оттуда трудно. Да и мало кто в такую глушь сунется. Один я такой любопытный."

    mc "Ближе к делу."

    homer "Не торопи."
    homer "Так вот, за западным болотом есть сеть ущелий. Если не заплутаешь, то скоро окажешься на берегу моря."
    homer "И вот там-то и ждёт напасть: здоровенная махина, дымит, зубами лязгает, жуть, да и только! Еле-еле удалось мне спастись, и только потому, что я был там ночью."
    homer "Вот такая история."

    hide mcsurp
    show mchar at right, stretch_in

    mc "Чушь какая. И ради этого дурацкого рассказа я столько километров проехал?"

    hide homer
    show homer at left, stretch_in

    homer "Обижаешь, начальник. Во-первых, это всё правда!"
    homer "Во-вторых, не станет такое чучело просто так дымить: что-то оно там охраняет."
    homer "А в-третьих, есть ещё один момент: только я один знаю место, где твой грузовик сможет по болоту проехать."

    hide mchar
    show mcsurp at right, stretch_in

    mc "Прости, что я вспылил: очень уж нервная у меня жизнь в последнее время."
    mc "Мне нужно проверить, что охраняет твой монстр. Подскажи, где проезд через болото?"

    homer "Эх, доброе у меня сердце."
    homer "Особенно после пары стаканчиков."
    homer "Вот в этом месте - сухое дерево, прямо напротив него - мелкое место. Только будь осторожнее."

    mc "Спасибо, добрый человек."

    hide homer with dissolve
    hide mcsurp with dissolve

    "Вы поехали к месту, указанному Гомером."

    jump tokranfight

label tokranfight:

    play music "music/bio05.ogg" fadeout 1.0
    scene bg_boloto with fade
    "Подъехав к болоту у вас возникли некоторые опасения."

    mc "Похоже, именно об этом месте и говорил Гомер. Точно ли я тут смогу проехать?"
    mc "Ладно, не попробуешь - не узнаешь..."

    scene bg_boloto_1 with dissolve

    mc "Старик не обманул, под слоем жижи было твёрдое дно."

    scene bg_boloto_2 with dissolve

    mc "Интересно, что ждёт меня по эту сторону?"

    scene black with fade

    $ renpy.movie_cutscene("movies/r1m4/bosskran.mp4")

    play sound "audio/sfx/stand1_boss02.wav" channel "sfx2"
    play music "music/intensedialogue01.ogg"
    scene bg_kran with fade
    
    mc "О господи! Это что ещё за...?"
    mc "Зачем только людям древности нужны были такие машины?"
    mc "Этот монстр охраняет проезд к Морским Вратам."
    mc "Мне нужно как-то справиться с ним..."

    scene black with fade

    play music "music/battle01.ogg" fadeout 1.0

    scene bg_kranfight with fade

    pause 0.5

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "kranboss"
    $ player_hp = 1500
    $ player_max_hp = player_hp
    $ enemy_hp = player_hp * 2
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 20
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Кран"
    $ bgname = "bg_kranfight"
    $ EnemyType = "Boss"
    $ BossIcon = "boss1.png"
    show kranboss at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide kranboss
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
        hide kranboss with dissolve
        stop sfx2 fadeout 1.0

        scene bg_bosskran_dead

        mc "Чудище повержено. Пора двигаться дальше."

        jump leaveregion1

label leaveregion1:

    play music "music/bio02.ogg" fadeout 1.0

    # cargo3 bg's doesn't show for some reason...

    if CurrentCargo == "Box":
        scene bg_leaver1_cargo3_1 with fade
    else:
        scene bg_leaver1_cargo1_1 with fade

    mc "Это то самое место, которое указал Гомер, но я не вижу никаких врат."
    mc "Неужели всё зря?!"

    pause 0.5

    if CurrentCargo == "Box":
        scene bg_leaver1_cargo3_2 with dissolve
    else:
        scene bg_leaver1_cargo1_2 with dissolve

    mc "Что это лезет из-под воды? Покой нам только снится..."
    mc "Только прикончил одного монстра, как второй на подходе..."
    mc "Впрочем, этот поспокойнее будет."

    play sound "sfx/boat_open.wav"
    play sound "sfx/boat_motor_loop_mono.wav" channel "sfx2"

    pause 0.5

    if CurrentCargo == "Box":
        scene bg_leaver1_cargo3_3 with dissolve
    else:
        scene bg_leaver1_cargo1_3 with dissolve

    mc "Похоже, он приглашает меня к себе в пасть. Так это же и есть Морские Врата!"
    mc "В животе чудища я и доплыву до Оракула."

    pause 0.5

    if CurrentCargo == "Box":
        scene bg_leaver1_cargo3_4 with dissolve
    else:
        scene bg_leaver1_cargo1_4 with dissolve

    mc "Страшно, конечно..."
    mc "Ну, терять мне нечего. Только вперёд!"

    scene black with fade

    "Конец первой главы."

    return

# With Lisa route