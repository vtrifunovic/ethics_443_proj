# ############################
# Linux Dictionaries
# ############################

lsd = {
    "bold"      : "\033[1;",
    "italics"   : "\033[3;",
    "underline" : "\033[4;",
    "blinking"  : "\033[5;",
    "invert"    : "\033[7;",
    "match"     : "\033[8;",
    "crossed"   : "\033[9;",
}

lcd = {
    "black"     : "30m",
    "red"       : "31m",
    "green"     : "32m",
    "yellow"    : "33m",
    "blue"      : "34m",
    "pink"      : "35m",
    "cyan"      : "36m",
    "white"     : "37m",
    "reset"     : "\033[0m"
}

lbd = {
    "black"     : "100m",
    "red"       : "101m",
    "green"     : "102m",
    "yellow"    : "103m",
    "blue"      : "104m",
    "pink"      : "105m",
    "cyan"      : "106m",
    "white"     : "107m",
}


def printc(text, fore="white", back=None, fore_style="bold", back_style="bold", end="\n", reset=True):
    if back:
        print(f"{lsd[fore_style]}{lcd[fore]}{lsd[back_style]}{lbd[back]}{text}", end="")
        if reset:
             print(lcd['reset'], end=end)
    else:
        print(f"{lsd[fore_style]}{lcd[fore]}{text}", end="")
        if reset:
             print(lcd['reset'], end=end)

if __name__ == "__main__":
    fore_colors = lcd.keys()
    fore_colors = [f for f in fore_colors if f != "reset"]
    back_colors = lbd.keys()
    fore_styles = lsd.keys()
    for i in fore_colors:
        for j in back_colors:
            for k in fore_styles:
                printc(f"{i}\t", fore=i, back=j, fore_style=k, end=" ", reset=False)
        print()
    printc("", reset=True, end="")