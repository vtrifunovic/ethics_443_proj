# ############################
# Linux Dictionaries
# ############################

lsd = {
    "bold"      : "\033[1;",
    "dim"       : "\033[2;",
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
    "black"     : "\033[1;100m",
    "red"       : "\033[1;101m",
    "green"     : "\033[1;102m",
    "yellow"    : "\033[1;103m",
    "blue"      : "\033[1;104m",
    "pink"      : "\033[1;105m",
    "cyan"      : "\033[1;106m",
    "white"     : "\033[1;107m",
}


def printc(text, fore="white", back=None, style="bold", end="\n", reset=True):
    if back:
        print(f"{lsd[style]}{lcd[fore]}{lbd[back]}{text}", end="")
        if reset:
             print(lcd['reset'], end=end)
    else:
        print(f"{lsd[style]}{lcd[fore]}{text}", end="")
        if reset:
             print(lcd['reset'], end=end)

if __name__ == "__main__":
    fore_colors = lcd.keys()
    fore_colors = [f for f in fore_colors if f != "reset"]
    back_colors = lbd.keys()
    styles = lsd.keys()
    for j in back_colors:
        for i in fore_colors:
            for k in styles:
                printc(f"{i+" "+k:<16}", fore=i, back=j, style=k, end=" ", reset=True)
            print()
    printc("", reset=True, end="")