screen onebuttonpopup(message):
    modal True
    zorder 200
    
    frame:
        xalign 0.5
        yalign 0.5
        xpadding 50
        ypadding 40
        
        vbox:
            spacing 30
            xalign 0.5
            
            text message:
                size 36
                xalign 0.5
                text_align 0.5
                color "#ffffff"
            
            textbutton "OK":
                xalign 0.5
                action Return()
                style "confirm_button"