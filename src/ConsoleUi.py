################################################################
# Warcaby: "/src/ConsoleUi.py"
################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
from typing import Tuple

from AbstractUi import AbstractUi
from Checkers import Checkers


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class ConsoleUi(AbstractUi):
    """
    Konsolowy interfejs do gry "Warcaby".
    """


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __init__(self, checkers: Checkers) -> None:
        """
        Inicjalizacja klasy `ConsoleUi`.
        ----
         * checkers: instancja Warcabów obsługiwana przez nowy interfejs.
        """

        super().__init__(checkers)

        # Tekstowa reprezentacja planszy Warcabów.
        self.__textBoard = [
            [None] * Checkers.BOARD_SIZE
            for _ in range(Checkers.BOARD_SIZE)
        ]

        # Komunikat generowany co każdy ruch.
        self.__message = ''

        # Graj dopóki gra się nie zakończy
        self.__gameState = Checkers.GAMESTATE_TAKE

        # Pseudo-graficzne dodatki
        self.__dashedLine = '-' * 64

        self.__columnNames = [
            chr(ord('A') + x) for x in range(Checkers.BOARD_SIZE)
        ]

        self.__rowNames = [
            str(Checkers.BOARD_SIZE - y) for y in range(Checkers.BOARD_SIZE)
        ]


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def enable(self, state: bool) -> None:
        """Patrz: `AbstractUi.enable`."""

        if state:
            self._checkers.newGame()
            self.gameLoop()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def updateBoard(self) -> None:
        """Patrz: `AbstractUi.updateBoard`."""

        simpleTextBoard = self._checkers.getTextBoard()

        for y in range(Checkers.BOARD_SIZE):
            for x in range(Checkers.BOARD_SIZE):

                # Odczytanie obiektu na danej pozycji planszy
                if (x & 1) ^ (y & 1):
                    t = simpleTextBoard[y][x]
                else:
                    t = ''

                # Zamiana na czytelniejszy format
                if not t:
                    t = '----'
                else:
                    t = f'{t:^4}'

                self.__textBoard[y][x] = t

        self.__message = self._checkers.getTextState()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def drawBoard(self) -> None:
        """Patrz: `AbstractUi.drawBoard`."""

        # Wyświetlenie głównego komunikatu.

        print(self.__dashedLine)
        print(self.__message)
        print(self.__dashedLine)
        print()

        # Wyświetlenie planszy.

        def printColNames() -> None:
            print('    ', end = '')
            for n in self.__columnNames:
                print(f' ({n:^2})', end = '')
            print()

        def printRowName(y: int) -> None:
            print(f' ({self.__rowNames[y]}) ', end = '')

        printColNames()

        for y, row in enumerate(self.__textBoard):
            printRowName(y)
            for x in row:
                print(f'{x} ', end = '')
            printRowName(y)
            print()

        printColNames()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def readInput(self) -> Tuple[int, int]:
        """
        Poproś użytkownika o wybranie pola w formacie szachowej notacji
         algebraicznej (LITERA i CYFRA). Funkcja zwraca parę koordynatów
         [X, Y]. Funkcja nie zakończy się dopóki nie zostaną podane
         poprawne indeksy (wiersz, kolumna)! Można jednak przerwać
         całą grę podając pusty tekst.
        """

        while True:
            try:
                print('Wybierz pozycję: ', end = '')
                t = input()

                if (not t) or (len(t) <= 0):
                    return None

                if len(t) != 2:
                    raise ValueError('Należy podać dwa znaki!')

                if t[0] not in self.__columnNames:
                    raise ValueError (
                        'Niewłaściwy identyfikator kolumny!' +
                        f' Proszę podać: {self.__columnNames}'
                    )

                if t[1] not in self.__rowNames:
                    raise ValueError (
                        'Niewłaściwy identyfikator wiersza!' +
                        f' Proszę podać: {self.__rowNames}'
                    )

                x = self.__columnNames.index(t[0])
                y = self.__rowNames.index(t[1])
                return (x, y)

            except ValueError as e:
                print(f'<< WYJĄTEK >>  {e}')


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def gameLoop(self) -> None:
        """
        Prosta pętla gry.
        """

        while Checkers.GAMESTATE_END != self.__gameState:
            self.updateBoard()
            self.drawBoard()

            print(self.__dashedLine)
            xy = self.readInput()
            print(self.__dashedLine)

            if xy is None:
                return

            self._checkers.processInput(xy[0], xy[1])
            self.__gamestate, _, _ = self._checkers.getGameState()


################################################################
