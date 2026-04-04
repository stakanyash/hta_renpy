label r1m4start:
    pause 0.5

    show bg_r1m4load at truecenter

    $ level_slides = ["loadinglvl0","loadinglvl1","loadinglvl2","loadinglvl3","loadinglvl4","loadinglvl5","loadinglvl6"]

    call show_loading(level_slides) from _call_show_loading_5

    scene black

    $ _game_menu_screen = "save_screen"
    $ _menu = True
    $ config.keymap['save'] = ['save']
    $ config.keymap['load'] = ['load']
    $ config.keymap['game_menu'] = ['game_menu']
    $ persistent._in_battle = False

    $ renpy.notify("Игра сохранена в слот 1.")
    $ renpy.save("checkpoint-1")

    $ player_config.current_region = "r1m4"
    play music "music/driving7.ogg" fadeout 1.0

    scene bg_helfirst with fade

    "Приехав в Хель Вы сразу направились в Ольм."

    $ player_config.update_town_info("City", "Ольм", "north_nath_traders")
    
    play music "music/town1.ogg" fadeout 1.0
    scene bg_olm with dissolve

    if player_config.r1m4warehouse_side_quest == "Q_CANBEGIVEN":
        jump galdenquest
    elif LisaAgreed == False:
        jump homersearch

# Without Lisa route

label homersearch:

    "В Ольме Вы решили начать поиски Гомера."

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

    $ player_config.town_type = "NotInCity"

    "Вы начали искать Гомера в рыбацких посёлках."

    $ CheckForRandomBattle()

    play music "music/driving7.ogg" fadeout 1.0
    scene bg_lauka with fade

    $ player_config.update_town_info("Village", "Лаука", "free_traders_alliance")

    "В Лауке его нет."

    scene bg_kalis with fade

    $ player_config.update_town_info("Village", "Калис", "free_traders_alliance")

    "В Калисе тоже..."

    mc "Мне что, придётся весь регион объездить в его поисках?!"

    $ CheckForRandomBattle()

    scene bg_kordan with fade

    $ player_config.update_town_info("Village", "Кордан", "free_traders_alliance")

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

    $ CheckForRandomBattle()

    $ player_config.update_town_info("Village", "Салиниом", "free_traders_alliance")
    
    play music "music/bar.ogg" fadeout 1.0
    scene bg_saliniom with fade

    $ renpy.notify("Игра сохранена в слот 2.")
    $ renpy.save("checkpoint-2")

    "Приехав в Салиниом Вы подходите к человеку, который подходит под описание Гомера."

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

    $ player_config.town_type = "NotInCity"

    $ CheckForRandomBattle()

    jump tokranfight

label tokranfight:

    play music "music/bio05.ogg" fadeout 1.0
    scene bg_boloto with fade
    "Подъехав к болоту у Вас возникли некоторые опасения."

    mc "Похоже, именно об этом месте и говорил Гомер. Точно ли я тут смогу проехать?"
    mc "Ладно, не попробуешь - не узнаешь..."

    scene bg_boloto_1 with dissolve

    mc "Старик не обманул, под слоем жижи было твёрдое дно."

    scene bg_boloto_2 with dissolve

    mc "Интересно, что ждёт меня по эту сторону?"

    scene black with fade

    $ renpy.movie_cutscene("movies/r1m4/bosskran.ogv")

    play sound "audio/sfx/stand1_boss02.wav" channel "sfx2"
    play music "music/intensedialogue01.ogg"
    scene bg_kran with fade
    
    mc "О господи! Это что ещё за...?"
    mc "Зачем только людям древности нужны были такие машины?"
    $ renpy.notify("Игра сохранена в слот 3.")
    $ renpy.save("checkpoint-3")
    mc "Этот монстр охраняет проезд к Морским Вратам."
    mc "Мне нужно как-то справиться с ним..."

    scene black with fade

    play music "music/battle01.ogg" fadeout 1.0

    scene bg_kranfight with fade

    pause 0.5

    $ player_config.max_hp = CarHP.get(player_config.car, CarHP["Van"])
    if player_config.hp is None:
        $ player_config.hp = player_config.max_hp

    $ battle_setup("kranboss", 2500, "bg_kranfight", "Бандит", "Boss", 2.5, "boss1")

    scene bg_kranfight
    show kranboss at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ battle_end_lose()
        hide kranboss
        play sound "sfx/explosion04.wav"
        jump fightlost
    else:
        $ battle_end_win()
        play sound "sfx/explosion04.wav"
        hide kranboss with dissolve
        stop sfx2 fadeout 1.0

        scene bg_bosskran_dead

        $ renpy.notify("Игра сохранена в слот 4.")
        $ renpy.save("checkpoint-4")

        mc "Чудище повержено. Пора двигаться дальше."

        jump leaveregion1

label leaveregion1:

    stop boss_charge fadeout 1.0

    play music "music/bio02.ogg" fadeout 1.0

    $ renpy.scene()
    $ renpy.show(f"bg_leaver1_{player_config.car}_1")
    $ renpy.with_statement(dissolve)

    mc "Это то самое место, которое указал Гомер, но я не вижу никаких врат."
    mc "Неужели всё зря?!"

    pause 0.5

    $ renpy.scene()
    $ renpy.show(f"bg_leaver1_{player_config.car}_2")
    $ renpy.with_statement(dissolve)

    mc "Что это лезет из-под воды? Покой нам только снится..."
    mc "Только прикончил одного монстра, как второй на подходе..."
    mc "Впрочем, этот поспокойнее будет."

    play sound "sfx/boat_open.wav"
    play sound "sfx/boat_motor_loop_mono.wav" channel "sfx2"

    pause 0.5

    $ renpy.scene()
    $ renpy.show(f"bg_leaver1_{player_config.car}_3")
    $ renpy.with_statement(dissolve)

    mc "Похоже, он приглашает меня к себе в пасть. Так это же и есть Морские Врата!"
    mc "В животе чудища я и доплыву до Оракула."

    pause 0.5

    $ renpy.scene()
    $ renpy.show(f"bg_leaver1_{player_config.car}_4")
    $ renpy.with_statement(dissolve)

    mc "Страшно, конечно..."
    mc "Ну, терять мне нечего. Только вперёд!"

    scene black with fade

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True

    pause 1.0

    jump demofinished

# With Lisa route

# Optional warehouse quest

label galdenquest:

    "Однако Вас подзывает незнакомец."

    show galden at left, stretch_in

    unknown "Ты бы не мог нам помочь?"

    show mchar at right, stretch_in

    mc "Чем же я могу Вам помочь?"

    galden "Наш склад был захвачен местным населением."

    "Вам не понятно причём тут вообще вы."

    hide mchar
    show mcsurp at right, stretch_in

    mc "Почему же Вы не можете его отбить силой?"

    galden "Нам не хочется ссориться окончательно с жителями этих земель, поэтому мы и просим тебя."

    menu:
        "Согласиться":
            $ renpy.notify("Игра сохранена в слот 5.")
            $ renpy.save("checkpoint-5")
            $ player_config.r1m4warehouse_side_quest = "Q_TAKEN"
            $ player_config.r1m4warehouse_side_quest_status = "Accepted"
            mc "Хорошо, я попробую разобраться."
            hide galden with dissolve
            "Вы уезжаете на склад."
            $ player_config.town_type = "NotInCity"
            hide mcsurp

            $ CheckForRandomBattle()
            
            if random.random() <= 0.7:
                if player_config.sidequest_findhusband == "Q_CANBETAKEN":
                    jump r1m4SideQuest_FindHusband_start
                else:
                    jump r1m4SideQuest_start
            else:
                jump r1m4SideQuest_start

        "Отказать":
            $ renpy.notify("Игра сохранена в слот 5.")
            $ renpy.save("checkpoint-5")
            $ player_config.r1m4warehouse_side_quest = "Q_FAILED"
            $ player_config.r1m4warehouse_side_quest_status = "Declined"
            mc "Мне это неинтересно."
            hide galden with dissolve
            "Вы спокойно уходите. Незнакомец ничего не говорит Вам в след."
            mc "Видимо ему уже не один раз отказали..."
            hide mcsurp with dissolve
            jump homersearch

label r1m4SideQuest_start:

    play music "music/town4.ogg" fadeout 1.0

    scene bg_warehouse with fade

    "На складе Вас явно не готовы принимать \"с распростертыми объятиями\"."

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

    mc "И чего же Вы хотите?"

    wsec "В данный момент мы просим освободить нашего лидера, только после этого мы уйдем со склада."

    menu:
        "Освободить лидера":
            $ player_config.r1m4warehouse_side_quest_status = "GoingForLeaderSave"
            $ renpy.notify("Игра сохранена в слот 6.")
            $ renpy.save("checkpoint-6")
            mc "Хорошо, я помогу вам. Где ваш лидер?"
            wsec "Знали бы, сами освободили. Это и есть твоя основная задача - узнать, где он."
            mc "Ладно, попробую всё выяснить."
            hide wsecurity
            hide mc6

            $ CheckForRandomBattle()
            
            jump r1m4SideQuest_whereisleader

        "Отбить склад силой":
            $ player_config.r1m4warehouse_side_quest_status = "LeaderIsNotSaved"
            $ renpy.notify("Игра сохранена в слот 6.")
            $ renpy.save("checkpoint-6")
            mc "Слишком это хлопотно, проще убить вас всех."
            hide wsecurity
            hide mc6
            "Между вами начинается бой."
            $ r1m4SideQuestLeaderSaved = False
            jump r1m4SideQuest_warehousefight

label r1m4SideQuest_warehousefight:

    $ randommus = random.choice([1, 2, 7])
    $ renpy.music.play(f"audio/music/battle{randommus}.ogg", channel='music')

    $ player_config.max_hp = CarHP.get(player_config.car, CarHP["Van"])
    if player_config.hp is None:
        $ player_config.hp = player_config.max_hp

    $ battle_setup("warehouseguard", 2125, "bg_warehouse", "Захватчики склада", "Regular", 1.5)

    scene bg_warehouse
    show warehouseguard at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ battle_end_lose()
        hide warehouseguard
        play sound "sfx/explosion04.wav"
        jump fightlost
    else:
        $ battle_end_win()
        play sound "sfx/explosion04.wav"
        hide warehouseguard with dissolve

        mc "Эти бандиты больше не будут мешать торговцам."
        mc "Осталось сообщить в Ольм об освобождении склада."

        jump r1m4SideQuest_finish

label r1m4SideQuest_whereisleader:

    $ player_config.update_town_info("City", "Ольм", "north_nath_traders")

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

    $ player_config.town_type = "NotInCity"

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

    $ renpy.notify("Игра сохранена в слот 1.")
    $ renpy.save("checkpoint-1")

    mc "Вы сами этого захотели. Главное - не задеть прицеп с пленником. Все остальные пусть горят синим пламенем!"

    $ randommus = random.choice([1, 2, 7])
    $ renpy.music.play(f"audio/music/battle{randommus}.ogg", channel='music')

    $ player_config.max_hp = CarHP.get(player_config.car, CarHP["Van"])
    if player_config.hp is None:
        $ player_config.hp = player_config.max_hp

    $ battle_setup("leadertakers", 2025, "bg_freeleaderfight", "Захватчики лидера рыбаков", "Regular", 1.35)

    scene bg_freeleaderfight
    show leadertakers at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ battle_end_lose()
        hide leadertakers
        play sound "sfx/explosion04.wav"
        jump fightlost
    else:
        $ battle_end_win()
        play sound "sfx/explosion04.wav"
        hide leadertakers with dissolve

        jump r1m4SideQuest_leaderisfree

label r1m4SideQuest_leaderisfree:

    play music "music/intensedialogue03.ogg" fadeout 1.0
    scene bg_leaderisfree with fade

    $ player_config.r1m4warehouse_side_quest_status = "LeaderSaved"

    mc "Чего ждёшь? Садись в мою машину. Торопись, они могли вызвать подмогу!"

    extleader "Спасибо, что освободил меня, незнакомец. Но каковы твои мотивы? Я не уверен, могу ли тебе доверять."

    mc "Я заключил договор с твоими бойцами, что освобожу тебя в обмен на одну нужную мне вещь."
    mc "И лучше бы им выполнить свою часть сделки!"

    $ CheckForRandomBattle()

    if random.random() <= 0.7:
        if player_config.sidequest_findhusband == "Q_CANBEGIVEN":
            jump r1m4SideQuest_FindHusband_start
        else:
            jump r1m4SideQuest_leaderisback
    else:
        jump r1m4SideQuest_leaderisback

label r1m4SideQuest_leaderisback:

    play music "music/town4.ogg" fadeout 1.0

    scene bg_warehouse with fade

    show wsecurity at right, stretch_in

    wsec "Я не верю своим глазам! Иноземец сдержал слово. Наш лидер снова с нами!"

    show mc_2 at left, stretch_in

    mc "Теперь и вы держите своё. Освобождайте склад."

    $ RandomR1M4SQReward = random.randint(1000, 3000)
    $ player_config.add_money(RandomR1M4SQReward)
    $ renpy.notify(f"Вы получили {RandomR1M4SQReward} монет.")

    wsec "Конечно, товарищ! Бери столько добра, сколько сможешь увезти, и возвращайся ещё."

    mc "Обязательно вернусь."

    hide wsecurity with dissolve

    mc "Надеюсь в Ольме меня ни в чём не заподозрят..."

    $ r1m4SideQuestLeaderSaved = True

    $ CheckForRandomBattle()

    jump r1m4SideQuest_finish

label r1m4SideQuest_finish:

    $ player_config.update_town_info("City", "Ольм", "north_nath_traders")

    play music "music/town1.ogg" fadeout 1.0

    scene bg_olm with fade

    if r1m4SideQuestLeaderSaved == True:
        "Вернувшись в Ольм Вы не замечаете ничего странного."

    show galden at left with dissolve

    galden "Как продвигаются твои дела?"

    show mcsurp at right with dissolve

    mc "Склад чист, работа сделана."

    $ player_config.add_money(1000)
    $ renpy.notify("Вы получили 1000 монет.")

    $ player_config.r1m4warehouse_side_quest = "Q_COMPLETED"
    $ player_config.r1m4warehouse_side_quest_status = "Completed"

    galden "Отлично! Вот тебе награда."

    mc "Супер!"

    $ renpy.notify("Игра сохранена в слот 2.")
    $ renpy.save("checkpoint-2")

    hide galden with dissolve

    mc "Надо возвращаться к основной задаче..."

    hide mcsurp

    jump homersearch

# Alla encounter (during warehouse sidequest)

label r1m4SideQuest_FindHusband_start:
    scene bg_allaencounter with fade

    play music "music/driving7.ogg" fadeout 1.0

    "Вы ехали в направлении склада, но тут вас останавливают..."

    show alla at right, stretch_in

    alla "Ох, молодой человек, беда у меня."

    show mc_2 at left, stretch_in

    mc "Что у Вас случилось?"

    hide alla
    show alla at right, stretch_in

    alla "Муж мой поехал на рынок и пропал. Наверное, продал товар и запил. Вот я и пошла на его поиски."

    menu:
        "Помочь":
            $ player_config.SideQuest_FindHusband = "Q_TAKEN"
            mc "Я могу Вам помочь в его поисках."
            alla "Спасибо тебе молодой человек, ты меня сможешь найти в деревне Перчь."
            mc "Скажите хоть, как зовут Вашего мужа? И опишите внешность."
            hide alla
            show alla at right, stretch_in
            alla "Ох, конечно! Зовут его Филимон. Кудрявый, с повязкой на лбу. Любит говорить \"встала и пошла\", а также неравнодушен к розовым кофточкам."
            mc "Я всё понял. Проедусь по местным барам, поищу."

            hide alla with dissolve
            hide mc_2 with dissolve

            $ CheckForRandomBattle()

            jump r1m4SideQuest_FindHusband_searches
        "Отказать":
            $ player_config.SideQuest_FindHusband = "Q_FAILED"
            mc "Это твои проблемы, решай их сама."

            hide alla with dissolve
            hide mc_2 with dissolve

            "После этого Вы поехали дальше к складу."

            $ CheckForRandomBattle()
                
            if player_config.r1m4warehouse_side_quest_status == "Accepted":
                jump r1m4SideQuest_start
            elif player_config.r1m4warehouse_side_quest_status == "LeaderSaved":
                jump r1m4SideQuest_leaderisback

label r1m4SideQuest_FindHusband_searches:
    scene bg_lauka with fade
    $ player_config.update_town_info("Village", "Лаука", "fishermen")

    "В Лауке его нет..."

    $ CheckForRandomBattle()

    scene bg_saliniom with fade
    $ player_config.update_town_info("Village", "Салиниом", "fishermen")

    "В Салиниоме его так-же нет..."

    $ CheckForRandomBattle()

    scene bg_olm with fade
    $ player_config.update_town_info("City", "Ольм", "north_nath_traders")

    "Даже в Ольме его нет..."
    mc "Хотя казалось бы, что ему тут делать?"

    $ CheckForRandomBattle()

    scene bg_kordan with fade
    $ player_config.update_town_info("Village", "Кордан", "fishermen")

    mc "Да где-же искать твоего Филимона-то?!"
    mc "Попробую поискать его в Калисе..."

    $ CheckForRandomBattle()

    scene bg_kalis with fade
    $ player_config.update_town_info("Village", "Калис", "fishermen")

    "В баре Калиса Вы замечаете подходящего под описание Филимона..."

    show filimon at right with dissolve
    show mc6 at left with dissolve

    filimon "Что ты хочешь от меня, мил человек?"
    mc "Филимон, твоя жена совсем с ног сбилась тебя искать, а ты тут по барам рассиживаешься."
    filimon "Устал я от неё! Дай отдохнуть, с мужиками посидеть."
    mc "Давай-ка я тебя провожу до дому."
    filimon "Не хочу домой! И ты мне надоел, встал и пошёл отсюда."
    mc "Лучше соглашайся по-хорошему!"
    filimon "Слушай, давай я тебе денег дам, и ты от меня отстанешь?"

    menu:
        "Согласиться":
            mc "Ладно, пожалею тебя. Сколько?"
            filimon "500 монет тебя устроит?"
            mc "Я большего от тебя и не ждал. Давай сюда."
            $ player_config.add_money(500)
            $ renpy.notify("Вы получили 500 монет.")
            $ player_config.sidequest_findhusband = "Q_FAILED"
            $ player_config.sidequest_findhusband_status = "Failed"

            hide filimon with dissolve
            hide mc6 with dissolve

            "После этого Вы поехали дальше к складу."

            $ player_config.town_type = "NotInCity"

            $ CheckForRandomBattle()
                
            if player_config.r1m4warehouse_side_quest_status == "Accepted":
                jump r1m4SideQuest_start
            elif player_config.r1m4warehouse_side_quest_status == "LeaderSaved":
                jump r1m4SideQuest_leaderisback
        "Отказать":
            mc "Нет, я пообещал, что верну тебя домой!"
            filimon "Делать нечего, поехали. Надоел ты мне уже."
            mc "Вот и ладненько."

            hide filimon with dissolve
            hide mc6 with dissolve

            "После этого Вы поехали в Перчь."

            $ player_config.town_type = "NotInCity"

            $ CheckForRandomBattle()

            jump r1m4SideQuest_FindHusband_bringback

label r1m4SideQuest_FindHusband_bringback:
    scene bg_perch with fade
    $ player_config.update_town_info("Village", "Перчь", "fishermen")

    "Приехав в Перчь Вы достаточно быстро находите Аллушку."

    show alla at right, stretch_in

    alla "Ты привёз мне моего мужа?"

    show mc6 at left, stretch_in

    mc "Вон он, жив и здрав."

    hide alla
    show alla at right, stretch_in

    alla "Ох, даже не знаю, как тебя отблагодарить. У меня тут есть вещи на продажу, вот я тебе их и отдам."

    python:
        if not player_config.try_add_item("Tobacco"):
            handle_full_inventory("Tobacco", ItemPricesVillage)
        else:
            renpy.notify("В ваш инвентарь добавлен предмет: Табак.")

        if not player_config.try_add_item("Book"):
            handle_full_inventory("Book", ItemPricesVillage)
        else:
            renpy.notify("В ваш инвентарь добавлен предмет: Книги.")

    mc "Спасибо. До свидания."

    hide alla with dissolve

    mc "Надо двигаться дальше..."

    $ player_config.town_type = "NotInCity"

    $ CheckForRandomBattle()
                
    if player_config.r1m4warehouse_side_quest_status == "Accepted":
        jump r1m4SideQuest_start
    elif player_config.r1m4warehouse_side_quest_status == "LeaderSaved":
        jump r1m4SideQuest_leaderisback