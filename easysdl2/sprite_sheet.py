# -*- coding: utf-8 -*-
"""
スプライトシート
メモリーの節約のため一つの画像を複数の画像として扱えるクラス
"""
from easysdl2 import Rect, SDL_DestroyTexture, SDL_Rect, SDL_Point, SDL_RenderCopyEx, SDL_RenderCopy, log, \
    SDL_FLIP_HORIZONTAL, SDL_FLIP_VERTICAL, SDL_SetTextureBlendMode, SDL_GetError, SDL_SetTextureAlphaMod, \
    SDL_SetTextureColorMod, SDL_BLENDMODE_NONE, SDL_FLIP_NONE, SDL_Texture, IMG_LoadTexture, IMG_GetError, Texture, \
    SDL_BLENDMODE_BLEND

from . import _common as g


class SpriteSheetFrame:
    """
    スプライトシートの1フレームの情報を格納するクラス
    """

    def __init__(self):
        self.name = ''
        self.texture_index = -1
        self.frame = Rect()
        self.pivot_x = 0
        self.pivot_y = 0


class SpriteSheetBlendParam:
    """
    スプライトシートのブレンド情報を格納するクラス
    """

    def __init__(self):
        self.red = 255
        self.green = 255
        self.blue = 255
        self.alpha = 255
        self.blend_mode = SDL_BLENDMODE_BLEND


class SpriteSheet:
    """
    画像を複数に分割して扱うためのクラス
    複数画像の登録にも対応
    """

    def __init__(self):
        """
        コンストラクタ
        """
        self.__frames = []
        self.__textures = []
        self.__texture_files = []
        self.__w = 0
        self.__h = 0
        self.__blend_param = SpriteSheetBlendParam()

    def __del__(self):
        """
        デストラクタ

        Note:
            delするとテクスチャを開放する
        """
        for texture in self.__textures:
            if texture:
                del texture

        del self.__frames[:]
        del self.__texture_files[:]

    def add_texture(self, file_path: str):
        """
        テクスチャを追加する

        Args:
            file_path (str): 画像ファイルのパス

        Returns:
            テクスチャ番号
        """
        texture = Texture(file_path)
        self.__textures.append(texture)
        self.__texture_files.append(file_path)

        return len(self.__textures) - 1

    def add_sprite(self, name, texture_index, rect):
        """
        スプライトを追加する

        Args:
            name (str): 一意の名前
            texture_index (int): 元になるテクスチャのインデックス
            rect (Rect): 切り出す範囲

        Note:
            表示、回転、拡縮の原点の設定を追加するかどうか？

        Returns:
            正の整数: スプライト番号
            -1: エラー
        """
        if texture_index >= len(self.__textures):
            log.error_log("Invalid texture index", "draw", "SpriteSheet")
            return -1
        frame = SpriteSheetFrame()
        frame.texture_index = texture_index
        frame.frame = rect
        frame.pivot_x = 0.5
        frame.pivot_y = 0.5
        frame.name = name
        self.__frames.append(frame)

    def draw(self, index, x, y):
        """
        画像を表示する

        Note:
            指定座標はpivotの位置になる。
            SDL_RenderCopyを使うのでdraw_exより速い。
            ただし、rotatedフラグが立っているとSDL_RenderCopyExを使う。

        Args:
            index (int): 画像のインデックス
            x (int): X座標
            y (int): Y座標
        """
        if len(self.__textures) == 0:
            log.error_log("not loaded", "draw", "SpriteSheet")
            return
        if index < 0 or index >= len(self.__frames):
            log.error_log("index out of range", "draw", "SpriteSheet")
            return

        frame = self.__frames[index]
        rect = frame.frame

        w, h = rect.w, rect.h
        px, py = frame.pivot_x, frame.pivot_y

        x -= w * px
        y -= h * py
        srcrect = SDL_Rect(rect.x, rect.y, w, h)
        dstrect = SDL_Rect(int(x), int(y), int(w), int(h))
        texture = self.__textures[frame.texture_index].get_texture()
        self.__set_blend_param_to_texture(texture)
        SDL_RenderCopy(g.current_renderer, texture, srcrect, dstrect)

    def draw_ex(self, index, x, y, ex_x=1.0, ex_y=1.0, angle=0.0, flip_h=False, flip_v=False):
        """
        画像を拡大縮小回転反転描画する

        Note:
            指定座標はpivotの位置になる

        Args:
            index (int): 画像のインデックス
            x (int): X座標
            y (int): Y座標
            ex_x (float): X軸方向の拡大率
            ex_y (float): Y軸方向の拡大率
            angle (float): 回転量(度数法)
            flip_h (bool): 左右反転フラグ
            flip_v (bool): 上下反転フラグ
        """
        if len(self.__textures) == 0:
            log.error_log("not loaded", "draw", "SpriteSheet")
            return
        if index < 0 or index >= len(self.__frames):
            log.error_log("index out of range", "draw", "SpriteSheet")
            return

        flip = 0
        if flip_h:
            flip |= SDL_FLIP_HORIZONTAL
        if flip_v:
            flip |= SDL_FLIP_VERTICAL

        frame = self.__frames[index]
        rect = frame.frame

        rw, rh = rect.w, rect.h
        px, py = frame.pivot_x, frame.pivot_y

        w = rw * ex_x
        h = rh * ex_y
        x -= rw * px * ex_x
        y -= rh * py * ex_y
        srcrect = SDL_Rect(rect.x, rect.y, rw, rh)
        dstrect = SDL_Rect(int(x), int(y), int(w), int(h))
        pt = SDL_Point(int(rw * px * ex_x), int(rh * py * ex_y))
        texture = self.__textures[frame.texture_index].get_texture()
        self.__set_blend_param_to_texture(texture)
        SDL_RenderCopyEx(g.current_renderer, texture, srcrect, dstrect, angle, pt, flip)

    def get_index(self, name):
        """
        スプライトの識別名からインデックスを得る

        Args:
            name (str): スプライトの識別名

        Returns:
            int: テクスチャのインデックス。失敗は-1
        """
        ret = -1
        i = 0
        for f in self.__frames:
            if f.name == name:
                ret = i
                break
            i += 1
        return ret

    def __set_blend_param_to_texture(self, texture):
        SDL_SetTextureBlendMode(texture, self.__blend_param.blend_mode)
        SDL_SetTextureAlphaMod(texture, self.__blend_param.alpha)
        SDL_SetTextureColorMod(texture, self.__blend_param.red, self.__blend_param.green, self.__blend_param.blue)

    def set_blend_param(self, red=255, green=255, blue=255, alpha=255, mode=SDL_BLENDMODE_BLEND):
        """
        ブレンドパラメータを設定する

        Args:
            red (int): 赤要素(0〜255)
            green (int): 緑要素(0〜255)
            blue (int): 青要素(0〜255)
            alpha (int): 不透明度(0〜255)
            mode (int): SDL_BLENDMODE_XXXXで定義されいるブレンドモード
        """
        self.__blend_param.r = red
        self.__blend_param.g = green
        self.__blend_param.b = blue
        self.__blend_param.a = alpha
        self.__blend_param.mode = mode
