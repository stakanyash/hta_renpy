init python:
    import os, json, random

    FLAGS_FILE = "hta.json"

    def load_flags():
        if os.path.exists(FLAGS_FILE):
            try:
                with open(FLAGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return {"license": False, "tutorial": False}

    def save_flags(flags):
        with open(FLAGS_FILE, "w", encoding="utf-8") as f:
            json.dump(flags, f)

    slide_count = 6
    total_time = random.uniform(3.0, 7.0)

    weights = [random.random() for _ in range(slide_count)]
    weight_sum = sum(weights)

    pauses = [total_time * w / weight_sum for w in weights]

    disclaimer_text = ""
    try:
        with open("game/docs/DISCLAIMER.md", "r", encoding="utf-8") as f:
            disclaimer_text = f.read()
    except Exception as e:
        disclaimer_text = (
            "Ошибка при открытии файла docs/DISCLAIMER.md, либо файл отсутствует!\n\n"
            "{a=https://github.com/stakanyash/hta_renpy/blob/main/DISCLAIMER.md}Текст дисклеймера доступен тут{/a}"
        )

screen license_prompt():
    tag menu
    modal True

    add Solid("#000000", alpha=0.7) at fadeinout

    frame at fadeinout:
        xalign 0.5
        yalign 0.5
        xsize 900
        ysize 500
        padding (30,30,30,30)
        background Solid("#1a1a1a")

        vbox:
            spacing 20
            xfill True
            yfill True

            null height 20

            text "Для использования требуется лицензия на оригинальную игру Hard Truck Apocalypse/Ex Machina. Нажимая «Принимаю», Вы подтверждаете, что у Вас есть такая лицензия." at fadeinout:
                size 25
                color "#ffffff"
                line_spacing 5
                text_align 0.5
                xalign 0.5

            null

            textbutton "Принимаю" action Return(True) at fadeinout:
                xalign 0.5
                xminimum 220
                yminimum 60
                background Solid("#3a753a")
                hover_background Solid("#4a954a")
                text_style "button_text_center"

            textbutton "Дисклеймер" at fadeinout:
                xalign 0.5
                xminimum 250
                yminimum 60
                background Solid("#2a2a2a")
                hover_background Solid("#444444")
                text_style "button_text_center"
                action [Hide("license_prompt"), Show("disclaimer_screen")]

screen disclaimer_screen():
    tag menu
    modal True
    frame at fadeinout:
        xalign 0.5
        yalign 0.5
        padding (30, 30, 30, 30)
        background Solid("#1a1a1a")
        xsize 1000
        ysize 890
        vbox:
            spacing 25
            xsize 950
            ysize 840

            text "Дисклеймер" at fadeinout size 44 xalign 0.5 color "#FFFFFF"

            viewport:
                id "vp"
                draggable True
                mousewheel True
                xsize 950
                ysize 650
                vbox:
                    xalign 0.5
                    spacing 12
                    text "[disclaimer_text]" at fadeinout size 24 color "#FFFFFF" xsize 900

            hbox:
                spacing 100
                xalign 0.5
                yalign 0.95
                textbutton "Принять" at fadeinout:
                    xminimum 250
                    yminimum 60
                    background Solid("#3a753a")
                    hover_background Solid("#4a954a")
                    text_style "button_text_center"
                    action Return()

                textbutton "Отказаться" at fadeinout:
                    xminimum 250
                    yminimum 60
                    background Solid("#b70000")
                    hover_background Solid("#d30101")
                    text_style "button_text_center"
                    action Quit()

label splashscreen:
    $ flags = load_flags()

    if not flags["license"]:
        $ renpy.call_screen("license_prompt")
        $ flags["license"] = True
        $ save_flags(flags)

    $ renpy.movie_cutscene("movies/disclaimer.avi")

    pause 0.5

    $ slides = ["loading_1", "loading_2", "loading_3", "loading_4", "loading_5", "loading_6"]
    python:
        for i in range(len(slides)):
            renpy.show(slides[i])
            renpy.pause(pauses[i], hard=True)
            renpy.hide(slides[i])

    return