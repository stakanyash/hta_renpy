define mc = Character("[player_name]", color="#FED11B")
define father = Character('Отец', color="#FED11B")
define lisa = Character('Лиса', color="#FED11B")
define sergo = Character('Серго', color="#FED11B")
define unknown = Character('???', color="#FED11B")
define dick = Character('Фермер Дик', color="#FED11B")
define felix = Character('Феликс', color="#FED11B")
define dronn = Character('Дронн', color="#FED11B")
define kventin = Character('Квентин', color="#FED11B")

init python:
    renpy.music.register_channel("sfx2", mixer="sfx", loop=True, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("shoot", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("damage", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")

transform stretch_in:
    yzoom 0.95
    linear 0.1 yzoom 1.0

transform fadeout_damage:
    alpha 1.0
    pause 0.5
    linear 1.5 alpha 0.0

transform blinking:
    alpha 1.0
    pause 0.3
    alpha 0.0
    pause 0.3
    repeat

image boss = "felixcar.png"

init python:
    import random
    import math
    from renpy.display.im import MatrixColor

    def apply_boss_attack():
        global player_hp, turn_count, player_max_hp
        if turn_count > 0 and turn_count % 5 == 0:
            damage = int(player_max_hp * 0.075)
            player_hp = max(0, player_hp - damage)

            renpy.sound.play(f"audio/sfx/landing_car_sparkle.wav", channel="damage")

            renpy.show("damage", at_list=[fadeout_damage])

    def attack_boss():
        global boss_hp, boss_max_hp, turn_count, attack_locked
        if attack_locked:
            return
        attack_locked = True

        if TakeGunFromZaimka == "True":
            damage_percent = random.uniform(0.005, 0.02)
        else:
            damage_percent = random.uniform(0.005, 0.0175)
        damage = int(boss_max_hp * damage_percent)

        shootsound = random.randint(1, 13)

        renpy.sound.play(f"audio/sfx/bullet{shootsound}.wav", channel="shoot")

        renpy.show("boss", at_list=[center, stretch_in], what=None)
        boss_hp = max(0, boss_hp - damage)
        turn_count += 1
        apply_boss_attack()
        renpy.restart_interaction()

    def heal():
        global player_hp, heal_count, max_heals, player_max_hp
        if heal_count < max_heals:
            heal_per = random.uniform(0.01, 0.08)
            heal_amount = int(player_max_hp * heal_per)
            player_hp = min(player_hp + heal_amount, player_max_hp)
            heal_count += 1

            renpy.sound.play(f"audio/sfx/life.wav", channel="sound")
        renpy.restart_interaction()

    def get_boss_bar_image():
        if boss_hp <= 0:
            return "gui/bossbar/boss_bar_0.png"
        percent = (boss_hp / boss_max_hp) * 100
        level = math.ceil(percent / 10.0) * 10
        level = max(10, min(100, level))
        return f"gui/bossbar/boss_bar_{level}.png"

    def hex_to_rgb(color_str):
        color_str = color_str.lstrip("#")
        return tuple(int(color_str[i:i+2], 16) / 255.0 for i in (0, 2, 4))

    def tint_image(path, hex_color):
        r, g, b = hex_to_rgb(hex_color)

        matrix = [
            r, 0, 0, 0, 0,
            0, g, 0, 0, 0,
            0, 0, b, 0, 0,
            0, 0, 0, 1, 0,
        ]

        return MatrixColor(path, matrix)

    def get_hp_digit_images(hp):
        s = str(hp).rjust(4, "E")
        percent = player_hp / float(player_max_hp)
        color = "#00FF00" if percent >= 0.15 else "#FF0000"

        return [tint_image(f"gui/digits/{c}.png", color) for c in s]

    def get_heal_digit_images(heal):
        s = str(heal).rjust(4, "E")
        color = "#00aeff"

        return [tint_image(f"gui/digits/{c}.png", color) for c in s]

    def get_remain_heals():
        return max_heals - heal_count

    def get_lowheal():
        percent = player_hp / float(player_max_hp)
        level = math.ceil(percent / 10.0) * 10
        level = max(10, min(100, level))
        if percent < 0.15:
            return f"gui/bossbar/redlight_hp.png"
        else:
            return f"gui/bossbar/redlight_blank.png"

    def get_lowhealamount():
        percent = get_remain_heals() / float(max_heals)
        level = math.ceil(percent / 10.0) * 10
        level = max(10, min(100, level))
        if percent < 0.30:
            return f"gui/bossbar/redlight_fuel.png"
        else:
            return f"gui/bossbar/redlight_blank.png"


label main_game:

    play music "music/bio07unloop.ogg" fadeout 1.0

    scene black with fade

    "{cps=20}История не сохранила точных сведений о тёмных временах, наступивших сразу после Катастрофы. Доподлинно известно лишь то, что люди выжили в отравленном воздухе благодаря защитным маскам."

    "{cps=20}Это творение неизвестного изобретателя уравняло всех. Тонкая преграда, вставшая на пути неминуемой смерти, стала символом нового человечества. Маски сплотили людей и придали им силы бороться за место под солнцем."

    "{cps=20}Возникли новые поселения вдали от прежних городов, ставших братскими могилами. Постепенно были налажены связи между разрозненными группами выживших."

    "{cps=20}Фермеры, шахтёры, торговцы – возвращение к простым занятиям пошло только на пользу растерянным людям."

    "{cps=20}Но человек остаётся человеком во все времена. Остались те, кто сохранял мудрость веков, чтобы делиться ею с миром. {cps=10}Были и те, кто предпочёл созиданию разрушение."

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

    menu:
        "Атаковать":
            $ renpy.save("autosave_firstattack")
            jump attack

        "Попытаться договориться":
            $ renpy.save("autosave_firsttrytalk")
            jump speak

label attack:

    "Вы атаковали враждебную машину и успешно с ней разделались."

    play music "music/driving1.ogg" fadeout 1.0

    mc "Вот чёрт, не успел в первый раз один поехать и уже ограбить захотели. Теперь я понимаю, почему отец так долго меня к этому не пускал."

    jump afterfirstattack

label speak:

    "Вы пытаетесь договориться с бандитом, но он не идёт на контакт. Вам пришлось открыть огонь и убить его."

    play music "music/driving1.ogg" fadeout 1.0

    mc "Эх, был он разговорчивым, может и смогли бы договориться..."

    mc "Хотя у меня всего 100 монет то в кармане, да и посылку я бы ему не отдал. О какой вообще договорённости может идти речь?"

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
            $ renpy.save("autosave_lisaagreed")
            $ LisaAgreed = "True"
            jump lisaagree

        "Отказать":
            $ renpy.save("autosave_lisareject")
            $ LisaAgreed = "False"
            jump lisarefuse

label lisaagree:

    mc "А почему бы и нет."

    play music "music/driving1.ogg" fadeout 1.0

    hide lisa with dissolve
    hide mc_2 with dissolve

    "Вы поехали по соседним деревням. Сначала решили заехать в Заимку."

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

    play music "music/battle1.ogg"

    "Вам ничего не остаётся, кроме как начать с ним перестрелку."

    play music "music/driving2.ogg" fadeout 1.0

    if LisaAgreed == "True":
        "После непродолжительного боя бандит был уничтожен, а вы дальше поехали к Заимке."
        jump tozaimka
    elif LisaAgreed == "False":
        "После непродолжительного боя бандит был уничтожен, а вы дальше поехали к заправке."
        jump dickzapravka

label tozaimka:

    scene bg_zaimka with fade

    "Вы приехали в Заимку. Остановившись вы услышали от Лисы..."

    show lisa2 at right with dissolve

    lisa "Подожди-ка здесь, пока я закончу свои дела."

    "Вы пытаетесь понять что-же она ищет, но не слышите о чём Лиса говорит с местными жителями."

    lisa "Готово. Поехали дальше."

    hide lisa2 with dissolve

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

    lisa "Ты выполнил свою часть сделки. Держи свои деньги."

    play music "audio/music/passage01unloop.ogg" fadeout 1.0

    hide lisa with dissolve

    "После этого Лиса спешно удаляется."

    play music "audio/music/quietdialogue01.ogg" fadeout 1.0

    mc "Что же она искала? Пора и мне домой возвращаться. Узнаю, из-за чего отец так волновался."

    mc "Но сначала мне надо заехать отдать посылку Серго. А то совсем из головы вылетело."

    hide mc_2 with dissolve

    "Вы направились в Южный."

    play music "music/town1.ogg" fadeout 1.0

    jump sergo

label sergo:

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
                jump felixmeet
            elif LisaAgreed == "False":
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
            $ renpy.save("autosave_felixmeet")
            "Вы бы с радостью отдали деньги, чтобы от вас отстали, но у вас нет 1000 монет."
            jump felixbeforefight

        "Отказать":
            $ renpy.save("autosave_felixmeet")
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
        "Атаковать охрану":
            "Вы начали атаковать охрану, однако не заметили как главарь заехал сзади и начал активно вас расстреливать."
            scene black with dissolve
            stop music fadeout 2.0
            "Из-за своей неопытности вы не смогли сориентироваться и были повержены..."
            mc "{cps=7}Я не смог... увернуться..."
            window hide
            pause 1.5
            
            jump titles

        "Атаковать главаря":
            $ RunFromFelix = "False"
            "Вы смело бросаетесь в атаку на главаря, игнорируя его охрану. Не смотря на то, что у бандитов больше опыта сражений силы слишком не равны и спустя некоторое время главарь сдаётся."
            jump felixafterfight

        "Попытаться уехать":
            scene bg_felixrun with dissolve
            $ RunFromFelix = "True"
            "Вы пытаетесь уехать под шквалом огня. На удивление бандиты не бросаются за вами в погоню и спустя несколько секунд огонь прекращается."
            "Однако по рации вы слышите следующее..."

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

    jump sowthagain


label dyingfather:

    scene bg_dyingfather with dissolve

    play music "audio/music/sadness1.ogg"

    father "{cps=15}...сынок...!"

    mc "О боже, отец! Что здесь произошло? Кто это сотворил?"

    father "{cps=15}Слушай внимательно. Ты мой приёмный сын. Возьми, это вещи твоего настоящего отца..."

    father "{cps=15}Найди Бена Дросселя. Он исследователь. {cps=10}Он поможет... Сын... не дай ненависти... {cps=7}отравить твою... {cps=5}душу..."

    scene black with fade

    stop music fadeout 2.0

    pause 2.0

    play music "audio/music/death01.ogg"

    scene bg_afterfdeath with fade

    mc "Моя жизнь..."

    mc "Что же мне делать дальше?"

    mc "У меня ведь никого не осталось... {cps=10}и ничего..."

    mc "Только это письмо..."

    pause 1.0

    "{cps=15}Сын, если ты читаешь это письмо - значит я не смог вернуться и вырастить тебя сам. Я знаю, что Пётр отлично справился с этой задачей."

    "{cps=15}Я вижу тебя, такого молодого и полного сил, и сердце моё обливается слезами..."

    "{cps=15}Я виню себя за то, что меня не было рядом, когда ты рос. И это моё страшное наказание. Но знай, что я не мог поступить иначе. Передо мной стоит задача всей жизни..."

    "{cps=15}Только выполнив задуманное, смогу я успокоиться и вновь почувствовать себя человеком. Если нет... значит, я недостоин жить. Это письмо - извинение."

    "{cps=15}Прости меня, если сможешь. Ты всегда в моём сердце, сын..."

    mc "Это всё? Никаких объяснений..."

    mc "Как я могу простить того, кого никогда не знал?"

    mc "Мне больше нечего здесь делать. Я отправлюсь на поиски Бена."

    mc "Кто бы это ни был, надеюсь, он поможет мне обрести себя."

    mc "Может быть, в Южном слышали о нём?"

    jump sowthagain

label sowthagain:

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
                $ renpy.save("autosave_gotokventin")
                play music "music/town2.ogg" fadeout 1.0
                jump KventinZaimka

            "Ехать сразу к Феликсу":
                $ TakeGunFromZaimka = "False"
                $ renpy.save("autosave_gotofelix")
                jump felixbase
    elif LisaAgreed == "False":

        "Вы приехали в Южный и встретили местного бармена. Бармен начинает диалог сам."

        show dronn at left with dissolve

        dronn "Ты из Глухого?"

#        show mc3 at right with dissolve

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

        # Temporary "return" (replace with jump to Ridzin)
        return

label KventinZaimka:

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

    "Вы ставите новое вооружение на свою машину и едете к Феликсу..."

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

    $ renpy.save("autosave_felixbasebattle")

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
        $ player_hp = 850
        $ player_max_hp = player_hp
        $ max_heals = 10
        $ boss_hp = player_hp * 2
    elif TakeGunFromZaimka == "False":
        $ player_hp = 500
        $ player_max_hp = 850
        $ max_heals = 20
        $ boss_hp = player_hp * 1.5
    $ turn_count = 0
    $ boss_max_hp = boss_hp
    $ heal_count = 0
    $ remainheals = max_heals - heal_count
    $ attack_locked = False
    $ boss_name = "Феликс"

    scene bg_felixbase
    show boss

    while boss_hp > 0 and player_hp > 0:
        call screen boss_ui

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

        hide boss with dissolve

        play music "music/intensedialogue03.ogg" fadeout 1.0
        jump felixdefeated

label fightlost:
    scene black with fade
    stop music fadeout 1.0
    mc "{cps=7}Я не смог... увернуться..."
    return

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

    # Add jump to Vaterland
    return