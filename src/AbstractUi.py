################################################################
# Warcaby: "AbstractUi.py"
################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from Checkers import Checkers


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class AbstractUi():
    """
    Abstrakcyjny intefejs użytkownika do gry "Warcaby".
    """


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __init__(self, checkers: Checkers) -> None:
        """
        Inicjalizacja klasy `AbstractUi`.
        ----
        checkers -- instancja Warcabów obsługiwana przez nowy interfejs.
        """

        self.checkers = checkers


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def enable(self, state: bool) -> None:
        """
        Pokazanie lub wyłączenie interfejsu.
        Interfejs jest domyślnie WYŁĄCZONY.
        ----
        state -- czy należy pokazać interfejs.
        """

        pass


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def updateBoard(self, checkers: Checkers) -> None:
        """
        Aktualizacja wyświetlanej planszy
        na podstawie aktualnego stanu gry.
        ----
        checkers -- instancja Warcabów.
        """

        pass


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def drawBoard(self) -> None:
        """
        Narysowanie planszy.
        """

        pass


################################################################
