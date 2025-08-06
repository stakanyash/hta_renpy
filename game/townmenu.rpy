# Town Menu

screen InGameMenu():
    tag menu

    frame:
        style "menu_frame"
        background "gui/townmenu/backmain.png"
        xsize 1920
        ysize 1080

        if 0 <= CurrentMoney <= 9:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"
        elif 10 <= CurrentMoney <= 99:
            text "Деньги:" size 19 xpos 65 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 135 ypos 20 textalign 0.5 color "#404040"
        elif 100 <= CurrentMoney <= 999:
            text "Деньги:" size 19 xpos 60 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 130 ypos 20 textalign 0.5 color "#404040"
        elif 1000 <= CurrentMoney <= 9999:
            text "Деньги:" size 19 xpos 55 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 125 ypos 20 textalign 0.5 color "#404040"
        elif 10000 <= CurrentMoney <= 99999:
            text "Деньги:" size 19 xpos 50 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 120 ypos 20 textalign 0.5 color "#404040"
        elif 100000 <= CurrentMoney <= 999999:
            text "Деньги:" size 19 xpos 45 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 115 ypos 20 textalign 0.5 color "#404040"
        elif CurrentMoney >= 1000000:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[format_money(CurrentMoney)]" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"

        textbutton "Магазин автомобилей" activate_sound "audio/sfx/click.wav":
            xalign 0.5
            ypos 400
            xsize gui.choice_button_width
            ysize gui.choice_button_height
            style "gamemenu_button"
            action [Hide("test"), Show("Car_Shop")]

        textbutton "Магазин оружия" activate_sound "audio/sfx/click.wav":
            xalign 0.5
            ypos 500
            xsize gui.choice_button_width
            ysize gui.choice_button_height
            style "gamemenu_button"
            action [Hide("test"), Show("Gun_Shop_Menu")]

        textbutton "Продажа из инвентаря" activate_sound "audio/sfx/click.wav":
            xalign 0.5
            ypos 600
            xsize gui.choice_button_width
            ysize gui.choice_button_height
            style "gamemenu_button"
            action [Hide("test"), Show("Selling_Menu")]

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/close_e.png" 
            hover "gui/townmenu/close_h.png"
            action Return()
            xalign 0.99
            yalign 0.0
            focus_mask True 

style gamemenu_vbox is vbox
style gamemenu_button is button
style gamemenu_button_text is button_text

style gamemenu_vbox:
    xalign 0.5
    ypos 405
    yanchor 0.5

    spacing gui.choice_spacing

style gamemenu_button is default:
    properties gui.button_properties("choice_button")

style gamemenu_button_text is default:
    properties gui.text_properties("choice_button")

# Inventory selling

screen Selling_Menu():
    tag menu

    frame:
        style "menu_frame"
        background "gui/townmenu/backmain.png"
        xsize 1920
        ysize 1080

        if 0 <= CurrentMoney <= 9:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"
        elif 10 <= CurrentMoney <= 99:
            text "Деньги:" size 19 xpos 65 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 135 ypos 20 textalign 0.5 color "#404040"
        elif 100 <= CurrentMoney <= 999:
            text "Деньги:" size 19 xpos 60 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 130 ypos 20 textalign 0.5 color "#404040"
        elif 1000 <= CurrentMoney <= 9999:
            text "Деньги:" size 19 xpos 55 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 125 ypos 20 textalign 0.5 color "#404040"
        elif 10000 <= CurrentMoney <= 99999:
            text "Деньги:" size 19 xpos 50 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 120 ypos 20 textalign 0.5 color "#404040"
        elif 100000 <= CurrentMoney <= 999999:
            text "Деньги:" size 19 xpos 45 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 115 ypos 20 textalign 0.5 color "#404040"
        elif CurrentMoney >= 1000000:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[format_money(CurrentMoney)]" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/close_e.png" 
            hover "gui/townmenu/close_h.png"
            action Return()
            xalign 0.99
            yalign 0.0
            focus_mask True 

# Gun Shop

screen Gun_Shop_Menu():
    tag menu

    frame:
        style "menu_frame"
        background "gui/townmenu/backmain.png"
        xsize 1920
        ysize 1080

        if 0 <= CurrentMoney <= 9:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"
        elif 10 <= CurrentMoney <= 99:
            text "Деньги:" size 19 xpos 65 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 135 ypos 20 textalign 0.5 color "#404040"
        elif 100 <= CurrentMoney <= 999:
            text "Деньги:" size 19 xpos 60 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 130 ypos 20 textalign 0.5 color "#404040"
        elif 1000 <= CurrentMoney <= 9999:
            text "Деньги:" size 19 xpos 55 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 125 ypos 20 textalign 0.5 color "#404040"
        elif 10000 <= CurrentMoney <= 99999:
            text "Деньги:" size 19 xpos 50 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 120 ypos 20 textalign 0.5 color "#404040"
        elif 100000 <= CurrentMoney <= 999999:
            text "Деньги:" size 19 xpos 45 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 115 ypos 20 textalign 0.5 color "#404040"
        elif CurrentMoney >= 1000000:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[format_money(CurrentMoney)]" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/close_e.png" 
            hover "gui/townmenu/close_h.png"
            action Return()
            xalign 0.99
            yalign 0.0
            focus_mask True 

# Car Shop

screen Car_Shop():
    tag menu

    frame:
        style "menu_frame"
        background "gui/townmenu/backmain.png"
        xsize 1920
        ysize 1080

        if 0 <= CurrentMoney <= 9:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"
        elif 10 <= CurrentMoney <= 99:
            text "Деньги:" size 19 xpos 65 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 135 ypos 20 textalign 0.5 color "#404040"
        elif 100 <= CurrentMoney <= 999:
            text "Деньги:" size 19 xpos 60 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 130 ypos 20 textalign 0.5 color "#404040"
        elif 1000 <= CurrentMoney <= 9999:
            text "Деньги:" size 19 xpos 55 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 125 ypos 20 textalign 0.5 color "#404040"
        elif 10000 <= CurrentMoney <= 99999:
            text "Деньги:" size 19 xpos 50 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 120 ypos 20 textalign 0.5 color "#404040"
        elif 100000 <= CurrentMoney <= 999999:
            text "Деньги:" size 19 xpos 45 ypos 20 textalign 0.5 color "#404040"
            text "[CurrentMoney] монет" size 19 xpos 115 ypos 20 textalign 0.5 color "#404040"
        elif CurrentMoney >= 1000000:
            text "Деньги:" size 19 xpos 70 ypos 20 textalign 0.5 color "#404040"
            text "[format_money(CurrentMoney)]" size 19 xpos 140 ypos 20 textalign 0.5 color "#404040"

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/close_e.png" 
            hover "gui/townmenu/close_h.png"
            action Return()
            xalign 0.99
            yalign 0.0
            focus_mask True 
    