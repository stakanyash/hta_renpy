# Default start-up

label vaterlandfirst:
    if not config.developer:
        pause 0.5

        show bg_r1m3load at truecenter

        $ level_slides = ["loadinglvl0","loadinglvl1","loadinglvl2","loadinglvl3","loadinglvl4","loadinglvl5","loadinglvl6"]

        call show_loading(level_slides) from _call_show_loading_3

        scene black

    $ _game_menu_screen = "save_screen"
    $ _menu = True
    $ config.keymap['save'] = ['save']
    $ config.keymap['load'] = ['load']
    $ config.keymap['game_menu'] = ['game_menu']
    $ persistent._in_battle = False

    $ player_config.current_region = "r1m3"

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

    $ player_config.update_town_info("City", "Асгард", "free_traders_alliance")

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

    $ player_config.town_type = "NotInCity"

    hide seller
    hide mcsurp

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_29

    jump mvillage

label mvillage:

    $ player_config.update_town_info("Village", "Горные шахты", "free_traders_alliance")

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
    $ renpy.notify("Игра сохранена в слот 1.")
    $ renpy.save("checkpoint-1")
    miner "Опять эти бандиты нападают!"

    hide mc5
    show mcsurp at right, stretch_in

    mc "Где?"

    miner "Все на стены. Враг не пройдёт! Слушай, если тебе нужна взрывчатка, помогай её защищать!"

    hide miner with dissolve

    mc "Опять двадцать пять. Ни дня без боя, что за жизнь!"

    hide mcsurp

    $ randommus = random.randint(1, 2)
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
    $ enemy_image = "minerattackers"
    $ player_hp = player_config.hp
    $ player_max_hp = player_config.max_hp
    $ enemy_hp = 500
    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = player_config.heals
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандиты"
    $ bgname = "bg_mvillage_fight"
    $ EnemyType = "Regular"
    $ enemy_damage_multiplier = 1.2

    scene bg_mvillage_fight
    show minerattackers at center

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
        $ renpy.sound.stop(channel="shoot")
        $ player_config.hp = player_hp
        $ player_config.heals = remainheals

        play sound "sfx/explosion04.wav"
        hide minerattackers with dissolve

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

    $ player_config.town_type = "NotInCity"

    jump brigdedestroy

label brigdedestroy:

    scene bg_nearbridgeenemy with fade
    $ randommus = random.randint(1, 2)
    $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')

    "Подъехав к мосту вы заметили бандитские машины."
    $ renpy.notify("Игра сохранена в слот 2.")
    $ renpy.save("checkpoint-2")
    mc "Видимо, чтобы осуществить свою задачу нужно их уничтожить, но куда деваться..."

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
    $ enemy_image = "brigde_defender"
    $ player_hp = player_config.hp
    $ player_max_hp = player_config.max_hp
    $ enemy_hp = 1000
    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = player_config.heals
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандиты"
    $ bgname = "bg_nearbridge"
    $ EnemyType = "Regular"
    $ enemy_damage_multiplier = 1.1

    scene bg_nearbridge
    show brigde_defender at center

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
        $ renpy.sound.stop(channel="shoot")
        $ player_config.hp = player_hp
        $ player_config.heals = remainheals

        play sound "sfx/explosion04.wav"
        hide brigde_defender with dissolve

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

        stop music fadeout 1.0
        jump BOOOM


label BOOOM:
    scene bg_bandbridge with fade

    mc "Ну что-же пора браться за дело..."

    stop sound

    $ renpy.movie_cutscene("movies/r1m3/bridge_destroy.ogv")

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

    $ player_config.update_town_info("City", "Пешт", "free_traders_alliance")

    hide pguard
    hide mc5

    $ player_config.town_type = "NotInCity"

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_30

    jump minin1st_nl

label minin1st_nl:

    $ player_config.update_town_info("City", "Минин", "north_nath_traders")

    scene bg_minin with fade
    play music "music/town3.ogg" fadeout 1.0

    "В Минине вы сразу привлекаете внимание местного рабочего."

    show mworker at right with dissolve

    sharki "Издалека, видать, приехал. По делам, или приключений ищешь?"

    show mc_2 at left with dissolve

    mc "Я слышал, здесь неподалёку жил исследователь Айвен. Мне бы хотелось побывать в его жилище."

    sharki "Ты приехал в нужное место: Айвен жил прямо в этом городе, вон в том доме, вместе с женой и сыном."
    sharki "А потом случилось несчастье: его жена погибла во время ночного нападения бандитов, когда муж был в отъезде."
    sharki "Конечно, никто из негодяев не ушёл живым. Айвен забрал сына и уехал куда-то. А дом до сих пор пустой стоит."

    mc "Спасибо за рассказ. Я, пожалуй, пойду."

    hide mc_2
    hide mworker

    $ player_config.town_type = "NotInCity"

    jump aivenhouse

label aivenhouse:

    scene bg_aivenhouse with fade

    play music "music/techno04.ogg" fadeout 1.0

    "Заехав в дом Айвена вы заметили, что его явно покидали в спешке..."

    show mcback at center with dissolve

    mc "Сколько же здесь всего..."
    mc "Странного..."
    mc "И повсюду следы погрома..."
    mc "На этой доске вырезано моё имя... Это же тайник, а внутри – какой-то оберег."
    mc "Любопытная штуковина – возьму себе..."

    "Из стоящего рядом приёмника послышался шум..."

    scene bg_benradio with dissolve

    play sound "audio/sfx/radiostart.ogg"
    play sound "audio/sfx/radionoise.ogg" channel "sfx2"

    unknown "Эй!"
    unknown "Ага, кажется, заработало!"
    ben "Это Бен, приём. Я настроил радиопередатчик."
    ben "Как движутся поиски?"

    show mc4_key at left, stretch_in

    mc "Радиосвязь на таком расстоянии? Да ты просто волшебник!"
    mc "Поиски ничего не дали, к сожалению. Тут только рухлядь."
    mc "Правда, я нашёл забавный амулет с кнопочками и надписью: \"UB-627 Red access\"..."

    ben "Точно как в старых манускриптах! Это же ключ от морских врат!"
    ben "Но откуда он взялся у твоего отца? Впрочем, неважно. Слушай внимательно."
    ben "Рассказывают, что на затерянном в океане острове живёт Оракул."
    ben "Тот, кто пройдёт через все испытания на пути к его жилищу, получит ответ на любой свой вопрос."
    ben "Естественно, всё это выдумки. Однако есть основания полагать, что у легенды этой имеется вполне научное основание."
    ben "И ключ, который ты сейчас носишь на шее, явное тому свидетельство."

    mc "Было бы неплохо узнать у этого Оракула, что случилось с Айвеном. В любом случае не зря такая редкая вещь оказалась в его тайнике."

    ben "Я читал старинные документы, где говорилось, а точнее сказать - можно было прочесть между строк, что на одном острове было какое-то крупное и очень засекреченное строительство."
    ben "Поезжай всё время на север. Где-то на самом краю земли находятся морские врата."
    ben "Ты сразу их узнаешь, когда увидишь. Больше я и сам не знаю."
    ben "Похоже, мой радиоприемник совсем сломал..."

    stop sfx2
    play sound "audio/sfx/radioend.ogg"

    hide mc4_key

    scene bg_aivenhouse with dissolve

    show mc4_key at center, stretch_in

    mc "Связь оборвалась... Но я понял, о чём говорил Бен. Узнаю подробности в Минине."

    hide mc4_key

    jump minin2nd_nl

label minin2nd_nl:

    $ player_config.update_town_info("City", "Минин", "north_nath_traders")

    play music "music/town3.ogg" fadeout 1.0
    scene bg_minin with fade

    "Вернувшись в Минин вы подходите к тому же рабочему, который указал вам на дом отца."

    show mworker at right with dissolve

    sharki "Чего тебе, бродяга?"

    show mc6 at left, stretch_in

    mc "Я ищу такое огромное сооружение. Говорят, раз увидишь - не забудешь. Оно должно быть где-то в ваших краях."

    sharki "Никогда не встречал ничего, подходящего под твоё яркое описание."

    "Вы немного разочарованы таким ответом."

    mc "Ладно, спрошу у кого-нибудь ещё."

    sharki "Спроси, конечно, но сперва дослушай. Так вот, я слышал от одного знакомого, который слышал от другого знакомого, который…"

    "Вам начинает это надоедать."

    hide mc6
    show mc_2 at left, stretch_in

    mc "Слушай, не томи!"

    sharki "Я знал рыбака, по имени… Забыл. Так вот, тот рыбак рассказывал сказки об одном интересном месте: подводные сокровища и страж-чудовище."
    sharki "Правда, никто так ничего и не нашёл. Видимо, только сам рыбак знает точное расположение этого местечка."

    mc "Так как же его звали?"

    sharki "Ты о ком?"

    mc "Да о рыбаке же!"

    sharki "Прости, что-то с памятью моей стало."

    mc "Так постарайся вспомнить! Это очень важно!"

    sharki "Видишь ли, в такие моменты мне нужна некоторая мотивация."

    mc "Ты серьёзно?!"

    jump hundredcointosharki

label hundredcointosharki:

    $ player_config.update_town_info("City", "Минин", "north_nath_traders")

    if player_config.farm_enabled == True:
        $ player_config.farm_enabled = False

    hide mworker
    hide mc_2
    show mworker at right
    show mc_2 at left

    menu:
        "Дать 100 монет" if player_config.money >= 100:
            $ player_config.spend_money(100)
            $ renpy.notify("Вы отдали 100 монет.")

            mc "Вот тебе 100 монет..."

            sharki "Начинаю что-то вспоминать. Ага! Это же был старик Гомер."

            mc "Гомер? И где я могу его найти?"

            sharki "Где все рыбаки - на побережье! В посёлке. Только тут, видишь ли, встаёт ещё одна проблема."
            sharki "Как ты уже заметил, у нас в городе напряг с бензином. Точнее, совсем его нет. Наши караваны не могут ехать на север. А путь до Ольма не самый простой! Один ты его не найдешь…"

            mc "Что, пытаешься ещё денег выкачать?!"

            sharki "Да ты что? Наоборот! Я вижу, ты смелый парень. Если поможешь, то сможешь вместе с нашим караваном поехать на север. Они покажут дорогу в Ольм."
            sharki "А сейчас обратись к мэру. Скажи, что Шарки послал помочь с проблемой."

            mc "Прямо сейчас к мэру и пойду."

            hide mworker with dissolve

            mc "Ужас какой-то! Так действовать на нервы надо уметь!"

            hide mc_2 with dissolve

            "Вы идёте к мэру."

            "Однако он кажется не рад вас видеть."

            show mimayor at left, stretch_in

            mayor "Говори быстрее, я занят!"

            show mchar at right with dissolve

            mc "Шарки послал помочь с проблемой."

            mayor "Тебя? Что ж, сейчас нам любая помощь пригодится…"

            mc "Что у вас за проблемы?"

            mayor "Тут как в анекдоте: \"Пушки не стреляли по 20 причинам: первая - не было патронов\"."
            mayor "Хех…"
            mayor "Нефтяную вышку захватили бандиты. Они обосновались где-то поблизости и совершали рейды, пока совсем не истощили наши силы."
            mayor "И теперь они окончательно отрезали нас от источника нефти. Наши запасы бензина подходят к концу."

            hide mchar
            show mcsurp at right, stretch_in

            mc "То есть вы хотите, чтобы я один отправился сражаться с бандитами, когда вы всем городом не могли с ними справиться?!"

            mayor "Признаться, мы не очень-то и сражались, так как были заняты внутренними проблемами: видишь ли, профсоюз работников объявил забастовку."

            mc "То есть мне придётся ещё и убедить работников работать или найти новых?"

            mayor "В двух словах…"
            mayor "Да."

            mc "Ладно, начнём с простой проблемы: бандитов. Бензин, надеюсь, будет казённый."

            mayor "В разумных пределах."

            mc "Ладно."

            hide mimayor with dissolve
            hide mcsurp with dissolve

            "Вы уходите из кабинета мэра и направляетесь в сторону нефтянной вышки."

            $ player_config.town_type = "NotInCity"

            stop music fadeout 1.0

            jump oilmine1st
        "\"У меня пока нет денег...\"" if player_config.r1m3_farm_count <= 5:
            $ renpy.notify("Игра сохранена в слот 3.")
            $ renpy.save("checkpoint-3")
            mc "У меня пока нет денег."

            hide mworker
            hide mc_2 with dissolve

            "Вы отправились искать врагов, чтобы заработать денег..."

            $ player_config.town_type = "NotInCity"
            $ player_config.farm_enabled = True

            jump fightformoney

label fightformoney:

    if player_config.farm_enabled == True and player_config.r1m3_farm_count <= 5:

        $ player_config.r1m3_farm_count += 1

        call randomfight from _call_randomfight_15

        scene bg_minin with fade
        play music "music/town3.ogg" fadeout 1.0
        jump hundredcointosharki
    else:
        "Больше здесь добыть не получится."
        play music "music/town3.ogg" fadeout 1.0
        jump hundredcointosharki

label oilmine1st:

    scene bg_oilenemy with fade

    $ randommus = random.randint(1, 2)
    $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
    
    "Приехав к нефтянной вышке вы действительно видите множество бандитов."

    $ renpy.notify("Игра сохранена в слот 3.")
    $ renpy.save("checkpoint-3") # Don't change number of checkpoint!!!

    "Между вами начинается вполне ожидаемая битва."

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
    $ enemy_image = "oilbandits"
    $ player_hp = player_config.hp
    $ player_max_hp = player_config.max_hp
    $ enemy_hp = 500
    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = player_config.heals
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Захватчики вышки"
    $ bgname = "bg_oil"
    $ EnemyType = "Regular"
    $ enemy_damage_multiplier = 1.2

    scene bg_oil
    show oilbandits at center

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
        
        hide oilbandits
        play sound "sfx/explosion04.wav"
        
        $ renpy.sound.stop(channel="shoot")
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
        hide oilbandits with dissolve

        jump oilisfree

label oilisfree:

    scene bg_oillastenemy with fade

    mc "Что ж, вышка освобождена!"
    mc "Последний враг бежал. Он может привести меня к базе бандитов."
    mc "Но надо ли мне это?"

    menu:
        "Проследить":
            jump followlastone

        "Ехать обратно в Минин":
            jump minin3rd_nl

label followlastone:

    play music "music/techno02.ogg" fadeout 1.0

    scene bg_oilspy_1 with fade

    "Вы осторожно следовали за бандитской машиной."

    mc "Интересно, куда же он меня ведёт..."

    scene bg_oilspy_2 with fade

    mc "Мы уже почти на месте, он ведёт меня на базу!"
    mc "Интересно, заметил ли он меня?"

    scene bg_oilspy_3 with fade
    $ randommus = random.randint(1, 2)
    $ renpy.music.play(f"audio/music/battle{randommus}.ogg", channel='music')

    "Приехав на базу вас сразу начали атаковать три машины."
    $ renpy.notify("Игра сохранена в слот 4.")
    $ renpy.save("checkpoint-4")
    mc "Всё таки заметил..."

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
    $ enemy_image = "banditsonbase"
    $ player_hp = player_config.hp
    $ player_max_hp = player_config.max_hp
    $ enemy_hp = 500
    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = player_config.heals 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандиты"
    $ bgname = "bg_oilspy_fight"
    $ EnemyType = "Regular"
    $ enemy_damage_multiplier = 1.2

    scene bg_oilspy_fight
    show banditsonbase at center

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
        
        hide banditsonbase
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
        hide banditsonbase with dissolve

        jump banditbaseelim

label banditbaseelim:

    if random.random() <= 0.4:
        if player_config.try_add_item("Elephant") == True:
            "Расправившись с бандитами вы заметили, что у одного из них стоит неплохое оружие."

            mc "Надо бы забрать себе."

            $ renpy.notify("Вы получили предмет \"Слон\".")

    mc "Пора ехать в Минин."

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_16

    jump minin3rd_nl

label minin3rd_nl:

    $ player_config.update_town_info("City", "Минин", "north_nath_traders")

    play music "music/town3.ogg" fadeout 1.0
    scene bg_minin with fade

    "Вернувшись в Минин вы сразу идёте к мэру."

    show mimayor at left with dissolve

    mayor "Огромное спасибо. Просто нечеловеческое! Мы, наконец, можем вздохнуть свободно, не опасаясь за свои жизни."

    show mcsurp at right with dissolve
    
    mc "\"И кошельки...\""

    mayor "Но ведь сама по себе нефть не потечёт."
    mayor "Эти мерзавцы сейчас протирают штаны в баре вместо того, чтобы работать для общего блага!"

    mc "Посмотрю, что можно сделать с работниками. Попытаюсь их уговорить."

    hide mimayor with dissolve
    hide mcsurp with dissolve

    "Вы идёте к Шарки."

    show mworker at right, stretch_in

    sharki "Опять ты?!"

    show mc6 at left, stretch_in

    mc "Что, ребята, работать будем?"

    sharki "Какая к чертям работа? У нас забастовка!"

    mc "А в чём, собственно, дело?"

    sharki "Работа тяжёлая, платят гроши. Вот мы и отказываемся батрачить! А мэр, собака, наживается на наших бедах."

    mc "Так он же говорит, что город бедный, совсем бандиты разорили."

    sharki "Это он сам и разорил. И вообще не понимаю, зачем нам мэр нужен? Тем более такой. Не будем мы работать, и всё тут!"

    mc "Но мне очень нужно…"

    sharki "И не проси!"

    mc "Что же делать? Придётся разобраться, что здесь у вас происходит."

    hide mc6 with dissolve
    hide mworker with dissolve

    $ player_config.town_type = "NotInCity"

    jump mayorspy

label mayorspy:

    play music "music/passage03a.ogg" fadeout 1.0

    scene bg_spymer_1 with fade

    "Выехав из Минина вы заметили странную машину..."

    mc "По-моему, в этой машине едет мэр!"
    scene bg_spymer_2 with dissolve
    mc "Куда, интересно, он так торопится? Надо бы проследить..."

    scene bg_spymer_3 with dissolve

    "Вы ехали позади машины мэра Минина и он кажется вас не замечал."

    scene bg_spymer_4 with dissolve

    "Однако в какой-то момент он свернул с дороги."

    mc "Опять меня заметили?! Даже если он ведёт меня в ловушку я продолжу за ним ехать..."

    play music "music/bio02.ogg" fadeout 1.0
    scene bg_spymer_5 with dissolve

    "Однако в какой-то момент он поехал к какой-то пещере."
    "Вы решили не следовать дальше за ним, а понаблюдать со стороны."

    scene bg_spymer_6 with dissolve

    pause 1.0

    mc "Сколько добра свалено в этом тайнике!"
    mc "Значит, мэр действительно вор!"
    mc "Если я расскажу об этом в Минине, то его точно прогонят с управляющего поста. Если не хуже."
    mc "И работники могут захотеть работать!"

    "С этой мыслью вы аккуратно покидаете место событий и уезжаете обратно в Минин."

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_17

    jump minin4th_nl

label minin4th_nl:

    $ player_config.update_town_info("City", "Минин", "north_nath_traders")

    play music "music/town3.ogg" fadeout 1.0
    scene bg_minin with fade

    "Вернувшись в Минин вы спешно ищете Шарки."

    "Ему сразу понятно, что вам есть о чём рассказать."

    show mworker at right, stretch_in

    sharki "Узнал что-нибудь?"

    show mc_2 at left, stretch_in

    mc "Вы правы, мэр - вор и обманщик. Я нашёл, куда он увозил городские богатства!"

    hide mworker
    show mworker at right, stretch_in

    sharki "Я же говорил! Не быть ему больше главой! Увижу - морду начищу."

    mc "Раз вы теперь сами себе хозяева, будете работать?"

    sharki "Не вопрос."

    mc "Тогда полезайте в кузов."

    "Шарки и рабочие залезают в ваш грузовик и вы направляетесь на нефтяную вышку."

    $ player_config.town_type = "NotInCity"

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_18

    jump oilmine2nd

label oilmine2nd:

    $ player_config.update_town_info("Village", "Нефтяная вышка", "north_nath_traders")
    
    play music "music/bar.ogg" fadeout 1.0
    scene bg_oil with fade

    show OilMineWorker at left with dissolve

    chris "Вот и первая бочка нефти."

    show mchar at right, stretch_in

    mc "Я отвезу её в город и расскажу всем, что больше не будет перебоев с топливом."
    mc "Специально поставлю её в кабину, чтобы ничего не случилось…"

    "Вы грузите бочку нефти в машину и уезжаете в Минин."

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_19

    jump minin5th_nl

label minin5th_nl:

    $ player_config.update_town_info("City", "Минин", "north_nath_traders")

    play music "music/town3.ogg" fadeout 1.0
    scene bg_minin with fade

    "Приехав в Минин вы выгружаете бочку."

    show MininWorker2 at left with dissolve
    show mchar at right with dissolve

    rid "Спасибо! Ты очень помог нашему городу и всем нам."
    rid "Ты всегда будешь здесь желанным гостем. Для тебя - на всё скидка."

    hide mchar
    show mcsurp at right, stretch_in

    mc "А как насчёт дороги на север?!"

    rid "Ага, вот, когда нефтеоборот налажен, можешь ехать за нашими караванами."
    rid "Они покажут тебе правильный путь на север, именно туда, куда ты хочешь."

    mc "Прощайте."

    $ renpy.notify("Игра сохранена в слот 5.")
    $ renpy.save("checkpoint-5")

    "Вы направились вслед за караваном в соседний регион."

    $ player_config.town_type = "NotInCity"

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_20

    scene black with fade

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True

    jump r1m4start

# With Lisa route

label r1m3withlisa:

    play music "music/bar.ogg" fadeout 1.0
    scene bg_pesht with fade

    $ player_config.update_town_info("City", "Пешт", "free_traders_alliance")

    "Приехав в Пешт вы подходите к одному из местных жителей."

    show pguard at left with dissolve

    "Он начинает разговор первым."

    pguard "Вижу, тебя заботит вопрос?"

    show mc5 at right, stretch_in

    mc "Я ищу девушку, вот такого примерно роста, красивая, на своей машине. Индивидуальный дизайн. Необычная расцветка. Назвалась Лисой."

    hide pguard
    show pguard at left, stretch_in

    pguard "Твоя подруга?"

    mc "Нет. Просто она знает кое-что, что мне бы очень хотелось услышать."

    pguard "Знаю я эту девицу. Вообще-то я бы не советовал никому с ней связываться."

    hide mc5
    show mcsurp at right, stretch_in

    mc "А что так?"

    pguard "Большие люди за ней стоят. И опасные."

    mc "Ты меня не пугай! Расскажи лучше, что знаешь."

    pguard "Она часто здесь бывает по своим делам. В основном, проезжает мимо."
    pguard "Последний раз, совсем недавно,  она направлялась на восток. И опять таки, я бы не советовал ее преследовать в этом направлении."

    mc "Что там ещё?"

    pguard "Там находится база бандитов. Довольно крупная и хорошо укрепленная. А бандиты понимают только язык оружия. Хватит ли у тебя сил потягаться с ними? Не уверен."

    mc "Раз другого пути нет, придется мне ехать. Так что, не поминайте лихом."

    hide mcsurp
    hide pguard

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_34

    jump base51lisa

label base51lisa:

    play music "music/town4.ogg" fadeout 1.0
    scene bg_base51 with fade

    $ player_config.update_town_info("Village", "База 51", "brigade")

    "Приехав на бандитскую базу на вас бросаются взгляды едва ли не всех, кто там находится."

    show bobbase51 at right, stretch_in

    bob "Чего тебе?"

    show mc_2 at left, stretch_in

    mc "Мне нужна Лиса!"

    bob "Всем нужна Лиса. Да только она никому не дается. Ха-ха-ха!"

    mc "Я знаю, что она у вас. И не уеду без нее!"

    bob "А кто тебе сказал, что ты отсюда вообще уедешь?"
    bob "Мы вообще-то страшные бандиты, если ты не заметил!"
    bob "Ну что, ребята, научим этого наглеца манерам?"

    mc "Да будь ты хоть сам Сатана, мне плевать. Я получу, то за чем пришел!"

    hide bobbase51 with dissolve
    hide mc_2 with dissolve

    $ renpy.notify("Игра сохранена в слот 6.")
    $ renpy.save("checkpoint-6")

    "После этого вы начинаете бой."

    $ player_config.town_type = "NotInCity"

    $ randommus = random.randint(1, 2)
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
    $ enemy_image = "base51fight"
    $ player_hp = player_config.hp
    $ player_max_hp = player_config.max_hp
    $ enemy_hp = 650
    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = player_config.heals 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандиты"
    $ bgname = "bg_base51fight"
    $ EnemyType = "Regular"
    $ enemy_damage_multiplier = 1.1

    scene bg_base51fight
    show base51fight at center

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
        
        hide base51fight
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
        hide base51fight with dissolve

        jump base51afterfight

label base51afterfight:

    $ randommus = random.randint(1, 2)
    $ renpy.music.play(f"audio/music/driving{randommus}.ogg", channel='music')

    scene bg_base51 with dissolve

    show bob at right
    show mc4 at left

    bob "А ты отчаянный парень, как я погляжу."
    bob "Не хочешь работать с нами в команде? Нам бы пригодился такой псих, как ты."

    hide mc4
    show mc6 at left, stretch_in

    mc "Мне не до вас с вашими мерзкими бандитскими делами! Я ищу убийцу моего отца!"

    bob "Лучше у тебя на пути не стоять."
    bob "Лиса была здесь недавно с посланием от своего шефа. Но она явно торопилась и, как только покончила с делами, сразу же уехала."

    hide mc6
    show mc_2 at left, stretch_in

    mc "Вы знаете куда?"

    bob "Она не говорила напрямую, но, похоже, ей была нужна какая-то хитрая аппаратура."
    bob "А достать такую можно только в Мидгарде, как я слышал."

    hide bob with dissolve
    hide mc_2 with dissolve

    "Вам ничего не остаётся, кроме как отправиться в Мидгард."

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_35
    
    scene black with fade

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True

    jump r1m2withlisa

label asgardtunnel:
    if not config.developer:
        pause 0.5

        show bg_r1m3load at truecenter

        $ level_slides = ["loadinglvl0","loadinglvl1","loadinglvl2","loadinglvl3","loadinglvl4","loadinglvl5","loadinglvl6"]

        call show_loading(level_slides) from _call_show_loading_4

        scene black

    $ _game_menu_screen = "save_screen"
    $ _menu = True
    $ config.keymap['save'] = ['save']
    $ config.keymap['load'] = ['load']
    $ config.keymap['game_menu'] = ['game_menu']
    $ persistent._in_battle = False

    $ player_config.current_region = "r1m3"

    if random.random() <= 0.5:
        scene bg_m3nolisa with fade
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_1

    $ player_config.update_town_info("City", "Асгард", "free_traders_alliance")

    play music "music/town1.ogg" fadeout 1.0
    scene bg_asgard with fade

    "Приехав в Асгард вы подходите к местному бармену."

    show pablo at right with dissolve

    pablo "Чего желаете?"

    show mc6 at left with dissolve

    mc "Я тут слышал, поблизости есть один любопытный тоннель."
    mc "Прямо через горы на запад ведет. Не слыхал?"

    pablo "А как же, конечно слыхал. Я тут все знаю."

    mc "А не подскажешь, где он начинается?"

    pablo "Давай, я помечу на твоей карте."

    hide mc6
    show mc_2 at left, stretch_in

    mc "Так просто? Ни денег тебе не надо, ни помощи?"

    hide pablo
    show pablo at right, stretch_in

    pablo "Молодой человек, не надо учить меня коммерции."

    mc "Что ты, я и не думал даже!"

    "Бармен делает отметку на вашей карте и после этого вы отправляетесь к туннелю."

    hide pablo
    hide mc_2

    if random.random() <= 0.5:
        $ current_music = renpy.music.get_playing(channel='music')

        if current_music and current_music not in battle_tracks:
            $ persistent._prebattle_music = current_music
        else:
            $ persistent._prebattle_music = None
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_36

    jump tunnelfirst