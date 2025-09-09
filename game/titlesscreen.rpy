label splashscreen:
    init python:
        import os

        def license_accepted_exists():
            return os.path.exists("license_accepted.flag")

        def create_license_flag():
            with open("license_accepted.flag", "w", encoding="utf-8") as f:
                f.write("License accepted by user.")

    if not license_accepted_exists():
        $ renpy.call_screen("license_prompt")
        $ create_license_flag()

    $ renpy.movie_cutscene("movies/disclaimer.mp4")

    return
