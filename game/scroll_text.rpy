transform scroll_up(duration=15.0, end_ypos=-1500):
    ypos 1080
    linear duration ypos end_ypos

screen crawl_text(text_content, sound_file=None, back_music=None, duration=15.0, scroll_speed=50):
    $ end_ypos = -(int(scroll_speed * duration))

    on "show" action SetField(store, "default_mouse", "empty")
    on "hide" action [
        SetField(store, "default_mouse", "default"),
        Function(renpy.sound.stop, channel="crawl_voice")
    ]

    add Solid("#000000")

    frame:
        background None
        xalign 0.5

        text text_content at scroll_up(duration, end_ypos):
            size 22
            color "#ffffff"
            text_align 0.5
            xalign 0.5
            xsize 1400

    add "gui/crawl_fade.png"

    timer duration action Return()

    key "K_SPACE" action Return()

    if sound_file:
        timer 0.5 action Function(renpy.sound.play, sound_file, channel="crawl_voice")
    
    if back_music:
        timer 0.5 action Function(renpy.sound.play, back_music, channel="music", loop=True)