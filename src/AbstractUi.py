################################################################
# Warcaby: "/src/AbstractUi.py"
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
         * `checkers`: instancja Warcabów obsługiwana przez nowy interfejs.
        """

        # Pole "protected", nie "private":
        # umożliwienie bezpośrednieg dostępu do pola w klasach dzieczących.

        self._checkers = checkers


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def enable(self, state: bool) -> None:
        """
        Pokazanie lub wyłączenie interfejsu.
        Interfejs jest domyślnie WYŁĄCZONY.
        ----
         * `state`: czy należy pokazać interfejs.
        """

        pass


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def updateBoard(self) -> None:
        """
        Aktualizacja wyświetlanej planszy
        na podstawie aktualnego stanu gry.
        """

        pass


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def drawBoard(self) -> None:
        """
        Narysowanie planszy.
        """

        pass


################################################################
