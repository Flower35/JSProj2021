################################################################
# Warcaby: "main.py"
################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from Checkers import Checkers
from TkinterUi import TkinterUi


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if '__main__' == __name__:

    x = '-' * 64

    print(x, 'Witamy w grze WARCABY!', x, sep = '\n')

    checkers = Checkers()

    ui = TkinterUi(checkers)

    ui.enable(True)

    print(x, 'Do widzenia!', x, sep = '\n')


################################################################
