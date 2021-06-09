################################################################
# Warcaby: "/src/StrongPawn.py"
################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from WeakPawn import WeakPawn


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class StrongPawn(WeakPawn):
    """
    Pionek-Damka w grze "Warcaby".
    """


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def pawnStr(self) -> str:
        """
        Tekstowa reprezentacja rodzaju pionka.
        """

        return 'd'


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def canMoveInDirection(self, direction: int) -> bool:
        """Patrz: `Abstractpawn.canMoveInDirection`."""

        return True


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def canTakeMultipleSteps(self) -> bool:
        """Patrz: `AbstractPawn.canTakeMultipleSteps`."""

        return True


################################################################
