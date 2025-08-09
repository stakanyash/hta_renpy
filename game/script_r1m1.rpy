# TODO: Make a video cutscene when leaving to r1m3

label main_game:

    $ _game_menu_screen = "save_screen"
    $ _menu = True
    $ config.keymap['save'] = ['save']
    $ config.keymap['load'] = ['load']
    $ config.keymap['game_menu'] = ['game_menu']
    $ persistent._in_battle = False

    play music "music/bio07unloop.ogg" fadeout 1.0

    scene black with fade

    "{cps=20}История не сохранила точных сведений о тёмных временах, наступивших сразу после Катастрофы. Доподлинно известно лишь то, что люди выжили в отравленном воздухе благодаря защитным маскам.{/cps}"

    "{cps=20}Это творение неизвестного изобретателя уравняло всех. Тонкая преграда, вставшая на пути неминуемой смерти, стала символом нового человечества. Маски сплотили людей и придали им силы бороться за место под солнцем.{/cps}"

    "{cps=20}Возникли новые поселения вдали от прежних городов, ставших братскими могилами. Постепенно были налажены связи между разрозненными группами выживших.{/cps}"

    "{cps=20}Фермеры, шахтёры, торговцы – возвращение к простым занятиям пошло только на пользу растерянным людям.{/cps}"

    "{cps=20}Но человек остаётся человеком во все времена. Остались те, кто сохранял мудрость веков, чтобы делиться ею с миром.{/cps} {cps=10}Были и те, кто предпочёл созиданию разрушение.{/cps}"

    "Вы тихо и мирно спали, как вдруг вас разбудил отец..."

    play music "music/quietdialogue01.ogg" fadeout 1.0

    scene bg_glukhoe with fade

    show fther at left with dissolve

    father "Проснулся, лежебока! Уже битый час я жду тебя, чтобы сказать кое-что весьма важное, а ты опять спишь как сурок..."

    show mchar at right with dissolve

    mc "И тебе доброе утро. Чего нервничаешь?"

    hide fther

    show fther2 at left, stretch_in

    father "Ладно, остынь."

    father "Вот так..."

    father "Сегодня большой день в твоей жизни. Ты всегда был мне верным подспорьем и многому научился от меня..."

    father "В общем, я решил, что настало время твоего совершеннолетия."

    father "Теперь ты настоящий мужчина и можешь делать всё, что пожелаешь, даже завести семью... Кхе, но лучше, конечно, сперва спросить разрешения."

    hide mchar

    show mcsurp at right, stretch_in

    mc "Неужели этот день настал?! Я думал, меня будут до старости мариновать на этой ферме!"

    mc "То есть, я хотел сказать, спасибо огромное, постараюсь оправдать оказанное мне доверие, сэр!"

    father "Опять ты ёрничаешь, а мне столько надо тебе сказать..."

    scene bg_caniride

    show mcsurp at right

    show fther2 at left

    mc "Что, прямо сейчас могу сесть и ехать куда захочу?"

    father "Ну, если ты так торопишься сесть за руль, то отправляйся в Южный и передай Серго этот пакет. А разговор отложим до твоего приезда."

    hide mcsurp

    show mc3 at right, stretch_in

    play sound "sfx/enginestart.wav"

    mc "Ур-ра-а! Я мигом! Бывай, старик."

    play music "music/driving1.ogg" fadeout 2.0

    hide mc3
    hide fther2
    scene bg_tosowth with fade

    "Вы поехали на стареньком грузовике в Южный, чтобы встретиться с Серго и передать ему посылку."

    play music "music/battle02.ogg" fadeout 1.0

    scene bg_firstenemy with fade

    "Однако вы замечаете на своём пути явно недружественный автомобиль."

    jump firstenemyfight

label firstenemyfight:
    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "firsteverenemy"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = 250
    $ bgname = "bg_firsteverenemy"
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 15 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ EnemyType = "Regular"
    scene bg_firsteverenemy
    show firsteverenemy at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide firsteverenemy
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
        hide firsteverenemy with dissolve

        play music "music/driving1.ogg" fadeout 1.0

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

        if random.randint(1,2) == 1:
            $ randommus = random.randint(1, 2)
            $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
            "На вас нападают!"
            call randomfight from _call_randomfight

        jump afterfirstattack

label afterfirstattack:

    scene bg_sowth with fade

    "По пути вы разделались ещё с парой бандитов, однако у Южного вам повстречалась очень интересная персона..."

    play music "music/passage01unloop.ogg" fadeout 0.5

    show lisa2 with dissolve

    lisa "Добрый день, юноша. Есть минутка?"

    "Я был немного ошарашен и волнительно спросил..."

    show lisa2 at right with dissolve
    show mc_2 at left with dissolve

    mc "Это вы мне?"

    lisa "Я смотрю, ты крутой водила, наверное, всю округу исколесил? Мне бы один груз помочь довезти, а я плохо знаю местность. Не съездишь со мной по окрестным деревням?"

    "Я только сел за руль и меня первая встречная девушка называет крутым водилой? Что-то тут не так..."

    mc "А что, собственно, за груз?"

    hide lisa2

    show lisa at right, stretch_in

    lisa "Да какая тебе разница? Дельце плёвое, а заплачу я хорошо."

    "Стоит ли мне в начале моей карьеры связываться с бандитами? Вовек потом не отмоешься!"

    lisa "Чего так крепко задумался? Согласен?"

    menu:
        "Согласиться":
            $ renpy.save("checkpoint-2")
            $ LisaAgreed = "True"
            jump lisaagree

        "Отказать":
            $ renpy.save("checkpoint-2")
            $ LisaAgreed = "False"
            jump lisarefuse

label lisaagree:

    mc "А почему бы и нет."

    play music "music/driving1.ogg" fadeout 1.0

    hide lisa with dissolve
    hide mc_2 with dissolve

    "Вы поехали по соседним деревням. Сначала решили заехать в Заимку."

    if random.randint(1,2) == 1:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_1

    jump secondenemy

label lisarefuse:

    mc "При всём моём уважении вынужден отказаться. С бандитами дел не имею!"
    lisa "Какая принципиальность! Ладно, без обид. Найду другого лопуха. Чао."
    mc "Я, пожалуй, тоже поеду."

    hide lisa with dissolve
    hide mc_2 with dissolve

    play music "music/driving1.ogg" fadeout 0.5

    "Странно всё это... Не важно. Пойду искать Серго."

    play music "music/town1.ogg" fadeout 1.0

    jump sergo

label secondenemy:

    scene bg_secenemy with fade

    play music "music/alarm1.ogg" fadeout 0.5

    "Однако не успели вы отъехать от Южного как на вас снова нападает бандит. Только в этот раз он уже чутка серьёзнее Клопа."

    "Вам ничего не остаётся, кроме как начать с ним перестрелку."

    play music "music/battle1.ogg"

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True
    $ enemy_image = "secenemy"
    $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
    $ player_max_hp = player_hp
    $ enemy_hp = 500
    $ bgname = "bg_secondenemy"
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 15 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Бандит"
    $ EnemyType = "Regular"
    scene bg_secondenemy
    show secenemy at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide secenemy
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
        hide secenemy with dissolve

        play music "music/driving2.ogg" fadeout 1.0

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

        if LisaAgreed == "True":
            jump tozaimka
        elif LisaAgreed == "False":
            jump dickzapravka

label tozaimka:

    $ TownType = "Village"

    scene bg_zaimka with fade

    "Вы приехали в Заимку. Остановившись вы услышали от Лисы..."

    show lisa2 at right with dissolve

    lisa "Подожди-ка здесь, пока я закончу свои дела."

    "Вы пытаетесь понять что-же она ищет, но не слышите о чём Лиса говорит с местными жителями."

    lisa "Готово. Поехали дальше."

    hide lisa2 with dissolve

    if random.randint(1,2) == 1:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_2

    scene bg_gugulino with dissolve

    "Всё тоже самое было в Гугулино..."

    scene bg_troitckoe with dissolve

    play music "audio/music/intensedialogue02.ogg" fadeout 1.0

    "А вот в Троицком..."

    show lisa at right with dissolve

    lisa "Чёрт возьми, сколько времени потрачено впустую! Я же знаю, что он где-то здесь!"

    lisa "Парень, мы точно объехали все здешние поселения?"

    show mc_2 at left with dissolve

    mc "Да, все деревни, как ты и сказала. Правда, осталось ещё одно село, Глухое."

    mc "Но там ты точно не найдёшь покупателей на свой товар. А что именно ты ищешь?"

    "Лиса явно раздражена этим ответом."

    lisa "Так что ты мне тут голову морочишь? Как туда проехать?"

    mc "Вообще-то, это на север отсюда за горами, совсем недалеко, но напрямик дороги нет. Нам придётся ехать через Южный..."

    lisa "Здесь наши пути расходятся: надоело мне тащиться следом за твоей развалюхой. К тому же там, где для тебя нет дороги, моя машина пройдёт с лёгкостью."

    $ CurrentMoney += 500

    lisa "Ты выполнил свою часть сделки. Держи свои деньги."

    play music "audio/music/passage01unloop.ogg" fadeout 1.0

    hide lisa with dissolve

    "После этого Лиса спешно удаляется."

    play music "audio/music/quietdialogue01.ogg" fadeout 1.0

    mc "Что же она искала? Пора и мне домой возвращаться. Узнаю, из-за чего отец так волновался."

    mc "Но сначала мне надо заехать отдать посылку Серго. А то совсем из головы вылетело."

    hide mc_2 with dissolve

    "Вы направились в Южный."

    if random.randint(1,2) == 1:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_3

    play music "music/town1.ogg" fadeout 1.0

    jump sergo

label sergo:

    $ TownType = "City"
    $ TownName = "Южный"
    $ GroupLogo = "farmers_union"

    scene bg_insowth with fade

    if LisaAgreed == "True":
        "Вы добрались до Южного и заехали в город. Спустя несколько секунд поисков вы находите Серго."
    elif LisaAgreed == "False":
        "Вы заехали в город и усердно ищете Серго. Спустя несколько секунд вы его находите."

    show sergo at left with dissolve

    sergo "Кто здесь у нас? Надеюсь, по делу?"

    show mchar at right with dissolve

    mc "День добрый! Вы Серго? Я приехал из Глухого и привёз вам этот пакет."

    sergo "Да, это я! А ты, видимо, сын Петра. Совсем уже взрослый, ездишь в одиночку…"

    hide sergo

    show sergo2 at left, stretch_in

    sergo "Опасные нынче времена: совсем бандиты распоясались. Еле добрался до Южного, двух охранников загубил. Наверное, это будет моя последняя поездка сюда."

    "В глубине души вы расстроились от этой новости, но не проявили этого на лице."

    hide mchar

    show mcsurp at right, stretch_in

    mc "Это мой первый рейс. Так что насчёт посылки?"

    sergo "Прыткий юноша. Давай посмотрим..."

    pause 1.0

    hide sergo2

    show sergo3 at left, stretch_in

    $ CurrentMoney += 200
    $ renpy.notify("Вы получили 200 монет.")

    sergo "Товар, как всегда, отличный. Держи, это твоя награда за доставку."

    mc "Спасибо, вообще-то, я и не рассчитывал ни на что."

    sergo "Ты очень мне помог. Передавай привет отцу."

    mc "Обязательно передам."

    hide sergo3 with dissolve

    "Вы уже собирались ехать домой, как тут вас подзывает странный тип."

    show farmerdi at left with dissolve

    unknown "Я вижу, у вас влиятельные знакомые, молодой человек. Не окажете ли Вы мне небольшую услугу?"

    mc "Посмотрим, а в чём, собственно, дело? И кто ты вообще такой?"

    hide farmerdi

    show farmerdi at left, stretch_in

    dick "Называй меня просто Фермер Дик. Я случайно застал Вашего знакомого, Серго, когда был здесь по делам."

    dick "У меня к нему есть важный разговор, который приведёт к взаимовыгодному сотрудничеству. Но, к сожалению, у меня с собой нет необходимых документов…"

    "Вы начинаете понимать к чему всё идёт..."

    mc "Говори проще, что тебе нужно…"

    dick "Отвезите меня на бензозаправку, пока Серго ещё не отправился на север. Я смогу подготовить необходимые документы и вернусь сюда своими силами."

    menu:
        "Согласиться":
            mc "Садись, показывай дорогу…"
            hide farmerdi with dissolve
            hide mcsurp with dissolve
            "Фермер сел в вашу машину и вы поехали в сторону заправки по его наводке."

            if LisaAgreed == "False":
                jump secondenemy
            elif LisaAgreed == "True":
                if random.randint(1,2) == 1:
                    $ randommus = random.randint(1, 2)
                    $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
                    "На вас нападают!"
                    call randomfight from _call_randomfight_4
                
                $ TownType = "NotInCity"
                jump dickzapravka

        "Отказать":
            mc "Нет, слишком далеко ехать. Меня дома ждут."
            hide farmerdi
            show farmerdi at left, stretch_in
            dick "Ты сорвал самую крупную сделку в моей жизни! Видеть тебя не желаю!"
            mc "Спокойно, спокойно…"

            hide farmerdi with dissolve
            hide mcsurp with dissolve

            "Вы спокойно уходите, а Фермер продолжает ругаться на вас в след."
            "Странный какой-то тип. Не зря я ему отказал."
            if LisaAgreed == "True":
                $ TownType = "NotInCity"
                jump felixmeet
            elif LisaAgreed == "False":
                $ TownType = "NotInCity"
                jump glukhoeburn

label dickzapravka:

    scene bg_zapravka with fade

    "Вы приехали к заправке. Фермер явно чем-то недоволен..."

    show farmerdi at left, stretch_in

    dick "М-да… Можно было и побыстрее. Мне же ещё все бумаги надо найти и подготовить."

    "Вы не стали терпеть такой наглости и ответили ему достаточно дерзко."

    show mcsurp at right, stretch_in

    mc "Плати деньги и проваливай из моей машины!"

    hide farmerdi
    show farmerdi at left, stretch_in

    dick "Обратно я найду себе другого водилу, порасторопнее."

    mc "Вчера в подворотне, а сегодня здесь - в моей машине!"

    mc "Ишь ты, не нравится ему, что так медленно! Для поездки в моей машине надо быть подготовленным! И вообще, мне не нравится твоя розовая курточка и твои…"

    hide farmerdi with dissolve

    "Не дав закончить фразу - Фермер уходит."

    hide mcsurp
    
    show mc3 at center, stretch_in

    mc "Да и пошёл он куда подальше! Надо бы уже домой возвращаться."

    hide mc3 with dissolve

    if LisaAgreed == "True":
        jump felixmeet
    elif LisaAgreed == "False":
        jump glukhoeburn

label felixmeet:

    scene bg_felix with fade

    play music "audio/music/intensedialogue01.ogg" fadeout 1.0

    "Вы возвращались домой, как вдруг вам встретился странный персонаж..."

    show felix with dissolve

    unknown "А вот и наш возмутитель спокойствия. Мои источники сообщают, что ты подвизался к Лисе в помощники, а она девушка щедрая..."

    unknown "За скромный вклад в 1000 монет ты можешь продолжать свои грязные делишки и даже рассчитывать на нашу поддержку."

    menu:
        "Отдать деньги":
            $ renpy.save("checkpoint-3")
            "Вы бы с радостью отдали деньги, чтобы от вас отстали, но у вас нет 1000 монет."
            jump felixbeforefight

        "Отказать":
            $ renpy.save("checkpoint-3")
            jump felixbeforefight

label felixbeforefight:

    hide felix

    show felix at left

    show mcsurp at right with dissolve

    mc "Да вы что? Откуда у меня такие деньги? И кто вы вообще такие?"

    "Видно, что незнакомца данный ответ не устраивает."

    hide felix

    show felix2 at left, stretch_in

    unknown "Придётся продать твою машину на запчасти, чтобы возместить нам моральный ущерб. Бей его!"

    hide felix2
    hide mcsurp

    scene bg_felixfight

    play music "audio/music/battle1.ogg"

    "Начинается перестрелка. Но кого-же атаковать сперва? Их ведь трое. А может вообще дать дёру?"

    menu:
        "Атаковать":
            $ _window_hide()
            $ _game_menu_screen = None
            $ _menu = False
            $ config.keymap['save'] = []
            $ config.keymap['load'] = []
            $ config.keymap['game_menu'] = []
            $ persistent._in_battle = True
            $ RunFromFelix = "False"
            $ enemy_image = "felixteam"
            $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
            $ player_max_hp = player_hp
            $ max_heals = 20
            $ enemy_hp = player_hp * 0.7
            $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
            $ turn_count = 0
            $ enemy_max_hp = enemy_hp
            $ heal_count = 0
            $ remainheals = max_heals - heal_count
            $ attack_locked = False
            $ enemy_name = "Бандиты"
            $ bgname = "bg_felix_nocars"
            $ EnemyType = "Regular"
            scene bg_felix_nocars
            show felixteam at center

            while enemy_hp > 0 and player_hp > 0:
                call screen enemy_ui

            if player_hp <= 0:
                $ _game_menu_screen = "save_screen"
                $ _menu = True
                $ config.keymap['save'] = ['save']
                $ config.keymap['load'] = ['load']
                $ config.keymap['game_menu'] = ['game_menu']
                $ persistent._in_battle = False
                
                hide felixteam
                play sound "sfx/explosion04.wav"
                jump fightlost
            else:
                $ _game_menu_screen = "save_screen"
                $ _menu = True
                $ config.keymap['save'] = ['save']
                $ config.keymap['load'] = ['load']
                $ config.keymap['game_menu'] = ['game_menu']
                $ persistent._in_battle = False

                hide felixteam with dissolve

                jump felixafterfight

        "Попытаться уехать":
            scene bg_felixrun with dissolve
            $ RunFromFelix = "True"
            "Вы пытаетесь уехать под шквалом огня. На удивление бандиты не бросаются за вами в погоню и спустя несколько секунд огонь прекращается."
            "Однако по рации вы слышите следующее..."
            jump felixafterfight

label felixafterfight:

    if RunFromFelix == "False":
        show felix2 with dissolve

    unknown "Мы ещё встретимся, щенок! Попомни мои слова, ты пожалеешь, что связался с Феликсом!"

    if RunFromFelix == "False":
        felix "Уходим!"
        hide felix2 with dissolve

    mc "Обязательно встретимся, Феликс..."

    if RunFromFelix == "True":
        "Вы починились на ближайшей заправке и продолжили путь до дома."
    elif RunFromFelix == "False":
        "Феликс со своей охраной поспешно удаляется, а вы поехали дальше домой."

    jump glukhoeburn


label glukhoeburn:

    scene black with fade

    stop music fadeout 1.0

    if LisaAgreed == "False":
        "Вы спокойно возвращались домой, гадая о чём же с вами хотел поговорить отец."
    elif LisaAgreed == "True":
        "Вы возвращались домой одновременно не понимая - что за чертовщина с вами произошла за столь короткое время. Но больше вас волновало о чём же хотел поговорить отец."

    scene bg_glburnaway with dissolve

    "Однако при подъезде к Глухому вы замечаете дым."

    "Понимая что что-то не так - вы жмёте газ в пол."

    scene bg_glburning with dissolve

    play sound "audio/sfx/burning.wav" channel "sfx2"

    "Оказавшись ближе у родной деревни вы видите, как она полностью охвачена огнём."

    if LisaAgreed == "True":
        jump deadfather
    elif LisaAgreed == "False":
        jump dyingfather

label deadfather:

    play music "audio/music/death01.ogg"

    "Вы обнаружили, что никого в живых уже не осталось."

    scene bg_fatherdead with dissolve

    mc "О нет! Отец!"

    mc "Что за чудовище могло сотворить такое..."

    mc "Все, кого я любил и знал, мертвы..."

    play sound "sfx/r1m1_1142_hero.ogg"

    mc "..."

    mc "Я могу сделать для них только одно: отомстить!"

    mc "Как бы далеко ни прятался убийца, я найду его даже на краю земли! И уничтожу!"

    mc "Слышишь, я найду тебя!"

    play music "music/battle02.ogg" fadeout 1.0

    scene bg_whatiffelix with dissolve

    show mc3 at center, stretch_in

    mc "А вдруг это Феликс собрал дружков и напал на беззащитную деревню?"

    mc "Если это так - ему не жить!"

    mc "Он бывает в баре Южного. Там я и начну поиски."

    hide mc3 with dissolve

    "Полностью раздосадованный вы уезжаете обратно в Южный."

    if random.randint(1,2) == 1:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_5

    jump sowthagain


label dyingfather:

    scene bg_dyingfather with dissolve

    play music "audio/music/sadness1.ogg"

    father "{cps=15}...сынок...!{/cps}"

    mc "О боже, отец! Что здесь произошло? Кто это сотворил?"

    father "{cps=15}Слушай внимательно. Ты мой приёмный сын. Возьми, это вещи твоего настоящего отца...{/cps}"

    father "{cps=15}Найди Бена Дросселя. Он исследователь.{/cps} {cps=10}Он поможет... Сын... не дай ненависти...{/cps} {cps=7}отравить твою...{/cps} {cps=5}душу...{/cps}"

    scene black with fade

    stop music fadeout 2.0

    pause 2.0

    play music "audio/music/death01.ogg"

    scene bg_afterfdeath with fade

    mc "Моя жизнь..."

    mc "Что же мне делать дальше?"

    mc "У меня ведь никого не осталось... {cps=10}и ничего...{/cps}"

    mc "Только это письмо..."

    scene bg_fatherdead with dissolve

    pause 1.0

    "{cps=15}\"Сын, если ты читаешь это письмо - значит я не смог вернуться и вырастить тебя сам. Я знаю, что Пётр отлично справился с этой задачей.\"{/cps}"

    "{cps=15}\"Я вижу тебя, такого молодого и полного сил, и сердце моё обливается слезами...\"{/cps}"

    "{cps=15}\"Я виню себя за то, что меня не было рядом, когда ты рос. И это моё страшное наказание. Но знай, что я не мог поступить иначе. Передо мной стоит задача всей жизни...\"{/cps}"

    "{cps=15}\"Только выполнив задуманное, смогу я успокоиться и вновь почувствовать себя человеком. Если нет... значит, я недостоин жить. Это письмо - извинение.\"{/cps}"

    "{cps=15}\"Прости меня, если сможешь. Ты всегда в моём сердце, сын...\"{/cps}"

    mc "Это всё? Никаких объяснений..."

    mc "Как я могу простить того, кого никогда не знал?"

    mc "Мне больше нечего здесь делать. Я отправлюсь на поиски Бена."

    mc "Кто бы это ни был, надеюсь, он поможет мне обрести себя."

    mc "Может быть, в Южном слышали о нём?"

    if random.randint(1,2) == 1:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_6

    jump sowthagain

label sowthagain:

    $ TownType = "City"

    stop sfx2

    scene bg_insowth with fade
    play music "music/town1.ogg" fadeout 1.0

    if LisaAgreed == "True":

        "Вы приехали в Южный и встретили местного бармена."

        show dronn at left with dissolve

        dronn "Что стряслось? На тебе лица нет."

        show mc5 at right with dissolve

        mc "Глухое сожгли, все погибли! Мой отец, все жители…"

        hide dronn
        show dronn at left, stretch_in

        dronn "Какой ужас! У нас уже много лет не случалось ничего подобного!"

        dronn "Но через Южный никто не проезжал. Мы бы заметили боевую технику…"

        mc "Значит, они приехали другим путем! Я должен их найти и отомстить!"

        dronn "Не горячись. Если у них достаточно сил, чтобы сжечь деревню и исчезнуть как дым, стоит ли тебе связываться с таким врагом?"

        "Вы немного возмущены таким ответом."

        hide mc5
        show mcsurp at right, stretch_in

        mc "Думай, что говоришь! Это же мой отец! И десятки невинных людей! Убийцы будут наказаны любой ценой!"

        "Бармен пытается вас успокоить."

        hide dronn
        show dronn at left, stretch_in

        dronn "Да я разве против! Дави гадов, если сможешь! Только как ты найдешь этих убийц, если их никто даже не видел?"

        mc "Есть у меня подозрения, что с этим связан Феликс. Не знаешь, где его найти?"

        "Бармен немного шокирован вашим заявлением."

        dronn "Феликс - опасный человек… Хотя я вижу, что тебе на это плевать."

        dronn "У него под началом небольшая бандитская деревенька или база."

        hide mcsurp
        show mc3 at right, stretch_in

        mc "Тогда это точно он! Собрал своих и…"

        dronn "Вообще-то у нас с ним что-то вроде договора о ненападении."

        dronn "Он никого не убивает, а мы не зовём наёмников, чтобы избавиться от него."

        mc "Уничтожение Глухого перечёркивает все соглашения! Я убью его!"

        if RunFromFelix == "False":
            mc "Я уже встречался с ним на поле боя и победил."

        dronn "Но теперь ты хочешь напасть на укреплённую базу. Не подумай, что я тебя отговариваю!"

        dronn "Я и сам давно хочу избавиться от этого нахлебника, а вот и повод. Только тебе понадобится более мощное вооружение."

        dronn "У меня в Заимке кое-что припрятано. Поезжай туда и скажи, что от меня."

        mc "Спасибо огромное!"

        hide dronn with dissolve
        hide mc3 with dissolve

        "Вы собираетесь ехать в Заимку, но тут у вас возникает мысль."

        mc "А точно ли мне нужно это \"более\" мощное вооружение? Неужели моего недостаточно?"

        menu:
            "Ехать в Заимку":
                $ TakeGunFromZaimka = "True"
                $ renpy.save("checkpoint-4")
                $ TownType = "NotInCity"
                if random.randint(1,2) == 1:
                    $ randommus = random.randint(1, 2)
                    $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
                    "На вас нападают!"
                    call randomfight from _call_randomfight_7
                play music "music/town2.ogg" fadeout 1.0
                jump KventinZaimka

            "Ехать сразу к Феликсу":
                $ TakeGunFromZaimka = "False"
                $ renpy.save("checkpoint-4")
                $ TownType = "NotInCity"
                if random.randint(1,2) == 1:
                    $ randommus = random.randint(1, 2)
                    $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
                    "На вас нападают!"
                    call randomfight from _call_randomfight_8
                jump felixbase

    elif LisaAgreed == "False":

        "Вы приехали в Южный и встретили местного бармена. Бармен начинает диалог сам."

        show dronn at left with dissolve

        dronn "Ты из Глухого?"

        show mc3 at right with dissolve

        mc "..."

        mc "На Глухое напали. Все погибли. Мой отец…"

        dronn "Мы слышали и соболезнуем. Всякое случается."

        dronn "Угощайся за счет заведения."

        mc "Спасибо, не надо. Я уезжаю отсюда. Никто не слышал ничего про Бена Дросселя или исследователей?"

        dronn "Нет, здесь тебе никто не поможет. Места у нас богом забытые."

        dronn "Попытай счастья в Восточном. Там вроде торговые пути сходятся, может, и узнаешь чего."

        "Вы не обрадованы этим ответом, но кажется сейчас это единственное, за что вы можете зацепиться."

        mc "Прощайте! Я отправляюсь искать свою судьбу."

        "Вы уходите из бара и начинаете ехать в сторону соседнего региона, где находится Восточный."

        hide dronn with dissolve
        hide mc3 with dissolve

        $ TownType = "NotInCity"

        if random.randint(1,2) == 1:
            $ randommus = random.randint(1, 2)
            $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
            "На вас нападают!"
            call randomfight from _call_randomfight_9

        scene black with fade

        jump leaver1m1toridzin

label KventinZaimka:

    $ TownType = "Village"

    scene bg_zaimka with fade

    "Приехав в Заимку вы ищете того, о ком говорил Дронн."

    show kventin at left with dissolve

    kventin "Я могу тебе чем-то помочь?"

    show mc3 at right with dissolve

    mc "Бармен из Южного послал меня забрать кое-что, принадлежащее ему."

    "Квентин понимает о чём идёт речь."

    hide kventin

    show kventin at left, stretch_in

    kventin "Бери, конечно. Всё в отличном состоянии."

    mc "Спасибо. Теперь можно отправляться на охоту!"

    hide mc3 with dissolve
    hide kventin with dissolve

    $ CurrentGun = "Storm"

    "Вы ставите новое вооружение на свою машину и едете к Феликсу..."

    "У вас есть возможность продать оружие \"Шершень\". Продажа принесёт вам 260 монет."

    menu:
        "Продать":
            $ CurrentMoney += 260
            "Вы решили продать \"Шершень\" и получили 260 монет.\nВаш текущий баланс: [CurrentMoney]."

        "Не продавать":
            if try_add_item("Hornet"):
                $ inventory_text = ", ".join(Inventory)
                "Вы решили не продавать \"Шершень\".\nВаш текущий инвентарь: [inventory_text]."
            else:
                $ CurrentMoney += 260
                "В вашем инвентаре недостаточно места! \"Шершень\" автоматически продан.\nВаш текущий баланс: [CurrentMoney]."

    jump felixbase

label felixbase:

    scene bg_felixbase with fade

    play music "music/intensedialogue01.ogg" fadeout 1.0

    "Приехав на базу Феликса вы видите множество машин, но вас это нисколько не пугает."

    mc "Я отомщу за смерть отца!"

    show felix2 at center, stretch_in

    felix "Ба, знакомые все лица!"

    hide felix2

    show felix at center, stretch_in

    felix "Покажите этому наглецу!"

    hide felix

    play music "music/battle2.ogg"

    if TakeGunFromZaimka == "True":
        scene bg_felixbaseeasy
    elif TakeGunFromZaimka == "False":
        scene bg_felba_hornet

    "Начинается бойня с охраной Феликса."

    if TakeGunFromZaimka == "True":
        scene bg_felixbasestorm
        "Но поскольку вы обзавелись более мощным оружием для вас не составляет труда расправиться с ними."
    elif TakeGunFromZaimka == "False":
        "Поскольку вы не забрали оружие из Заимки - вы с трудом расправляетесь с ними и чувствуете как тяжело вашему грузовику."

    play music "music/passage03.ogg" fadeout 1.0

    mc "Это всё, что у тебя есть? Выходи сам на честный бой!"

    felix "А парень не промах..."

    if TakeGunFromZaimka == "True":
        felix "Где он взял такое вооружение?"

    felix "Ладно, хочешь сделать что-то хорошо - делай это сам. Посторонись!"

    $ renpy.save("checkpoint-5")
    $ renpy.notify("Игра сохранена.")

    "Вы снова начинаете бой с Феликсом."

    $ _window_hide()
    $ _game_menu_screen = None
    $ _menu = False
    $ config.keymap['save'] = []
    $ config.keymap['load'] = []
    $ config.keymap['game_menu'] = []
    $ persistent._in_battle = True

    jump felix_battle

label felix_battle:
    if TakeGunFromZaimka == "True":
        $ player_hp = CarHP.get(CurrentCar, CarHP["Van"])
        $ player_max_hp = player_hp
        $ max_heals = 10
        $ enemy_hp = player_hp * 2
    elif TakeGunFromZaimka == "False":
        $ player_hp = int(CarHP.get(CurrentCar, CarHP["Van"])) - 350
        $ player_max_hp = 850
        $ max_heals = 20
        $ enemy_hp = player_hp * 1.5
    $ damage_range = gun_stats.get(CurrentGun, gun_stats["Hornet"])
    $ max_heals = 15 
    $ turn_count = 0
    $ enemy_max_hp = enemy_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ enemy_name = "Феликс"
    $ enemy_image = "felixcar"
    $ bgname = "bg_felixbase"
    $ EnemyType = "Regular"


    scene bg_felixbase
    show felixcar at center

    while enemy_hp > 0 and player_hp > 0:
        call screen enemy_ui

    if player_hp <= 0:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False
        
        hide felixcar
        play sound "sfx/explosion04.wav"
        jump fightlost
    else:
        $ _game_menu_screen = "save_screen"
        $ _menu = True
        $ config.keymap['save'] = ['save']
        $ config.keymap['load'] = ['load']
        $ config.keymap['game_menu'] = ['game_menu']
        $ persistent._in_battle = False

        hide felixcar with dissolve

        play music "music/intensedialogue03.ogg" fadeout 1.0
        jump felixdefeated

label felixdefeated:

    scene bg_felixdlg with fade

    show mc3 at right with dissolve

    mc "Теперь ты умрёшь за свои злодеяния!"

    show felix at left, stretch_in

    felix "Постой, я никого не убивал уже много лет. У нас уговор с местными!"

    felix "Это ты ворвался в мой дом и начал калечить моих людей!"

    mc "Только у тебя хватило бы сил и наглости сжечь целую деревню!"

    felix "Так ты из Глухого!"

    felix "Поверь, это были не мы, а какие-то гастролёры из соседних областей!"

    pause 1.0

    "Вы неудовлетворены таким ответом..."

    hide mc3

    show mchar at right, stretch_in

    mc "ТЫ ЛЖЁШЬ!"

    hide felix

    show felix2 at left, stretch_in

    felix "Клянусь могилой своего отца!"

    felix "Да спроси хоть у своей подружки Лисы. Она всё видела."

    "Вы не понимаете причём тут вообще Лиса."

    hide mchar

    show mcsurp at right, stretch_in

    mc "Откуда ты знаешь?"

    hide felix2

    show felix at left, stretch_in

    felix "Так она же нам про это и рассказала!"

    felix "А потом умчалась на север. В сторону Пешта."

    "Вы удивлены от услышанного."

    mc "Лиса..."

    mc "Я чувствую, что она как-то со всем этим связана..."

    mc "Я найду её и узнаю, что произошло на самом деле."

    mc "Ладно, Феликс, я сохраню тебе жизнь."

    mc "Иди на все четыре стороны. Только не смей больше показываться в этих краях!"

    "Феликс лишь ухмыляется."

    felix "Ты победил. Но мы ещё встретимся, и тогда я буду лучше подготовлен."

    mc "До скорого!"

    hide felix with dissolve
    hide mcsurp with dissolve

    if random.randint(1,2) == 1:
        $ randommus = random.randint(1, 2)
        $ renpy.music.play(f"audio/music/alarm{randommus}.ogg", channel='music')
        "На вас нападают!"
        call randomfight from _call_randomfight_10

    jump leaver1m1tovaterland

label leaver1m1tovaterland:

    $ TownType = "City"

    scene bg_sowth with Fade

    "Перед тем, как ехать искать Лису вы решили заехать в Южный, чтобы рассказать Дронну, как всё прошло."

    show dronn at left with dissolve

    dronn "Ну, как дела?"

    show mchar at right with dissolve

    mc "Больше Феликс вас не побеспокоит. Я прогнал его."

    dronn "За это прими наше большое человеческое спасибо."
    $ CurrentMoney += 250
    $ renpy.notify("Вы получили 250 монет.")
    dronn "Вот, возьми: эти деньги я как раз собрал, чтобы заплатить очередные бандитские поборы."
    dronn "Я даю их тебе в знак благодарности. Ты также можешь оставить себе моё оружие. Желаю тебе удачи в долгом и опасном путешествии."

    mc "Прощай, добрый человек. Не знаю, вернусь ли я, но всегда буду помнить родные места."

    hide dronn
    hide mchar
    
    $ TownType = "NotInCity"

    jump vaterlandfirst

label leaver1m1toridzin:

    $ renpy.movie_cutscene("movies/leaver1m1/leaver1m1tom2_hornet.mp4")

    play music "music/driving2.ogg"

    $ TakeGunFromZaimka = "False"

    pause 1.5

    jump arrivetor1m2