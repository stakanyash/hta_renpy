# Default's definitions

default shop_random_weapons = None
default shop_random_city = None

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
            text player_config.town_name xalign 0.5 yalign 0.5 size 28 color "#404040" font "fonts/ARIALBD.ttf"

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
                xpos 1230
                ypos 280
                xsize 500
                ysize 300
                background None
                padding (20, 20)

                text item_data["name"] size 40 color "#353535" xanchor 0.5 font "fonts/ARIALBD.ttf"

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

    on "show" action generate_random_weapons()

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
                combined_weapons = {}
                for w in shop_random_weapons:
                    if w in smallweapon_prices:
                        combined_weapons[w] = smallweapon_prices[w]
                    elif w in bigweapon_prices:
                        combined_weapons[w] = bigweapon_prices[w]

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
                                    text "[gun_names.get(weapon_name, weapon_name)]" size 30 color "#353535" font "fonts/ARIALBD.ttf"
                                    text "[price] монет" size 28 color "#353535"

        if selected_shop_item:
            $ item_data = GunDatabase[selected_shop_item]
            $ min_dmg, max_dmg = gun_stats.get(selected_shop_item, (0, 0))
            $ base_desc = item_data["desc"]
            $ full_desc = f"{base_desc}\n\nНаносимый урон: от {min_dmg} до {max_dmg} единиц"
        
            frame:
                xpos 1230
                ypos 280
                xsize 500
                ysize 300
                background None
                padding (20, 20)

                text item_data["name"] size 40 color "#353535" xanchor 0.5

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

        textbutton _("Купить как второе оружие (недоступно)") activate_sound "audio/sfx/click.wav" text_color "#808080" action NullAction() xpos 935 yalign 0.86 sensitive selected_shop_item in bigweapon_prices

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
    default selected_car = None
    default tooltip_text = ""
    default tooltip_pending_text = ""
    default tooltip_showing = False
    default mouse_pos = (0, 0)

    timer 0.02 repeat True action [
        SetScreenVariable("mouse_pos", renpy.get_mouse_pos()),
        If(tooltip_showing,
            SetScreenVariable("tooltip_text", tooltip_pending_text),
            SetScreenVariable("tooltip_text", "")
        )
    ]

    frame:
        background "gui/townmenu/carshop.png"
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

        text "Сравнение:" size 22 color "#404040" font "fonts/ARIALBD.ttf" xpos 1138 ypos 871

        imagebutton activate_sound "audio/sfx/click.wav":
            idle "gui/townmenu/close_e.png" 
            hover "gui/townmenu/close_h.png"
            action [Hide("Car_Shop"), Show("InGameMenu")]
            xalign 0.99
            yalign 0.0
            focus_mask True 

        if player_config.town_type == "City":
            viewport:
                xpos 115
                ypos 190
                xsize 550
                ysize 770
                scrollbars "vertical"
                mousewheel True

                vbox:
                    spacing 12

                    python:
                        car_requirements = {
                            "Van": "r1m1",
                            "Molokovoz": "r1m2",
                            "Ural": "r1m4"
                        }

                        available_cars = {}
                        for car_name, price in CarPrices.items():
                            if car_name in car_requirements:
                                required_region = car_requirements[car_name]
                                if player_config.region_allowed(required_region):
                                    available_cars[car_name] = price

                    for car_name, price in available_cars.items():
                        $ is_current = (player_config.car == car_name)

                        button:
                            xsize 440
                            background None
                            hover_background Solid("#4c4c4c40")
                            sensitive (player_config.town_type == "City")
                            action SetScreenVariable("selected_car", car_name)

                            vbox:
                                spacing 4
                                text car_names.get(car_name, car_name) size 28 color ("#007700" if is_current else "#333333") font "fonts/ARIALBD.ttf"
                                text "[price] монет" size 24 color "#555555"

        python:
            if player_config.hp < player_config.max_hp and player_config.car:
                hp_to_repair = player_config.max_hp - player_config.hp
                repair_cost = int(hp_to_repair * 0.75)
                can_repair = (player_config.money >= repair_cost)
            else:
                hp_to_repair = 0
                repair_cost = 0
                can_repair = False

            heals_needed = player_config.max_heals - player_config.heals
            price_per_heal = battle_heal_prices.get(player_config.car, 48)
            heal_cost = heals_needed * price_per_heal
            can_buy_heals = (player_config.money >= heal_cost and heals_needed > 0)

        fixed:
            xpos 793
            ypos 563
            xysize (217, 79)

            imagebutton auto "gui/townmenu/buttons/carshopbtn_%s.png":
                selected False
                sensitive (player_config.town_type == "City")
                action If(
                    selected_car and player_config.car != selected_car,
                    Confirm(
                        "Купить {name} за {cost} монет?".format(
                            name=car_names.get(selected_car, selected_car or ""),
                            cost=max(CarPrices.get(selected_car, 0) - CarSellPrices.get(player_config.car, 0), 0),
                        ),
                        yes=Function(buy_car_with_exchange, selected_car)
                    ),
                    NullAction()
                )
                activate_sound "audio/sfx/click.wav"
            text ("Купить" if player_config.town_type == "City" else ("{color=#960000}Купить{/color}")) xalign 0.5 yalign 0.46 size 28 color "#fed11b"

            fixed:
                ypos 185
                xysize (217, 79)
                imagebutton auto "gui/townmenu/buttons/carshopbtn_%s.png" sensitive can_repair:
                    hovered [ SetScreenVariable("tooltip_pending_text", "Починить машину (0.75 монет за 1 HP)"),
                                SetScreenVariable("tooltip_showing", True) ]
                    unhovered [ SetScreenVariable("tooltip_pending_text", ""),
                                SetScreenVariable("tooltip_showing", False),
                                SetScreenVariable("tooltip_text", "") ]
                    selected False
                    action If(can_repair,
                            Confirm("Починить машину?\n\nВосстановить: {0} HP\nСтоимость: {1} монет".format(hp_to_repair, repair_cost),
                                    yes=Function(repair_car)),
                            NullAction())
                    activate_sound "audio/sfx/click.wav"
                text ("[repair_cost]" if can_repair else ("{color=#960000}0{/color}" if hp_to_repair == 0 else "{color=#960000}[repair_cost]{/color}")) xalign 0.5 yalign 0.46 size 28 color "#fed11b"
            
            fixed:
                ypos 370
                xysize (217, 79)
                imagebutton auto "gui/townmenu/buttons/carshopbtn_%s.png" sensitive can_buy_heals:
                    hovered [ SetScreenVariable("tooltip_pending_text", "Пополнить запас лечения ([battle_heal_prices.get(player_config.car, 48)] монет за 1 лечение)"),
                                SetScreenVariable("tooltip_showing", True) ]
                    unhovered [ SetScreenVariable("tooltip_pending_text", ""),
                                SetScreenVariable("tooltip_showing", False),
                                SetScreenVariable("tooltip_text", "") ]
                    selected False
                    action If(can_buy_heals,
                            Confirm("Восстановить все лечения?\n\nКоличество: {0}\nСтоимость: {1} монет".format(heals_needed, heal_cost),
                                    yes=Function(buy_heals)),
                            NullAction())
                    activate_sound "audio/sfx/click.wav"

                text ("[heal_cost]" if can_buy_heals else ("{color=#960000}0{/color}" if heals_needed == 0 else "{color=#960000}[heal_cost]{/color}")) xalign 0.5 yalign 0.46 size 28 color "#fed11b"

        if selected_car:
            $ car_hp = CarHP.get(selected_car, 0)
            $ car_price = CarPrices.get(selected_car, 0)
            $ sell_price = CarSellPrices.get(player_config.car, 0)
            $ actual_cost = car_price - sell_price if player_config.car != selected_car else 0
            $ car_desc = car_descriptions.get(selected_car, "Описание отсутствует.")

            $ selected_max_hp = CarHP.get(selected_car, 0)
            $ selected_max_heals = CarMaxHeals.get(selected_car, 0)
            $ selected_heal_price = battle_heal_prices.get(selected_car, 0)
            
            $ current_max_hp = player_config.max_hp if player_config.car else 0
            $ current_max_heals = player_config.max_heals if player_config.car else 0
            $ current_heal_price = battle_heal_prices.get(player_config.car, 0) if player_config.car else 0
            
            $ hp_diff = selected_max_hp - current_max_hp
            $ heals_diff = selected_max_heals - current_max_heals
            $ heal_price_diff = selected_heal_price - current_heal_price

            text car_names.get(selected_car, selected_car):
                xpos 1480
                ypos 124
                xanchor 0.5
                size 26
                color "#353535"

            hbox:
                spacing 260
                vbox:
                    xpos 1065
                    ypos 768
                    spacing 20
                    text "Макс. HP:" size 20 color "#353535" font "fonts/ARIALBD.ttf"
                    text "Цена:" size 20 color "#353535" font "fonts/ARIALBD.ttf"

                vbox:
                    xpos 991
                    ypos 768
                    xanchor 0.5
                    xsize 100
                    text "[car_hp]" size 20 color "#353535"

                python:
                    price_str = str(car_price)
                    price_len = len(price_str)

                    if price_len == 3:
                        price_x = 632
                    elif price_len == 4:
                        price_x = 632
                    elif price_len >= 5:
                        price_x = 622
                    else:
                        price_x = 632

                vbox:
                    xpos price_x
                    ypos 812
                    xanchor 0.5
                    xsize 100
                    text "[car_price]" size 20 color "#353535"

            add f"{selected_car}_slideshow" xpos 1480 ypos 450 xanchor 0.5 yanchor 0.5

            if player_config.car:
                vbox:
                    xpos 1060
                    ypos 915
                    spacing 18.5
                    
                    hbox:
                        spacing 5
                        text "Макс. HP: " size 18 color "#404040" font "fonts/ARIALBD.ttf" xsize 180 textalign 1.0
                        if hp_diff > 0:
                            text "[current_max_hp] → {color=#007700}[selected_max_hp]{/color}" size 20 color "#404040" ypos -3
                        elif hp_diff < 0:
                            text "[current_max_hp] → {color=#960000}[selected_max_hp]{/color}" size 20 color "#404040" ypos -3
                        else:
                            text "[current_max_hp] → [selected_max_hp]" size 20 color "#404040" ypos -3
                    
                    hbox:
                        spacing 5
                        text "Макс. лечений: " size 18 color "#404040" font "fonts/ARIALBD.ttf" xsize 180 textalign 1.0
                        if heals_diff > 0:
                            text "[current_max_heals] → {color=#007700}[selected_max_heals]{/color}" size 20 color "#404040" ypos -3
                        elif heals_diff < 0:
                            text "[current_max_heals] → {color=#960000}[selected_max_heals]{/color}" size 20 color "#404040" ypos -3
                        else:
                            text "[current_max_heals] → [selected_max_heals]" size 20 color "#404040" ypos -3
                    
                    hbox:
                        spacing 5
                        text "Цена покупки лечения: " size 16 color "#404040" font "fonts/ARIALBD.ttf" xsize 200 textalign 1.0
                        if heal_price_diff > 0:
                            text "[current_heal_price] → {color=#960000}[selected_heal_price]{/color}" size 20 color "#404040" ypos -3
                        elif heal_price_diff < 0:
                            text "[current_heal_price] → {color=#007700}[selected_heal_price]{/color}" size 20 color "#404040" ypos -3
                        else:
                            text "[current_heal_price] → [selected_heal_price]" size 20 color "#404040" ypos -3

            vbox:
                xsize 495
                ysize 270
                xalign 0.98
                yalign 0.96

                frame:
                    background None
                    xsize 495
                    ysize 270
                    text "[car_desc]" style "cardesc"

    fixed:
        xpos 792
        ypos 200

        hbox:
            xalign 0.0134
            yalign 0.0145
            for digit_img in get_hp_digit_images(player_config.hp):
                add digit_img

        hbox:
            xalign 0.037
            yalign 0.034
            if player_config.hp <= 0:
                add get_lowhealincs()
            elif "redlight_hp.png" in get_lowhealincs():
                add get_lowhealincs() at blinking
            else:
                add get_lowhealincs()

    fixed:
        hbox:
            xalign 0.467
            yalign 0.384
            if player_config.heals <= 0:
                add get_lowhealamountincs()
            elif "redlight_fuel.png" in get_lowhealamountincs():
                add get_lowhealamountincs() at blinking
            else:
                add get_lowhealamountincs()

        hbox:
            xalign 0.483
            yalign 0.357
            for healing in get_heal_digit_images(player_config.heals):
                add healing

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

    if player_config.town_type == "City":
        imagebutton:
            idle "gui/townmenu/buttons/tab_weapon_e.png" 
            hover "gui/townmenu/buttons/tab_weapon_s.png"
            action [Hide("Car_Shop"), Show("Gun_Shop_Menu")]
            xpos 1456
            ypos 7
            focus_mask True

    imagebutton activate_sound "audio/sfx/click.wav":
        idle "gui/townmenu/buttons/tab_truck_s.png" 
        hover "gui/townmenu/buttons/tab_truck_s.png"
        action NullAction()
        xpos 1276
        ypos 7
        focus_mask True

    if tooltip_text:
        frame:
            background Solid("#000C")
            padding (10, 6)
            text tooltip_text size 20 color "#fff"
            xpos mouse_pos[0] + 15
            ypos mouse_pos[1] + 15
            xanchor 0.0
            yanchor 0.0

style cardesc:
    xmaximum 495
    color "#404040"
    size 18