# -*- coding: utf-8 -*-
"""
sdl_gfxを使わない図形描画関数を定義します
"""

from . import _common as gl
from . import log
from .functions import *


def color(r, g, b, a=255):
    """
    描画する色を設定する
    
    Args:
        r (int): 赤成分(0〜255)
        g (int): 緑成分(0〜255)
        b (int): 青成分(0〜255)
        a (int): 不透明度(0〜255)
    
    Returns:
        bool: True:成功 False:失敗
    """
    res = SDL_SetRenderDrawColor(gl.current_renderer, r, g, b, a)
    if res < 0:
        log.write("draw.color() failed. error={}".format(SDL_GetError()))
        return False
    return True


def blend_mode(mode):
    """
    描画に使うブレンドモードを指定する
    
    Args:
        mode (SDL_BlendMode): ブレンドモード(DL_BLENDMODE_NONE, SDL_BLENDMODE_BLEND, SDL_BLENDMODE_ADD, SDL_BLENDMODE_MOD)

    Returns:
        bool: True:成功 False:失敗
    """
    res = SDL_SetRenderDrawBlendMode(gl.current_renderer, mode)
    if res < 0:
        log.write("draw.blend_mode() failed. error={}".format(SDL_GetError()))
        return False
    return True


def point(x, y):
    """
    点を描画する

    Args:
        x (int): X座標
        y (int): Y座標

    Returns:
        bool: True:成功 False:失敗
    """
    res = SDL_RenderDrawPoint(gl.current_renderer, int(x), int(y))
    if res < 0:
        log.write("draw.point() failed. error={}".format(SDL_GetError()))
        return False
    return True


def points(point_list):
    """
    点を複数描画する

    Args:
        point_list (list): 点の座標を格納したタプルのリスト[(x, y), (x, y)..]

    Returns:
        bool: True:成功 False:失敗
    """
    length = len(point_list)
    ARRTYPE = SDL_Point * length
    arr = ARRTYPE(*(SDL_Point(x, y) for x, y in point_list))
    res = SDL_RenderDrawPoints(gl.current_renderer, arr, length)
    if res < 0:
        log.write("draw.points() failed. error={}".format(SDL_GetError()))
        return False
    return True


def line(x1, y1, x2, y2):
    """
    直線を描画する

    Args:
        x1 (int): 始点のX座標
        y1 (int): 始点のY座標
        x2 (int): 終点のX座標
        y2 (int): 終点のY座標

    Returns:
        bool: True:成功 False:失敗
    """
    res = SDL_RenderDrawLine(gl.current_renderer, int(x1), int(y1), int(x2), int(y2))
    if res < 0:
        log.write("draw.line() failed. error={}".format(SDL_GetError()))
        return False
    return True


def lines(point_list):
    """
    直線をつなげて複数描画する

    Args:
        point_list (list): 点の座標を格納したタプルのリスト[(x, y), (x, y)..]
    
    Returns:
        bool: True:成功 False:失敗
    """
    length = len(point_list)
    ARRTYPE = SDL_Point * length
    arr = ARRTYPE(*(SDL_Point(x, y) for x, y in point_list))
    res = SDL_RenderDrawLines(gl.current_renderer, arr, length)
    if res < 0:
        log.write("draw.points() failed. error={}".format(SDL_GetError()))
        return False
    return True


def rect(x, y, w, h):
    """
    長方形を描く
    
    Args:
        x (int): 長方形の左端のX座標
        y (int): 長方形の上端のY座標
        w (int): 長方形の幅
        h (int): 長方形の高さ

    Returns:
        bool: True:成功 False:失敗
    """
    res = SDL_RenderDrawRect(gl.current_renderer, SDL_Rect(int(x), int(y), int(w), int(h)))
    if res < 0:
        log.write("draw.rect() failed. error={}".format(SDL_GetError()))
        return False
    return True


def rects(rect_list):
    """
    長方形を複数描く

    Args:
        rect_list (list): 長方形の座標、サイズを格納したタプルのリスト[(x,y,w,h), (x,y,w,h)...]

    Returns:
        bool: True:成功 False:失敗
    """
    length = len(rect_list)
    ARRTYPE = SDL_Rect * length
    arr = ARRTYPE(*(SDL_Rect(int(x), int(y), int(w), int(h)) for x, y, w, h in rect_list))
    res = SDL_RenderDrawRects(gl.current_renderer, arr, length)
    if res < 0:
        log.write("draw.rects() failed. error={}".format(SDL_GetError()))
        return False
    return True


def fill_rect(x, y, w, h):
    """
    塗りつぶしの長方形を描く
    
    Args:
        x (int): 長方形の左端のX座標
        y (int): 長方形の上端のY座標
        w (int): 長方形の幅
        h (int): 長方形の高さ

    Returns:
        bool: True:成功 False:失敗
    """
    res = SDL_RenderFillRect(gl.current_renderer, SDL_Rect(int(x), int(y), int(w), int(h)))
    if res < 0:
        log.write("draw.fill_rect() failed. error={}".format(SDL_GetError()))
        return False
    return True


def fill_rects(rect_list):
    """
    塗りつぶしの長方形を複数描く

    Args:
        rect_list (list): 長方形の座標、サイズを格納したタプルのリスト[(x,y,w,h), (x,y,w,h)...]

    Returns:
        bool: True:成功 False:失敗
    """
    length = len(rect_list)
    ARRTYPE = SDL_Rect * length
    arr = ARRTYPE(*(SDL_Rect(int(x), int(y), int(w), int(h)) for x, y, w, h in rect_list))
    res = SDL_RenderFillRects(gl.current_renderer, arr, length)
    if res < 0:
        log.write("draw.fill_rects() failed. error={}".format(SDL_GetError()))
        return False
    return True
