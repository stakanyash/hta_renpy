# Town Menu

screen InGameMenu():
    tag menu

    frame:
        style "menu_frame"
        background "gui/townmenu/backmain.png"
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

        frame:
            background None
            xalign 0.5
            yalign 0.5

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/close_e.png" 
            hover "gui/townmenu/close_h.png"
            action Return()
            xalign 0.99
            yalign 0.0
            focus_mask True 

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/buttons/tab_stats_e.png" 
            hover "gui/townmenu/buttons/tab_stats_s.png"
            action [Hide("InGameMenu"), Show("statistics_screen")]
            xpos 350
            focus_mask True 

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/buttons/tab_invent_e.png" 
            hover "gui/townmenu/buttons/tab_invent_s.png"
            action [Hide("InGameMenu"), Show("Selling_Menu")]
            xpos 1630
            focus_mask True 

        if player_config.town_type == "City":
            imagebutton activate_sound "audio/sfx/click.wav":
                idle "gui/townmenu/buttons/tab_weapon_e.png" 
                hover "gui/townmenu/buttons/tab_weapon_s.png"
                action [Hide("InGameMenu"), Show("Gun_Shop_Menu")]
                xpos 1450
                ypos 1
                focus_mask True 

            imagebutton activate_sound "audio/sfx/click.wav":
                idle "gui/townmenu/buttons/tab_truck_e.png" 
                hover "gui/townmenu/buttons/tab_truck_s.png"
                action [Hide("InGameMenu"), Show("Car_Shop")]
                xpos 1270
                ypos 1
                focus_mask True 

        hbox:
            xsize 527
            ysize 63
            xpos 1365
            yalign 0.12
            text player_config.town_name xalign 0.5 yalign 0.5 size 28 color "#404040"

        add f"gui/townmenu/clans/{player_config.group_logo}.png" xpos 1510 ypos 450

style centered_towntext is text:
    xpos 0.83
    yalign 0.13
    textalign 0.5
    padding (10, 10)

# Inventory selling

screen Selling_Menu():
    tag menu

    default selected_item = None

    python:
        def sell_item_immediately(item_key):
            if item_key is None:
                return

            if player_config.town_type == "City":
                price = ItemPricesCity.get(item_key)
            else:
                price = ItemPricesVillage.get(item_key)

            if price is None:
                return

            if item_key in player_config.inventory:
                renpy.sound.play("audio/sfx/coins.wav", channel="sellitem")
                player_config.inventory.remove(item_key)
                player_config.add_money(price)
        
        def delete_item(item_key):
            if item_key in player_config.inventory:
                player_config.inventory.remove(item_key)
        
        def install_weapon(weapon_key):
            if weapon_key is None or weapon_key not in player_config.inventory:
                return
            
            if weapon_key not in GunDatabase:
                return

            gun_data = GunDatabase[weapon_key]
            gun_type = gun_data.get("type", "")
            gun_size = gun_data.get("size", "Small")

            if gun_size == "Big" and player_config.big_gun_install != "Possible":
                renpy.notify("Невозможно установить это оружие в данный слот.")
                return
            
            old_gun = player_config.current_gun
            
            player_config.inventory.remove(weapon_key)
            
            player_config.current_gun = weapon_key
            player_config.gun_type = GunDatabase[weapon_key]["type"]
            
            player_config.inventory.append(old_gun)
        
        def is_weapon(item_key):
            return item_key in GunDatabase


    frame:
        style "menu_frame"
        background ("gui/townmenu/backinv_gunsel.png" if (selected_item and is_weapon(selected_item)) else "gui/townmenu/backinv.png")
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

        viewport:
            xpos 230
            ypos 290
            xsize 500
            ysize 900
            scrollbars None
            mousewheel False

            grid 3 4 spacing -15:

                for item_id in player_config.inventory:

                    $ item_data = ItemDatabase.get(item_id)

                    if item_data:

                        frame:
                            xsize 180
                            ysize 180
                            background None

                            imagebutton activate_sound "audio/sfx/click.wav":
                                idle item_data["icon"]
                                hover item_data["icon"]
                                hover_background Solid("#50505031")
                                action SetScreenVariable("selected_item", item_id)
                                focus_mask True

        frame:
            xalign 0.9
            yalign 0.145
            xsize 100
            ysize 60
            background None
            
            text "[len(player_config.inventory)]/[CarInventoryLimits.get(player_config.car, 0)]" xalign 0.5 yalign 0.5 color "#404040"

        if selected_item and is_weapon(selected_item):
            textbutton _("Установить") activate_sound "audio/sfx/click.wav" action [Function(install_weapon, selected_item), SetScreenVariable("selected_item", None)] xpos 1500 yalign 0.702 sensitive selected_item != player_config.current_gun

        textbutton _("Продать") activate_sound "audio/sfx/click.wav" action [Function(sell_item_immediately, selected_item), SetScreenVariable("selected_item", None)] xpos 1190 yalign 0.788 sensitive selected_item is not None and (player_config.town_type in ["City", "Village"])
        textbutton _("Удалить") activate_sound "audio/sfx/click.wav" action [Confirm("Вы действительно хотите удалить этот предмет?\nВНИМАНИЕ: Действие необратимо!", yes=Function(delete_item, selected_item), no=None), SetScreenVariable("selected_item", None)] xpos 1193 yalign 0.859 sensitive selected_item is not None and (player_config.town_type in ["City", "Village"])

        if selected_item:
            $ item_data = ItemDatabase[selected_item]

            if player_config.town_type in ["City", "Village"]:
                $ price = ItemPricesVillage.get(selected_item, 0) if player_config.town_type == "Village" else ItemPricesCity.get(selected_item, 0)
            else:
                $ price = 0
        
            frame:
                xpos 1170
                ypos 280
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

                if is_weapon(selected_item):
                    $ min_dmg, max_dmg = gun_stats.get(selected_item, (0, 0))
                    
                    if selected_item == player_config.current_gun:
                        text "[item_data['desc']]\n\nНаносимый урон: от [min_dmg] до [max_dmg] единиц\n\n{color=#247724}Данное оружие является текущим установленным.{/color}" size 25 color "#353535"
                    else:
                        text "[item_data['desc']]\n\nНаносимый урон: от [min_dmg] до [max_dmg] единиц" size 25 color "#353535"
                else:
                    text "[item_data['desc']]" size 25 color "#353535"

            frame:
                xpos 800
                ypos 702
                xsize 960
                ysize 300
                background None
                padding (20, 20)

                if price > 0:
                    text "Цена: [price] монет" size 30 color "#353535"

    imagebutton activate_sound "audio/sfx/click.wav":
        idle "gui/townmenu/buttons/tab_stats_e.png" 
        hover "gui/townmenu/buttons/tab_stats_s.png"
        action [Hide("Selling_Menu"), Show("statistics_screen")]
        xpos 356
        ypos 6
        focus_mask True 

    imagebutton:
        idle "gui/townmenu/buttons/tab_invent_s.png" 
        hover "gui/townmenu/buttons/tab_invent_s.png"
        action NullAction()
        xpos 1636
        ypos 6
        focus_mask True 

    if player_config.town_type in ["City"]:
        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/buttons/tab_weapon_e.png" 
            hover "gui/townmenu/buttons/tab_weapon_s.png"
            action [Hide("Selling_Menu"), Show("Gun_Shop_Menu")]
            xpos 1456
            ypos 7
            focus_mask True 

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/buttons/tab_truck_e.png" 
            hover "gui/townmenu/buttons/tab_truck_s.png"
            action [Hide("Selling_Menu"), Show("Car_Shop")]
            xpos 1276
            ypos 7
            focus_mask True

# Gun Shop

screen Gun_Shop_Menu():
    tag menu

    default selected_shop_item = None

    frame:
        style "menu_frame"
        background "gui/townmenu/backgunshop.png"
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
            action [Hide("Gun_Shop_Menu"), Show("InGameMenu")]
            xalign 0.99
            yalign 0.0
            focus_mask True 

        viewport:
            xpos 245
            ypos 280
            xsize 480
            ysize 660
            scrollbars "vertical"
            mousewheel True

            has vbox

            python:
                combined_weapons = dict(smallweapon_prices)
                if player_config.big_gun_install == "Possible":
                    combined_weapons.update(bigweapon_prices)

            grid 1 len(combined_weapons) spacing 20:

                for weapon_name, price in combined_weapons.items():

                    $ icon_path = f"gui/townmenu/items/{weapon_name}.png"

                    frame:
                        xsize 500
                        ysize 100
                        background None

                        button:
                            xsize 450
                            background None
                            action SetScreenVariable("selected_shop_item", weapon_name)
                            hover_background Solid("#50505031")
                            
                            hbox:
                                spacing 15
                                yalign 0.5

                                imagebutton:
                                    idle im.Scale(icon_path, 90, 90)
                                    hover im.Scale(icon_path, 90, 90)
                                    action NullAction()
                                    focus_mask True

                                vbox:
                                    spacing 5
                                    yalign 0.5
                                    xpos 20
                                    text "[gun_names.get(weapon_name, weapon_name)]" size 30 color "#353535"
                                    text "[price] монет" size 28 color "#353535"

        if selected_shop_item:
            $ item_data = GunDatabase[selected_shop_item]
            $ min_dmg, max_dmg = gun_stats.get(selected_shop_item, (0, 0))
            $ base_desc = item_data["desc"]
            $ full_desc = f"{base_desc}\n\nНаносимый урон: от {min_dmg} до {max_dmg} единиц"
        
            frame:
                xpos 1170
                ypos 280
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

                text full_desc size 25 color "#353535"

        textbutton _("Купить") xpos 1190 yalign 0.788 sensitive selected_shop_item is not None action Confirm(
            _("Вы уверены, что хотите купить это оружие?"),
            yes=Function(buy_weapon_with_old_handling, selected_shop_item),
            no=NullAction()
        )

        textbutton _("Купить как второе оружие") activate_sound "audio/sfx/click.wav" action NullAction() xpos 1045 yalign 0.86 sensitive selected_shop_item in bigweapon_prices

    imagebutton activate_sound "audio/sfx/click.wav":
        idle "gui/townmenu/buttons/tab_stats_e.png" 
        hover "gui/townmenu/buttons/tab_stats_s.png"
        action [Hide("Gun_Shop_Menu"), Show("statistics_screen")]
        xpos 356
        ypos 6
        focus_mask True 

    imagebutton activate_sound "audio/sfx/click.wav":
        idle "gui/townmenu/buttons/tab_invent_e.png" 
        hover "gui/townmenu/buttons/tab_invent_s.png"
        action [Hide("Gun_Shop_Menu"), Show("Selling_Menu")]
        xpos 1636
        ypos 6
        focus_mask True 

    imagebutton:
        idle "gui/townmenu/buttons/tab_weapon_s.png" 
        hover "gui/townmenu/buttons/tab_weapon_s.png"
        action NullAction()
        xpos 1456
        ypos 7
        focus_mask True

    if player_config.town_type == "City":
        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/buttons/tab_truck_e.png" 
            hover "gui/townmenu/buttons/tab_truck_s.png"
            action [Hide("Gun_Shop_Menu"), Show("Car_Shop")]
            xpos 1276
            ypos 7
            focus_mask True

# Car Shop

screen Car_Shop():
    tag menu

    frame:
        style "menu_frame"
        background "gui/townmenu/backmain.png"
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
            action [Hide("Car_Shop"), Show("InGameMenu")]
            xalign 0.99
            yalign 0.0
            focus_mask True 

        text "Work in progress..." size 60 xalign 0.5 yalign 0.5 color "#FFF"

    imagebutton activate_sound "audio/sfx/click.wav":
        idle "gui/townmenu/buttons/tab_stats_e.png" 
        hover "gui/townmenu/buttons/tab_stats_s.png"
        action [Hide("Car_Shop"), Show("statistics_screen")]
        xpos 356
        ypos 6
        focus_mask True 

    imagebutton activate_sound "audio/sfx/click.wav":
        idle "gui/townmenu/buttons/tab_invent_e.png" 
        hover "gui/townmenu/buttons/tab_invent_s.png"
        action [Hide("Car_Shop"), Show("Selling_Menu")]
        xpos 1636
        ypos 6
        focus_mask True 

    if player_config.town_type in ["City", "Village"]:
        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/buttons/tab_weapon_e.png" 
            hover "gui/townmenu/buttons/tab_weapon_s.png"
            action [Hide("Car_Shop"), Show("Gun_Shop_Menu")]
            xpos 1456
            ypos 7
            focus_mask True

    imagebutton:
        idle "gui/townmenu/buttons/tab_truck_s.png" 
        hover "gui/townmenu/buttons/tab_truck_s.png"
        action NullAction()
        xpos 1276
        ypos 7
        focus_mask True 
