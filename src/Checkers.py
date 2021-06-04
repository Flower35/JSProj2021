################################################################
# Warcaby: "Checkers.py"
################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from typing import List, Tuple

from AbstractPawn import AbstractPawn
from WeakPawn import WeakPawn
from StrongPawn import StrongPawn


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class Checkers():
    """
    Główna klasa gry "Warcaby".
    """

    BOARD_SIZE = 8

    GAMESTATE_TAKE = 0
    GAMESTATE_PUT  = 1
    GAMESTATE_END  = 2

    TURNINFO_NOTHING      = 0
    TURNINFO_CANCELLED    = 1
    TURNINFO_OBLIG_FIGHT  = 2
    TURNINFO_FIGHT_AGAIN  = 3
    TURNINFO_WRONG_PLAYER = 4
    TURNINFO_INVALID_MOVE = 5

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __init__(self) -> None:
        """
        Inicjalizacja klasy `Checkers`.
        """

        # Pusta plansza

        self._board = [
            [None] * self.BOARD_SIZE
            for _ in range(self.BOARD_SIZE)
        ]

        # Stan rozgrywki

        self._state = self.GAMESTATE_END

        # Informacja o danej turze

        self._turninfo = self.TURNINFO_NOTHING

        # Tura którego gracza?

        self._player = (-1)

        # Pionki sprawdzane co każdą turę

        self._selectedPawnPos = None
        self._fightingPawnPos = None
        self._multiFightPawn = None
        self._obligatoryPawns = []


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def newGame(self) -> None:
        """
        Przygotowanie nowej gry.
        Ułożenie pionków na planszy, ustawienie tury gracza pierwszego.
        """

        half = self.BOARD_SIZE // 2

        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                self._board[y][x] = WeakPawn(int(y < half)) \
                    if ((x & 1) ^ (y & 1)) \
                    and ((y < (half - 1)) or (y > half)) \
                    else None

        self._state = self.GAMESTATE_TAKE
        self._turninfo = self.TURNINFO_NOTHING

        self._player = 0

        self._obligatoryPawns = []


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def getTextBoard(self) -> List[List[str]]:
        """
        Zwrócenie tekstowej reprezentacji planszy.
        """

        return [
            [
                '' if self._board[y][x] is None else str(self._board[y][x])
                for x in range(self.BOARD_SIZE)
            ]
            for y in range(self.BOARD_SIZE)
        ]


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def _playerName(self) -> str:
        """
        Zwraca tekstową nazwę gracza (numer oraz kolor pionków).
        """

        colors = ['CZARN', 'BIAŁ']

        return f'{1 + self._player} ({colors[self._player]}E)'


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def getTextState(self) -> str:
        """
        Zwrócenie tekstowego komunikatu o aktualnym stanie gry.
        """

        def checkPreviusTurnInfo() -> str:

            if self.TURNINFO_NOTHING != self._turninfo:

                if self.TURNINFO_WRONG_PLAYER == self._turninfo:
                    return 'To nie jest twój pionek!'

                if self.TURNINFO_INVALID_MOVE == self._turninfo:
                    return 'Ruch niedozwolony!'

                if self.TURNINFO_FIGHT_AGAIN == self._turninfo:
                    return 'Możesz bić dalej. Wskaż kolejne pole:'

                if self.TURNINFO_OBLIG_FIGHT == self._turninfo:
                    return 'Nie! Masz przynajmniej jedno obowiązkowe bicie.'

                return None

        t = checkPreviusTurnInfo()
        self._turninfo = self.TURNINFO_NOTHING
        if t is not None:
            return t

        if self.GAMESTATE_END == self._state:
            return f'Gra skończona. Wygrał gracz {self._playerName()}.'

        if self.GAMESTATE_TAKE == self._state:
            return f'Tura gracza {self._playerName()}.'

        if self.GAMESTATE_PUT == self._state:
            return f'Wskaż, gdzie chcesz postawić pionka:'


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def getDiagonalPawns(self, direction: int, bx: int, by: int) \
    -> Tuple[List[AbstractPawn]]:
        """
        Zwraca przekątne listy pionków w czterech kierunkach
        (NW, NE, SW, SE) od dowolnej pozycji na planszy.
        ----
         * `direction`: Ograniczenie do wyłącznie jednego kierunku.
          (0 = NW, 1 = NE, 2 = SW, 3 = SE)
         * `bx`, `by`: pozycje względem których wybierane są przekątne.
        """

        colBorder = [
            lambda x: x >= 0,
            lambda x: x < self.BOARD_SIZE
        ]

        rowBorder = [
            lambda y: y >= 0,
            lambda y: y < self.BOARD_SIZE
        ]

        def grabPawns(x_dir: int, y_dir: int) -> List[AbstractPawn]:
            result = []
            x, y = bx, by
            x_step = (-1) if 0 == x_dir else (+1)
            y_step = (-1) if 0 == y_dir else (+1)

            x += x_step
            y += y_step
            while colBorder[x_dir](x) and colBorder[y_dir](y):
                result.append(self._board[y][x])
                x += x_step
                y += y_step

            return result

        if (direction >= 0) and (direction < 4):
            return grabPawns((direction & 1), ((direction >> 1) & 1))

        # Kierunek: Północny-Zachód (North-West)
        nw = grabPawns(0, 0)

        # Kierunek: Północny-Wschód (North-East)
        ne = grabPawns(1, 0)

        # Kierunek: Południowy-Zachód (South-West)
        sw = grabPawns(0, 1)

        # Kierunek: Południowy-Wschód (South-East)
        se = grabPawns(1, 1)

        return nw, ne, sw, se


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def canPawnFight(self, pawn: AbstractPawn, sx: int, sy: int) -> bool:
        """
        Czy pionek na danej pozycji może wykonać jakieś bicie?
        ----
         * `pawn`: sprawdzany pionek źródłowy.
         * `sx`, `sy`: pozycja, z której pionek dalej bije.
        """

        diagonals = list(self.getDiagonalPawns((-1), sx, sy))

        if not pawn.canTakeMultipleSteps():
            for i, d in enumerate(diagonals):
                diagonals[i] = d[:2]

        player = pawn.getPlayer()

        def checkDiagonal(d: List[AbstractPawn]) -> bool:
            enemySpotted = False
            for x in d:
                if x is None:
                    if enemySpotted:
                        return True
                else:
                    if (not x.isRedundant()) and (x.getPlayer() != player):
                        enemySpotted = True
                    else:
                        return False
            return False

        for d in diagonals:
            if checkDiagonal(d):
                return True

        return False


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def validateSelectedPawnMove(self, \
    sx: int, sy: int, dx: int, dy: int) -> Tuple[int, int]:
        """
        Sprawdzenie poprawności ruchu od zaznaczonego pionka.
        Zwraca liczbę przeskoczonych pól i liczbę zbitych pionków
        oraz oznacza przeskoczone pionki przeciwnika jako pionki do usunięcia.
        ----
         * `sx`, `sy`: pozycja startowa.
         * `dx`, `dy`: wskazana kolumna i wskazany wiersz.
        """

        x_step, y_step = (dx - sx), (dy - sy)

        # Anuluj, jeśli ruch nie jest po przekątnej
        if abs(x_step) != abs(y_step):
            return (0, 0)

        # Sprawdź kierunek ruchu (NW = 0, NE = 1, SW = 2, SE = 3)
        direction = (int(y_step > 0) << 1) | int(x_step > 0)

        # Skopiuj wszystkie pionki z danej przekątnej
        diagonal = self.getDiagonalPawns(direction, sx, sy)

        # Indeks pola na przekątnej po wykonaniu ruchu przez pionka
        d_step = abs(x_step) - 1

        # Czy pionek może poruszać się o więcej niż jedno pole?
        if d_step > 0:
            if not self._multiFightPawn.canTakeMultipleSteps():
                if (d_step > 1) or (diagonal[0] is None):
                    return (0, 0)

        player = self._multiFightPawn.getPlayer()

        # Czy pionek próbuje przeskoczyć pionka swojego gracza?
        for i in range((d_step - 1), (-1), (-1)):
            if (diagonal[i] is not None) \
            and (diagonal[i].getPlayer() == player):
                return (0, 0)

        # Oznacz wszystkie pionki na drodze jako martwe
        defeated_pawns = 0
        for i in range(0, d_step):
            if diagonal[i] is not None:
                diagonal[i].setState(AbstractPawn.STATE_GONE)
                defeated_pawns += 1

        # Jeżeli nie zbito żadnego pionka, to czy zaznaczony
        # pionek może poruszać się w danym kierunku (północ-południe)?
        if (defeated_pawns <= 0) \
        and (not self._multiFightPawn.canMoveInDirection(direction >> 1)):
            return (0, 0)

        return ((d_step + 1), defeated_pawns)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def removeMarkedPawns(self) -> None:
        """
        Usunięcie wszystkich nieprawdziwych pionków po skończonym biciu.
        """

        for y in range(len(self._board)):
            for x, pawn in enumerate(self._board[y]):
                if pawn is not None:
                    if pawn.isRedundant():
                        self._board[y][x] = None


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def resetMarkedPawns(self) -> None:
        """
        Zresetowanie pionków, które nie są w stanie bezczynności.
        Dodatkowo następuje usunięcie pozycji wielokrotnego bicia.
        """

        for row in self._board:
            for pawn in row:
                if (pawn is not None) \
                and (AbstractPawn.STATE_GONE == pawn.getState()):
                    pawn.setState(AbstractPawn.STATE_STANDBY)

        self.removeMarkedPawns()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def _updateGameData(self) -> None:
        """
        Warcaby aktualizują dane odnośnie planszy.
        ----
        Sprawdzane są obowiązkowe bicia dla gracza w następnej turze.
        ----
        Jeżeli na planszy zostanie tylko jeden pionek, to gra się kończy.
        """

        self._obligatoryPawns = []
        left_pawns = [0, 0]

        for y in range(len(self._board)):
            for x, pawn in enumerate(self._board[y]):
                if pawn is not None:
                    player = pawn.getPlayer()
                    left_pawns[player] += 1

                    if (player == self._player) \
                    and self.canPawnFight(pawn, x, y):
                        self._obligatoryPawns.append((x, y))

        # Czy na planszy nie został żaden pionek któregoś z graczy?
        for i, c in enumerate(left_pawns):
            if c <= 0:
                # Zwycięzcą jest gracz, którego pionki zostały
                self._player = i ^ 1
                self._state = self.GAMESTATE_END
                return


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def processInput(self, x: int, y: int) -> bool:
        """
        Przetwarzanie wyboru pola w trakcie gry.
        Zwraca prawdę, jeśli należy zaaktualizować planszę.
        ----
         * `x`: indeks kolumny, od lewej do prawej [0-7].
         * `y`: indeks wiersza, od góry do dołu [0-7].
        """

        checkPawns = False

        def subprocess() -> bool:

            # Czy wybrano "białe" pole zamiast pola "czarnego"?
            if (not ((x & 1) ^ (y & 1))):
                return False

            # Czy gracz powinien wybrać pionka?
            if self.GAMESTATE_TAKE == self._state:

                # Czy jakikolwiek pionek w ogóle istnieje na danym polu?
                # Jeśli nie, to przypomnij o wybraniu właściwego pola.
                if self._board[y][x] is None:
                    return True

                # Czy gracz wybrał swojego pionka?
                if self._board[y][x].getPlayer() != self._player:
                    self._turninfo = self.TURNINFO_WRONG_PLAYER
                    return True

                # Czy gracz powinien wykonać obowiązkowe bicie?
                if len(self._obligatoryPawns) > 0:
                    if (x, y) not in self._obligatoryPawns:
                        self._turninfo = self.TURNINFO_OBLIG_FIGHT
                        return True

                self._multiFightPawn = self._board[y][x]
                self._multiFightPawn.setState(AbstractPawn.STATE_SELECTED)
                self._selectedPawnPos = (x, y)
                self._fightingPawnPos = self._selectedPawnPos
                self._state = self.GAMESTATE_PUT
                return True

            # Czy gracz powinien przesunąć pionka?
            if self.GAMESTATE_PUT == self._state:
                no_more_moves = False
                accept_move = False
                sx, sy = self._selectedPawnPos
                fx, fy = self._fightingPawnPos

                # Domyślnie zakończ każdą turę zmieniając stan
                # na wymagane podniesienie kolejnego pionka
                self._state = self.GAMESTATE_TAKE

                # Czy odklikniętio zaznaczonego pionka?
                if (sx == x) and (sy == y):
                    self._turninfo = self.TURNINFO_CANCELLED
                    no_more_moves = True

                # Czy dane pole jest zablokowane przez innego pionka?
                elif self._board[y][x] is not None:
                    self._turninfo = self.TURNINFO_INVALID_MOVE
                    no_more_moves = True

                else:

                    # Czy zaznaczony pionek może wykonać żądany ruch?
                    a, b = self.validateSelectedPawnMove(fx, fy, x, y)
                    if a > 0:

                        # Czy zbito przynajmniej jedneg pionka przeciwnika
                        if b > 0:

                            # Czy zaznaczony pionek może bić dalej?
                            if self.canPawnFight(self._multiFightPawn, x, y):

                                # Dodanie pośredniego pola bicia
                                self._board[y][x] = AbstractPawn()
                                self._fightingPawnPos = (x, y)

                                # Pozostanie w stanie przeskakiwania na pola
                                self._state = self.GAMESTATE_PUT
                                self._turninfo = self.TURNINFO_FIGHT_AGAIN
                                return True
                            else:
                                no_more_moves = True
                                accept_move = True
                        else:
                            no_more_moves = True

                            # Nie zbito żadnego pionka, ale istnieje
                            # przynajmniej jedno obowiązkowe bicie!
                            if len(self._obligatoryPawns) > 0:
                                self._turninfo = self.TURNINFO_INVALID_MOVE
                            else:
                                accept_move = True

                    else:
                        self._turninfo = self.TURNINFO_INVALID_MOVE
                        no_more_moves = True

                # Odznaczenie pionka, kiedy nie może już się poruszać.
                if no_more_moves:
                    self._multiFightPawn.setState(AbstractPawn.STATE_STANDBY)

                # Przeniesienie zaznaczonego pionka na nową pozycję
                # oraz usunięcie zbędnych (pokonanych i pośrednich) pionków
                if accept_move:
                    pawn = self._board[sy][sx]
                    self._board[y][x] = pawn
                    self._board[sy][sx] = None
                    self.removeMarkedPawns()

                    # Czy pionek może awansować?
                    promotion = (0, len(self._board) - 1)
                    if (type(pawn) == WeakPawn) \
                    and promotion[self._player] == y:
                        self._board[y][x] = StrongPawn(self._player)

                    # Przekazanie tury dla kolejnego gracza oraz sprawdzenie
                    # stanu planszy po przeniesieniu jednego pionka.
                    self._player = self._player ^ 1
                    nonlocal checkPawns
                    checkPawns = True
                else:
                    self.resetMarkedPawns()

                return True

            return False

        t = subprocess()
        if checkPawns:
            self._updateGameData()
        return t


################################################################
