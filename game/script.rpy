default temp_name = ""
default player_name = "Вы"

label start:

    $ player_name = "Вы"

    call screen name_input_screen

label titles:

    $ renpy.movie_cutscene("movies/titles.mp4")

    return