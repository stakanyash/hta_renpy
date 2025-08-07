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

    default selected_item = None

    python:
        def sell_item_with_confirm(item_key):
            if TownType == "City":
                price = ItemPricesCity.get(item_key)
            else:
                price = ItemPricesVillage.get(item_key)

            if price is None:
                return

            item = ItemDatabase.get(item_key)
            if item is None:
                return

            if renpy.confirm("Продать «{}» за {} монет?".format(item["name"], price)):
                global CurrentMoney, Inventory
                CurrentMoney += price
                Inventory.remove(item_key)


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

        viewport:
            xpos 235
            ypos 290
            xsize 500
            ysize 900
            scrollbars None
            mousewheel False

            grid 3 4 spacing 25:

                for item_id in Inventory:

                    $ item_data = ItemDatabase.get(item_id)

                    if item_data:

                        frame:
                            xsize 140
                            ysize 140
                            background Solid("#8b8a8ac0")

                            imagebutton:
                                idle item_data["icon"]
                                hover item_data["icon"]
                                action SetScreenVariable("selected_item", item_id)
                                focus_mask True

        textbutton _("Продать") action Function(sell_item_with_confirm, selected_item) xalign 0.5

        if selected_item:
            $ item_data = ItemDatabase[selected_item]
            $ price = ItemPricesVillage[selected_item] if TownType == "Village" else ItemPricesCity[selected_item]
        
            frame:
                xpos 1150
                ypos 285
                xsize 500
                ysize 300
                background None
                padding (20, 20)

                text item_data["name"] size 40 color "#353535"

            frame:
                xpos 800
                ypos 380
                xsize 930
                ysize 300
                background None
                padding (20, 20)

                text item_data["desc"] size 25 color "#353535"

            frame:
                xpos 800
                ypos 705
                xsize 960
                ysize 300
                background None
                padding (20, 20)

                text "Цена: [price] монет" size 30 color "#353535"

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
    