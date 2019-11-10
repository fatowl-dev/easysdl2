# -*- coding: utf-8 -*-
"""
easysdl2パッケージ内で共通で使う変数、定数
"""

from collections import defaultdict

from sdl2 import *

# 定数
DEFAULT_NUM_CHANNEL = 10  # 効果音再生時のデフォルトのチャンネル数

# 初期化フラグ
sdl_init_flags = SDL_INIT_EVERYTHING

# メインウィンドウの描画に関係するもの
main_window = None
main_window_renderer = None
current_renderer = None  # 描画に使用するレンダラ

# イベント処理系
event_hooker = None  # SDL_Eventを独自処理するためのフック関数

key_flags = defaultdict(lambda: False)  # キーボード押下状態を保存する辞書。SDL_Keycodeをkeyにして状態を保存する
mouse_x = 0
mouse_y = 0
mouse_button_flags = defaultdict(lambda: False)  # マウスボタンの押下状態を保存する辞書
