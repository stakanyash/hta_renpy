# TODO: Make a video cutscene when leaving to r1m1 and to r1m3

# Without Lisa route

label arrivetor1m2:

    $ CurrentRegion = "r1m2"
    
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
    $ enemy_image = "lootdefender"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = 400
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 20
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ bgname = "bg_fightforloot"
    $ EnemyType = "Regular"
    scene bg_fightforloot
    show lootdefender at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

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
    $ randomgun = random.randint(1, 9)

    if try_add_item("Hornet"):
        $ renpy.notify("В ваш инвентарь добавлен \"Шершень\".")
    else:
        $ renpy.notify("В вашем инвентаре недостаточно места!")
        "\"Шершень\" автоматически продан за 130 монет."

    if 1 <= randomgun <= 3:
        "Вы нашли оружие \"Корд\"!"
        $ CurrentGun = "Kord"
    elif 4 <= randomgun <= 6:
        "Вы нашли оружие \"ПКТ\"!"
        $ CurrentGun = "PKT"
    else:
        "Вы нашли оружие \"Шторм\"!"
        $ CurrentGun = "Storm"

    mc "О, то что нужно!"
    mc "Пора таки двигаться в Восточное."

    jump movetovostochnoe

label movetovostochnoe:

    $ TownType = "City"

    play music "music/bar.ogg" fadeout 1.0
    scene bg_vostochnoe with fade

    if Inventory:
        call selling from _call_selling_4

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

    $ TownType = "Village"

    scene bg_locus with fade
    play music "music/town2.ogg" fadeout 1.0

    if Inventory:
        call selling from _call_selling_5

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

    mc "Странная она какая-то..."
    mc "Ладно, надо ехать в Мидгард."

    hide mc6 with dissolve

    jump tomidgard

label tomidgard:

    $ TownType = "City"

    scene bg_midgard with fade
    play music "music/town3.ogg" fadeout 1.0

    if Inventory:
        call selling from _call_selling_6

    "Заехав в Мидгард вы стокнулись с явным негостеприимством..."

    show scientist at left with dissolve

    unknown "Из-под какого камня ты выполз? Сразу видно: невежественный фермер. Никто здесь с тобой даже разговаривать не будет."

    show mcsurp at right with dissolve

    mc "А в чём дело?"

    hide scientist
    show scientist at left, stretch_in

    unknown "Как в чём? Да ты когда последний раз в зеркало смотрел? Наш город - последний оплот цивилизации в этом проклятом мире."
    unknown "И всяким невежам здесь не место, особенно в музее, ещё экспонаты испортишь. Иди в бар, работяга."

    "Вы явно возмущены от такого приёма, но всё же сдерживаетесь от ответной агрессии."

    mc "Я думал, музей – для всех. Нести культуру в массы и всё такое."

    unknown "Вообще-то, так оно и есть… Наверное, я погорячился. Слушай, нам как раз нужен такой дикарь, как ты, чтобы защитить транспорт."
    unknown "Довезешь его в цельности и сохранности до Порто, тогда не только я закрою глаза на твоё происхождение, но и сам мэр руку пожмет."

    hide mcsurp
    show mc5 at right, stretch_in

    mc "Совсем вы тут сдурели со своей цивилизацией. Нормальному человеку помочь не можете."
    mc "Так и быть, доставлю ваш транспорт куда надо. Только потом не отвертишься, ответишь на все вопросы!"

    unknown "Безусловно! Отправляйся к завхозу, у него пройдёшь инструктаж."

    mc "Посмотрим, что у вас за завхоз."

    hide mc5 with dissolve
    hide scientist with dissolve

    mc "Да что-же это такое! Куда не зайди, с ходу так и наровят выгнать или оскорбить! Фермер в Восточном, бабка в Локусе, а теперь ещё и он! Безобразие!"

    "Вы идёте к завхозу."

    show zavhoz at left with dissolve

    zavhoz "Ты, что ли, доброволец? Хлипковат…"
    zavhoz "Надеюсь, водить и стрелять ты умеешь."

    show mchar at right with dissolve

    mc "Справлюсь, не волнуйся. Говори, куда ехать."

    zavhoz "Так, давай помечу на твоей карте пункт назначения и возможные места нападения бандитов."
    zavhoz "..."
    hide zavhoz
    show zavhoz at left, stretch_in
    zavhoz "Вот здесь - узкое место. Надо быть особенно бдительным."
    zavhoz "Транспорт будет ехать сам. Твоя задача - обеспечить безопасность во время движения и доставку груза."
    zavhoz "Ясно?"

    mc "Предельно. Когда выступаем?"

    zavhoz "Если готов, хоть сейчас. Можешь сделать покупки и установить необходимое оборудование."

    mc "Можем выдвигаться прямо сейчас."

    hide mchar with dissolve
    hide zavhoz with dissolve

    "Вы выдвигаетесь в сторону Порто."

    jump toportoe1

label toportoe1:

    play music "music/driving1.ogg" fadeout 1.0

    scene bg_toporto with fade

    "Вы спокойно ехали в Порто и уже думали, что сопровождение окажется лёгкой прогулкой."

    play music "music/alarm1.ogg"
    scene bg_toportoe1 with dissolve

    "Однако вы замечаете бандитскую машину."
    $ renpy.save("checkpoint-1")
    $ renpy.notify("Игра сохранена.")
    "Вам ничего не остаётся, кроме как начать с ней бой."

    play music "music/battle1.ogg"

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "to_porto_e1"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = 850
    $ bgname = "bg_toporto"
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 15 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ EnemyType = "Regular"
    scene bg_toporto
    show to_porto_e1 at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide to_porto_e1
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
        hide to_porto_e1 with dissolve

        jump portoa

label portoa:

    $ TownType = "City"

    play music "music/bar.ogg" fadeout 1.0

    scene bg_porto with fade

    if Inventory:
        call selling from _call_selling_7

    "Далее по пути вам больше никого не встретилось и вы спокойно доехали до Порто."

    show shon at right with dissolve

    shon "Спасибо, мил человек! Мы давно ждем этот груз, а то бандиты совсем озверели, все проходы перекрыли."

    show mc4 at left with dissolve

    mc "Рад был помочь."

    pause 1.0

    shon "Мы разгрузились. Ещё немного, и поедем обратно. Как будешь готов - свистни."

    mc "Отправляемся прямо сейчас!"

    hide mc4 with dissolve
    hide shon with dissolve

    jump backtomidgard

label backtomidgard:

    $ TownType = "City"

    scene bg_midgard with fade

    play music "music/town3.ogg" fadeout 1.0

    if Inventory:
        call selling from _call_selling_8

    "Обратно до Мидгарда вы добрались без каких-либо проишествий."

    show scientist at left with dissolve

    unknown "Кто помогает городу жить, тому и мы поможем. Что тебе было нужно?"

    show mchar at right with dissolve

    mc "Мне сказали, что здесь я смогу найти Бена Дросселя."

    unknown "Бена, говоришь?"
    unknown "..."
    hide scientist
    show scientist at left, stretch_in
    unknown "Знаем такого. Он построил себе хижину неподалеку, там и живет."
    unknown "Давай помечу на твоей карте."

    mc "Спасибо. Наконец-то я узнаю, кто я такой."

    hide scientist with dissolve
    hide mchar with dissolve

    "Однако перед тем, как отправиться к Бену вы решили купить себе новую машину."

    pause 1.0

    $ CurrentCar = "Molokovoz"

    "Вы купили новую машину \"Молоковоз\"."
    
    mc "Вот теперь можно ехать."

    jump firstmeetben

label firstmeetben:

    play music "music/bio07unloop.ogg" fadeout 1.0
    scene bg_ben1 with fade

    "Приехав к дому Бена вы заметили старика на балконе."

    mc "Это явно Бен..."

    play music "music/quietdialogue01.ogg" fadeout 1.0

    scene bg_ben with dissolve

    show ben1 at left, stretch_in

    ben "Айвен, неужели ты вернулся!?"
    ben "..."
    ben "Прости, молодой человек, обознался. Глаза уже не те…"
    ben "Что привело тебя ко мне?"

    show mchar at right with dissolve

    mc "Мой посёлок сожгли. Перед смертью мой отец сказал, что я приёмный сын, и сказал найти тебя."
    mc "Вот вещи моего настоящего отца. И вот я стою перед тобой и не знаю, что делать дальше."

    hide ben1
    show ben2 at left, stretch_in

    ben "Ёшкин кот! Неужели нашёлся!"

    hide mchar
    show mcsurp at right, stretch_in

    mc "Кто нашёлся?"

    ben "Смотри, как похож. Не зря я обознался."

    "Вы перестаёте что либо понимать."

    mc "Помедленнее! Объясни как следует."

    ben "Прости уж меня, что так тороплюсь. Такие дела творятся."
    hide ben2
    show ben3 at left, stretch_in
    ben "Слушай же: твой отец, настоящий, я имею в виду, – великий человек! Его имя – Айвен Го."
    ben "Он объехал весь мир, открывая новые земли и технологии."
    ben "Это он во многом предопределил весь путь развития человечества за последние, дай подумать, 30 лет!"

    hide mcsurp
    show mc5 at right, stretch_in

    mc "Так прямо и предопределил…"

    ben "Да-да! Именно! Его открытия помогли людям встать на ноги."
    ben "Мир, который ты видишь вокруг, стал таким совсем недавно. Ещё совсем недавно мы жались по своим домишкам, в темноте, без электричества, без связи."
    ben "Каждый был уверен, что в мире, кроме него, никого нет. А ты знал, что это твой отец открыл людям радио?"

    mc "Вообще-то, до этого момента я ничего не знал о своем отце."

    hide ben3
    show ben2 at left, stretch_in

    ben "Ах, да. Ну, так знай же теперь, каким великим человеком он был!"

    hide mc5
    show mcsurp at right, stretch_in

    mc "Что же случилось с ним? Он погиб?"

    ben "В том-то и дело, что никто не знает."
    hide ben2
    show ben3 at left, stretch_in
    ben "Однажды он просто пропал. Притом что его хорошо знали, и никто бы не осмелился поднять руку на него."
    ben "И к тому же Айвена было очень непросто победить в бою. Он сделал из своей машины просто чудо!"

    mc "Значит, отец может быть ещё жив?"

    ben "Столько времени прошло. Не стоит зря обнадёживаться."

    hide mcsurp
    show mc5 at right, stretch_in

    mc "Но ты говоришь, отец был лучшим! Он знал, что его ожидает опасное путешествие, и оставил след, по которому я смогу найти и спасти его."
    mc "Это загадочное письмо. И странный диск - они приведут меня к цели!"

    hide ben3
    show ben1 at left, stretch_in

    ben "Молодёжь…"
    ben "Когда-то и я был таким. Ты прав, не будем терять надежду. Я слишком стар для странствий, а тебе, я вижу, всё по плечу."

    mc "С чего же начать поиски?"

    ben "Твой диск непростой. Это что-то вроде книги. Правда, прочесть её будет сложно."
    ben "Раз твой отец эту книгу записал, значит, у него дома должно быть устройство, чтобы её прочесть. Кажется, его тайное убежище было где-то за Пештом, на северо-востоке."
    hide ben1
    show ben3 at left, stretch_in
    ben "Поезжай туда, а я пока пороюсь в книгах. Может быть, придумаю что-нибудь ещё. В добрый путь."

    mc "Отправляюсь немедленно! Спасибо за помощь."

    hide ben3 with dissolve
    hide mc5 with dissolve

    jump vaterlandfirst

# With Lisa route