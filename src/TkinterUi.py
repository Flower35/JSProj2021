################################################################
# Warcaby: "TkinterUi.py"
################################################################

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
import tkinter

from AbstractUi import AbstractUi
from Checkers import Checkers


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class TkinterUi(AbstractUi):
    """
    Graficzny interfejs do gry "Warcaby".
    """

    WINDOW_TITLE = "WARCABY"
    WINDOW_WIDTH = 640
    WINDOW_HEIGHT = 480

    FONT = ('Courier New', 12)

    LABEL_X = 16
    LABEL_Y = 16
    LABEL_WIDTH = WINDOW_WIDTH - 2 * LABEL_X
    LABEL_HEIGHT = 32

    BOARD_SIZE = 8

    BOARDBTN_WIDTH = 48
    BOARDBTN_HEIGHT = 48
    BOARDBTN_DARKCOLOR = '#A4795D'
    BOARDBTN_LIGHTCOLOR = '#DBCCA3'

    BOARD_WIDTH = BOARD_SIZE * BOARDBTN_WIDTH
    BOARD_HEIGHT = BOARD_SIZE * BOARDBTN_HEIGHT
    BOARD_X = 16
    BOARD_Y = 64

    RESETBTN_WIDTH = 128
    RESETBTN_HEIGHT = 64
    RESETBTN_X = WINDOW_WIDTH - 16 - RESETBTN_WIDTH
    RESETBTN_Y = WINDOW_HEIGHT - 16 - RESETBTN_HEIGHT


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def __init__(self, checkers: Checkers) -> None:
        """
        Inicjalizacja klasy `TkinterUi`.
        ----
         * checkers: instancja Warcabów obsługiwana przez nowy interfejs.
        """

        super().__init__(checkers)

        # Główne okno Tkinter

        self._master = tkinter.Tk()

        self._master.title(self.WINDOW_TITLE)
        self._master.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        # Etykieta na komunikaty

        msgFrame = tkinter.Frame (
            self._master, borderwidth = 2, relief = tkinter.SUNKEN,
            width = self.LABEL_WIDTH, height = self.LABEL_HEIGHT,
            bg = '#FFFFFF'
        )

        self._msgLabel = tkinter.Label (
            msgFrame, text = 'Rozpocznij nową grę!',
            font = self.FONT, bg = '#FFFFFF'
        )

        self._msgLabel.pack(fill = tkinter.BOTH, expand = True)

        msgFrame.pack_propagate(False)
        msgFrame.place(x = self.LABEL_X, y = self.LABEL_Y)

        # Przyciski na planszy

        buttonsFrame = tkinter.Frame (
            self._master,
            width = 16 + self.BOARD_WIDTH,
            height = 16 + self.BOARD_HEIGHT,
            bg = '#000000'
        )

        self._boardButtons = []

        for y in range(self.BOARD_SIZE):
            rowOfButtons = []

            for x in range(self.BOARD_SIZE):
                boardButton = tkinter.Button(buttonsFrame)

                boardButton.place (
                    x = 8 + x * self.BOARDBTN_WIDTH,
                    y = 8 + y * self.BOARDBTN_HEIGHT,
                    width = self.BOARDBTN_WIDTH,
                    height = self.BOARDBTN_HEIGHT
                )

                if (x & 1) ^ (y & 1):
                    rowOfButtons.append(boardButton)

                    boardButton['bg'] = self.BOARDBTN_DARKCOLOR
                    boardButton['fg'] = self.BOARDBTN_LIGHTCOLOR
                    boardButton['font'] = self.FONT

                    boardButton['command'] = \
                        lambda bx = x, by = y: \
                            self.processBoardButton(bx, by)
                else:
                    rowOfButtons.append(None)

                    boardButton['bg'] = self.BOARDBTN_LIGHTCOLOR
                    boardButton['relief'] = tkinter.SUNKEN
                    boardButton['state'] = tkinter.DISABLED

            self._boardButtons.append(rowOfButtons)

        buttonsFrame.pack_propagate(False)
        buttonsFrame.place(x = self.BOARD_X, y = self.BOARD_Y)

        # Przycisk resetujący grę

        resetFrame = tkinter.Frame (
            self._master,
            width = self.RESETBTN_WIDTH,
            height = self.RESETBTN_HEIGHT,
        )

        resetButton = tkinter.Button (
            resetFrame, text = 'Nowa gra',
            font = self.FONT, bg = '#000000', fg = '#FFFFFF',
            command = lambda: self.processResetButton()
        )

        resetButton.pack(fill = tkinter.BOTH, expand = True)

        resetFrame.pack_propagate(False)
        resetFrame.place(x = self.RESETBTN_X, y = self.RESETBTN_Y)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def enable(self, state: bool) -> None:
        """Patrz: `AbstractUi.enable`."""

        if state:
            self._master.mainloop()

        else:
            self._master.destroy()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def updateBoard(self) -> None:
        """Patrz: `AbstractIi.updateBoard`."""

        textBoard = self._checkers.getTextBoard()

        for y in range(self.BOARD_SIZE):
            for x in range(self.BOARD_SIZE):
                if (x & 1) ^ (y & 1):
                    self._boardButtons[y][x]['text'] = textBoard[y][x]

        self._msgLabel['text'] = self._checkers.getTextState()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def processBoardButton(self, x: int, y: int) -> None:
        """
        Przetwarzanie po wciśnięciu przycisku na planszy.
        ----
         * `x`: indeks kolumny, od lewej do prawej [0-7].
         * `y`: indeks wiersza, od góry do dołu [0-7].
        """

        if self._checkers.processInput(x, y):
            self.updateBoard()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    def processResetButton(self) -> None:
        """
        Wciśnięcie przycisku do uruchomienia nowej gry.
        """

        self._checkers.newGame()

        self.updateBoard()


################################################################
