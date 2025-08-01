# TODO: Make a video cutscene when leaving to r1m2 (high priority) and r1m1 (middle priority)

# Default start-up

label vaterlandfirst:
    $ CurrentRegion = "r1m3"

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

    $ TownType = "City"

    play music "music/town1.ogg" fadeout 1.0
    scene bg_asgard with fade

    if Inventory:
        call selling from _call_selling_9

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

    $ TownType = "Village"

    play music "music/bar.ogg" fadeout 1.0
    scene bg_mvillage with fade

    if Inventory:
        call selling from _call_selling_10

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
    $ enemy_image = "minerattackers"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = 2000
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 20
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандиты"
    $ bgname = "bg_mvillage_fight"
    $ EnemyType = "Regular"
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

        $ drops = get_random_drops()

        if drops:
            python:
                drop_names_text = []
                dropped_something = False

                for drop_id, drop_name in drops:
                    if try_add_item(drop_id):
                        drop_names_text.append(drop_name)
                        dropped_something = True
                    else:
                        renpy.say(None, "В вашем инвентаре не хватает места!")

                if dropped_something:
                    drop_names_str = ", ".join(drop_names_text)
                    renpy.say(None, f"Найдены следующие предметы: {drop_names_str}")

        jump mvillageafterfight

label mvillageafterfight:

    scene bg_mvillage with dissolve
    play music "music/bar.ogg" fadeout 1.0

    if Inventory:
        call selling from _call_selling_11

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
    $ enemy_image = "brigde_defender"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = player_hp
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 20
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандиты"
    $ bgname = "bg_nearbridge"
    $ EnemyType = "Regular"

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

        $ drops = get_random_drops()

        if drops:
            python:
                drop_names_text = []
                dropped_something = False

                for drop_id, drop_name in drops:
                    if try_add_item(drop_id):
                        drop_names_text.append(drop_name)
                        dropped_something = True
                    else:
                        renpy.say(None, "В вашем инвентаре не хватает места!")

                if dropped_something:
                    drop_names_str = ", ".join(drop_names_text)
                    renpy.say(None, f"Найдены следующие предметы: {drop_names_str}")

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

    $ TownType = "City"

    if Inventory:
        call selling from _call_selling_12

    hide pguard
    hide mc5

    jump minin1st_nl

label minin1st_nl:

    $ TownType = "City"

    scene bg_minin with fade
    play music "music/town3.ogg" fadeout 1.0

    if Inventory:
        call selling from _call_selling_13

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

    $ TownType = "City"

    play music "music/town3.ogg" fadeout 1.0
    scene bg_minin with fade

    if Inventory:
        call selling from _call_selling_14

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

    if Inventory and FarmEnabled == True:
        $ FarmEnabled = False
        call selling from _call_selling_15

    hide mworker
    hide mc_2
    show mworker at right
    show mc_2 at left

    menu:
        "Дать 100 монет" if CurrentMoney >= 100:
            $ CurrentMoney -= 100
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

            stop music fadeout 1.0

            jump oilmine1st
        "\"У меня пока нет денег...\"" if R1M3FarmCount <= 5:
            mc "У меня пока нет денег."

            hide mworker
            hide mc_2 with dissolve

            "Вы отправились искать врагов, чтобы заработать денег..."

            $ FarmEnabled = True

            jump fightformoney
        "Продать предметы" if Inventory:
            jump r1m3sellalias

label r1m3sellalias:

    call selling from _call_selling_16

    jump hundredcointosharki

label fightformoney:

    if FarmEnabled == True and R1M3FarmCount <= 5:

        $ R1M3FarmCount += 1

        call randomfight

        scene bg_minin with fade
        play music "music/town3.ogg" fadeout 1.0
        jump hundredcointosharki
    else:
        "Больше здесь добыть не получится."
        play music "music/town3.ogg" fadeout 1.0
        jump hundredcointosharki

label oilmine1st:

    scene bg_oilenemy with fade

    play music "music/alarm1.ogg"

    $ renpy.save("checkpoint-2")
    $ renpy.notify("Игра сохранена.")
    
    "Приехав к нефтянной вышке вы действительно видите множество бандитов."

    "Между вами начинается вполне ожидаемая битва."

    play music "music/battle1.ogg"

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "oilbandits"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = player_hp
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 15 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Захватчики вышки"
    $ bgname = "bg_oil"
    $ EnemyType = "Regular"

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
        
        hide oilbandits
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
        hide oilbandits with dissolve

        jump oilisfree

label oilisfree:

    scene bg_oillastenemy with fade

    mc "Что ж, вышка освобождена!"
    mc "Последний враг бежал. Он может привести меня к базе бандитов."
    mc "Но надо ли мне это?"

    menu:
        "Проследить":
            $ renpy.save("checkpoint-3")
            jump followlastone

        "Ехать обратно в Минин":
            $ renpy.save("checkpoint-3")
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
    play music "music/battle2.ogg"

    "Приехав на базу вас сразу начали атаковать три машины."
    $ renpy.save("checkpoint-4")
    $ renpy.notify("Игра сохранена.")
    mc "Всё таки заметил..."

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "banditsonbase"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = player_hp
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 15 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандиты"
    $ bgname = "bg_oilspy_fight"
    $ EnemyType = "Regular"

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

        play sound "sfx/explosion04.wav"
        hide banditsonbase with dissolve

        jump banditbaseelim

label banditbaseelim:

    if random.random() <= 0.4:
        if try_add_item("Elephant") == True:
            "Расправившись с бандитами вы заметили, что у одного из них стоит неплохое оружие."

            mc "Надо бы забрать себе."

            $ GotElephant = True

            "Вы получили предмет \"Слон\"."
        else:
            $ GotElephant = False
    else:
        $ GotElephant = False

    mc "Пора ехать в Минин."

    if random.random() <= 0.3:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight

    jump minin3rd_nl

label minin3rd_nl:

    $ TownType = "City"

    play music "music/town3.ogg" fadeout 1.0
    scene bg_minin with fade

    $ elprice = random.randint(19000, 28000)

    $ weapon_prices = {
        "Вектор": 5520,
        "Вулкан": 5630,
        "КПВТ": 6400,
        "Шмель": 13310,
        "Ураган": 14910,
        "Флаг": 17860,
    }

    $ oldweapon_price = {
        "Hornet": 280,
        "PKT": 1670,
        "Storm": 3450,
        "Kord": 3680
    }

    if Inventory:
        call selling

    if CurrentCar == "Molokovoz":
        if CurrentMoney >= 19000:
            "Ваших средств достаточно для обновления кузова и установки нового оружия."
            "Хотите установить кузов \"Бокс\"? Цена покупки: 10000."
            menu:
                "Установить":
                    $ renpy.save("checkpoint-6")
                    $ CurrentMoney -= 10000
                    "Вы установили кузов \"Бокс\" и отдали 10000 монет."
                    $ OldWeaponPrice = oldweapon_price.get(CurrentGun, oldweapon_price["Hornet"])
                    $ CurrentGun = "None"
                    $ CurrentCargo = "Box"
                    if CurrentMoney >= 5520:
                        $ CurrentMoney += OldWeaponPrice
                        "Нужно установить новое оружие. Ваше старое оружие автоматически продано за [OldWeaponPrice] монет."

                        python:
                            affordable_weapons = [name for name, price in weapon_prices.items() if price <= CurrentMoney]
                            weapon_text = ", ".join(affordable_weapons)
                        "Ваших средств достаточно на: [weapon_text]."
                        menu:
                            "Вектор" if CurrentMoney >= 5520:
                                $ CurrentMoney -= 5520
                                $ CurrentGun = "Vector" 
                                $ GunType = "BigGun"
                                "Вы установили оружие \"Вектор\" и отдали 5520 монет. У вас осталось [CurrentMoney] монет."
                                $ renpy.save("checkpoint-1")

                            "Вулкан" if CurrentMoney >= 5630:
                                $ CurrentMoney -= 5630
                                $ CurrentGun = "Vulcan" 
                                $ GunType = "BigGun"
                                "Вы установили оружие \"Вулкан\" и отдали 5630 монет. У вас осталось [CurrentMoney] монет."  
                                $ renpy.save("checkpoint-1")

                            "КПВТ" if CurrentMoney >= 6400:
                                $ CurrentMoney -= 6400
                                $ CurrentGun = "KPVT" 
                                $ GunType = "BigGun"
                                "Вы установили оружие \"КПВТ\" и отдали 6400 монет. У вас осталось [CurrentMoney] монет."  
                                $ renpy.save("checkpoint-1")

                            "Шмель" if CurrentMoney >= 13310:
                                $ CurrentMoney -= 13310
                                $ CurrentGun = "Bumblebee" 
                                $ GunType = "BigGun"
                                "Вы установили оружие \"Шмель\" и отдали 13310 монет. У вас осталось [CurrentMoney] монет."
                                $ renpy.save("checkpoint-1")

                            "Ураган" if CurrentMoney >= 14910:
                                $ CurrentMoney -= 14910
                                $ CurrentGun = "Hurricane" 
                                $ GunType = "BigGun"
                                "Вы установили оружие \"Ураган\" и отдали 14910 монет. У вас осталось [CurrentMoney] монет."
                                $ renpy.save("checkpoint-1")

                            "Флаг" if CurrentMoney >= 17860:
                                $ CurrentMoney -= 17860
                                $ CurrentGun = "Flag" 
                                $ GunType = "BigGun"
                                "Вы установили оружие \"Флаг\" и отдали 17860 монет. У вас осталось [CurrentMoney] монет."
                                $ renpy.save("checkpoint-1")
                                    

                "Не устанавливать":
                    $ renpy.save("checkpoint-6")
                    $ CurrentCargo = "Tent"
                    $ GunType = "SmlGun"

                    "Вы решили не устанавливать новый кузов. На вашем балансе: [CurrentMoney] монет."

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

    if random.random() <= 0.3:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight

    jump minin4th_nl

label minin4th_nl:

    $ TownType = "City"

    play music "music/town3.ogg" fadeout 1.0
    scene bg_minin with fade

    if Inventory:
        call selling from _call_selling_17

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

    if random.random() <= 0.3:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight

    jump oilmine2nd

label oilmine2nd:

    $ TownType = "Village"
    
    play music "music/bar.ogg" fadeout 1.0
    scene bg_oil with fade

    if Inventory:
        call selling from _call_selling_18

    show OilMineWorker at left with dissolve

    chris "Вот и первая бочка нефти."

    show mchar at right, stretch_in

    mc "Я отвезу её в город и расскажу всем, что больше не будет перебоев с топливом."
    mc "Специально поставлю её в кабину, чтобы ничего не случилось…"

    "Вы грузите бочку нефти в машину и уезжаете в Минин."

    if random.random() <= 0.3:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight

    jump minin5th_nl

label minin5th_nl:

    $ TownType = "City"

    play music "music/town3.ogg" fadeout 1.0
    scene bg_minin with fade

    if Inventory:
        call selling from _call_selling_19

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

    "Вы направились вслед за караваном в соседний регион."

    if random.random() <= 0.3:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight

    jump r1m4start

# With Lisa route