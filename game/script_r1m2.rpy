# TODO: Make a video cutscene when leaving to r1m1 and to r1m3

# Without Lisa route

label arrivetor1m2:
    
    if not config.developer:
        pause 0.5

        show bg_r1m2load at truecenter

        $ level_slides = ["loadinglvl0","loadinglvl1","loadinglvl2","loadinglvl3","loadinglvl4","loadinglvl5","loadinglvl6"]

        call show_loading(level_slides) from _call_show_loading_1

        scene black

    $ _game_menu_screen = "save_screen"
    $ _menu = True
    $ config.keymap['save'] = ['save']
    $ config.keymap['load'] = ['load']
    $ config.keymap['game_menu'] = ['game_menu']
    $ persistent._in_battle = False

    $ renpy.notify("Игра сохранена в слот 1.")
    $ renpy.save("checkpoint-1")

    play music "music/driving2.ogg" fadeout 1.0

    $ TakeGunFromZaimka = "False"

    $ player_config.current_region = "r1m2"
    
    scene bg_ridzin with fade

    "Приехав в соседний регион вы оказались в замешательстве."
    mc "А где тут вообще находится Восточное?.."
    mc "Поеду дальше по дороге, надеюсь сориентируюсь."
    scene bg_razvyazka with dissolve
    "Вы доехали до первой развязки и вновь задумались."
    mc "Так. А здесь то куда?"
    mc "Прямо вроде \"тупик\". Значит нужно поехать направо."

    scene bg_loot with dissolve
    $ randommus = random.randint(1, 2)
    $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')

    "Однако впереди вы замечаете лежащий в развалинах ящик."
    mc "Там может быть что-то полезное..."
    mc "Однако он охраняется..."

    menu:
        "Атаковать охранника":
            $ renpy.notify("Игра сохранена в слот 2.")
            $ renpy.save("checkpoint-2")
            jump attackforloot

        "Двигаться дальше в Восточное":
            $ renpy.notify("Игра сохранена в слот 2.")
            $ renpy.save("checkpoint-2")
            jump movetovostochnoe

label attackforloot:
    $ renpy.music.play(f"audio/music/battle{randommus}.ogg", channel='music')

    $ persistent.player_max_hp = CarHP.get(player_config.car, CarHP["Van"])

    if persistent.player_hp is None:
        $ persistent.player_hp = persistent.player_max_hp

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "lootdefender"
    $ player_hp = persistent.player_hp
    $ player_max_hp = persistent.player_max_hp
    $ enemy_hp = 200
    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = persistent.player_heals
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ bgname = "bg_fightforloot"
    $ EnemyType = "Regular"
    $ enemy_damage_multiplier = 1.0

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
        $ renpy.sound.stop(channel="shoot")
        
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
        $ renpy.sound.stop(channel="shoot")
        $ persistent.player_hp = player_hp
        $ persistent.player_heals = remainheals

        play sound "sfx/explosion04.wav"
        hide lootdefender with dissolve

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

        jump defeateddefender

label defeateddefender:

    mc "Посмотрим, что в этом ящике..."
    $ randomgun = random.randint(1, 9)

    if player_config.try_add_item(player_config.current_gun):
        $ renpy.notify(f"В ваш инвентарь добавлен {gun_names.get(player_config.current_gun, player_config.current_gun)}.")
    else:
        $ price = ItemPricesCity.get(player_config.current_gun)
        $ player_config.add_money(price)
        $ renpy.notify(f"В вашем инвентаре недостаточно места! {gun_names.get(player_config.current_gun, player_config.current_gun)} автоматически продан за {price} монет.")

    if 1 <= randomgun <= 3:
        "Вы нашли оружие \"Корд\"!"
        $ player_config.current_gun = "Kord"
        $ player_config.gun_type = "Firearm"
    elif 4 <= randomgun <= 6:
        "Вы нашли оружие \"ПКТ\"!"
        $ player_config.current_gun = "PKT"
        $ player_config.gun_type = "Firearm"
    else:
        "Вы нашли оружие \"Шторм\"!"
        $ player_config.current_gun = "Storm"
        $ player_config.gun_type = "Shotgun"

    mc "О, то что нужно!"
    mc "Пора таки двигаться в Восточное."

    jump movetovostochnoe

label movetovostochnoe:

    $ player_config.update_town_info("City", "Восточное", "farmers_union")

    play music "music/bar.ogg" fadeout 1.0
    scene bg_vostochnoe with fade

    "Приехав в Восточное вы не знаете к кому обратиться."
    show hose at left with dissolve
    "Однако замечаете человека, похожего на фермера и решаете подойти к нему."
    "Но он с ходу на вас бросается..."

    unknown "Сразу видать, нездешний."

    "Поняв, что \"дружеского\" приветствия не получится вы решаете сразу перейти к делу."

    show mchar at right, stretch_in

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

    $ player_config.town_type = "NotInCity"

    if random.random() <= 0.5:
        $ persistent._prebattle_music = renpy.music.get_playing(channel='music')
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_11

    jump tolocus

label tolocus:

    $ player_config.update_town_info("Village", "Локус", "technicians")

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

    mc "Странная она какая-то..."
    mc "Ладно, надо ехать в Мидгард."

    hide mc6 with dissolve

    if random.random() <= 0.5:
        $ persistent._prebattle_music = renpy.music.get_playing(channel='music')
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_12

    jump tomidgard

label tomidgard:

    $ player_config.update_town_info("City", "Мидгард", "technicians")

    scene bg_midgard with fade
    play music "music/town3.ogg" fadeout 1.0

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

    $ player_config.town_type = "NotInCity"

    "Вы выдвигаетесь в сторону Порто."

    jump toportoe1

label toportoe1:

    play music "music/driving1.ogg" fadeout 1.0

    scene bg_toporto with fade

    "Вы спокойно ехали в Порто и уже думали, что сопровождение окажется лёгкой прогулкой."

    $ randommus = random.randint(1, 2)
    $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
    scene bg_toportoe1 with dissolve

    $ renpy.notify("Игра сохранена в слот 3.")
    $ renpy.save("checkpoint-3")

    "Однако вы замечаете бандитскую машину."
    "Вам ничего не остаётся, кроме как начать с ней бой."

    $ renpy.music.play(f"audio/music/battle{randommus}.ogg", channel='music')

    $ persistent.player_max_hp = CarHP.get(player_config.car, CarHP["Van"])

    if persistent.player_hp is None:
        $ persistent.player_hp = persistent.player_max_hp

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "to_porto_e1"
    $ player_hp = persistent.player_hp
    $ player_max_hp = persistent.player_max_hp
    $ enemy_hp = 850
    $ bgname = "bg_toporto"
    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = persistent.player_heals 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ EnemyType = "Regular"
    $ enemy_damage_multiplier = 1.0

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
        $ renpy.sound.stop(channel="shoot")
        
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
        $ renpy.sound.stop(channel="shoot")
        $ persistent.player_hp = player_hp
        $ persistent.player_heals = remainheals

        play sound "sfx/explosion04.wav"
        hide to_porto_e1 with dissolve

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

        jump portoa

label portoa:

    $ player_config.update_town_info("City", "Порто", "technicians")

    play music "music/bar.ogg" fadeout 1.0

    scene bg_porto with fade

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

    $ player_config.town_type = "NotInCity"

    if random.random() <= 0.5:
        $ persistent._prebattle_music = renpy.music.get_playing(channel='music')
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_13

    jump backtomidgard

label backtomidgard:

    $ player_config.update_town_info("City", "Мидгард", "technicians")

    scene bg_midgard with fade

    play music "music/town3.ogg" fadeout 1.0

    "Обратно до Мидгарда вы добрались без каких-либо проишествий."

    show scientist at left with dissolve

    $ player_config.add_money(1000)
    $ renpy.notify("Вы получили 1000 монет.")

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

    $ player_config.town_type = "NotInCity"

    hide scientist with dissolve
    hide mchar with dissolve

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

    $ renpy.notify("Игра сохранена в слот 4.")
    $ renpy.save("checkpoint-4")

    mc "Отправляюсь немедленно! Спасибо за помощь."

    hide ben3 with dissolve
    hide mc5 with dissolve

    if random.random() <= 0.5:
        $ persistent._prebattle_music = renpy.music.get_playing(channel='music')
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_14

    scene black with fade

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True

    jump vaterlandfirst

# With Lisa route

label r1m2withlisa:

    if not config.developer:
        pause 0.5

        show bg_r1m2load at truecenter

        $ level_slides = ["loadinglvl0","loadinglvl1","loadinglvl2","loadinglvl3","loadinglvl4","loadinglvl5","loadinglvl6"]

        call show_loading(level_slides) from _call_show_loading_2

        scene black

    $ _game_menu_screen = "save_screen"
    $ _menu = True
    $ config.keymap['save'] = ['save']
    $ config.keymap['load'] = ['load']
    $ config.keymap['game_menu'] = ['game_menu']
    $ persistent._in_battle = False

    $ player_config.current_region = "r1m2"
    $ player_config.update_town_info("City", "Мидгард", "technicians")
    play music "music/town3.ogg" fadeout 1.0

    scene bg_midgard with fade

    "Вы без особых проблем добрались до Мидгарда и подходите к одному из местных."

    show scientist at left with dissolve

    unknown "Что тебе?"

    show mc5 at right with dissolve

    mc "Я ищу женщину, зовут ее Лиса."

    hide scientist
    show scientist at left, stretch_in

    unknown "Лиса была здесь недавно, а потом уехала в Порто."

    mc "Будем искать дальше."

    "Вы направились в Порто."

    if random.random() <= 0.5:
        $ persistent._prebattle_music = renpy.music.get_playing(channel='music')
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_31

    jump portolisa

label portolisa:

    scene bg_porto with fade
    play music "music/bar.ogg" fadeout 1.0
    $ player_config.update_town_info("City", "Порто", "technicians")

    "Вам эти поиски уже кажутся нескончаемыми. Но делать нечего - вы подходите к одному из местных жителей в Порто."

    show kane at left with dissolve

    kane "Если вы ко мне обращаетесь, то я вас внимательно слушаю."

    show mcsurp at right, stretch_in

    mc "Я ищу женщину, зовут её Лиса."

    kane "Лисы здесь не было уже давно."
    kane "Может быть, ее что-то задержало на полпути? Бандиты буйствуют на наших дорогах... "

    mc "Сейчас проверим."

    "Вы отправляетесь искать Лису по пути Порто - Мидгард."

    if random.random() <= 0.5:
        $ persistent._prebattle_music = renpy.music.get_playing(channel='music')
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_32

    jump lisanearporto

label lisanearporto:

    $ player_config.town_type = "NotInCity"
    play music "music/intensedialogue01.ogg" fadeout 1.0

    scene bg_lisarescue with fade

    $ renpy.notify("Игра сохранена в слот 5.")
    $ renpy.save("checkpoint-5")

    "Прямо недалеко от Порто вы заметили что-то странное..."

    if player_config.car == "Van":
        scene bg_lisarescue1_van with dissolve
    elif player_config.car == "Molokovoz":
        scene bg_lisarescue1_ml with dissolve

    unknown "Ага... Тебя-то здесь и не хватало..."

    scene bg_lisarescue2 with dissolve

    mc "Ни дня без боя..."

    stop music fadeout 1.0

    scene black with fade

    scene bg_lisarescue_fight with fade

    $ randommus = random.randint(1, 2)
    $ renpy.music.play(f"audio/music/battle{randommus}.ogg", channel='music')

    $ persistent.player_max_hp = CarHP.get(player_config.car, CarHP["Van"])

    if persistent.player_hp is None:
        $ persistent.player_hp = persistent.player_max_hp

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "lisarescue_fight"
    $ player_hp = persistent.player_hp
    $ player_max_hp = persistent.player_max_hp
    $ enemy_hp = 650
    $ damage_range = gun_stats.get(player_config.current_gun, gun_stats["Hornet"])
    $ max_heals = persistent.player_heals 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандиты"
    $ bgname = "bg_lisarescue_fight"
    $ EnemyType = "Regular"
    $ enemy_damage_multiplier = 1.1

    scene bg_lisarescue_fight
    show lisarescue_fight at center

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
        
        hide lisarescue_fight
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
        $ persistent.player_hp = player_hp
        $ persistent.player_heals = remainheals

        play sound "sfx/explosion04.wav"
        hide lisarescue_fight with dissolve

        jump lisasavedporto

label lisasavedporto:

    play music "music/intensedialogue02.ogg" fadeout 1.0

    $ renpy.scene()
    $ renpy.show(f"bg_lr_1_{player_config.car}_{player_config.current_gun}")
    $ renpy.with_statement(fade)

    lisa "Ты? Что ты здесь делаешь?"
    lisa "Ты всё испортил..."
    lisa "Ну, то есть... спасибо за чудесное избавление."

    mc "Я спас тебя, Лиса."
    mc "Теперь ты ответишь на мои вопросы: мне нужно знать, кто убил моего отца!"

    $ renpy.scene()
    $ renpy.show(f"bg_lr_2_{player_config.car}_{player_config.current_gun}")
    $ renpy.with_statement(dissolve)

    lisa "Что?"
    lisa "Кого?"
    lisa "Я ни при чём. Я никого не убивала!"
    lisa "И не думай повесить на меня мокрое дело!"

    mc "Да я тебя и не обвиняю."
    mc "По крайней мере до выяснения всех подробностей."

    play music "music/intensedialogue01.ogg" fadeout 1.0

    $ renpy.scene()
    $ renpy.show(f"bg_lr_3_{player_config.car}_{player_config.current_gun}")
    $ renpy.with_statement(dissolve)

    lisa "Так что же ты за мной притащился в такую даль?"

    mc "Я здесь задаю вопросы!"
    mc "Отвечай, кто убил жителей села Глухое?"
    mc "Кто совершил это злодеяние? Ты отправилась туда, когда мы расстались, и знаешь, что там произошло!"

    lisa "Так ты, значит... То есть..."
    lisa "Да, я была там, когда это произошло, и видела, кто это сделал."

    $ renpy.scene()
    $ renpy.show(f"bg_lr_4_{player_config.car}_{player_config.current_gun}")
    $ renpy.with_statement(dissolve)

    mc "Говори же!"

    lisa "Это были борцы за новый мировой порядок."
    lisa "Алый Рассвет - так они себя называют. Безжалостные убийцы с запада."
    lisa "Обычно они не выезжают за пределы своей страны, но сейчас они начали экспансию в соседние регионы."

    mc "Откуда ты знаешь столько про них?"

    lisa "Я много путешествую по миру, ищу новые способы... новые технологии."
    lisa "Куда только меня не заносило."

    mc "Но я всё равно не понимаю, зачем они убили невинных людей?"

    $ renpy.scene()
    $ renpy.show(f"bg_lr_5_{player_config.car}_{player_config.current_gun}")
    $ renpy.with_statement(dissolve)

    lisa "Это обычная тактика. Они совершат несколько неожиданных рейдов."
    lisa "А когда среди населения начнётся паника, они заявятся и предложат своё покровительство. Естественно, не бесплатно."

    mc "Какая низость!"
    mc "Я не позволю им протянуть свои грязные лапы к моей родине! Я убью их всех!"

    lisa "Не горячись, среди этих бандитов есть и те, кто пошёл служить, чтобы спасти свои семьи от голода."
    lisa "Есть и те, кого вынудили и запугали."
    lisa "На самом деле по-настоящему виноват только один человек - главарь, Аксель."
    lisa "На его железной воле держится вся империя зла. Если устранить его - могучая сила рассыпется как карточный домик."

    play music "music/quietdialogue03.ogg" fadeout 1.0

    $ renpy.scene()
    $ renpy.show(f"bg_lr_6_{player_config.car}_{player_config.current_gun}")
    $ renpy.with_statement(dissolve)

    mc "Ты права, отвечать должен тот, кто отдал приказ. Аксель будет повержен!"

    lisa "Знай же, что добраться до него очень и очень непросто. И придётся действовать не столько грубой силой, сколько хитростью."

    mc "Я справлюсь. Укажи только дорогу на запад."

    lisa "Я знаю только один путь – тоннель, идущий под горой. Спроси о нём в Асгарде. Прощай, герой!"

    mc "Прощай. Спасибо за помощь."

    $ renpy.notify("Игра сохранена в слот 6.")
    $ renpy.save("checkpoint-6")

    "После этого вы направились в Асгард."

    if random.random() <= 0.5:
        $ persistent._prebattle_music = renpy.music.get_playing(channel='music')
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_33

    scene black with fade

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    
    jump asgardtunnel