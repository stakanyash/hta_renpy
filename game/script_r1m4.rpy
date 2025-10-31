label r1m4start:
    $ CurrentRegion = "r1m4"

    scene bg_helfirst with fade
    play music "music/driving7.ogg" fadeout 1.0

    "Приехав в Хель вы сразу направились в Ольм."

    $ UpdateTownInfo("City", "Ольм", "north_nath_traders")
    
    play music "music/town1.ogg" fadeout 1.0
    scene bg_olm with dissolve

    if r1m4SideQuest == "CanBeGiven":
        jump galdenquest
    elif LisaAgreed == "False":
        jump homersearch

# Without Lisa route

label homersearch:

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

    $ TownType = "NotInCity"

    "Вы начали искать Гомера в рыбацких посёлках."

    if random.random() <= 0.5:
        $ randommus = random.choice([1, 2, 7])
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_21

    play music "music/driving7.ogg" fadeout 1.0
    scene bg_lauka with fade

    $ UpdateTownInfo("Village", "Лаука", "free_traders_alliance")

    "В Лауке его нет."

    scene bg_kalis with fade

    $ UpdateTownInfo("Village", "Калис", "free_traders_alliance")

    "В Калисе тоже..."

    mc "Мне что, придётся весь регион объездить в его поисках?!"

    if random.random() <= 0.5:
        $ randommus = random.choice([1, 2, 7])
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_22

    scene bg_kordan with fade

    $ UpdateTownInfo("Village", "Кордан", "free_traders_alliance")

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

    if random.random() <= 0.5:
        $ randommus = random.choice([1, 2, 7])   
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_23

    $ UpdateTownInfo("Village", "Салиниом", "free_traders_alliance")
    
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

    if random.random() <= 0.5:
        $ randommus = random.choice([1, 2, 7])
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_24

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
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = 1600
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

    if CurrentCar == "Molokovoz":
        if CurrentCargo == "Box":
            scene bg_leaver1_cargo3_1 with dissolve
        else:
            scene bg_leaver1_cargo1_1 with dissolve
    elif CurrentCar == "Ural":
        scene bg_leaver1_ural_1 with dissolve
    else:
        scene bg_leaver1_van_1 with dissolve

    mc "Это то самое место, которое указал Гомер, но я не вижу никаких врат."
    mc "Неужели всё зря?!"

    pause 0.5

    if CurrentCar == "Molokovoz":
        if CurrentCargo == "Box":
            scene bg_leaver1_cargo3_2 with dissolve
        else:
            scene bg_leaver1_cargo1_2 with dissolve
    elif CurrentCar == "Ural":
        scene bg_leaver1_ural_2 with dissolve
    else:
        scene bg_leaver1_van_2 with dissolve

    mc "Что это лезет из-под воды? Покой нам только снится..."
    mc "Только прикончил одного монстра, как второй на подходе..."
    mc "Впрочем, этот поспокойнее будет."

    play sound "sfx/boat_open.wav"
    play sound "sfx/boat_motor_loop_mono.wav" channel "sfx2"

    pause 0.5

    if CurrentCar == "Molokovoz":
        if CurrentCargo == "Box":
            scene bg_leaver1_cargo3_3 with dissolve
        else:
            scene bg_leaver1_cargo1_3 with dissolve
    elif CurrentCar == "Ural":
        scene bg_leaver1_ural_3 with dissolve
    else:
        scene bg_leaver1_van_3 with dissolve

    mc "Похоже, он приглашает меня к себе в пасть. Так это же и есть Морские Врата!"
    mc "В животе чудища я и доплыву до Оракула."

    pause 0.5

    if CurrentCar == "Molokovoz":
        if CurrentCargo == "Box":
            scene bg_leaver1_cargo3_4 with dissolve
        else:
            scene bg_leaver1_cargo1_4 with dissolve
    elif CurrentCar == "Ural":
        scene bg_leaver1_ural_4 with dissolve
    else:
        scene bg_leaver1_van_4 with dissolve

    mc "Страшно, конечно..."
    mc "Ну, терять мне нечего. Только вперёд!"

    scene black with fade

    "Конец первой главы."

    return

# With Lisa route

# Optional warehouse quest

label galdenquest:

    "Однако вас подзывает незнакомец."

    show galden at left, stretch_in

    unknown "Ты бы не мог нам помочь?"

    show mchar at right, stretch_in

    mc "Чем же я могу вам помочь?"

    galden "Наш склад был захвачен местным населением."

    "Вам не понятно причём тут вообще вы."

    hide mchar
    show mcsurp at right, stretch_in

    mc "Почему же вы не можете его отбить силой?"

    galden "Нам не хочется ссориться окончательно с жителями этих земель, поэтому мы и просим тебя."

    menu:
        "Согласиться":
            $ r1m4SideQuest = "Taken"
            mc "Хорошо, я попробую разобраться."
            hide galden with dissolve
            "Вы уезжаете на склад."
            $ TownType = "NotInCity"
            hide mcsurp

            if random.random() <= 0.5:
                $ randommus = random.choice([1, 2, 7])
                $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
                "На вас нападают!"
                call randomfight from _call_randomfight_25
            
            jump r1m4SideQuest_start

        "Отказать":
            $ r1m4SideQuest = "Failed"
            mc "Мне это неинтересно."
            hide galden with dissolve
            "Вы спокойно уходите. Незнакомец ничего не говорит вам в след."
            mc "Видимо ему уже не один раз отказали..."
            hide mcsurp with dissolve
            jump homersearch

label r1m4SideQuest_start:

    play music "music/town4.ogg" fadeout 1.0

    scene bg_warehouse with fade

    "На складе вас явно не готовы принимать \"с распростертыми объятиями\"."

    show wsecurity at right, stretch_in

    wsec "Стой! Кто идёт?"

    show mc6 at left with dissolve

    mc "Спокойно, я не враг вам."

    wsec "Это уж нам решать. Выкладывай, кто таков?"

    mc "Мне поручили важную миссию: договориться с вами об освобождении склада."

    wsec "Ха, торговцы поняли, что захват нашего лидера был не лучшим их поступком, и они готовы его освободить?"

    mc "Они захватили вашего лидера?"
    mc "\"Хоть бы меня предупредили!\""

    wsec "У нас сейчас сложные времена, понимаешь. Этот склад - единственный рычаг, с помощью которого мы можем диктовать свои требования грязным торговцам."

    mc "И чего же вы хотите?"

    wsec "В данный момент мы просим освободить нашего лидера, только после этого мы уйдем со склада."

    menu:
        "Освободить лидера":
            mc "Хорошо, я помогу вам. Где ваш лидер?"
            wsec "Знали бы, сами освободили. Это и есть твоя основная задача - узнать, где он."
            mc "Ладно, попробую всё выяснить."
            hide wsecurity
            hide mc6

            if random.random() <= 0.5:
                $ randommus = random.choice([1, 2, 7])
                $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
                "На вас нападают!"
                call randomfight from _call_randomfight_26
            
            jump r1m4SideQuest_whereisleader

        "Отбить склад силой":
            mc "Слишком это хлопотно, проще убить вас всех."
            hide wsecurity
            hide mc6
            "Между вами начинается бой."
            $ r1m4SideQuestLeaderSaved = False
            jump r1m4SideQuest_warehousefight

label r1m4SideQuest_warehousefight:

    play music "music/battle7.ogg"

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "warehouseguard"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = 4250
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 20
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Захватчики склада"
    $ bgname = "bg_warehouse"
    $ EnemyType = "Regular"
    scene bg_warehouse
    show warehouseguard at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide warehouseguard
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
        hide warehouseguard with dissolve

        mc "Эти бандиты больше не будут мешать торговцам."
        mc "Осталось сообщить в Ольм об освобождении склада."

        jump r1m4SideQuest_finish

label r1m4SideQuest_whereisleader:

    $ UpdateTownInfo("City", "Ольм", "north_nath_traders")

    play music "music/town1.ogg" fadeout 1.0

    scene bg_olm with fade

    show galden at left with dissolve

    galden "Удалось освободить склад?"

    show mcsurp at right, stretch_in

    mc "Нет. Чёртовы аборигены стоят насмерть."
    mc "Может быть, мне удастся уговорить их лидера распустить всех по домам?"

    galden "Этого зверя? Вряд ли. Даже пойманный, он отказывается сотрудничать с нами."

    mc "А всё-таки где он?"

    galden "Сейчас фургон с ним должен выехать из рыбацкого поселка и направляется сюда."

    mc "Спасибо. Я найду его."

    $ TownType = "NotInCity"

    jump r1m4SideQuest_freeleader

label r1m4SideQuest_freeleader:
    
    play music "music/passage01unloop.ogg" fadeout 1.0
    scene bg_freeleader with fade

    extguard "Не приближаться! Любые подозрительные действия будут расцениваться как агрессия!"

    mc "Вы перевозите груз, который мне нужен. Я готов щедро заплатить."

    play music "music/intensedialogue01.ogg" fadeout 1.0
    scene bg_freeleader_1 with dissolve

    extguard "Попытка подкупа должностного лица при исполнении!"

    mc "Похоже, придётся действовать по-плохому..."
    mc "Освободите пленника и катитесь на все четыре стороны. Второго шанса у вас не будет."

    scene bg_freeleader_2 with dissolve

    extguard "Все к орудиям! Покажем этому наглецу, как связываться со служителями порядка!"

    mc "Вы сами этого захотели. Главное - не задеть прицеп с пленником. Все остальные пусть горят синим пламенем!"

    play music "music/battle7.ogg"

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "leadertakers"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = 2025 # 50% HP of 3 Vans and 1 Lorry
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 20
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Захватчики лидера рыбаков"
    $ bgname = "bg_freeleaderfight"
    $ EnemyType = "Regular"
    scene bg_freeleaderfight
    show leadertakers at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide leadertakers
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
        hide leadertakers with dissolve

        jump r1m4SideQuest_leaderisfree

label r1m4SideQuest_leaderisfree:

    play music "music/intensedialogue03.ogg" fadeout 1.0
    scene bg_leaderisfree with fade

    mc "Чего ждёшь? Садись в мою машину. Торопись, они могли вызвать подмогу!"

    extleader "Спасибо, что освободил меня, незнакомец. Но каковы твои мотивы? Я не уверен, могу ли тебе доверять."

    mc "Я заключил договор с твоими бойцами, что освобожу тебя в обмен на одну нужную мне вещь."
    mc "И лучше бы им выполнить свою часть сделки!"

    if random.random() <= 0.5:
        $ randommus = random.choice([1, 2, 7])
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_27

    jump r1m4SideQuest_leaderisback

label r1m4SideQuest_leaderisback:

    play music "music/town4.ogg" fadeout 1.0

    scene bg_warehouse with fade

    show wsecurity at right, stretch_in

    wsec "Я не верю своим глазам! Иноземец сдержал слово. Наш лидер снова с нами!"

    show mc_2 at left, stretch_in

    mc "Теперь и вы держите своё. Освобождайте склад."

    $ RandomR1M4SQReward = random.randint(2000, 4000)
    $ CurrentMoney += RandomR1M4SQReward
    $ renpy.notify(f"Вы получили {RandomR1M4SQReward} монет.")

    wsec "Конечно, товарищ! Бери столько добра, сколько сможешь увезти, и возвращайся ещё."

    mc "Обязательно вернусь."

    hide wsecurity with dissolve

    mc "Надеюсь в Ольме меня ни в чём не заподозрят..."

    $ r1m4SideQuestLeaderSaved = True

    if random.random() <= 0.5:
        $ randommus = random.choice([1, 2, 7])
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_28

    jump r1m4SideQuest_finish

label r1m4SideQuest_finish:

    $ UpdateTownInfo("City", "Ольм", "north_nath_traders")

    play music "music/town1.ogg" fadeout 1.0

    scene bg_olm with fade

    if r1m4SideQuestLeaderSaved == True:
        "Вернувшись в Ольм вы не замечаете ничего странного."

    show galden at left with dissolve

    galden "Как продвигаются твои дела?"

    show mcsurp at right with dissolve

    mc "Склад чист, работа сделана."

    $ CurrentMoney += 1000
    $ renpy.notify("Вы получили 1000 монет.")

    galden "Отлично! Вот тебе награда."

    mc "Супер!"

    hide galden with dissolve

    mc "Надо возвращаться к основной задаче..."

    hide mcsurp

    jump homersearch