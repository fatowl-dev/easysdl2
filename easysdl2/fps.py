# -*- coding: utf-8 -*-
"""
フレームレートを計算したり、フレームレートをキープしたりする
"""

from statistics import mean

from sdl2 import *

_FPS_INTERVAL = 30

_pf = 0  # 1秒あたりの分解能
_prev_count = 0
_fps_list = [0 for i in range(_FPS_INTERVAL)]
_frame_count = 0
_fps = 0


def _init():
    """
    モジュールの初期化
    """
    global _pf, _prev_count, _frame_count
    _pf = SDL_GetPerformanceFrequency()
    _prev_count = SDL_GetPerformanceCounter()
    _frame_count = 0


def wait(fps=60):
    """
    次回更新タイミングを待つ

    Args:
        fps (int): 1秒間の更新回数
    """
    if fps <= 0: fps = 999999
    global _prev_count, _frame_count, _fps
    next_count = _prev_count + _pf // fps
    while True:
        now_count = SDL_GetPerformanceCounter()
        if now_count >= next_count:
            i = _frame_count % _FPS_INTERVAL
            _fps_list[i] = _pf / (now_count - _prev_count)
            if i == _FPS_INTERVAL - 1:
                _fps = mean(_fps_list)
            _frame_count += 1
            _prev_count = now_count
            break
        SDL_Delay(0)


def get_fps():
    """
    現在のフレームレートを取得する
   
    Returns:
        float: フレームレート
    """
    return _fps
