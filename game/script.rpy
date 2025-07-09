default temp_name = ""
default player_name = "Вы"

init python:
    renpy.music.register_channel("sfx2", mixer="sfx", loop=True, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("shoot", mixer="sfx", loop=False, stop_on_mute=True, tight=False, file_prefix="", file_suffix="")
    renpy.music.register_channel("damage", mixer="sfx", loop=False, stop_on_mute=False, tight=False, file_prefix="", file_suffix="")

transform stretch_in:
    yzoom 0.95
    linear 0.1 yzoom 1.0

label start:

    $ player_name = "Вы"

    call screen name_input_screen

label titles:

    $ renpy.movie_cutscene("movies/titles.mp4")

    return