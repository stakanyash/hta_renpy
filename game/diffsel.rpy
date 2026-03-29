screen difficulty_select():
    zorder 100
    modal True

    default selected_diff = "normal"
    default diff_label = "Бывалый"
    default show_dropdown = False

    add "#0000007e"
    add "gui/overlay/diffsel.png"

    frame:
        style_prefix "menu"
        xalign 0.5
        yalign 0.505
        padding (30, 30)
        xsize 400
        background None

        vbox:
            spacing 20
            xalign 0.5

            text "Уровень сложности" xalign 0.5 size 20 color "#404040"

            null height 10

            frame:
                xsize 340
                ysize 45
                xalign 0.5
                background Solid("#abb2b2")

                hbox:
                    xfill True
                    text "[diff_label]" xoffset 10 size 24 color "#404040"
                    textbutton "▼" activate_sound "audio/sfx/click.wav" xalign 1.0 yoffset -10 action SetScreenVariable("show_dropdown", not show_dropdown)

            null height 10
            
            hbox:
                xalign 0.5
                spacing 50
                yoffset -3

                textbutton "Выбрать" activate_sound "audio/sfx/click.wav" style "diff_button" action [
                    SetVariable("difficulty", selected_diff),
                    SetVariable("difficulty_base_multiplier", {"easy": 0.02, "normal": 0.03, "hard": 0.04, "expert": 0.055}[selected_diff]),
                    Function(profile_save_difficulty, selected_diff, {"easy": 0.02, "normal": 0.03, "hard": 0.04, "expert": 0.055}[selected_diff]),
                    Start()
                ]

                textbutton "Вернуться" activate_sound "audio/sfx/click.wav" style "diff_button" action Hide("difficulty_select")

    if show_dropdown:
        button:
            style "empty"
            xfill True
            yfill True
            action SetScreenVariable("show_dropdown", False)

        frame:
            xalign 0.5
            yalign 0.5
            yoffset -30
            xsize 340
            background Solid("#abb2b2")

            vbox:
                spacing 0
                textbutton "Новичок" activate_sound "audio/sfx/click.wav" style "diff_button" action [
                    SetScreenVariable("selected_diff", "easy"),
                    SetScreenVariable("diff_label", "Новичок"),
                    SetScreenVariable("show_dropdown", False)
                ]
                textbutton "Бывалый" activate_sound "audio/sfx/click.wav" style "diff_button" action [
                    SetScreenVariable("selected_diff", "normal"),
                    SetScreenVariable("diff_label", "Бывалый"),
                    SetScreenVariable("show_dropdown", False)
                ]
                textbutton "Профессионал" activate_sound "audio/sfx/click.wav" style "diff_button" action [
                    SetScreenVariable("selected_diff", "hard"),
                    SetScreenVariable("diff_label", "Профессионал"),
                    SetScreenVariable("show_dropdown", False)
                ]
                textbutton "Мастер" activate_sound "audio/sfx/click.wav" style "diff_button" action [
                    SetScreenVariable("selected_diff", "expert"),
                    SetScreenVariable("diff_label", "Мастер"),
                    SetScreenVariable("show_dropdown", False)
                ]

style diff_button_text is default:
    color "#404040"
    hover_color "#ffcc00"
    selected_color "#404040"
    selected_hover_color "#ffcc00"
    size 24