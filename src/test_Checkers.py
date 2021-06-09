################################################################
# Warcaby: "/src/test_Checkers.py"
################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
import unittest
import copy
from typing import List, Tuple

from Checkers import Checkers


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def multilineBoardTextToList(textBoard: str) -> List[List[str]]:
    """
    Konwersja wielolinijkowego tekstu na dwuwymiarową tablicę
     reprezentująca testowany przypadek rozegrania Warcabów.
    ----
        * `textBoard`: pionki oddzielone spacjami i znakami nowej linii.
         Brak pionka oznakowany jest podłogą (`"_"`).
    """

    result = []

    for line in textBoard.splitlines():
        resultRow = []

        for x in line.split():
            if '_' in x:
                resultRow.append('')
            else:
                resultRow.append(x)

        result.append(resultRow)

    return result


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class test_Checkers(unittest.TestCase):
    """
    Testy jednostkowe gry "Warcaby"
    """

    TESTMOVES_INVALID     = 0
    TESTMOVES_PAWNTAKEN   = 1
    TESTMOVES_MULTIFIGHT  = 2
    TESTMOVES_PAWNPUTBACK = 3


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    @classmethod
    def setUpClass(cls) -> None:
        """
        Inicjalizacja klasy testującej.
        """

        # Instancja klasy Warcabowej
        cls.__checkers = Checkers()

        # Układ pionków w nowej grze
        cls.__newGameBoard = multilineBoardTextToList (
            " _ B _ B _ B _ B \n"
            " B _ B _ B _ B _ \n"
            " _ B _ B _ B _ B \n"
            " _ _ _ _ _ _ _ _ \n"
            " _ _ _ _ _ _ _ _ \n"
            " C _ C _ C _ C _ \n"
            " _ C _ C _ C _ C \n"
            " C _ C _ C _ C _ \n"
        )

        # Odstępy między wypisywanymi danymi tekstowymi
        cls.__dashedLine = '-' * 64
        cls.__doubleDashedLine = '=' * 64


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __printTestHeader(self, methodName: str, methodDoc: str) -> None:
        """
        Wypisanie nagłówka na początku każdgo testu
        ----
         * `methodName`: nazwa uruchamianego testu.
         * `methodDoc`: opis uruchamianego testu
        """

        print (
            '', self.__doubleDashedLine, self.__doubleDashedLine,
            '', f'    << {methodName} >>',
            '', f'    {methodDoc.strip()}',
            '', self.__doubleDashedLine,
            '', sep = '\n'
        )


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __printTestFooter(self) -> None:
        """
        Wypisanie stopki na końcu każdgo testu
        """

        print (
            '', self.__doubleDashedLine, self.__doubleDashedLine,
            '', sep = '\n'
        )


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    @staticmethod
    def __printBoard(board: List[List[str]]):
        """
        Rysowanie planszy w każdym teście jednostkowym.
        ----
         * `board`: dwuwymiarowa tablica tekstowa.
        """

        for row in board:
            print('    ', end = '')
            print(' '.join(['____' if not x else f'{x:^4}' for x in row]))
        print()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __changingBoardProceduralMoves (
        self, startingPlayer: int, board: List[List[str]],
        moves: List[Tuple[int, int, int]]
    ) -> None:
        """
        Testowanie przebiegu gry, zaczynając od wybranej planszy
        i od wybranego gracza, wykonując kolejne ruchy,
        generowanie kolejnych plansz proceduralnie.
        ----
         * `startingPlayer`: gracz rozpoczynający turę (0 lub 1).
         * `board`: tekstowa reprezentacja pierwszej planszy.
         * `moves`: lista kolejnych ruchów (pole [X,Y] do zaznaczenia
          na planszy, oczekiwana prawidłowość bądź nieprawidłowość).
        """

        print(self.__dashedLine)
        print('SPRAWDZANIE RUCHÓW OD PLANSZY:')
        self.__printBoard(board)

        playerId = startingPlayer

        board = copy.deepcopy(board)
        lastValidBoard = copy.deepcopy(board)

        lastPawnTaken = None
        multiFightPosList = []

        self.__checkers.newGame()
        self.__checkers.setTextBoard(board)
        self.__checkers.setCurrentPlayer(playerId)

        for move in moves:

            self.assertFalse (
                ((move[0] & 1) ^ (move[0] & 1)),
                "Próba wybrania złego pola (jasne zamiast ciemnego)"
            )

            playerIcon = Checkers.PLAYER_ICONS[playerId]
            print(f'Gracz [{playerIcon}] wybrał pole', end = '')
            notation = chr(ord("A") + move[0])
            notation += str(Checkers.BOARD_SIZE - move[1])
            print(f' {notation} (x = {move[0]}, y = {move[1]})')

            # Niepoprawny ruch:
            if self.TESTMOVES_INVALID == move[2]:
                expectedGameState = Checkers.GAMESTATE_TAKE
                expectedTurnInfo = Checkers.TURNINFO_INVALID_MOVE

                board = copy.deepcopy(lastValidBoard)
                multiFightPosList = []

            # Podniesiono pionka:
            elif self.TESTMOVES_PAWNTAKEN == move[2]:
                expectedGameState = Checkers.GAMESTATE_PUT
                expectedTurnInfo = Checkers.TURNINFO_NOTHING

                x = board[move[1]][move[0]]
                lastPawnTaken = (move[0], move[1], x)
                board[move[1]][move[0]] = f'[{x}]'

            # Multibicie:
            elif self.TESTMOVES_MULTIFIGHT == move[2]:
                expectedGameState = Checkers.GAMESTATE_PUT
                expectedTurnInfo = Checkers.TURNINFO_FIGHT_AGAIN

                multiFightPosList.append((move[0], move[1]))
                board[move[1]][move[0]] = 'x'

            # Poprawne odłożenie pionka:
            elif self.TESTMOVES_PAWNPUTBACK == move[2]:
                expectedGameState = Checkers.GAMESTATE_TAKE
                expectedTurnInfo = Checkers.TURNINFO_NOTHING

                # Wykasowanie niepotrzebnych pionków
                # (funkcja pomocnicza, pętla lokalna)

                def walkAndDestroy(x0: int, y0: int, x1: int, y1: int):
                    """
                    Przespaceruj się po fragmencie planszy
                     (w linii prostej) i wykasuj
                     wszystkie pionki na swej drodze.
                    ----
                     * `x0`, `y0`: punkt startowy (czyszczony włącznie)
                     * `x1`, `y1`: punkt końcowy (wyłączny)
                    """

                    nonlocal board

                    x_diff = x1 - x0
                    x_diff_abs = abs(x_diff)
                    y_diff = y1 - y0
                    y_diff_abs = abs(y_diff)
                    self.assertEqual (
                        x_diff_abs, y_diff_abs,
                        "Niepoprawne kroki w funkcji spacerującej?"
                    )

                    x_step = x_diff // x_diff_abs
                    y_step = y_diff // y_diff_abs

                    while (x0 != x1) and (y0 != y1):
                        board[y0][x0] = ''
                        x0 += x_step
                        y0 += y_step

                multiFightPosList = \
                    [lastPawnTaken[:2]] + multiFightPosList + [move[:2]]

                for i in range(len(multiFightPosList) - 1):
                    pos0 = multiFightPosList[i]
                    pos1 = multiFightPosList[i + 1]
                    walkAndDestroy(pos0[0], pos0[1], pos1[0], pos1[1])

                multiFightPosList = []

                # Sprawdzenie, czy pionek nie powinien zamienić się w damkę.
                if len(lastPawnTaken[2]) < 2:
                    y = (Checkers.BOARD_SIZE - 1) if (1 == playerId) else 0
                    if y == move[1]:
                        x = lastPawnTaken[2] + 'd'
                        lastPawnTaken = ('wspaniale!', 'awansujesz!', x)

                # Przestawienie ostatnio wziętego pionka,
                # zamiana indeksu gracza od następnej tury,
                # zapamiętanie planszy po ostatnim prawidłowym ruchu.
                board[move[1]][move[0]] = lastPawnTaken[2]
                playerId ^= 1
                lastValidBoard = copy.deepcopy(board)

            print('Oczekiwana plansza po przyjęciu koordynatów:')
            self.__printBoard(board)

            self.__checkers.processInput(move[0], move[1])

            checkerboard = self.__checkers.getTextBoard()

            self.assertEqual (
                board, checkerboard,
                "Niezgodny układ planszy po wykonanym zapytaniu."
            )

            gameState, turnInfo, nextPlayer = self.__checkers.getGameState()

            self.assertEqual (
                gameState, expectedGameState,
                "Niezgodny stan gry po wykonanym zapytaniu."
            )

            self.assertEqual (
                turnInfo, expectedTurnInfo,
                "Niezgodna informacja o poprzedniej turze."
            )

            self.assertEqual (
                nextPlayer, playerId,
                "Niezgodny indeks gracza z następnej tury."
            )

        print(self.__dashedLine, end = '\n\n')


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def test_NewGameBoard(self) -> None:
        """
        Testowanie ułożenia pionków po włączeniu nowej gry.
        """

        self.__printTestHeader (
            "test_NewGameBoard",
            self.test_NewGameBoard.__doc__
        )

        self.__printBoard(self.__newGameBoard)

        self.__checkers.newGame()

        checkerboard = self.__checkers.getTextBoard()
        self.assertListEqual(self.__newGameBoard, checkerboard)

        gameState, turnInfo, nextPlayer = self.__checkers.getGameState()
        self.assertEqual(gameState, Checkers.GAMESTATE_TAKE)
        self.assertEqual(turnInfo, Checkers.TURNINFO_NOTHING)
        self.assertEqual(nextPlayer, 0)

        self.__printTestFooter()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def test_RegularPlayerMoves(self) -> None:
        """
        Testowanie naprzemiennych ruchów graczy.
        """

        self.__printTestHeader (
            "test_RegularPlayerMoves",
            self.test_RegularPlayerMoves.__doc__
        )

        self.__changingBoardProceduralMoves (
            0,  # Gracz 0 (CZARNE)
            self.__newGameBoard,
            [
                (4, 5, self.TESTMOVES_PAWNTAKEN),
                (3, 4, self.TESTMOVES_PAWNPUTBACK),
                (5, 2, self.TESTMOVES_PAWNTAKEN),
                (6, 3, self.TESTMOVES_PAWNPUTBACK),
                (5, 6, self.TESTMOVES_PAWNTAKEN),
                (4, 5, self.TESTMOVES_PAWNPUTBACK),
                (3, 2, self.TESTMOVES_PAWNTAKEN),
                (2, 3, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__printTestFooter()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def test_InvalidMoves(self) -> None:
        """
        Testowanie niepowodzenia błędnego ruchu pionkiem.
        """

        self.__printTestHeader (
            "test_InvalidMoves",
            self.test_InvalidMoves.__doc__
        )

        self.__changingBoardProceduralMoves (
            0,  # Gracz 0 (CZARNE)
            multilineBoardTextToList (
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ C _ _ _ _ \n"
                " _ _ C _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
            ),
            [
                # wejście na innego pionka
                (2, 3, self.TESTMOVES_PAWNTAKEN),
                (3, 2, self.TESTMOVES_INVALID),
                # próba zbicia swojego pionka
                (2, 3, self.TESTMOVES_PAWNTAKEN),
                (4, 1, self.TESTMOVES_INVALID),
                # ruch do tyłu
                (2, 3, self.TESTMOVES_PAWNTAKEN),
                (3, 4, self.TESTMOVES_INVALID),
                # ruch za daleko
                (2, 3, self.TESTMOVES_PAWNTAKEN),
                (0, 1, self.TESTMOVES_INVALID),
                # ruch nie na ukos
                (2, 3, self.TESTMOVES_PAWNTAKEN),
                (2, 1, self.TESTMOVES_INVALID)
            ]
        )

        self.__changingBoardProceduralMoves (
            1,  # Gracz 1 (BIAŁE)
            multilineBoardTextToList (
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ B _ _ _ _ \n"
                " _ _ _ _ B _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
            ),
            [
                # wejście na innego pionka
                (3, 4, self.TESTMOVES_PAWNTAKEN),
                (4, 5, self.TESTMOVES_INVALID),
                # próba zbicia swojego pionka
                (3, 4, self.TESTMOVES_PAWNTAKEN),
                (5, 6, self.TESTMOVES_INVALID),
                # ruch do tyłu
                (3, 4, self.TESTMOVES_PAWNTAKEN),
                (4, 3, self.TESTMOVES_INVALID),
                # ruch za daleko
                (3, 4, self.TESTMOVES_PAWNTAKEN),
                (1, 6, self.TESTMOVES_INVALID),
                # ruch nie na ukos
                (3, 4, self.TESTMOVES_PAWNTAKEN),
                (3, 6, self.TESTMOVES_INVALID)
            ]
        )

        self.__changingBoardProceduralMoves (
            0,  # Gracz 0 (CZARNE)
            multilineBoardTextToList (
                " _ __ _ _ _ _ _ _ \n"
                " _ __ _ _ _ _ _ _ \n"
                " _ __ _ _ _ _ _ _ \n"
                " _ __ _ _ B _ _ _ \n"
                " _ __ _ B _ _ _ _ \n"
                " _ __ _ _ _ _ _ _ \n"
                " _ Cd _ _ _ _ _ _ \n"
                " _ __ _ _ _ _ _ _ \n"
            ),
            [
                # próba zbicia damką dwóch pionków bez odstępu
                (1, 6, self.TESTMOVES_PAWNTAKEN),
                (5, 2, self.TESTMOVES_INVALID)
            ]
        )

        self.__changingBoardProceduralMoves (
            1,  # Gracz 1 (BIAŁE)
            multilineBoardTextToList (
                " _ _ _ _ _ __ _ _ \n"
                " _ _ _ _ _ __ _ _ \n"
                " _ _ _ _ _ __ _ _ \n"
                " _ _ C _ _ __ _ _ \n"
                " _ _ _ C _ __ _ _ \n"
                " _ _ _ _ _ __ _ _ \n"
                " _ _ _ _ _ Bd _ _ \n"
                " _ _ _ _ _ __ _ _ \n"
            ),
            [
                # próba zbicia damką dwóch pionków bez odstępu
                (5, 6, self.TESTMOVES_PAWNTAKEN),
                (1, 2, self.TESTMOVES_INVALID)
            ]
        )

        self.__printTestFooter()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def test_RegularFights(self) -> None:
        """
        Testowanie pojedynczego bicia pionkami.
        """

        self.__printTestHeader (
            "test_RegularFights",
            self.test_RegularFights.__doc__
        )

        # Rozstawienia pionków umożliwiające wyłącznie pojedyncze bicia
        # oraz niepozwalające na zakończenie gry w jednym ruchu.

        testBoards = [
            [
                multilineBoardTextToList (
                    " _ _ _ _ _ _ _ _ \n"
                    " _ _ _ _ _ _ _ _ \n"
                    " _ _ _ _ _ _ _ _ \n"
                    " _ _ _ _ _ _ _ _ \n"
                    " _ B _ B _ _ _ _ \n"
                    " _ _ C _ _ _ _ _ \n"
                    " _ B _ B _ _ _ _ \n"
                    " _ _ _ _ _ _ _ _ \n"
                ),
                (2, 5)
            ],
            [
                multilineBoardTextToList (
                    " _ _ _ _ _ _ _ _ \n"
                    " _ _ _ _ C _ C _ \n"
                    " _ _ _ _ _ B _ _ \n"
                    " _ _ _ _ C _ C _ \n"
                    " _ _ _ _ _ _ _ _ \n"
                    " _ _ _ _ _ _ _ _ \n"
                    " _ _ _ _ _ _ _ _ \n"
                    " _ _ _ _ _ _ _ _ \n"
                ),
                (5, 2)
            ]
        ]

        # Cztery kierunki bicia.

        directions = [
            ((-2), (-2)), ((+2), (-2)),
            ((-2), (+2)), ((+2), (+2))
        ]

        for i, b in enumerate(testBoards):
            for dir in directions:
                (x0, y0) = (b[1][0], b[1][1])
                (x1, y1) = (x0 + dir[0], y0 + dir[1])
                self.__changingBoardProceduralMoves (
                    i, b[0],
                    [
                        (x0, y0, self.TESTMOVES_PAWNTAKEN),
                        (x1, y1, self.TESTMOVES_PAWNPUTBACK),
                    ]
                )

        self.__printTestFooter()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def test_MultiFights(self) -> None:
        """
        Testowanie wielokrotnego bicia zwykłym pionkiem.
        """

        self.__printTestHeader (
            "test_MultiFights",
            self.test_MultiFights.__doc__
        )

        self.__changingBoardProceduralMoves (
            0,  # Gracz 0 (CZARNE)
            multilineBoardTextToList (
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ B _ B _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ B _ _ _ B _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ B _ B _ B _ _ \n"
                " C _ _ _ _ _ _ _ \n"
            ),
            [
                (0, 7, self.TESTMOVES_PAWNTAKEN),
                (2, 5, self.TESTMOVES_MULTIFIGHT),
                (4, 7, self.TESTMOVES_MULTIFIGHT),
                (6, 5, self.TESTMOVES_MULTIFIGHT),
                (4, 3, self.TESTMOVES_MULTIFIGHT),
                (2, 1, self.TESTMOVES_MULTIFIGHT),
                (0, 3, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__changingBoardProceduralMoves (
            1,  # Gracz 1 (BIAŁE)
            multilineBoardTextToList (
                " _ _ _ _ _ _ _ B \n"
                " _ _ C _ C _ C _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ C _ _ _ C _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ C _ C _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
            ),
            [
                (7, 0, self.TESTMOVES_PAWNTAKEN),
                (5, 2, self.TESTMOVES_MULTIFIGHT),
                (3, 0, self.TESTMOVES_MULTIFIGHT),
                (1, 2, self.TESTMOVES_MULTIFIGHT),
                (3, 4, self.TESTMOVES_MULTIFIGHT),
                (5, 6, self.TESTMOVES_MULTIFIGHT),
                (7, 4, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__printTestFooter()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def test_pawnPromotion(self) -> None:
        """
        Testowanie zamiany pionka w damkę.
        """

        self.__printTestHeader (
            "test_pawnPromotion",
            self.test_pawnPromotion.__doc__
        )

        self.__changingBoardProceduralMoves (
            0,  # Gracz 0 (CZARNE)
            multilineBoardTextToList (
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ C _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ B _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
            ),
            [
                (4, 1, self.TESTMOVES_PAWNTAKEN),
                (3, 0, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__changingBoardProceduralMoves (
            1,  # Gracz 1 (BIAŁE)
            multilineBoardTextToList (
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ _ _ C _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
                " _ _ _ B _ _ _ _ \n"
                " _ _ _ _ _ _ _ _ \n"
            ),
            [
                (3, 6, self.TESTMOVES_PAWNTAKEN),
                (4, 7, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__printTestFooter()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def test_StrongPawnAttacks(self) -> None:
        """
        Testowanie bić przez damkę wykonywanych.
        """

        self.__printTestHeader (
            "test_StrongPawnAttacks",
            self.test_StrongPawnAttacks.__doc__
        )

        self.__changingBoardProceduralMoves (
            0,  # Gracz 0 (CZARNE)
            multilineBoardTextToList (
                " __ _ _ _ _ _ _ B \n"
                " __ _ _ _ B _ _ _ \n"
                " __ B _ _ _ _ _ _ \n"
                " __ _ _ _ B _ _ _ \n"
                " __ _ _ _ _ _ _ _ \n"
                " __ _ B _ _ _ _ _ \n"
                " __ _ _ _ _ _ _ _ \n"
                " Cd _ _ _ _ _ _ _ \n"
            ),
            [
                (0, 7, self.TESTMOVES_PAWNTAKEN),
                (5, 2, self.TESTMOVES_MULTIFIGHT),
                (3, 0, self.TESTMOVES_MULTIFIGHT),
                (0, 3, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__changingBoardProceduralMoves (
            0,  # Gracz 0 (CZARNE)
            multilineBoardTextToList (
                " ___ B _ B _ _ _ _ \n"
                "  B  _ B _ _ _ B _ \n"
                " ___ B _ _ _ _ _ _ \n"
                "  B  _ _ _ B _ _ _ \n"
                " ___ _ _ _ _ _ _ B \n"
                " ___ _ B _ _ _ B _ \n"
                " ___ _ _ _ _ B _ B \n"
                " Cd  _ _ _ B _ B _ \n"
            ),
            [
                (0, 7, self.TESTMOVES_PAWNTAKEN),
                (7, 0, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__changingBoardProceduralMoves (
            1,  # Gracz 1 (BIAŁE)
            multilineBoardTextToList (
                " _ _ _ _ _ _ _ Bd \n"
                " _ _ _ _ _ _ _ __ \n"
                " _ _ _ _ _ C _ __ \n"
                " _ _ _ _ _ _ _ __ \n"
                " _ _ _ C _ _ _ __ \n"
                " _ _ _ _ _ _ C __ \n"
                " _ _ _ C _ _ _ __ \n"
                " C _ _ _ _ _ _ __ \n"
            ),
            [
                (7, 0, self.TESTMOVES_PAWNTAKEN),
                (2, 5, self.TESTMOVES_MULTIFIGHT),
                (4, 7, self.TESTMOVES_MULTIFIGHT),
                (7, 4, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__changingBoardProceduralMoves (
            1,  # Gracz 1 (BIAŁE)
            multilineBoardTextToList (
                " _ C _ C _ _ _ Bd  \n"
                " C _ C _ _ _ _ ___ \n"
                " _ C _ _ _ C _ ___ \n"
                " C _ _ _ _ _ _ ___ \n"
                " _ _ _ C _ _ _  C  \n"
                " _ _ _ _ _ _ C ___ \n"
                " _ C _ _ _ C _  C  \n"
                " _ _ _ _ C _ C ___ \n"
            ),
            [
                (7, 0, self.TESTMOVES_PAWNTAKEN),
                (0, 7, self.TESTMOVES_PAWNPUTBACK)
            ]
        )

        self.__printTestFooter()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def test_Winning(self) -> None:
        """
        Testowania wygrania gry przez dowolnego z graczy.
        """

        self.__printTestHeader (
            "test_Winning",
            self.test_Winning.__doc__
        )

        emptyBoard = [
            ['' for _ in range(Checkers.BOARD_SIZE)]
            for _ in range(Checkers.BOARD_SIZE)
        ]

        positions = [
            [(0, 7), (2, 5), (1, 6)],
            [(7, 0), (5, 2), (6, 1)]
        ]

        boards = [None] * 3
        gamestates = [Checkers.GAMESTATE_PUT, Checkers.GAMESTATE_END]

        for i, p in enumerate(positions):
            print(self.__dashedLine)
            winnerIcon = Checkers.PLAYER_ICONS[i]
            loserIcon = Checkers.PLAYER_ICONS[i ^ 1]

            boards[0] = copy.deepcopy(emptyBoard)
            boards[0][p[0][1]][p[0][0]] = winnerIcon
            boards[0][p[2][1]][p[2][0]] = loserIcon
            self.__printBoard(boards[0])

            boards[1] = copy.deepcopy(boards[0])
            boards[1][p[0][1]][p[0][0]] = f'[{winnerIcon}]'
            self.__printBoard(boards[1])

            boards[2] = copy.deepcopy(emptyBoard)
            boards[2][p[1][1]][p[1][0]] = winnerIcon
            self.__printBoard(boards[2])

            self.__checkers.newGame()
            self.__checkers.setTextBoard(boards[0])
            self.__checkers.setCurrentPlayer(i)

            print(f'Podniesienie pionka przez gracza {[winnerIcon]} ...')
            for k in range(2):
                self.__checkers.processInput(p[k][0], p[k][1])

                checkerboard = self.__checkers.getTextBoard()
                self.assertListEqual(boards[1 + k], checkerboard)

                gameState, turnInfo, nextPlayer = self.__checkers.getGameState()
                self.assertEqual(gameState, gamestates[k])
                self.assertEqual(turnInfo, Checkers.TURNINFO_NOTHING)
                self.assertEqual(nextPlayer, i)

            print(f'Wygrana gracza {[winnerIcon]} !')
            print(self.__dashedLine, end = '\n\n')

        self.__printTestFooter()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
def runTests() -> None:
    unittest.main()


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
if '__main__' == __name__:
    runTests()


################################################################
