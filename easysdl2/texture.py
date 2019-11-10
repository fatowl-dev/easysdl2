# -*- coding: utf-8 -*-
"""
テクスチャ（画像）を扱うクラスを定義します。
"""

import ctypes
import json
import os

from sdl2 import *
from sdl2.sdlimage import *

from . import _common as g
from . import log


class Rect():
    """
    長方形のクラス。主にコピー元、コピー先の指定に使う。
    """

    def __init__(self, x=0, y=0, w=0, h=0):
        """
        コンストラクタ

        Args:
            x (int): x座標
            y (int): y座標
            w (int): 幅
            h (int): 高さ
        """
        self.x = x
        self.y = y
        self.w = w
        self.h = h


class Texture():
    """
    画像ファイルからテクスチャを読み込み、表示するためのクラス
    """

    # 定数
    BLEND_NONE = SDL_BLENDMODE_NONE
    BLEND_ALPHA = SDL_BLENDMODE_BLEND
    BLEND_ADD = SDL_BLENDMODE_ADD
    BLEND_MOD = SDL_BLENDMODE_MOD
    """
    Note:
        ブレンドモードの定数はSDLのものを使っても良い
    """

    def __init__(self, filename=""):
        """
        コンストラクタ

        Note:
            filenameをしてしなければインスタンのみ生成し、後でload()できる。

        Args:
            filename: ロードする画像ファイルのパス(utf-8)
        """
        self.__texture = None
        self.__w = 0
        self.__h = 0
        if filename:
            if not self.load(filename):
                log.error_log("failed", "__init__", "Texture")

    def __del__(self):
        """
        デストラクタ
        
        Note:
            delするとテクスチャを開放する
        """
        if self.__texture:
            SDL_DestroyTexture(self.__texture)

    def load(self, filename):
        """
        画像を読み込む
        
        Args: 
            filename (str): 読み込む画像ファイルのパス(utf-8)
    
        Returns: 
            bool: True:成功 False:失敗
        """
        if self.__texture:
            SDL_DestroyTexture(self.__texture)
            self.__texture = None

        texture = IMG_LoadTexture(g.current_renderer, filename.encode("utf-8"))
        if not texture:
            log.error_log(IMG_GetError(), "load", "Texture", filename)
            return False
        self.__texture = texture

        # サイズを取得する
        w = ctypes.c_int()
        h = ctypes.c_int()
        SDL_QueryTexture(self.__texture, None, None, ctypes.byref(w), ctypes.byref(h))
        self.__w = w.value
        self.__h = h.value
        return True

    def draw(self, x, y):
        """
        画像を描画する
       
        Note:
            指定座標は画像の左上端になる。
        
        Args: 
            x (int): X座標
            y (int): Y座標
        """
        if not self.__texture:
            log.error_log("not loaded", "draw", "Texture")
            return

        dstrect = SDL_Rect(int(x), int(y), int(self.__w), int(self.__h))
        SDL_RenderCopy(g.current_renderer, self.__texture, None, dstrect)

    def draw_crop(self, rect, x, y):
        """
        元画像を切り取って描画する

        Note:
            指定座標は画像の左上端になる。
        
        Args: 
            rect (Rect): 切り取る範囲
            x (int): X座標
            y (int): Y座標
        """
        if not self.__texture:
            log.error_log("not loaded", "draw_crop", "Texture")
            return
        srcrect = SDL_Rect(int(rect.x), int(rect.y), int(rect.w), int(rect.h))
        dstrect = SDL_Rect(int(x), int(y), int(self.__w), int(self.__h))
        SDL_RenderCopy(g.current_renderer, self.__texture, srcrect, dstrect)

    def draw_center(self, x, y):
        """
        指定座標を画像の中心として描画する。
      
        Note:
            SDL_RenderCopyを使うのでdraw_exより速い？
       
        Args: 
            x (int): X座標
            y (int): Y座標
        """
        if not self.__texture:
            log.error_log("not loaded", "draw", "Texture")
            return
        x = x - self.__w / 2
        y = y - self.__h / 2
        dstrect = SDL_Rect(int(x), int(y), int(self.__w), int(self.__h))
        SDL_RenderCopy(g.current_renderer, self.__texture, None, dstrect)

    def draw_crop_center(self, rect, x, y):
        """
        指定座標を切り取った画像の中心として描画する。
       
        Note:
            SDL_RenderCopyを使うのでdraw_exより速い？

        Args: 
            rect (Rect): 切り取る範囲
            x (int): X座標
            y (int): Y座標
        """
        if not self.__texture:
            log.error_log("not loaded", "draw_crop_center", "Texture")
            return
        x = x - self.__w / 2
        y = y - self.__h / 2
        srcrect = SDL_Rect(int(rect.x), int(rect.y), int(rect.w), int(rect.h))
        dstrect = SDL_Rect(int(x), int(y), int(self.__w), int(self.__h))
        SDL_RenderCopy(g.current_renderer, self.__texture, srcrect, dstrect)

    def draw_ex(self, x, y, ex_x=1.0, ex_y=1.0, angle=0.0, flip_h=False, flip_v=False):
        """
        画像を拡大縮小回転反転描画する
        
        Note:
            指定座標は画像の中心になる
       
        Args:
            x (int): X座標
            y (int): Y座標
            ex_x (float): X軸方向の拡大率
            ex_y (float): Y軸方向の拡大率
            angle (float): 回転量(度数法) 
            flip_h (bool): 左右反転フラグ
            flip_v (bool): 上下反転フラグ
        """
        if not self.__texture:
            log.error_log("not loaded", "draw_ex", "Texture")
            return
        flip = 0
        if flip_h:
            flip |= SDL_FLIP_HORIZONTAL
        if flip_v:
            flip |= SDL_FLIP_VERTICAL

        w = self.__w * ex_x
        h = self.__h * ex_y
        x -= w / 2
        y -= h / 2
        dstrect = SDL_Rect(int(x), int(y), int(w), int(h))
        SDL_RenderCopyEx(g.current_renderer, self.__texture, None, dstrect, angle, None, flip)

    def draw_crop_ex(self, rect, x, y, ex_x=1.0, ex_y=1.0, angle=0.0, flip_h=False, flip_v=False):
        """
        画像を切り取って拡大縮小回転反転描画する
        
        Note:
            指定座標は画像の中心になる
       
        Args:
            rect (Rect): 切り取る範囲
            x (int): X座標
            y (int): Y座標
            ex_x (float): X軸方向の拡大率
            ex_y (float): Y軸方向の拡大率
            angle (float): 回転量(度数法) 
            flip_h (bool): 左右反転フラグ
            flip_v (bool): 上下反転フラグ
        """
        if not self.__texture:
            log.error_log("not loaded", "draw_crop_ex", "Texture")
            return
        flip = 0
        if flip_h:
            flip |= SDL_FLIP_HORIZONTAL
        if flip_v:
            flip |= SDL_FLIP_VERTICAL

        w = rect.w * ex_x
        h = rect.h * ex_y
        x -= w / 2
        y -= h / 2
        srcrect = SDL_Rect(int(rect.x), int(rect.y), int(rect.w), int(rect.h))
        dstrect = SDL_Rect(int(x), int(y), int(w), int(h))
        SDL_RenderCopyEx(g.current_renderer, self.__texture, srcrect, dstrect, angle, None, flip)

    def render_copy(self, srcrect, dstrect):
        """
        SDL_RenderCopyをそのまま使う

        Args:
            srcrect (Rect): コピー元の範囲
            dstrect (Rect): コピー先の範囲
        """
        if not self.__texture:
            log.error_log("not loaded", "render_copy", "Texture")
            return
        srcrect_sdl = SDL_Rect(int(srcrect.x), int(srcrect.y), int(srcrect.w), int(srcrect.h))
        dstrect_sdl = SDL_Rect(int(dstrect.x), int(dstrect.y), int(dstrect.w), int(dstrect.h))
        SDL_RenderCopy(g.current_renderer, self.__texture, srcrect_sdl, dstrect_sdl)

    def render_copy_ex(self, srcrect, dstrect, angle=0.0, center=None, flip=SDL_FLIP_NONE):
        """
        SDL_RenderCopyExをそのまま使う

        Args:
            srcrect (Rect): コピー元の範囲
            dstrect (Rect): コピー先の範囲
            angle (float): 回転角度(度数法)
            center (SDL_Point): 回転の中心点
            flip (SDL_RendererFlip): 上下左右反転フラグの論理和(SDL_FLIP_NONE SDL_FLIP_HORIZONTAL SDL_FLIP_VERTICAL) 
        """
        if not self.__texture:
            log.error_log("not loaded", "render_copy_ex", "Texture")
            return
        srcrect_sdl = SDL_Rect(int(srcrect.x), int(srcrect.y), int(srcrect.w), int(srcrect.h))
        dstrect_sdl = SDL_Rect(int(dstrect.x), int(dstrect.y), int(dstrect.w), int(dstrect.h))
        SDL_RenderCopyEx(g.current_renderer, self.__texture, srcrect_sdl, dstrect_sdl, angle, center, flip)

    def set_blend_mode(self, mode):
        """
        テクスチャのブレンドモードを設定
       
        Args:
            mode (SDL_BlendMode): SDLのブレンドモード
    
        Returns:
            bool: True:成功 False:失敗
        """
        res = SDL_SetTextureBlendMode(self.__texture, mode)
        if res < 0:
            log.error_log(SDL_GetError(), "set_blend_mode", "Texture")
            return False
        return True

    def set_blend_alpha(self, alpha):
        """
        テクスチャのコピー時の不透明度を設定する
    
        Args:
            alpha (int): 不透明度(0-255)
   
        Returns:
            bool: True:成功 False:失敗        
        """
        res = SDL_SetTextureAlphaMod(self.__texture, alpha)
        if res < 0:
            log.error_log(SDL_GetError(), "set_blend_alpha", "Textrue")
            return False
        return True

    def set_blend_color(self, red, green, blue):
        """
        テクスチャのコピー時に乗算される色を設定
  
        Args:
            red (int): 赤要素(0〜255) 
            green (int): 緑要素(0〜255) 
            blue (int): 青要素(0〜255) 

        Returns:
            bool: True:成功 False:失敗
        """
        res = SDL_SetTextureColorMod(self.__texture, red, green, blue)
        if res < 0:
            log.error_log(SDL_GetError(), "set_blend_color", "Textrue")
            return False
        return True

    def set_blend(self, mode=SDL_BLENDMODE_NONE, red=255, green=255, blue=255, alpha=255):
        """
        コピー時のブレンドパラメータ一括指定
       
        Args: 
            mode (SDL_BlendMode): SDLのブレンドモード
            red (int): 赤要素(0〜255) 
            green (int): 緑要素(0〜255) 
            blue (int): 青要素(0〜255) 
            alpha (int): 不透明度(0〜255)
            
        Returns:
            bool: True:成功 False:失敗
        """
        ret = True
        if not self.set_blend_mode(mode): ret = False
        if not self.set_blend_alpha(alpha): ret = False
        if not self.set_blend_color(red, green, blue): ret = False
        return ret


class TextureAtlasFrame():
    """
    テクスチャアトラスの1フレームの情報を格納するクラス
    """

    def __init__(self):
        self.filename = ""
        self.frame = Rect()
        self.rotated = False
        # self.trimmed = False
        # self.spriteSourceSize = Rect()
        # self.sourceWidth = 0
        # self.sourceHeight = 0
        self.pivotX = 0
        self.pivotY = 0


class TextureAtlas():
    """
    jsonファイルからテクスチャアトラスの情報を読み取り、表示するためのクラス。
    TexturePackerのjson(array)と同じ形式
    """

    def __init__(self, filename=""):
        """
        コンストラクタ

        Note:
            filenameをしてしなければインスタンのみ生成し、後でload()できる。

        Args:
            filename: ロードする画像ファイルのパス(utf-8)
        """
        self.__frames = []
        self.__texture = None
        self.__texture_file = ""
        self.__w = 0
        self.__h = 0
        if filename:
            if not self.load(filename):
                log.error_log("failed", "__init__", "TextrueAtlas")

    def __del__(self):
        """
        デストラクタ
        
        Note:
            delするとテクスチャを開放する
        """
        if self.__texture:
            SDL_DestroyTexture(self.__texture)

        del self.__frames[:]

    def load(self, filename):
        """
        テクスチャアトラスを読み込む
        
        Args: 
            filename (str): 読み込むjosnファイルのパス(utf-8)
    
        Returns: 
            bool: True:成功 False:失敗
        """
        if len(self.__frames) > 0:
            del self.__frames[:]

        try:
            with open(filename) as fi:
                data = json.load(fi)

            meta = data["meta"]
            path, fn = os.path.split(filename)
            self.__texture_file = path + os.path.sep + meta["image"]
            frames = data["frames"]
            for frm in frames:
                taf = TextureAtlasFrame()
                taf.filename = str(frm["filename"])
                rect = frm["frame"]
                taf.frame.x = int(rect["x"])
                taf.frame.y = int(rect["y"])
                taf.frame.w = int(rect["w"])
                taf.frame.h = int(rect["h"])
                taf.rotated = frm["rotated"]
                # taf.trimmed = frm["trimmed"]
                # rect = frm["spriteSourceSize"]
                # taf.spriteSourceSize.x = int(rect["x"])
                # taf.spriteSourceSize.y = int(rect["y"])
                # taf.spriteSourceSize.w = int(rect["w"])
                # taf.spriteSourceSize.h = int(rect["h"])
                # size = frm["sourceSize"]
                # taf.sourceWidth = int(size["w"])
                # taf.sourceHeight = int(size["h"])
                pt = frm["pivot"]
                taf.pivotX = float(pt["x"])
                taf.pivotY = float(pt["y"])

                self.__frames.append(taf)

        except Exception:
            log.error_log("Invalid json file", "load", "TextrueAtlas", filename)
            self.__texture_file = ""
            del self.__frames[:]
            return False

        if self.__texture:
            SDL_DestroyTexture(self.__texture)
            self.__texture = None

        texture = IMG_LoadTexture(g.main_window_renderer, self.__texture_file.encode("utf-8"))
        if not texture:
            log.error_log(IMG_GetError(), "load", "TextrueAtlas", self.__texture_file)
            self.__texture_file = ""
            del self.__frames[:]
            return False
        self.__texture = texture

        # サイズを取得する
        w = ctypes.c_int()
        h = ctypes.c_int()
        SDL_QueryTexture(self.__texture, None, None, ctypes.byref(w), ctypes.byref(h))
        self.__w = w.value
        self.__h = h.value
        return True

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
        if not self.__texture:
            log.error_log("not loaded", "draw", "TextrueAtlas")
            return

        if index < 0 or index >= len(self.__frames):
            log.error_log("index out of range", "draw_ex", "TextrueAtlas")
            return

        frame = self.__frames[index]
        rect = frame.frame

        if frame.rotated:
            w, h = rect.h, rect.w
            px, py = -frame.pivotY, frame.pivotX
        else:
            w, h = rect.w, rect.h
            px, py = frame.pivotX, frame.pivotY

        x -= w * px
        y -= h * py
        srcrect = SDL_Rect(rect.x, rect.y, w, h)
        dstrect = SDL_Rect(int(x), int(y), int(w), int(h))
        if frame.rotated:
            pt = SDL_Point(int(w * px), int(h * py))
            SDL_RenderCopyEx(g.current_renderer, self.__texture, srcrect, dstrect, -90, pt, SDL_FLIP_NONE)
        else:
            SDL_RenderCopy(g.current_renderer, self.__texture, srcrect, dstrect)

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
        if not self.__texture:
            log.error_log("not loaded", "draw_ex", "TextrueAtlas")
            return
        if index < 0 or index >= len(self.__frames):
            log.error_log("index out of range", "draw_ex", "TextrueAtlas")
            return

        flip = 0
        if flip_h:
            flip |= SDL_FLIP_HORIZONTAL
        if flip_v:
            flip |= SDL_FLIP_VERTICAL

        frame = self.__frames[index]
        rect = frame.frame

        if frame.rotated:
            rw, rh = rect.h, rect.w
            ex_x, ex_y = ex_y, ex_x
            px, py = -frame.pivotY, frame.pivotX
            angle -= 90
        else:
            rw, rh = rect.w, rect.h
            px, py = frame.pivotX, frame.pivotY

        w = rw * ex_x
        h = rh * ex_y
        x -= rw * px * ex_x
        y -= rh * py * ex_y
        srcrect = SDL_Rect(rect.x, rect.y, rw, rh)
        dstrect = SDL_Rect(int(x), int(y), int(w), int(h))
        pt = SDL_Point(int(rw * px * ex_x), int(rh * py * ex_y))
        SDL_RenderCopyEx(g.current_renderer, self.__texture, srcrect, dstrect, angle, pt, flip)

    def get_index(self, filename):
        """
        ファイル名（テクスチャの識別名）からインデックスを得る

        Args:
            filename (str): テクスチャの識別名(filename要素)
        
        Returns:
            int: テクスチャのインデックス。失敗は-1
        """
        ret = -1
        i = 0
        for f in self.__frames:
            if f.filename == filename:
                ret = i
                break
            i += 1
        return ret

    def set_blend_mode(self, mode):
        """
        テクスチャのブレンドモードを設定
       
        Args:
            mode (SDL_BlendMode): SDLのブレンドモード
    
        Returns:
            bool: True:成功 False:失敗
        """
        res = SDL_SetTextureBlendMode(self.__texture, mode)
        if res < 0:
            log.error_log(SDL_GetError(), "set_blend_mode", "TextrueAtlas")
            return False
        return True

    def set_blend_alpha(self, alpha):
        """
        テクスチャのコピー時の不透明度を設定する
    
        Args:
            alpha (int): 不透明度(0-255)
   
        Returns:
            bool: True:成功 False:失敗        
        """
        res = SDL_SetTextureAlphaMod(self.__texture, alpha)
        if res < 0:
            log.error_log(SDL_GetError(), "set_blend_alpha", "TextrueAtlas")
            return False
        return True

    def set_blend_color(self, red, green, blue):
        """
        テクスチャのコピー時に乗算される色
  
        Args:
            red (int): 赤要素(0〜255) 
            green (int): 緑要素(0〜255) 
            blue (int): 青要素(0〜255) 

        Returns:
            bool: True:成功 False:失敗
        """
        res = SDL_SetTextureColorMod(self.__texture, red, green, blue)
        if res < 0:
            log.error_log(SDL_GetError(), "set_blend_color", "TextrueAtlas")
            return False
        return True

    def set_blend(self, mode=SDL_BLENDMODE_NONE, red=255, green=255, blue=255, alpha=255):
        """
        コピー時のブレンドパラメータ一括指定
        
        Returns:
            bool: True:成功 False:失敗
        """
        ret = True
        if not self.set_blend_mode(mode): ret = False
        if not self.set_blend_alpha(alpha): ret = False
        if not self.set_blend_color(red, green, blue): ret = False
        return ret
