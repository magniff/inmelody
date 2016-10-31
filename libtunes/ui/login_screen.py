import urwid


LOGO = """
▄█    ▄       █▀▄▀█ ▄███▄   █    ████▄ ██▄ ▀▄    ▄ 
██     █      █ █ █ █▀   ▀  █    █   █ █  █  █  █  
██ ██   █     █ ▄ █ ██▄▄    █    █   █ █   █  ▀█   
▐█ █ █  █     █   █ █▄   ▄▀ ███▄ ▀████ █  █   █    
 ▐ █  █ █        █  ▀███▀       ▀      ███▀ ▄▀     
   █   ██       ▀                                  
"""


logo_widget = urwid.Padding(urwid.Text(LOGO), align='center', width=51)

