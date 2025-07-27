screen name_input_screen():

    frame:
        style "name_input_frame"
        xalign 0.5
        yalign 0.5
        padding (40, 40)

        vbox:
            spacing 30
            xalign 0.5

            text "Введите ваше имя:" size 36 xalign 0.5 color "#404040"

            input value VariableInputValue("temp_name") length 14 pixel_width 500 align (0.5, 0.5):
                style "centered_input"

            textbutton "Подтвердить" activate_sound "audio/sfx/click.wav" action [
                SetVariable("player_name", temp_name.strip() or "Игрок"),
                Hide("name_input_screen"),
                Jump("tutorial_check")
            ] style "smaller_button" xalign 0.5

style name_input_frame is default:
    background Frame("gui/frame.png", 20, 20)
    xsize 600
    ysize 300

style centered_input is input:
    xalign 0.5
    textalign 0.5
    size 28
    color "#404040"
    background "#0008"
    padding (10, 10)

style smaller_button is button:
    size_group "name_button"
    xpadding 30
    ypadding 40
    color "#404040"

style smaller_button_text is button_text:
    size 22
    xalign 0.5
    textalign 0.5
    color "#404040"
    hover_color "#6d6d6d"