################################################################################
## Инициализация
################################################################################

init python:
    # Difficulty
    def set_difficulty(mode, multiplier):
        store.difficulty = mode
        store.difficulty_base_multiplier = multiplier

        persistent.difficulty = mode
        persistent.difficulty_multiplier = multiplier

    def load_difficulty():
        if hasattr(persistent, "difficulty"):
            store.difficulty = persistent.difficulty
            store.difficulty_base_multiplier = persistent.difficulty_multiplier
        else:
            set_difficulty("normal", 0.03)

    # Support all screen sizes by stretching the view

    def stretch_view_size(w, h):
        return (w, h)

    config.adjust_view_size = stretch_view_size

################################################################################
## Стили
################################################################################

# Fade when "New Game" pressed

define startfade = Fade(1.0, 0.0, 1.0)

style default:
    properties gui.text_properties()
    language gui.language

style input:
    properties gui.text_properties("input", accent=True)
    adjust_spacing False

style hyperlink_text:
    properties gui.text_properties("hyperlink", accent=True)
    hover_underline True

style gui_text:
    properties gui.text_properties("interface")


style button:
    properties gui.button_properties("button")

style button_text is gui_text:
    properties gui.text_properties("button")
    yalign 0.5


style label_text is gui_text:
    properties gui.text_properties("label", accent=True)

style prompt_text is gui_text:
    properties gui.text_properties("prompt")


style bar:
    ysize gui.bar_size
    left_bar Frame("gui/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    xsize gui.bar_size
    top_bar Frame("gui/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    ysize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    xsize gui.scrollbar_size
    base_bar Frame("gui/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    ysize gui.slider_size
    base_bar Frame("gui/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/slider/horizontal_[prefix_]thumb.png"

style vslider:
    xsize gui.slider_size
    base_bar Frame("gui/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/slider/vertical_[prefix_]thumb.png"


style frame:
    padding gui.frame_borders.padding
    background Frame("gui/frame.png", gui.frame_borders, tile=gui.frame_tile)

################################################################################
## Внутриигровые экраны
################################################################################

## Screen for fight

style centered_text is text:
    xpos 0.83
    yalign 0.883
    textalign 0.5
    color "#ffffff"
    padding (10, 10)

style atk_button_text:
    idle_color "#b1b1b1"
    insensitive_color "#505050"

transform fadeinout:
    alpha 0.0
    linear 1.5 alpha 1.0
    on hide:
        linear 1.5 alpha 0.0

style button_text_center is default:
    xalign 0.5
    yalign 0.5
    text_align 0.5
    color "#999999"
    hover_color "#FFF"

screen enemy_ui():

    # Панель действий игрока
    frame:
        align (0.05, 0.98)
        padding (20, 40)
        xsize 450
        background "gui/bossbar/frame.png"

        vbox:
            spacing 10
            xalign 0.5
            text _("Выберите действие:") xalign 0.5

            # Кнопка "Атаковать"
            if not attack_locked:
                textbutton _("Атаковать") style "atk_button" action Function(attack_enemy) xalign 0.5
            else:
                textbutton _("Атаковать") style "atk_button" xalign 0.5 sensitive False

            # Кнопка "Лечиться"
            if heal_count < max_heals:
                textbutton _("Лечиться") style "atk_button" action Function(heal) xalign 0.5 sensitive player_hp < player_max_hp
            else:
                textbutton _("Лечиться") style "atk_button" xalign 0.5 sensitive False

    # Кнопка для разработчика
    if config.developer:
        textbutton _("Убить") action SetVariable("enemy_hp", 0) xalign 0.5 yalign 0.9 background "#0000005b"

    # Фон и иконка врага
    if EnemyType == "Boss":
        add "gui/bossbar/background.png" yalign 1.0 xalign 0.95
        add "gui/bossbar/icons/" + BossIcon xalign 0.957 yalign 0.865
    else:
        add "gui/bossbar/background_noboss.png" yalign 1.0 xalign 0.95

    # Имя врага
    text "[enemy_name]":
        style "centered_text"

    # Полоса здоровья врага
    fixed:
        xalign 1.0215
        yalign 0.9385
        xmaximum 600
        ysize 40

        add get_enemy_bar_image()

    # Панель здоровья игрока
    fixed:
        xalign 0.98
        yalign 0.1
        add "gui/digits/HP.png"

        # Цифры HP игрока
        hbox:
            xalign 0.0134
            yalign 0.0136
            for digit_img in get_hp_digit_images(player_hp):
                add digit_img

        # Красная подсветка HP
        hbox:
            xalign 0.037
            yalign 0.03
            if player_hp <= 0:
                add get_lowheal()
            elif "redlight_hp.png" in get_lowheal():
                add get_lowheal() at blinking
            else:
                add get_lowheal()

        # Красная подсветка оставшихся лечений
        hbox:
            xalign 0.965
            yalign 0.03
            if get_remain_heals() <= 0:
                add get_lowhealamount()
            elif "redlight_fuel.png" in get_lowhealamount():
                add get_lowhealamount() at blinking
            else:
                add get_lowhealamount()

        # Цифры оставшихся лечений
        hbox:
            xalign 0.9861
            yalign 0.015
            for healing in get_heal_digit_images(get_remain_heals()):
                add healing

    # Таймер разблокировки атаки
    if attack_locked:
        python:
            reload_times = {
                "Shotgun": 1.3,
                "Plasma": 2.5,
                "Energy": 0.75,
                "Artillery": 0.75,
                "Rocket": 1.1,
                "Explosive": 1.0
            }
            reload_time = reload_times.get(player_config.gun_type, 0.5)
    
        timer reload_time action SetVariable("attack_locked", False)

    # Завершение боя
    if enemy_hp <= 0 or player_hp <= 0:
        timer 0.1 action Return()

# Tutorial asking

screen tutorial_prompt_call():

    modal True
    zorder 100

    add "#0006"

    frame:
        xalign 0.5
        yalign 0.5
        padding (40, 40)

        xsize 900
        ysize 380

        vbox:
            spacing 20
            xalign 0.5
            yalign 0.5
            text "Кажется, вы в первый раз играете в\nEx Machina RenPy.\n\nХотите пройти обучение?" size 36 textalign 0.5

            hbox:
                spacing 200
                xalign 0.5
                ypos 30
                textbutton "Да" activate_sound "audio/sfx/click.wav" action Return(True)
                textbutton "Нет" activate_sound "audio/sfx/click.wav" action Return(False)




## Экран разговора #############################################################
##
## Экран разговора используется для показа диалога игроку. Он использует два
## параметра — who и what — что, соответственно, имя говорящего персонажа и
## показываемый текст. (Параметр who может быть None, если имя не задано.)
##
## Этот экран должен создать текст с id "what", чтобы Ren'Py могла показать
## текст. Здесь также можно создать наложения с id "who" и id "window", чтобы
## применить к ним настройки стиля.
##
## https://www.renpy.org/doc/html/screen_special.html#say

screen say(who, what):

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "namebox"
                text who id "who"

        text what id "what"


    ## Если есть боковое изображение ("голова"), показывает её поверх текста.
    ## По стандарту не показывается на варианте для мобильных устройств — мало
    ## места.
    if not renpy.variant("small"):
        add SideImage() xalign 0.0 yalign 1.0


## Делает namebox доступным для стилизации через объект Character.
init python:
    config.character_id_prefixes.append('namebox')

style window is default
style say_label is default
style say_dialogue is default
style say_thought is say_dialogue

style namebox is default
style namebox_label is say_label


style window:
    xalign 0.7
    xfill True
    yalign gui.textbox_yalign
    ysize gui.textbox_height

    background Image("gui/textbox.png", xalign=0.7, yalign=1.0)

style namebox:
    xpos gui.name_xpos
    xanchor gui.name_xalign
    xsize gui.namebox_width
    ypos gui.name_ypos
    ysize gui.namebox_height

    background Frame("gui/namebox.png", gui.namebox_borders, tile=gui.namebox_tile, xalign=gui.name_xalign)
    padding gui.namebox_borders.padding

style say_label:
    properties gui.text_properties("name", accent=True)
    xalign gui.name_xalign
    yalign 0.5

style say_dialogue:
    properties gui.text_properties("dialogue")

    xpos gui.dialogue_xpos
    xsize gui.dialogue_width
    ypos gui.dialogue_ypos
    line_spacing 10

    adjust_spacing False

## Экран ввода #################################################################
##
## Этот экран используется, чтобы показывать renpy.input. Это параметр запроса,
## используемый для того, чтобы дать игроку ввести в него текст.
##
## Этот экран должен создать наложение ввода с id "input", чтобы принять
## различные вводимые параметры.
##
## https://www.renpy.org/doc/html/screen_special.html#input

screen input(prompt):
    style_prefix "input"

    window:

        vbox:
            xanchor gui.dialogue_text_xalign
            xpos gui.dialogue_xpos
            xsize gui.dialogue_width
            ypos gui.dialogue_ypos

            text prompt style "input_prompt"
            input id "input"

style input_prompt is default

style input_prompt:
    xalign gui.dialogue_text_xalign
    properties gui.text_properties("input_prompt")

style input:
    xalign gui.dialogue_text_xalign
    xmaximum gui.dialogue_width


## Экран выбора ################################################################
##
## Этот экран используется, чтобы показывать внутриигровые выборы,
## представленные оператором menu. Один параметр, вложения, список объектов,
## каждый с заголовком и полями действия.
##
## https://www.renpy.org/doc/html/screen_special.html#choice

screen choice(items):
    vbox:
        align (0.5, 0.5)
        spacing 15

        for i in items:
            textbutton i.caption action i.action:
                xsize gui.choice_button_width
                ysize gui.choice_button_height
                style "choice_button"



style choice_vbox is vbox
style choice_button is button
style choice_button_text is button_text

style choice_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style choice_button is default:
    properties gui.button_properties("choice_button")

style choice_button_text is default:
    properties gui.text_properties("choice_button")


## Экран быстрого меню #########################################################
##
## Быстрое меню показывается внутри игры, чтобы обеспечить лёгкий доступ к
## внеигровым меню.

screen quick_menu():

    ## Гарантирует, что оно появляется поверх других экранов.
    zorder 100

    if not persistent._in_battle:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.98

            textbutton _("Главное меню") activate_sound "audio/sfx/click.wav" action ShowMenu('save')
            textbutton _("Авто") activate_sound "audio/sfx/click.wav" action Preference("auto-forward", "toggle")
            textbutton _("Быстрое сохранение") activate_sound "audio/sfx/click.wav" action QuickSave()
            textbutton _("Быстрая загрузка") activate_sound "audio/sfx/click.wav" action QuickLoad()
            textbutton _("Статистика") activate_sound "audio/sfx/click.wav" action ShowMenu("statistics_screen")

            if player_config.town_type == "City" or player_config.town_type == "Village":
                textbutton _("Меню города") activate_sound "audio/sfx/click.wav" action ShowMenu("InGameMenu")



## Данный код гарантирует, что экран быстрого меню будет показан в игре в любое
## время, если только игрок не скроет интерфейс.
init python:
    config.overlay_screens.append("quick_menu")

default quick_menu = True

style quick_button is default
style quick_button_text is button_text

style quick_button:
    properties gui.button_properties("quick_button")

style quick_button_text:
    properties gui.text_properties("quick_button")


################################################################################
## Экраны Главного и Игрового меню
################################################################################

## Экран навигации #############################################################
##
## Этот экран включает в себя главное и игровое меню, и обеспечивает навигацию к
## другим меню и к началу игры.

screen navigation_main_menu():

    vbox:
        style_prefix "navigationmm"
        xpos 50
        yalign 0.5
        spacing 9

        textbutton _("Новая игра") activate_sound "audio/sfx/click.wav" action Show("name_input_screen")

        textbutton _("Загрузить") activate_sound "audio/sfx/click.wav" action ShowMenu("load")

        textbutton _("Настройки") activate_sound "audio/sfx/click.wav" action ShowMenu("preferences")

        textbutton _("Об игре") activate_sound "audio/sfx/click.wav" action ShowMenu("about")

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("Помощь") activate_sound "audio/sfx/click.wav" action ShowMenu("help")

        if renpy.variant("pc"):
            textbutton _("Выход") activate_sound "audio/sfx/click.wav" action Quit(confirm=True)

screen navigation_in_game():

    vbox:
        style_prefix "navigation"
        xalign 0.5
        yalign 0.52
        spacing 10

        textbutton _("История") activate_sound "audio/sfx/click.wav" action ShowMenu("history") style "navigation_button"

        textbutton _("Сохранить") activate_sound "audio/sfx/click.wav" action ShowMenu("save_hta") style "navigation_button"

        textbutton _("Загрузить") activate_sound "audio/sfx/click.wav" action ShowMenu("load") style "navigation_button"

        textbutton _("Настройки") activate_sound "audio/sfx/click.wav" action ShowMenu("preferences") style "navigation_button"

        textbutton _("Об игре") activate_sound "audio/sfx/click.wav" action ShowMenu("about") style "navigation_button"

        if renpy.variant("pc") or (renpy.variant("web") and not renpy.variant("mobile")):
            textbutton _("Помощь") activate_sound "audio/sfx/click.wav" action ShowMenu("help") style "navigation_button"

        if _in_replay:
            textbutton _("Завершить повтор") activate_sound "audio/sfx/click.wav" action EndReplay(confirm=True) style "navigation_button"

        textbutton _("Главное меню") activate_sound "audio/sfx/click.wav" action MainMenu() style "navigation_button"

        if renpy.variant("pc"):
            textbutton _("Выход") activate_sound "audio/sfx/click.wav" action Quit(confirm=True) style "navigation_button"

        textbutton _("Вернуться"):
            style "navigation_button"
            activate_sound "audio/sfx/click.wav"
            yoffset 20

            action Return()


style navigation_button is gui_button
style navigation_button_text is gui_button_text

style navigation_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigation_button_text:
    xalign 0.5
    text_align 0.5
    color "#404040"
    hover_color "#202020"

style navigationmm_button is gui_button
style navigationmm_button_text is gui_button_text

style navigationmm_button:
    size_group "navigation"
    properties gui.button_properties("navigation_button")

style navigationmm_button_text:
    color "#fed11b"
    hover_color "#f9fd00"


## Экран главного меню #########################################################
##
## Используется, чтобы показать главное меню после запуска игры.
##
## https://www.renpy.org/doc/html/screen_special.html#main-menu

screen main_menu():

    ## Этот тег гарантирует, что любой другой экран с тем же тегом будет
    ## заменять этот.
    tag menu

    add "mainmenu_loop"

    add "gui/overlay/main_menu.png" xpos 0 ypos 0

    ## Оператор use включает отображение другого экрана в данном. Актуальное
    ## содержание главного меню находится на экране навигации.
    
    use navigation_main_menu

    if gui.show_name:

        vbox:
            style "main_menu_vbox"

            text "[config.name!t]":
                style "main_menu_title"

            text "[config.version]":
                style "main_menu_version"

    if config.developer:
        text "Ex Machina Ren'Py - developer version [config.version!t] ([hta_build!t])" xpos 460 ypos 0.02 yanchor 0.0 style "main_menu_text" color "#fff" xmaximum 800 size 17
    else:
        text "Ex Machina Ren'Py - demo version [config.version!t] ([hta_build!t])" xpos 430 ypos 0.02 yanchor 0.0 style "main_menu_text" color "#fff" xmaximum 800 size 17

style main_menu_frame is empty
style main_menu_vbox is vbox
style main_menu_text is gui_text
style main_menu_title is main_menu_text
style main_menu_version is main_menu_text

style main_menu_frame:
    xsize 420
    yfill True

    background "gui/overlay/main_menu.png"

style main_menu_vbox:
    xalign 1.0
    xoffset -30
    xmaximum 1200
    yalign 1.0
    yoffset -30

style main_menu_text:
    properties gui.text_properties("main_menu", accent=True)

style main_menu_title:
    properties gui.text_properties("title")

style main_menu_version:
    properties gui.text_properties("version")


## Game stats screen

screen statistics_screen():
    tag menu

    python:
        def format_time(seconds):
            minutes = seconds // 60
            hours = minutes // 60
            minutes = minutes % 60
            return "%02d:%02d" % (hours, minutes)

    frame:
        style "menu_frame"
        background "gui/townmenu/backstats.png"
        xsize 1920
        ysize 1080

        if 0 <= player_config.money <= 9:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[player_config.money] монет" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"
        elif 10 <= player_config.money <= 99:
            text "Деньги:" size 19 xpos 65 ypos 20 textalign 0.5 color "#404040"
            text "[player_config.money] монет" size 19 xpos 135 ypos 20 textalign 0.5 color "#404040"
        elif 100 <= player_config.money <= 999:
            text "Деньги:" size 19 xpos 60 ypos 20 textalign 0.5 color "#404040"
            text "[player_config.money] монет" size 19 xpos 130 ypos 20 textalign 0.5 color "#404040"
        elif 1000 <= player_config.money <= 9999:
            text "Деньги:" size 19 xpos 55 ypos 20 textalign 0.5 color "#404040"
            text "[player_config.money] монет" size 19 xpos 125 ypos 20 textalign 0.5 color "#404040"
        elif 10000 <= player_config.money <= 99999:
            text "Деньги:" size 19 xpos 50 ypos 20 textalign 0.5 color "#404040"
            text "[player_config.money] монет" size 19 xpos 120 ypos 20 textalign 0.5 color "#404040"
        elif 100000 <= player_config.money <= 999999:
            text "Деньги:" size 19 xpos 45 ypos 20 textalign 0.5 color "#404040"
            text "[player_config.money] монет" size 19 xpos 115 ypos 20 textalign 0.5 color "#404040"
        elif player_config.money >= 1000000:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[format_money(player_config.money)]" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/close_e.png" 
            hover "gui/townmenu/close_h.png"
            action Return()
            xalign 0.99
            yalign 0.0
            focus_mask True 

        text "Молодой человек, только вступивший во взрослую жизнь, которая\nготовит ему массу неприятных сюрпризов." size 22 xalign 0.145 yalign 0.715 color "#404040"

        vbox:
            spacing 20
            xalign 0.645
            yalign 0.455
            text "Имя" size 24 color "#2a2a2a"
            text "Оружие" size 24 color "#2a2a2a"
            text "Тип оружия" size 24 color "#2a2a2a"
            text "Второе оружие" size 24 color "#2a2a2a"
            text "Машина" size 24 color "#2a2a2a"
            text "Сложность" size 24 color "#2a2a2a"
            text "Регион" size 24 color "#2a2a2a"
            text "Текущее время игры (ч : мин)" size 24 color "#2a2a2a"
            text "Текущее HP" size 24 color "#2a2a2a"
            text "Остаток лечений" size 24 color "#2a2a2a"

        vbox:
            spacing 20
            xalign 0.85
            yalign 0.455
            text "[player_name]" size 24 color "#2a2a2a"
            text "[gun_names.get(player_config.current_gun, '—')]" size 24 color "#2a2a2a"
            text "[GunTypeName.get(player_config.gun_type, '—')]" size 24 color "#2a2a2a"
            text "[gun_names.get(player_config.second_gun, '—')]" size 24 color "#2a2a2a"
            text "[car_names.get(player_config.car, '—')]" size 24 color "#2a2a2a"
            text "[DifficultyNames.get(difficulty, '—')]" size 24 color "#2a2a2a"
            text "[region_names.get(player_config.current_region, '—')]" size 24 color "#2a2a2a"
            text "[format_time(renpy.get_game_runtime())]" size 24 color "#2a2a2a"
            text "[player_config.hp]" size 24 color "#2a2a2a"
            text "[player_config.heals]" size 24 color "#2a2a2a"

        imagebutton:
            idle "gui/townmenu/buttons/tab_stats_s.png" 
            hover "gui/townmenu/buttons/tab_stats_s.png"
            action NullAction()
            xpos 350
            focus_mask True 

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/buttons/tab_invent_e.png" 
            hover "gui/townmenu/buttons/tab_invent_s.png"
            action [Hide("statistics_screen"), Show("Selling_Menu")]
            xpos 1630
            focus_mask True 

        if player_config.town_type == "City":
            imagebutton activate_sound "audio/sfx/click.wav":
                idle "gui/townmenu/buttons/tab_weapon_e.png" 
                hover "gui/townmenu/buttons/tab_weapon_s.png"
                action [Hide("statistics_screen"), Show("Gun_Shop_Menu")]
                xpos 1450
                ypos 1
                focus_mask True 

        if player_config.town_type in ["City", "Village"]:
            imagebutton activate_sound "audio/sfx/click.wav":
                idle "gui/townmenu/buttons/tab_truck_e.png" 
                hover "gui/townmenu/buttons/tab_truck_s.png"
                action [Hide("statistics_screen"), Show("Car_Shop")]
                xpos 1270
                ypos 1
                focus_mask True 


## Экран игрового меню #########################################################
##
## Всё это показывает основную, обобщённую структуру экрана игрового меню. Он
## вызывается с экраном заголовка и показывает фон, заголовок и навигацию.
##
## Параметр scroll может быть None или один из "viewport" или "vpgrid". Этот
## экран предназначен для использования с одним или несколькими дочерними
## элементами, которые трансклюдируются (помещаются) внутрь него.

screen game_menu(title, scroll=None, yinitial=0.0, spacing=0):

    style_prefix "game_menu"

    if main_menu:
        add gui.main_menu_background
    else:
        add Solid("#5a5a5a4f")
        add "scrach_anim_24fps"
        add "gui/ingame_mm.png" 

    frame:
        style "game_menu_outer_frame"

        hbox:

            ## Резервирует пространство для навигации.
            frame:
                style "game_menu_navigation_frame"

            frame:
                style "game_menu_content_frame"

                if scroll == "viewport":

                    viewport:
                        yinitial yinitial
                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        vbox:
                            spacing spacing

                            transclude

                elif scroll == "vpgrid":

                    vpgrid:
                        cols 1
                        yinitial yinitial

                        scrollbars "vertical"
                        mousewheel True
                        draggable True
                        pagekeys True

                        side_yfill True

                        spacing spacing

                        transclude

                else:

                    transclude

    use navigation_in_game

    label title

    if main_menu:
        key "game_menu" action ShowMenu("main_menu")


style game_menu_outer_frame is empty
style game_menu_navigation_frame is empty
style game_menu_content_frame is empty
style game_menu_viewport is gui_viewport
style game_menu_side is gui_side
style game_menu_scrollbar is gui_vscrollbar

style game_menu_label is gui_label
style game_menu_label_text is gui_label_text

style return_button is navigation_button
style return_button_text is navigation_button_text

style game_menu_outer_frame:
    bottom_padding 45
    top_padding 180

style game_menu_navigation_frame:
    xsize 420
    yfill True

style game_menu_content_frame:
    left_margin 60
    right_margin 30
    top_margin 15

style game_menu_viewport:
    xsize 1380

style game_menu_vscrollbar:
    unscrollable gui.unscrollable

style game_menu_side:
    spacing 15

style game_menu_label:
    xpos 75
    ysize 180

style game_menu_label_text:
    size gui.title_text_size
    color "#fed11b"
    yalign 0.4
    font "fonts/ARIALBD.ttf"

style return_button:
    yalign 0.8


## Экран Об игре ###############################################################
##
## Этот экран показывает авторскую информацию об игре и Ren'Py.
##
## В этом экране нет ничего особенного, и он служит только примером того, каким
## можно сделать свой экран.

screen about():
    modal True
    zorder 200

    # Затемнение фона
    button:
        style "empty"
        xfill True
        yfill True
        action NullAction()
        background "#000000cc"

    # Статическое изображение меню поверх видео (если нужно)
    add "gui/settings_menu.png"

    # Основное окно с контентом
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        padding (50, 50)
        background None

        vbox:
            spacing 20

            # Заголовок
            hbox:
                xfill True
                text "Об игре" size 60 color "#fed11b" font "fonts/ARIALBD.ttf" ypos 20 xpos 5

                # Кнопка закрытия
                imagebutton:
                    idle "gui/townmenu/close_e.png"
                    hover "gui/townmenu/close_h.png"
                    action Hide("about")
                    xalign 1.0
                    yalign 0.0
                    activate_sound "audio/sfx/click.wav"

            null height 1

            # Основной контент
            viewport:
                scrollbars "vertical"
                mousewheel True
                ypos 100
                xsize 1350
                ysize 585

                vbox:
                    spacing 20

                    label "[config.name!t]"
                    text _("Версия [config.version!t] [[[hta_build!t]]\n")

                    text _("Данный продукт является фанатской адаптацией игры\nEx Machina/Hard Truck Apocalypse на движок для визуальных новелл RenPy.\n")
                    text _("Посвящен 20-летию оригинальной Ex Machina/Hard Truck Apocalypse.\n")
                    text _("Данная версия является демонстрационной, её разработка не завершена!\n")
                    text _("GitHub репозиторий проекта доступен {a=https://github.com/stakanyash/hta_renpy}здесь{/a}.")
                    text _("{a=https://github.com/stakanyash/hta_renpy/blob/main/DISCLAIMER.md}Дисклеймер{/a}\n")
                    text _("Сделано с помощью {a=https://www.renpy.org/}Ren'Py{/a} [renpy.version_only].")


style about_label is gui_label
style about_label_text is gui_label_text
style about_text is gui_text

style about_label_text:
    size gui.label_text_size


## Экраны загрузки и сохранения ################################################
##
## Эти экраны ответственны за возможность сохранять и загружать игру. Так
## как они почти одинаковые, оба реализованы по правилам третьего экрана —
## file_slots.
##
## https://www.renpy.org/doc/html/screen_special.html#save

screen save():

    tag menu

    use game_menu("")

screen save_hta(title="Сохранить", is_load=False):
    modal True
    zorder 200

    # Затемнение фона
    button:
        style "empty"
        xfill True
        yfill True
        action NullAction()
        background "#000000cc"

    # Статическое изображение меню поверх видео (если нужно)
    add "gui/settings_menu.png"

    default page_name_value = FilePageNameInputValue(
        pattern=_("{} страница"), 
        auto=_("Автосохранения"), 
        quick=_("Быстрые сохранения"), 
        checkpoint=_("Чекпоинты")
    )

    $ current_page = FileCurrentPage()

    # Основное окно с контентом
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        padding (50, 50)
        background None

        vbox:
            spacing 20

            # Заголовок
            hbox:
                xfill True
                text title size 50 color "#fed11b" font "fonts/ARIALBD.ttf" ypos 10 xpos 5

                # Кнопка закрытия
                imagebutton:
                    idle "gui/townmenu/close_e.png"
                    hover "gui/townmenu/close_h.png"
                    action Hide("save_hta")
                    xalign 1.0
                    yalign 0.0
                    activate_sound "audio/sfx/click.wav"

            null height 1

            # Контент слотов
            fixed:

                # Номер страницы
                button:
                    style "page_label"
                    key_events True
                    xalign 0.5
                    ypos -70
                    action page_name_value.Toggle()

                    input:
                        style "page_label_text"
                        value page_name_value

                # Сетка слотов
                grid gui.file_slot_cols gui.file_slot_rows:
                    style_prefix "slot"
                    xalign 0.5
                    ypos 100
                    spacing gui.slot_spacing

                    for i in range(gui.file_slot_cols * gui.file_slot_rows):
                        $ slot = i + 1
                        button:
                            if current_page == "checkpoint" and not is_load:
                                action NullAction()
                                sensitive False
                            else:
                                action FileAction(slot)

                            has vbox
                            add FileScreenshot(slot) xalign 0.5
                            text FileTime(slot, format=_("{#file_time}%A, %d %B %Y, %H:%M"), empty=_("Пустой слот")):
                                style "slot_time_text"
                            text FileSaveName(slot):
                                style "slot_name_text"
                            key "save_delete" action FileDelete(slot)

                # Кнопки страниц
                vbox:
                    style_prefix "page"
                    xalign 0.51
                    yalign 0.01

                    $ current_page = FileCurrentPage()

                    hbox:
                        xalign 0.5
                        spacing gui.page_spacing

                        if current_page not in ("auto", "quick", "checkpoint"):
                            textbutton _("<") activate_sound "audio/sfx/click.wav" action FilePagePrevious()
                            key "save_page_prev" activate_sound "audio/sfx/click.wav" action FilePagePrevious()

                        if config.has_autosave:
                            textbutton _("{#auto_page}А") activate_sound "audio/sfx/click.wav" action FilePage("auto")

                        if config.has_quicksave:
                            textbutton _("{#quick_page}Б") activate_sound "audio/sfx/click.wav" action FilePage("quick")

                        textbutton "Ч" activate_sound "audio/sfx/click.wav" action FilePage("checkpoint")

                        for page in range(1, 10):
                            textbutton "[page]" activate_sound "audio/sfx/click.wav" action FilePage(page)

                        if current_page not in ("auto", "quick", "checkpoint"):
                            textbutton _(">") activate_sound "audio/sfx/click.wav" action FilePageNext()
                            key "save_page_next" activate_sound "audio/sfx/click.wav" action FilePageNext()

screen load(title="Загрузить", is_load=True):
    modal True
    zorder 200

    # Затемнение фона
    button:
        style "empty"
        xfill True
        yfill True
        action NullAction()
        background "#000000cc"

    # Статическое изображение меню поверх видео (если нужно)
    add "gui/settings_menu.png"

    default page_name_value = FilePageNameInputValue(
        pattern=_("{} страница"), 
        auto=_("Автосохранения"), 
        quick=_("Быстрые сохранения"), 
        checkpoint=_("Чекпоинты")
    )

    $ current_page = FileCurrentPage()

    # Основное окно с контентом
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        padding (50, 50)
        background None

        vbox:
            spacing 20

            # Заголовок
            hbox:
                xfill True
                text title size 50 color "#fed11b" font "fonts/ARIALBD.ttf" ypos 10 xpos 5

                # Кнопка закрытия
                imagebutton:
                    idle "gui/townmenu/close_e.png"
                    hover "gui/townmenu/close_h.png"
                    action Hide("load")
                    xalign 1.0
                    yalign 0.0
                    activate_sound "audio/sfx/click.wav"

            null height 1

            # Контент слотов
            fixed:

                # Номер страницы
                button:
                    style "page_label"
                    key_events True
                    xalign 0.5
                    ypos -70
                    action page_name_value.Toggle()

                    input:
                        style "page_label_text"
                        value page_name_value

                # Сетка слотов
                grid gui.file_slot_cols gui.file_slot_rows:
                    style_prefix "slot"
                    xalign 0.5
                    ypos 100
                    spacing gui.slot_spacing

                    for i in range(gui.file_slot_cols * gui.file_slot_rows):
                        $ slot = i + 1
                        button:
                            if current_page == "checkpoint" and not is_load:
                                action NullAction()
                                sensitive False
                            else:
                                action FileAction(slot)

                            has vbox
                            add FileScreenshot(slot) xalign 0.5
                            text FileTime(slot, format=_("{#file_time}%A, %d %B %Y, %H:%M"), empty=_("Пустой слот")):
                                style "slot_time_text"
                            text FileSaveName(slot):
                                style "slot_name_text"
                            key "save_delete" action FileDelete(slot)

                # Кнопки страниц
                vbox:
                    style_prefix "page"
                    xalign 0.51
                    yalign 0.01

                    $ current_page = FileCurrentPage()

                    hbox:
                        xalign 0.5
                        spacing gui.page_spacing

                        if current_page not in ("auto", "quick", "checkpoint"):
                            textbutton _("<") activate_sound "audio/sfx/click.wav" action FilePagePrevious()
                            key "save_page_prev" activate_sound "audio/sfx/click.wav" action FilePagePrevious()

                        if config.has_autosave:
                            textbutton _("{#auto_page}А") activate_sound "audio/sfx/click.wav" action FilePage("auto")

                        if config.has_quicksave:
                            textbutton _("{#quick_page}Б") activate_sound "audio/sfx/click.wav" action FilePage("quick")

                        textbutton "Ч" activate_sound "audio/sfx/click.wav" action FilePage("checkpoint")

                        for page in range(1, 10):
                            textbutton "[page]" activate_sound "audio/sfx/click.wav" action FilePage(page)

                        if current_page not in ("auto", "quick", "checkpoint"):
                            textbutton _(">") activate_sound "audio/sfx/click.wav" action FilePageNext()
                            key "save_page_next" activate_sound "audio/sfx/click.wav" action FilePageNext()

screen file_slots(title, is_load=False):

    default page_name_value = FilePageNameInputValue(pattern=_("{} страница"), auto=_("Автосохранения"), quick=_("Быстрые сохранения"), checkpoint=_("Чекпоинты"))

    $ current_page = FileCurrentPage()

    use game_menu(title):

        fixed:

            ## Это гарантирует, что ввод будет принимать enter перед остальными
            ## кнопками.
            order_reverse True

            ## Номер страницы, который может быть изменён посредством клика на
            ## кнопку.
            button:
                style "page_label"

                key_events True
                xalign 0.5
                action page_name_value.Toggle()

                input:
                    style "page_label_text"
                    value page_name_value

            ## Таблица слотов.
            grid gui.file_slot_cols gui.file_slot_rows:
                style_prefix "slot"

                xalign 0.5
                yalign 0.5

                spacing gui.slot_spacing

                for i in range(gui.file_slot_cols * gui.file_slot_rows):

                    $ slot = i + 1

                    button:
                        if current_page == "checkpoint" and not is_load:
                            action NullAction()
                            sensitive False
                        else:
                            action FileAction(slot)

                        has vbox

                        add FileScreenshot(slot) xalign 0.5

                        text FileTime(slot, format=_("{#file_time}%A, %d %B %Y, %H:%M"), empty=_("Пустой слот")):
                            style "slot_time_text"

                        text FileSaveName(slot):
                            style "slot_name_text"

                        key "save_delete" action FileDelete(slot)

            ## Кнопки для доступа к другим страницам.
            vbox:
                style_prefix "page"

                xalign 0.51
                yalign 0.92

                $ current_page = FileCurrentPage()

                hbox:
                    xalign 0.5

                    spacing gui.page_spacing

                    if current_page not in ("auto", "quick", "checkpoint"):
                        textbutton _("<") activate_sound "audio/sfx/click.wav" action FilePagePrevious()
                        key "save_page_prev" activate_sound "audio/sfx/click.wav" action FilePagePrevious()

                    if config.has_autosave:
                        textbutton _("{#auto_page}А") activate_sound "audio/sfx/click.wav" action FilePage("auto")

                    if config.has_quicksave:
                        textbutton _("{#quick_page}Б") activate_sound "audio/sfx/click.wav" action FilePage("quick")

                    textbutton "Ч" activate_sound "audio/sfx/click.wav" action FilePage("checkpoint")

                    ## range(1, 10) задаёт диапазон значений от 1 до 9.
                    for page in range(1, 10):
                        textbutton "[page]" activate_sound "audio/sfx/click.wav" action FilePage(page)

                    if current_page not in ("auto", "quick", "checkpoint"):
                        textbutton _(">") activate_sound "audio/sfx/click.wav" action FilePageNext()
                        key "save_page_next" activate_sound "audio/sfx/click.wav" action FilePageNext()

style page_label is gui_label
style page_label_text is gui_label_text
style page_button is gui_button
style page_button_text is gui_button_text

style slot_button is gui_button
style slot_button_text is gui_button_text
style slot_time_text is slot_button_text
style slot_name_text is slot_button_text

style page_label:
    xpadding 75
    ypadding 30

style page_label_text:
    textalign 0.5
    layout "subtitle"
    color "#ffcc00"

style page_button:
    properties gui.button_properties("page_button")

style page_button_text:
    color "#AD8E13"
    hover_color "#ffcc00"
    selected_color "#ffcc00"

style slot_button:
    properties gui.button_properties("slot_button")

style slot_button_text:
    properties gui.text_properties("slot_button")


## Экран настроек ##############################################################
##
## Экран настроек позволяет игроку настраивать игру под себя.
##
## https://www.renpy.org/doc/html/screen_special.html#preferences

screen preferences():
    modal True
    zorder 200

    default current_tab = "sound"
    default help_title = ""
    default help_text = ""

    button:
        style "empty"
        xfill True
        yfill True
        action NullAction()
        background "#000000cc"

    add "gui/settings_menu.png"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        padding (50, 50)
        background None

        vbox:
            spacing 20

            hbox:
                xfill True
                text "Настройки" size 50 color "#fed11b" font "fonts/ARIALBD.ttf" ypos 10 xpos 5
                
                imagebutton:
                    idle "gui/townmenu/close_e.png"
                    hover "gui/townmenu/close_h.png"
                    action Hide("preferences")
                    xalign 1.0
                    yalign 0.0
                    activate_sound "audio/sfx/click.wav"

            null height 1

            hbox:
                spacing 25
                yoffset -8

                hbox:
                    spacing 25
                    
                    fixed:
                        xysize (180, 90)
                        imagebutton auto "gui/test/b_opts_%s.png":
                            selected (current_tab == "sound")
                            action SetScreenVariable("current_tab", "sound")
                            activate_sound "audio/sfx/click.wav"
                        
                        text "Звук" xalign 0.5 yalign 0.38 size 28 color "#fed11b"

                    fixed:
                        xysize (180, 90)
                        imagebutton auto "gui/test/b_opts_%s.png":
                            selected (current_tab == "game")
                            action SetScreenVariable("current_tab", "game")
                            activate_sound "audio/sfx/click.wav"
                        
                        text "Игра" xalign 0.5 yalign 0.38 size 28 color "#fed11b"
                
            hbox:
                spacing 0

                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    xsize 800
                    ysize 800

                    if current_tab == "sound":
                        vbox:
                            spacing 40

                            if config.has_music:
                                vbox:
                                    spacing 10
                                    style_prefix "slider"

                                    label _("Громкость музыки") style "exm_settings_label"

                                    bar:
                                        value Preference("music volume")
                                        xsize 750
                                        hovered [SetScreenVariable("help_title", "Громкость музыки"), SetScreenVariable("help_text", "Регулирует громкость фоновой музыки в игре.")]
                                        unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]

                            if config.has_sound:
                                vbox:
                                    spacing 10
                                    style_prefix "slider"

                                    label _("Громкость звуков") style "exm_settings_label"

                                    bar:
                                        value Preference("sound volume")
                                        xsize 750
                                        hovered [SetScreenVariable("help_title", "Громкость звуков"), SetScreenVariable("help_text", "Регулирует громкость звуковых эффектов (выстрелы, взрывы, UI).")]
                                        unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]

                            if config.has_voice:
                                vbox:
                                    spacing 10
                                    style_prefix "slider"

                                    label _("Громкость голоса") style "exm_settings_label"

                                    bar:
                                        value Preference("voice volume")
                                        xsize 750
                                        hovered [SetScreenVariable("help_title", "Громкость голоса"), SetScreenVariable("help_text", "Регулирует громкость озвучки персонажей.")]
                                        unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]

                            if config.has_music or config.has_sound or config.has_voice:
                                null height 20

                                textbutton _("Без звука"):
                                    action Preference("all mute", "toggle")
                                    style "settings_text_button"
                                    hovered [SetScreenVariable("help_title", "Без звука"), SetScreenVariable("help_text", "Полностью отключает все звуки в игре.")]
                                    unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]

                                textbutton _("Тест звука"):
                                    xpos 0 
                                    action Function(lambda: renpy.sound.play(config.sample_sound) if config.sample_sound else None)
                                    style "settings_text_button"
                                    hovered [SetScreenVariable("help_title", "Тест звука"), SetScreenVariable("help_text", "Проигрывает тестовый звук для проверки громкости.")]
                                    unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]

                    elif current_tab == "game":
                        vbox:
                            spacing 40

                            vbox:
                                spacing 10
                                style_prefix "slider"

                                label _("Скорость текста") style "exm_settings_label"

                                bar:
                                    value Preference("text speed")
                                    xsize 750
                                    hovered [SetScreenVariable("help_title", "Скорость текста"), SetScreenVariable("help_text", "Скорость появления текста на экране. Чем выше — тем быстрее.")]
                                    unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]

                            vbox:
                                spacing 10
                                style_prefix "slider"

                                label _("Скорость авточтения") style "exm_settings_label"

                                bar:
                                    value Preference("auto-forward time")
                                    xsize 750
                                    hovered [SetScreenVariable("help_title", "Скорость авточтения"), SetScreenVariable("help_text", "Задержка перед автоматическим переходом к следующей реплике.")]
                                    unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]

                            null height 20

                            hbox:
                                spacing 100

                                if renpy.variant("pc") or renpy.variant("web"):
                                    vbox:
                                        style_prefix "radio"
                                        label _("Режим экрана") style "exm_settings_label"
                                        textbutton _("Оконный"):
                                            action Preference("display", "window")
                                            style "settings_text_button"
                                            hovered [SetScreenVariable("help_title", "Оконный режим"), SetScreenVariable("help_text", "Игра запускается в окне.")]
                                            unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]
                                            activate_sound "audio/sfx/click.wav"
                                        textbutton _("Полный"):
                                            action Preference("display", "fullscreen")
                                            style "settings_text_button"
                                            hovered [SetScreenVariable("help_title", "Полноэкранный режим"), SetScreenVariable("help_text", "Игра занимает весь экран.")]
                                            unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]
                                            activate_sound "audio/sfx/click.wav"

                                vbox:
                                    style_prefix "radio"
                                    label _("Сложность боёв") style "exm_settings_label"
                                    textbutton _("Новичок"):
                                        action Function(set_difficulty, "easy", 0.015)
                                        selected (difficulty == "easy")
                                        style "settings_text_button"
                                        hovered [SetScreenVariable("help_title", "Новичок"), SetScreenVariable("help_text", "Урон:\n2% от максимального HP.\n\nУрон может быть выше в зависимости от количества противников.")]
                                        unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]
                                        activate_sound "audio/sfx/click.wav"
                                    textbutton _("Бывалый"):
                                        action Function(set_difficulty, "normal", 0.03)
                                        selected (difficulty == "normal")
                                        style "settings_text_button"
                                        hovered [SetScreenVariable("help_title", "Бывалый"), SetScreenVariable("help_text", "Урон:\n3% от максимального HP.\n\nУрон может быть выше в зависимости от количества противников.")]
                                        unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]
                                        activate_sound "audio/sfx/click.wav"
                                    textbutton _("Профессионал"):
                                        action Function(set_difficulty, "hard", 0.04)
                                        selected (difficulty == "hard")
                                        style "settings_text_button"
                                        hovered [SetScreenVariable("help_title", "Профессионал"), SetScreenVariable("help_text", "Урон:\n4% от максимального HP.\n\nУрон может быть выше в зависимости от количества противников.")]
                                        unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]
                                        activate_sound "audio/sfx/click.wav"
                                    textbutton _("Мастер"):
                                        action Function(set_difficulty, "expert", 0.055)
                                        selected (difficulty == "expert")
                                        style "settings_text_button"
                                        hovered [SetScreenVariable("help_title", "Мастер"), SetScreenVariable("help_text", "Урон:\n5.5% от максимального HP.\n\nУрон может быть выше в зависимости от количества противников.")]
                                        unhovered [SetScreenVariable("help_title", ""), SetScreenVariable("help_text", "")]
                                        activate_sound "audio/sfx/click.wav"

                frame:
                    xsize 450
                    ysize 550
                    background None
                    padding (30, 20)

                    vbox:
                        spacing 20
                        xfill True

                        if help_title:
                            text help_title size 33 color "#404040" font "fonts/ARIALBD.ttf"
                        else:
                            text "Справка" size 33 color "#555555" font "fonts/ARIALBD.ttf"

                        null height 20

                        if help_text:
                            text help_text size 25 color "#404040"
                        else:
                            text "Наведите курсор на элемент, чтобы увидеть подсказку." size 25 color "#555555"

style pref_label is gui_label
style pref_label_text is gui_label_text
style pref_vbox is vbox

style radio_label is pref_label
style radio_label_text is pref_label_text
style radio_button is gui_button
style radio_button_text is gui_button_text
style radio_vbox is pref_vbox

style check_label is pref_label
style check_label_text is pref_label_text
style check_button is gui_button
style check_button_text is gui_button_text
style check_vbox is pref_vbox

style slider_label is pref_label
style slider_label_text is pref_label_text
style slider_slider is gui_slider
style slider_button is gui_button
style slider_button_text is gui_button_text
style slider_pref_vbox is pref_vbox

style settings_text_button is check_button
style settings_text_button_text is default:
    color "#505050"
    hover_color "#303030"

style mute_all_button is check_button
style mute_all_button_text is default

style exm_settings_label_text is default:
    color "#383838"
    size 35

style pref_label:
    top_margin gui.pref_spacing
    bottom_margin 3

style pref_label_text:
    yalign 1.0

style pref_vbox:
    xsize 338

style radio_vbox:
    spacing gui.pref_button_spacing

style radio_button:
    properties gui.button_properties("radio_button")
    foreground "gui/button/radio_[prefix_]foreground.png"

style radio_button_text:
    properties gui.text_properties("radio_button")

style check_vbox:
    spacing gui.pref_button_spacing

style check_button:
    properties gui.button_properties("check_button")
    foreground "gui/button/check_[prefix_]foreground.png"

style check_button_text:
    properties gui.text_properties("check_button")

style slider_slider:
    xsize 525

style slider_button:
    properties gui.button_properties("slider_button")
    yalign 0.5
    left_margin 15

style slider_button_text:
    properties gui.text_properties("slider_button")

style slider_vbox:
    xsize 675


## Экран истории ###############################################################
##
## Этот экран показывает игроку историю диалогов. Хотя в этом экране нет ничего
## особенного, он имеет доступ к истории диалогов, хранимом в _history_list.
##
## https://www.renpy.org/doc/html/history.html

screen history():
    modal True
    zorder 200

    button:
        style "empty"
        xfill True
        yfill True
        action NullAction()
        background "#000000cc"

    add "gui/settings_menu.png"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        padding (50, 50)
        background None

        vbox:
            spacing 20

            hbox:
                xfill True
                text "История" size 60 color "#fed11b" font "fonts/ARIALBD.ttf" ypos 20 xpos 5

                imagebutton:
                    idle "gui/townmenu/close_e.png"
                    hover "gui/townmenu/close_h.png"
                    action Hide("history")
                    xalign 1.0
                    yalign 0.0
                    activate_sound "audio/sfx/click.wav"

            null height 1

            viewport:
                scrollbars "vertical"
                mousewheel True
                ypos 100
                xsize 1350
                ysize 585

                vbox:
                    spacing 50

                    if _history_list:
                        for h in _history_list:

                            vbox:
                                spacing 5

                                if h.who:
                                    label h.who:
                                        style "history_name"
                                        substitute False
                                        if "color" in h.who_args:
                                            text_color "#404040"

                                $ what = renpy.filter_text_tags(h.what, allow=gui.history_allow_tags)
                                text what:
                                    substitute False

                    else:
                        text _("История диалогов пуста.") size 30 color "#FFFFFF"

## Это определяет, какие теги могут отображаться на экране истории.

define gui.history_allow_tags = { "alt", "noalt", "rt", "rb", "art" }


style history_window is empty

style history_name is gui_label
style history_name_text is gui_label_text
style history_text is gui_text

style history_label is gui_label
style history_label_text is gui_label_text

style history_window:
    ysize gui.history_height
    ypos 1

style history_name:
    xpos gui.history_name_xpos
    ypos gui.history_name_ypos
    xsize gui.history_name_width
    color "#404040"

style history_name_text:
    min_width gui.history_name_width
    textalign gui.history_name_xalign
    color "#404040"

style history_text:
    xpos gui.history_text_xpos
    ypos gui.history_text_ypos
    xanchor gui.history_text_xalign
    xsize gui.history_text_width
    min_width gui.history_text_width
    textalign gui.history_text_xalign
    layout ("subtitle" if gui.history_text_xalign else "tex")

style history_label:
    xfill True

style history_label_text:
    xalign 0.5


## Экран помощи ################################################################
##
## Экран, дающий информацию о клавишах управления. Он использует другие экраны
## (keyboard_help, mouse_help, и gamepad_help), чтобы показывать актуальную
## помощь.

screen help():
    modal True
    zorder 200

    default device = "keyboard"

    # Затемнение фона
    button:
        style "empty"
        xfill True
        yfill True
        action NullAction()
        background "#000000cc"

    # Статическое изображение меню (по желанию)
    add "gui/settings_menu.png"

    # Основное окно с контентом
    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 900
        padding (50, 50)
        background None

        vbox:
            spacing 20

            # Заголовок
            hbox:
                xfill True
                text _("Помощь") size 60 color "#fed11b" font "fonts/ARIALBD.ttf" ypos 10 xpos 5

                # Кнопка закрытия
                imagebutton:
                    idle "gui/townmenu/close_e.png"
                    hover "gui/townmenu/close_h.png"
                    action Hide("help")
                    xalign 1.0
                    yalign 0.0
                    activate_sound "audio/sfx/click.wav"

            null height 1

            # Выбор устройства
            hbox:
                spacing 20
                yoffset -12

                fixed:
                    xysize (180, 90)
                    imagebutton auto "gui/test/b_opts_%s.png":
                        action SetScreenVariable("device", "keyboard")
                        activate_sound "audio/sfx/click.wav"
                    
                    text "Клавиатура" xalign 0.5 yalign 0.4 size 24 color "#fed11b"

                fixed:
                    xysize (180, 90)
                    imagebutton auto "gui/test/b_opts_%s.png":
                        action SetScreenVariable("device", "mouse")
                        activate_sound "audio/sfx/click.wav"
                    
                    text "Мышь" xalign 0.5 yalign 0.38 size 28 color "#fed11b"

                #textbutton _("Клавиатура") activate_sound "audio/sfx/click.wav" action SetScreenVariable("device", "keyboard")
                #textbutton _("Мышь") activate_sound "audio/sfx/click.wav" action SetScreenVariable("device", "mouse")

            null height 20

            # Контент с прокруткой
            viewport:
                scrollbars "vertical"
                mousewheel True
                xsize 1350
                ysize 700

                vbox:
                    spacing 15

                    if device == "keyboard":
                        hbox:
                            label _("Enter")
                            text _("Прохождение диалогов, активация интерфейса.") xpos 30

                        hbox:
                            label _("Пробел")
                            text _("Прохождение диалогов без возможности делать выбор.") xpos 30

                        hbox:
                            label _("Стрелки")
                            text _("Навигация по интерфейсу.") xpos 30

                        hbox:
                            label _("Esc")
                            text _("Вход в игровое меню.") xpos 30

                        hbox:
                            label "H"
                            text _("Скрывает интерфейс пользователя.") xpos 30

                        hbox:
                            label "S"
                            text _("Делает снимок экрана.") xpos 30

                    elif device == "mouse":
                        hbox:
                            label _("Левый клик")
                            text _("Прохождение диалогов, активация интерфейса.") xpos 30

                        hbox:
                            label _("Клик колёсиком")
                            text _("Скрывает интерфейс пользователя.") xpos 30

                        hbox:
                            label _("Правый клик")
                            text _("Вход в игровое меню.") xpos 30



screen keyboard_help():

    hbox:
        label _("Enter")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Пробел")
        text _("Прохождение диалогов без возможности делать выбор.")

    hbox:
        label _("Стрелки")
        text _("Навигация по интерфейсу.")

    hbox:
        label _("Esc")
        text _("Вход в игровое меню.")

    hbox:
        label "H"
        text _("Скрывает интерфейс пользователя.")

    hbox:
        label "S"
        text _("Делает снимок экрана.")


screen mouse_help():

    hbox:
        label _("Левый клик")
        text _("Прохождение диалогов, активация интерфейса.")

    hbox:
        label _("Клик колёсиком")
        text _("Скрывает интерфейс пользователя.")

    hbox:
        label _("Правый клик")
        text _("Вход в игровое меню.")


style help_button is gui_button
style help_button_text is gui_button_text
style help_label is gui_label
style help_label_text is gui_label_text
style help_text is gui_text

style help_button:
    properties gui.button_properties("help_button")
    xmargin 12

style help_button_text:
    properties gui.text_properties("help_button")

style help_label:
    xsize 375
    right_padding 30

style help_label_text:
    size gui.text_size
    xalign 1.0
    textalign 1.0



################################################################################
## Дополнительные экраны
################################################################################


## Экран подтверждения #########################################################
##
## Экран подтверждения вызывается, когда Ren'Py хочет спросить у игрока вопрос
## Да или Нет.
##
## https://www.renpy.org/doc/html/screen_special.html#confirm

screen confirm(message, yes_action, no_action):

    ## Гарантирует, что другие экраны будут недоступны, пока показан этот экран.
    modal True

    zorder 200

    style_prefix "confirm"

    add "gui/overlay/confirm.png"

    frame:

        vbox:
            xalign .5
            yalign .5
            spacing 45

            label _(message):
                style "confirm_prompt"
                xalign 0.5

            hbox:
                xalign 0.5
                spacing 150

                textbutton _("Да") action yes_action
                textbutton _("Нет") action no_action

    ## Правый клик и esc, как ответ "Нет".
    key "game_menu" action no_action


style confirm_frame is gui_frame
style confirm_prompt is gui_prompt
style confirm_prompt_text is gui_prompt_text
style confirm_button is gui_medium_button
style confirm_button_text is gui_medium_button_text

style confirm_frame:
    background Frame([ "gui/confirm_frame.png", "gui/frame.png"], gui.confirm_frame_borders, tile=gui.frame_tile)
    padding gui.confirm_frame_borders.padding
    xalign .5
    yalign .5

style confirm_prompt_text:
    textalign 0.5
    layout "subtitle"

style confirm_button:
    properties gui.button_properties("confirm_button")

style confirm_button_text:
    properties gui.text_properties("confirm_button")


## Экран индикатора пропуска ###################################################
##
## Экран индикатора пропуска появляется для того, чтобы показать, что идёт
## пропуск.
##
## https://www.renpy.org/doc/html/screen_special.html#skip-indicator

screen skip_indicator():

    zorder 100
    style_prefix "skip"

    frame:

        hbox:
            spacing 9

            text _("Пропускаю")

            text "▸" at delayed_blink(0.0, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.2, 1.0) style "skip_triangle"
            text "▸" at delayed_blink(0.4, 1.0) style "skip_triangle"


## Эта трансформация используется, чтобы мигать стрелками одна за другой.
transform delayed_blink(delay, cycle):
    alpha .5

    pause delay

    block:
        linear .2 alpha 1.0
        pause .2
        linear .2 alpha 0.5
        pause (cycle - .4)
        repeat


style skip_frame is empty
style skip_text is gui_text
style skip_triangle is skip_text

style skip_frame:
    ypos gui.skip_ypos
    background Frame("gui/skip.png", gui.skip_frame_borders, tile=gui.frame_tile)
    padding gui.skip_frame_borders.padding

style skip_text:
    size gui.notify_text_size

style skip_triangle:
    ## Нам надо использовать шрифт, имеющий в себе символ U+25B8 (стрелку выше).
    font "DejaVuSans.ttf"


## Экран уведомлений ###########################################################
##
## Экран уведомлений используется, чтобы показать игроку оповещение. (Например,
## когда игра автосохранилась, или был сделан скриншот)
##
## https://www.renpy.org/doc/html/screen_special.html#notify-screen

screen notify(message):

    zorder 100
    style_prefix "notify"

    frame at notify_appear:
        xalign 0.5
        yalign 0.03
        
        text "[message!tq]" xpos 20 yalign 0.5 text_align 0.5

    timer 3.25 action Hide('notify')


transform notify_appear:
    on show:
        alpha 0
        linear .25 alpha 1.0
    on hide:
        linear .5 alpha 0.0


style notify_frame is empty
style notify_text is gui_text

style notify_frame:
    ypos gui.notify_ypos

    background Frame("gui/notify.png", gui.notify_frame_borders, tile=gui.frame_tile)
    padding gui.notify_frame_borders.padding

style notify_text:
    properties gui.text_properties("notify")


## Экран NVL ###################################################################
##
## Этот экран используется в диалогах и меню режима NVL.
##
## https://www.renpy.org/doc/html/screen_special.html#nvl


screen nvl(dialogue, items=None):

    window:
        style "nvl_window"

        has vbox:
            spacing gui.nvl_spacing

        ## Показывает диалог или в vpgrid, или в vbox.
        if gui.nvl_height:

            vpgrid:
                cols 1
                yinitial 1.0

                use nvl_dialogue(dialogue)

        else:

            use nvl_dialogue(dialogue)

        ## Показывает меню, если есть. Меню может показываться некорректно, если
        ## config.narrator_menu установлено на True.
        for i in items:

            textbutton i.caption:
                action i.action
                style "nvl_button"

    add SideImage() xalign 0.0 yalign 1.0


screen nvl_dialogue(dialogue):

    for d in dialogue:

        window:
            id d.window_id

            fixed:
                yfit gui.nvl_height is None

                if d.who is not None:

                    text d.who:
                        id d.who_id

                text d.what:
                    id d.what_id


## Это контролирует максимальное число строк NVL, могущих показываться за раз.
define config.nvl_list_length = gui.nvl_list_length

style nvl_window is default
style nvl_entry is default

style nvl_label is say_label
style nvl_dialogue is say_dialogue

style nvl_button is button
style nvl_button_text is button_text

style nvl_window:
    xfill True
    yfill True

    background "gui/nvl.png"
    padding gui.nvl_borders.padding

style nvl_entry:
    xfill True
    ysize gui.nvl_height

style nvl_label:
    xpos gui.nvl_name_xpos
    xanchor gui.nvl_name_xalign
    ypos gui.nvl_name_ypos
    yanchor 0.0
    xsize gui.nvl_name_width
    min_width gui.nvl_name_width
    textalign gui.nvl_name_xalign

style nvl_dialogue:
    xpos gui.nvl_text_xpos
    xanchor gui.nvl_text_xalign
    ypos gui.nvl_text_ypos
    xsize gui.nvl_text_width
    min_width gui.nvl_text_width
    textalign gui.nvl_text_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_thought:
    xpos gui.nvl_thought_xpos
    xanchor gui.nvl_thought_xalign
    ypos gui.nvl_thought_ypos
    xsize gui.nvl_thought_width
    min_width gui.nvl_thought_width
    textalign gui.nvl_thought_xalign
    layout ("subtitle" if gui.nvl_text_xalign else "tex")

style nvl_button:
    properties gui.button_properties("nvl_button")
    xpos gui.nvl_button_xpos
    xanchor gui.nvl_button_xalign

style nvl_button_text:
    properties gui.text_properties("nvl_button")


## Пузырьковый экран ###########################################################
##
## Экран пузырьков используется для отображения диалога игроку при использовании
## речевых пузырьков. Экран пузырьков принимает те же параметры, что и экран
## say, должен создать отображаемый объект с id "what", и может создавать
## отображаемые объекты с id "namebox", "who" и "window".
##
## https://www.renpy.org/doc/html/bubble.html#bubble-screen

screen bubble(who, what):
    style_prefix "bubble"

    window:
        id "window"

        if who is not None:

            window:
                id "namebox"
                style "bubble_namebox"

                text who:
                    id "who"

        text what:
            id "what"

style bubble_window is empty
style bubble_namebox is empty
style bubble_who is default
style bubble_what is default

style bubble_window:
    xpadding 30
    top_padding 5
    bottom_padding 5

style bubble_namebox:
    xalign 0.5

style bubble_who:
    xalign 0.5
    textalign 0.5
    color "#000"

style bubble_what:
    align (0.5, 0.5)
    text_align 0.5
    layout "subtitle"
    color "#000"

define bubble.frame = Frame("gui/bubble.png", 55, 55, 55, 95)
define bubble.thoughtframe = Frame("gui/thoughtbubble.png", 55, 55, 55, 55)

define bubble.properties = {
    "bottom_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "bottom_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=1),
        "window_bottom_padding" : 27,
    },

    "top_left" : {
        "window_background" : Transform(bubble.frame, xzoom=1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "top_right" : {
        "window_background" : Transform(bubble.frame, xzoom=-1, yzoom=-1),
        "window_top_padding" : 27,
    },

    "thought" : {
        "window_background" : bubble.thoughtframe,
    }
}

define bubble.expand_area = {
    "bottom_left" : (0, 0, 0, 22),
    "bottom_right" : (0, 0, 0, 22),
    "top_left" : (0, 22, 0, 0),
    "top_right" : (0, 22, 0, 0),
    "thought" : (0, 0, 0, 0),
}



################################################################################
## Мобильные варианты
################################################################################

style pref_vbox:
    variant "medium"
    xsize 675

## Раз мышь может не использоваться, мы заменили быстрое меню версией,
## использующей меньше кнопок, но больших по размеру, чтобы их было легче
## касаться.
screen quick_menu():
    variant "touch"

    zorder 100

    if quick_menu:

        hbox:
            style_prefix "quick"

            xalign 0.5
            yalign 0.975

            textbutton _("Назад") action Rollback()
            textbutton _("Пропуск") action Skip() alternate Skip(fast=True, confirm=True)
            textbutton _("Авто") action Preference("auto-forward", "toggle")
            textbutton _("Меню") action ShowMenu()
            textbutton _("Профиль") activate_sound "audio/sfx/click.wav" action ShowMenu("statistics_screen")
            textbutton _("Меню города") activate_sound "audio/sfx/click.wav" action ShowMenu("InGameMenu")


style window:
    variant "small"
    background "gui/phone/textbox.png"

style radio_button:
    variant "small"
    foreground "gui/phone/button/radio_[prefix_]foreground.png"

style check_button:
    variant "small"
    foreground "gui/phone/button/check_[prefix_]foreground.png"

style nvl_window:
    variant "small"
    background "gui/phone/nvl.png"

style main_menu_frame:
    variant "small"
    background "gui/phone/overlay/main_menu.png"

style game_menu_outer_frame:
    variant "small"
    background "gui/phone/overlay/game_menu.png"

style game_menu_navigation_frame:
    variant "small"
    xsize 510

style game_menu_content_frame:
    variant "small"
    top_margin 0

style pref_vbox:
    variant "small"
    xsize 600

style bar:
    variant "small"
    ysize gui.bar_size
    left_bar Frame("gui/phone/bar/left.png", gui.bar_borders, tile=gui.bar_tile)
    right_bar Frame("gui/phone/bar/right.png", gui.bar_borders, tile=gui.bar_tile)

style vbar:
    variant "small"
    xsize gui.bar_size
    top_bar Frame("gui/phone/bar/top.png", gui.vbar_borders, tile=gui.bar_tile)
    bottom_bar Frame("gui/phone/bar/bottom.png", gui.vbar_borders, tile=gui.bar_tile)

style scrollbar:
    variant "small"
    ysize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/horizontal_[prefix_]bar.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/horizontal_[prefix_]thumb.png", gui.scrollbar_borders, tile=gui.scrollbar_tile)

style vscrollbar:
    variant "small"
    xsize gui.scrollbar_size
    base_bar Frame("gui/phone/scrollbar/vertical_[prefix_]bar.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)
    thumb Frame("gui/phone/scrollbar/vertical_[prefix_]thumb.png", gui.vscrollbar_borders, tile=gui.scrollbar_tile)

style slider:
    variant "small"
    ysize gui.slider_size
    base_bar Frame("gui/phone/slider/horizontal_[prefix_]bar.png", gui.slider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/horizontal_[prefix_]thumb.png"

style vslider:
    variant "small"
    xsize gui.slider_size
    base_bar Frame("gui/phone/slider/vertical_[prefix_]bar.png", gui.vslider_borders, tile=gui.slider_tile)
    thumb "gui/phone/slider/vertical_[prefix_]thumb.png"

style slider_vbox:
    variant "small"
    xsize None

style slider_slider:
    variant "small"
    xsize 900
