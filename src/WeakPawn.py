################################################################
# Warcaby: "WeakPawn.py"
################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from AbstractPawn import AbstractPawn


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class WeakPawn(AbstractPawn):
    """
    Zwykły pionek w grze "Warcaby".
    """


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __init__(self, player: int) -> None:
        """
        Inicjalizacja klasy `WeakPawn`.
        ----
         * `player`: numer gracza (0 lub 1).
          Określa też dozwolony kierunek ruchu pionka.
        """

        self._state = self.STATE_STANDBY

        self._player = player


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def playerStr(self) -> str:
        """
        Tekstowa reprezentacja właściciela pionka.
        ----
        Zwraca `C` (CZARNE) dla gracza o indeksie `0` (gracza pierwszego)
        lub 'B' (BIAŁE) dla gracza o indeksie `1` (gracza drugiego).
        """

        return 'C' if 0 == self._player else 'B'


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def pawnStr(self) -> str:
        """
        Tekstowa reprezentacja rodzaju pionka.
        """

        return ''


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __repr__(self) -> str:
        return f'PAWN({self._player})'


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __str__(self) -> str:
        """
        Tekstowa reprezentacja pionka.
        ----
        Jeśli pionek jest zaznaczony, to zwracany tekst
        jest objęty w nawiasy kwadratowe.
        """

        t = self.playerStr() + self.pawnStr()

        if self.STATE_SELECTED == self._state:
            t = '[' + t + ']'

        return t


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def getPlayer(self) -> int:
        """Patrz: `AbstracPawn.getPlayer`."""

        return self._player


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def canMoveInDirection(self, direction: int) -> bool:
        """Patrz: `AbstractPawn.canMoveInDirection`."""

        return direction == self._player


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    pass


################################################################
