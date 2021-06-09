################################################################
# Warcaby: "/src/AbstractPawn.py"
################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from typing import Tuple


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class AbstractPawn():
    """
    Abstrakcyjny pionek w grze "Warcaby".
    """

    STATE_STANDBY = 0
    STATE_SELECTED = 1
    STATE_GONE = 2
    STATE_MARKED = 3


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __init__(self) -> None:
        """
        Inicjalizacja klasy `AbstractPawn`.
        """

        self._state = self.STATE_MARKED


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __str__(self) -> str:
        """
        Tekstowa reprezentacja pionka.
        ----
        Pionek abstrakcyjny używany jest do wskazywania
        miejsc wielokrotnego bicia damkami.
        """

        return 'x'


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def getPlayer(self) -> int:
        """
        Zwraca numer gracza będącego właścicielem pionka.
        """

        return (-1)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def isRedundant(self) -> bool:
        """
        Czy dany pionek powinien być usunięty z planszy?
        """

        return (self.STATE_GONE == self._state) \
            or (self.STATE_MARKED == self._state)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def getState(self) -> int:
        """
        Sprawdza stan danego pionka.
        """

        return self._state


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def setState(self, state: int) -> int:
        """
        Ustawia nowy stan danego pionka.
        ----
         * `state`: jedna ze stałych wartości
          zdefiniowanych w klasie `AbstractPawn`.
        """

        self._state = state


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def canMoveInDirection(self, direction: int) -> bool:
        """
        Czy pionek może przesuwać się w danym kierunku,
        nie uwzględniając bicia?
        ----
         * `direction`: 0 na północ, 1 na południe.
        """

        return False


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def canTakeMultipleSteps(self) -> bool:
        """
        Czy pionek może przesuwać się o więcej niż jedno pole?
        """

        return False


################################################################
