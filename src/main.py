################################################################
# Warcaby: "/src/main.py"
################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from Checkers import Checkers
from TkinterUi import TkinterUi
from ConsoleUi import ConsoleUi


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if '__main__' == __name__:

    x = '-' * 64

    print(x, 'Witaj w grze WARCABY!', x, sep = '\n')

    checkers = Checkers()

    print(x, 'Wypróbuj interfejs \"Tkinter\" :)', x, sep = '\n')

    ui = TkinterUi(checkers)
    ui.enable(True)

    print(x, 'Wypróbuj interfejs \"Console\" :)', x, sep = '\n')

    ui = ConsoleUi(checkers)
    ui.enable(True)

    print(x, 'Dziękuję za grę!', x, sep = '\n')


################################################################
