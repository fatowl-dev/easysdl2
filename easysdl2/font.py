# -*- coding: utf-8 -*-
"""
フォントを扱うクラスを定義します。
"""

from . import _common as g
from . import log
from .functions import *
from .texture import *


class Font():
    """
    フォントを扱うクラス
    """
    # 描画スタイル
    SOLID = 0
    SHADED = 1
    BLENDED = 2

    def __init__(self, filename="", size=20):
        """
        コンストラクタ 
        
        Note:
            filenameを指定しなければ何もしない

        Args:
            filename (str): ttfファイルのパス(utf-8)
            size (int): フォントサイズ(縦のピクセル数？)
        """
        self.__font = None
        self.__size = size
        if filename:
            if not self.load(filename, size):
                log.write("__init__() in Font object failed.")

    def __del__(self):
        """
        デストラクタ

        Note:
            delされたらフォントを開放する
        """
        if self.__font and TTF_WasInit():  # TTF_QuitされたあとにTTF_CloseFontが呼ばれるのを防止する(その場合開放されないかも？
            TTF_CloseFont(self.__font)

    def load(self, filename, size):
        """
        フォントを読み込む
        
        Args:
            filename (str): ttfファイルのパス(utf-8)
            size (int): フォントサイズ
       
        Returns:
            bool: True:成功 False:失敗
        """
        if self.__font:
            TTF_CloseFont(self.__font)
            self.__font = None

        font = TTF_OpenFont(filename.encode("utf-8"), int(size))
        if not font:
            log.write("load('{}') in Font object failed. error={}".format(filename, TTF_GetError()))
            return False
        self.__font = font
        return True

    def get_surface(self, text, color=(255, 255, 255), style=0, bg_color=(0, 0, 0)):
        """
        textを画像化したSDL_Surfaceを取得する
        
        Note:
            ここで取得したSDL_Surfaceは呼び出し側で開放しなければならない
      
        Returns:
            SDL_Surface: SDL_Surface object:成功 None:失敗
        """
        sdlcol = SDL_Color(color[0], color[1], color[2], 255)
        if style == Font.SOLID:
            sur = TTF_RenderUTF8_Solid(self.__font, text.encode("utf-8"), sdlcol)
        elif style == Font.SHADED:
            sdlcol_bg = SDL_Color(bg_color[0], bg_color[1], bg_color[2], 255)
            sur = TTF_RenderUTF8_Shaded(self.__font, text.encode("utf-8"), sdlcol, sdlcol_bg)
        elif style == Font.BLENDED:
            sur = TTF_RenderUTF8_Blended(self.__font, text.encode("utf-8"), sdlcol)
        else:
            log.write("get_surface() in Font object failed. Unknown style={}".format(style))
            return None

        if not sur:
            log.write("get_surface() in Font object failed. error={}".format(TTF_GetError()))
            return None

        return sur

    def get_texture(self, text, color=(255, 255, 255), style=0, bg_color=(0, 0, 0)):
        """
        textを画像化したテクスチャを取得する
    
        Args: 
            text (str): 画像化する文字列(utf-8)
            color (tuple): テキストの色(red, green, blue)
            style (int): Fontクラス内の定数を指定
            bg_color (tuple): テキストの背景色(red, green, blue) (Font.SHADEDのみ)

        Returns:
            Texture: Texture instance:成功 None:失敗
        """
        surface = self.get_surface(text, color, style, bg_color)
        if not surface:
            log.write("get_texture() in Font object failed.")
            return None

        texture = SDL_CreateTextureFromSurface(g.main_window_renderer, surface)
        if not texture:
            log.write("get_texture() in Font object failed. error={}".format(SDL_GetError()))
            SDL_FreeSurface(surface)
            return None

        texture_instance = Texture()
        texture_instance._Texture__texture = texture
        # サイズを取得する
        w = ctypes.c_int()
        h = ctypes.c_int()
        SDL_QueryTexture(texture, None, None, ctypes.byref(w), ctypes.byref(h))
        texture_instance._Texture__w = w.value
        texture_instance._Texture__h = h.value

        SDL_FreeSurface(surface)

        return texture_instance

    def draw(self, x, y, text, color=(255, 255, 255), style=0, bg_color=(0, 0, 0)):
        """
        文字列を描画する

        Note:
            主にデバッグ情報表示用。
            呼び出すたびにテクスチャを生成、開放するので遅い。
            大量に描画するならget_textureでテクスチャ化したほうが良い。
  
        Args:
            text (str): 文字列
            x (int): X座標
            y (int): Y座標
            color (tuple): 文字列の色(red, green, blue)
            style (int): Fontクラス内の定数
            bg_color (tuple): SHADEDで使用する背景色(red, green, blue)
        """
        texture = self.get_texture(text, color, style, bg_color)
        if not texture:
            log.write("draw() in Font object failed.")
            return

        texture.draw(x, y)
