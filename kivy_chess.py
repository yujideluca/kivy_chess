from kivy.config import Config
import numpy as np
import random

Config.set("input", "mouse", "mouse,disable_multitouch")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.graphics import *

#                                                 rows
# chess_table = np.array([[0, 1, 2, 3, 4, 5, 6, 7], #0
#                         [0, 1, 2, 3, 4, 5, 6, 7], #1
#                         [0, 1, 2, 3, 4, 5, 6, 7], #2
#                         [0, 1, 2, 3, 4, 5, 6, 7], #3
#                         [0, 1, 2, 3, 4, 5, 6, 7], #4
#                         [0, 1, 2, 3, 4, 5, 6, 7], #5
#                         [0, 1, 2, 3, 4, 5, 6, 7], #6
#                         [0, 1, 2, 3, 4, 5, 6, 7]])#7


class MyScreenManager(ScreenManager):
    returned = False


class TopOfEverything(FloatLayout):
    window_size = [800, 600]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyboard_setup()
        Clock.schedule_once(self.after_init)
        Window.size = self.window_size

    def after_init(self, *args):
        pass

    def keyboard_setup(self, me=None, *args):
        # Keyboard for debug
        if me == None:
            me = self
        me._keyboard = Window.request_keyboard(me._keyboard_closed, me)
        me._keyboard.bind(on_key_down=me._on_keyboard_down)
        me._keyboard.bind(on_key_up=me._on_keyboard_up)
        self.key_pressed = None

    def _keyboard_closed(self):
        pass

    def _on_keyboard_up(self, keycode, text):
        pass

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        pass


class MyWidget(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ClickableImage(ButtonBehavior, Image):
    selected = BooleanProperty(False)
    highlight_rect = None

    def highlight(self):
        if self.selected:
            self.canvas.remove(self.highlight_rect)
            self.highlight_rect = None
        else:
            with self.canvas:
                Color(.498, .149, 1, .3)
                self.highlight_rect = Rectangle(pos=self.pos, size=self.size)
        self.selected = not self.selected

    def on_release(self):
        super().on_release()
        self.highlight()

    pass


class Tile(ClickableImage):
    def __init__(self, tile_color, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tile_color = tile_color
        self.number = number

    def highlight(self):
        super().highlight()
        print(self.number)
    pass


class GameBoard(Screen):
    tiles_source = [
        "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\square gray light _png_shadow_128px.png",
        "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\square gray dark _png_shadow_128px.png"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.after_init)

    def after_init(self, *args):
        self.make_board()
        self.place_chess()

    def call_abs_coord(self, tile_x, tile_y):
        abs_coord = tile_x + (tile_y * 8)
        return abs_coord

    def make_board(self):
        board = self.ids.board
        tile_mod = 0
        for tile in range(64):
            tile_image = Tile(source=self.tiles_source[(tile + tile_mod) % 2],
                              allow_stretch=True,
                              keep_ratio=False,
                              number=tile,
                              tile_color=["white", "black"][(tile + tile_mod) % 2])
            tile_image.number = tile
            board.add_widget(tile_image)
            if tile % 8 == 7:
                tile_mod += 1

    black_pieces = {
        "pawn": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\b_pawn_png_shadow_128px.png",
        "rook": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\b_rook_png_shadow_128px.png",
        "knight": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\b_knight_png_shadow_128px.png",
        "bishop": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\b_bishop_png_shadow_128px.png",
        "king": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\b_king_png_shadow_128px.png",
        "queen": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\b_queen_png_shadow_128px.png"
    }
    white_pieces = {
        "pawn": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\w_pawn_png_shadow_128px.png",
        "rook": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\w_rook_png_shadow_128px.png",
        "knight": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\w_knight_png_shadow_128px.png",
        "bishop": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\w_bishop_png_shadow_128px.png",
        "queen": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\w_queen_png_shadow_128px.png",
        "king": "C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_images\\w_king_png_shadow_128px.png"
    }
    opponent_pieces_dict = {
        "rook": [(0, 0), (7, 0)],
        "knight": [(1, 0), (6, 0)],
        "bishop": [(2, 0), (5, 0)],
        "queen": [(3, 0)],
        "king": [(4, 0)],
        "pawn": [(i, 1) for i in range(8)]
    }
    player_pieces_dict = {
        "rook": [(0, 7), (7, 7)],
        "knight": [(1, 7), (6, 7)],
        "bishop": [(2, 7), (5, 7)],
        "queen": [(3, 7)],
        "king": [(4, 7)],
        "pawn": [(i, 6) for i in range(8)]
    }

    def place_chess(self):
        for piece_name, coordinates in self.opponent_pieces_dict.items():
            for coordinate in coordinates:
                # adds black pieces
                black_piece = Piece(source=self.black_pieces[piece_name],
                                    allow_stretch=True,
                                    keep_ratio=False,
                                    piece_color="black",
                                    coordinate=list(coordinate),
                                    piece_type=piece_name)
                tile_ind = self.call_abs_coord(list(coordinate)[0], list(coordinate)[1])
                self.ids.board.children[63-tile_ind].ids.anchor.add_widget(black_piece)
        for piece_name, coordinates in self.player_pieces_dict.items():
            for coordinate in coordinates:
                # adds white pieces
                white_piece = Piece(source=self.white_pieces[piece_name],
                                    allow_stretch=True,
                                    keep_ratio=False,
                                    piece_color="white",
                                    coordinate=list(coordinate),
                                    piece_type=piece_name)
                tile_ind = self.call_abs_coord(list(coordinate)[0], list(coordinate)[1])
                self.ids.board.children[63-tile_ind].ids.anchor.add_widget(white_piece)
                # self.ids.board.children's index is the reverse of tile_ind's, because the first tile generated is the
                #  last one in the GridLayout, while the matrix coordinates we use for organize the chessboard considers
                # the first left superior tile as the (0, 0) coordinate,
                # so: self.ids.board.children's index == 63 - tile_ind
            # troubleshooting
            # for ind, tile in enumerate(self.ids.board.children):
            #     print(ind, tile.number, end=' ')
            #     if len(tile.children[0].children) > 0:
            #         piece = tile.children[0].children[0]
            #         print(piece.piece_type, piece.piece_color, piece.coordinate)
            #     else:
            #         print()


class Piece(ClickableImage):
    def __init__(self, piece_color, coordinate, piece_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.piece_color = piece_color
        self.coordinate = coordinate
        self.piece_type = piece_type

    def valid_tiles(self):
        y_coord = self.coordinate[1]
        x_coord = self.coordinate[0]
        range_dict = {
            "pawn": [(x_coord, y_coord - move) for move in range(1, 2)],
            "special_pawn": [(x_coord, y_coord - 1), (x_coord, y_coord - 2)],
            # if pawn in original coordinate append (x_coord, y_coord + 2)
            "rook": [(x_coord - move, y_coord) for move in range(1, x_coord+1)] +
                    [(x_coord, y_coord - move) for move in range(1, y_coord+1)] +
                    [(x_coord + move, y_coord) for move in range(1, 8-x_coord)] +
                    [(x_coord, y_coord + move) for move in range(1, 8-y_coord)],
            "knight": [(x_coord + 2*(-1)**ex, y_coord + (-1)**exp) for ex in range(2) for exp in range(2)] +
                      [(x_coord + (-1)**ex, y_coord + 2*(-1)**exp) for ex in range(2) for exp in range(2)],
            "bishop": [(x_coord + move, y_coord + move) for move in range(1, 8)] +
                      [(x_coord + move, y_coord - move) for move in range(1, 8)] +
                      [(x_coord - move, y_coord + move) for move in range(1, 8)] +
                      [(x_coord - move, y_coord - move) for move in range(1, 8)],
            "queen": [(x_coord - move, y_coord) for move in range(1, x_coord+1)] +
                     [(x_coord, y_coord - move) for move in range(1, y_coord+1)] +
                     [(x_coord + move, y_coord) for move in range(1, 8-x_coord)] +
                     [(x_coord, y_coord + move) for move in range(1, 8-y_coord)] +
                     [(x_coord - move, y_coord) for move in range(1, 8)] +
                     [(x_coord, y_coord - move) for move in range(1, 8)] +
                     [(x_coord + move, y_coord) for move in range(1, 8)] +
                     [(x_coord, y_coord + move) for move in range(1, 8)],
            "king": [(x_coord + move, y_coord + move) for move in range(-1, 2, 2)] +
                    [(x_coord + move, y_coord - move) for move in range(-1, 2, 2)] +
                    [(x_coord + move, y_coord) for move in range(-1, 2, 2)] +
                    [(x_coord, y_coord + move) for move in range(-1, 2, 2)]
        }
        board_list = [(x, y) for x in range(8) for y in range(8)]
        piece_list = [(x, y) for x, y in range_dict[self.piece_type] if (x, y) in board_list]
        if self.piece_type == "pawn":
            if self.coordinate in [[i, 6] for i in range(8)]:
                print(range_dict["special_pawn"])
                return range_dict["special_pawn"]
            else:
                print(range_dict["pawn"])
                return range_dict["pawn"]
        else:
            print(piece_list)
            return piece_list

    # def highlight(self):
    #     super().highlight()
    #     self.valid_tiles()


class ChessGame(GameBoard, Piece):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def move_options(self):
        super().valid_tiles()
        for coord in super(Piece).valid_tiles():
            if coord in super(GameBoard).player_pieces_dict.values():
                super(Piece).valid_tiles().pop((x, y))
            else:
                pass
        print(super(Piece).valid_tiles())

    def highlight(self):
        super(ClickableImage).highlight()
        super(Piece).valid_tiles()
        self.move_options()


####################
class MyKivyChess(App):
    def build(self):
        return TopOfEverything()


with open("C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_layout.kv", "rb") as kvfile:
    kivystr = kvfile.read()
    Builder.load_string(kivystr.decode('cp1252'))

if __name__ == "__main__":
    MyKivyChess().run()