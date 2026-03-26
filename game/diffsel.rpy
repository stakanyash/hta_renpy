screen difficulty_select():
    zorder 100
    modal True

    add "#0000007e"

    frame:
        style_prefix "menu"
        xalign 0.5
        yalign 0.5
        padding (30, 30)
        xsize 800
        ysize 550

        vbox:
            spacing 10
            xalign 0.5
            yalign 0.5

            text "Выберите уровень сложности:" xalign 0.5 size 40

            null height 20

            textbutton "Новичок" activate_sound "audio/sfx/click.wav" xalign 0.5 style "diff_button" action [
                SetVariable("difficulty", "easy"),
                SetVariable("difficulty_base_multiplier", 0.02),
                Function(profile_save_difficulty, "easy", 0.02),
                Start()
            ]
            textbutton "Бывалый" activate_sound "audio/sfx/click.wav" xalign 0.5 style "diff_button" action [
                SetVariable("difficulty", "normal"),
                SetVariable("difficulty_base_multiplier", 0.03),
                Function(profile_save_difficulty, "normal", 0.03),
                Start()
            ]
            textbutton "Профессионал" activate_sound "audio/sfx/click.wav" xalign 0.5 style "diff_button" action [
                SetVariable("difficulty", "hard"),
                SetVariable("difficulty_base_multiplier", 0.04),
                Function(profile_save_difficulty, "hard", 0.04),
                Start()
            ]
            textbutton "Мастер" activate_sound "audio/sfx/click.wav" xalign 0.5 style "diff_button" action [
                SetVariable("difficulty", "expert"),
                SetVariable("difficulty_base_multiplier", 0.055),
                Function(profile_save_difficulty, "expert", 0.055),
                Start()
            ]

            null height 20
            null height 20

            textbutton "Вернуться" activate_sound "audio/sfx/click.wav" xalign 0.5 style "diff_button_back" action Hide("difficulty_select")

style diff_button_text is default:
    color "#404040"
    hover_color "#ffcc00"
    selected_color "#404040"
    selected_hover_color "#ffcc00"

style diff_button_back is diff_button

style diff_button_back_text is diff_button_text:
    size 20
