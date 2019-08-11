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
        "chess_images/square gray light _png_shadow_128px.png",
        "chess_images/square gray dark _png_shadow_128px.png"
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
        "pawn": "chess_images/b_pawn_png_shadow_128px.png",
        "rook": "chess_images/b_rook_png_shadow_128px.png",
        "knight": "chess_images/b_knight_png_shadow_128px.png",
        "bishop": "chess_images/b_bishop_png_shadow_128px.png",
        "king": "chess_images/b_king_png_shadow_128px.png",
        "queen": "chess_images/b_queen_png_shadow_128px.png"
    }
    white_pieces = {
        "pawn": "chess_images/w_pawn_png_shadow_128px.png",
        "rook": "chess_images/w_rook_png_shadow_128px.png",
        "knight": "chess_images/w_knight_png_shadow_128px.png",
        "bishop": "chess_images/w_bishop_png_shadow_128px.png",
        "queen": "chess_images/w_queen_png_shadow_128px.png",
        "king": "chess_images/w_king_png_shadow_128px.png"
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

    def move_list_gen(self):
        # Generates a list of touples with the possible move coordinates (considers an empty board, the pieces which
        # prevents the movement to be done will be considered after
        move_list = []

        if self.piece_type == "pawn":
            y_pawn = self.coordinate[1]
            x_pawn = self.coordinate[0]
            if self.coordinate == [x_pawn, 6]:
                move_list.append((x_pawn, y_pawn+1))
                move_list.append((x_pawn, y_pawn+2))
            else:
                move_list.append((x_pawn, y_pawn + 1))

        elif self.piece_type == "rook":
            y_rook = self.coordinate[1]
            x_rook = self.coordinate[0]
            for x_r_axis in range(8):
                if x_r_axis == x_rook:
                    pass
                else:
                    move_list.append((x_r_axis, y_rook))
            for y_r_axis in range(8):
                if y_r_axis == y_rook:
                    pass
                else:
                    move_list.append((x_rook, y_r_axis))

        elif self.piece_type == "knight":
            y_knight = self.coordinate[1]
            x_knight = self.coordinate[0]
            # the if statements with range(8) check if the coordinate will be inside the board
            # the -2, 2 range refers to the x axis. When the knight moves +/-2 in X (if abs(x_kn) == 2:)
            # it moves +/-1 in Y
            # When it moves +/- 1 in X (elif abs(x_kn) == 1:)
            # then it moves +/- 2 in Y
            for x_kn in range(-2, 2):
                if x_kn + x_knight in range(8):
                    if abs(x_kn) == 2:
                        if y_knight + 1 in range(8):
                            move_list.append((x_knight+x_kn, y_knight+1))
                        elif y_knight - 1 in range(8):
                            move_list.append((x_knight+x_kn, y_knight-1))
                    elif abs(x_kn) == 1:
                        if y_knight + 2 in range(8):
                            move_list.append((x_knight+x_kn, y_knight+2))
                        elif  y_knight - 2 in range(8):
                            move_list.append((x_knight+x_kn, y_knight-2))

        elif self.piece_type == "bishop":
            y_bishop = self.coordinate[1]
            x_bishop = self.coordinate[0]
            board_list = [(x, y) for x in range(8) for y in range(8)]
            for (x_b, y_b) in board_list:
                if x_bishop - abs(x_b) == y_bishop - abs(y_b) and (x_bishop, y_bishop) != (x_b, y_b):
                    move_list.append((x_b, y_b))

        elif self.piece_type == "queen":
            y_queen = self.coordinate[1]
            x_queen = self.coordinate[0]
            board_list = [(x, y) for x in range(8) for y in range(8)]
            for x_q_axis in range(8):
                if x_q_axis != x_queen:
                    move_list.append((x_q_axis, y_queen))
            for y_q_axis in range(8):
                if y_q_axis != y_queen:
                    move_list.append((x_queen, y_q_axis))
            for (x_q, y_q) in board_list:
                if x_queen - abs(x_q) == y_queen - abs(y_q) and (x_queen, y_queen) != (x_q, y_q):
                    move_list.append((x_q, y_q))

        else:
            y_king = self.coordinate[1]
            x_king = self.coordinate[0]
            king_prelist = list([(x_king + move, y_king + move) for move in range(-1, 2, 2)] +
                                [(x_king + move, y_king - move) for move in range(-1, 2, 2)] +
                                [(x_king + move, y_king) for move in range(-1, 2, 2)] +
                                [(x_king, y_king + move) for move in range(-1, 2, 2)])
            for (x_ki, y_ki) in king_prelist:
                if x_ki and y_ki in range(8):
                    move_list.append((x_ki, y_ki))

        print(move_list)
        print("hello")
        return move_list

    def highlight(self):
        super().highlight()
        self.move_list_gen()


####################
class MyKivyChess(App):
    def build(self):
        return TopOfEverything()


with open("C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_layout.kv", "rb") as kvfile:
    kivystr = kvfile.read()
    Builder.load_string(kivystr.decode('cp1252'))

if __name__ == "__main__":
    MyKivyChess().run()