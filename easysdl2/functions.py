# coding: utf-8
#
# for easysdl2 interface  
#

import ctypes

from sdl2 import *
from sdl2.sdlimage import *
from sdl2.sdlmixer import *
from sdl2.sdlttf import *

from . import _common as g
from . import fps
from . import log


def init(img_init_flags=0, mix_init_flags=0):
    """
    モジュール全体の初期化

    Note:
        Windowsのdllだと何故かmix_init_flagsに0以外を渡すと失敗する。
        ファイルを読み込むときに初期化されるので大きな問題はない？
    
    Args:
        img_init_flags: SDL_Imageの初期化フラグ
        mix_init_flags: SDL_Mixerの初期化フラグ

    Returns:
        bool: True:成功 False:失敗
    """
    res = SDL_Init(g.sdl_init_flags)
    if res != 0:
        log.write("SDL_Init failed. error={}".format(SDL_GetError(res)))
        quit()
        return False

    res = IMG_Init(img_init_flags)
    if img_init_flags != res & img_init_flags:
        log.write("IMG_Init failed. code={}".format(res))
        quit()
        return False

    res = Mix_Init(mix_init_flags)
    if mix_init_flags != res & mix_init_flags:
        log.write("Mix_Init failed. code={}".format(res))
        quit()
        return False

    res = TTF_Init()
    if res == -1:
        log.write("TTF_Init failed. error={}".format(TTF_GetError()))
        quit()
        return False

    res = Mix_OpenAudio(MIX_DEFAULT_FREQUENCY, MIX_DEFAULT_FORMAT, 2, 1024)
    if res == -1:
        log.write("Mix_OpenAudio() failed. error={}".format(MixGetError()))
        quit()
        return False

    # デフォルトのチャンネル数を設定
    set_num_channel(g.DEFAULT_NUM_CHANNEL)

    # fps制御モジュールの初期化
    fps._init()


def quit():
    """
    モジュール全体の終了
    
    Returns:
        bool: True:成功 False:失敗
    """
    SDL_DestroyWindow(g.main_window)
    SDL_DestroyRenderer(g.main_window_renderer)

    Mix_CloseAudio()

    IMG_Quit()
    while Mix_Init(0):
        Mix_Quit()
    TTF_Quit()
    SDL_Quit()

    return True


def create_window(width=640, height=480, caption="SDL Window",
                  x=SDL_WINDOWPOS_CENTERED,
                  y=SDL_WINDOWPOS_CENTERED,
                  window_flags=SDL_WINDOW_SHOWN,
                  renderer_flags=0):
    """
    メインウィンドウを生成する
    
    Args:
        size: スクリーンの幅と高さのタプル
        caption: ウィンドウのタイトル(utf-8)
        x: ウィンドウのスクリーン座標系のX座標, SDL_WINDOWPOS_CENTERED, または SDL_WINDOWPOS_UNDEFINED
        y: ウィンドウのスクリーン座標系のY座標, SDL_WINDOWPOS_CENTERED, または SDL_WINDOWPOS_UNDEFINED
        window_flags: SDL_WindowFlagsの論理和
        renderer_flags: SDL_RendererFlagsの論理和(0だとSDL_RENDERER_ACCELERATEDになるらしい？
    
    Returns:
        bool: True:成功 False:失敗
    """
    window = SDL_CreateWindow(caption.encode("utf-8"),
                              x, y, int(width), int(height), window_flags)
    if not window:
        log.write("create_window() failed. error={}".format(SDL_GetError()))
        return False

    renderer = SDL_CreateRenderer(window, -1, renderer_flags)
    if not renderer:
        log.write("create_window() failed. error={}".format(SDL_GetError()))
        SDL_DestroyWindow(window)
        return False

    g.main_window = window
    g.main_window_renderer = renderer
    g.current_renderer = renderer


def process_events():
    """
    イベント処理を行う。
   
    Note: 
        メインループ内で必ず読んでください。
        この関数がFalseを返したらメインループを抜けるように。
        イベント処理を独自に行うにはフック関数を登録する。

    Returns:
        bool: False: SDL_QUITが処理された True: それ以外
    """
    retval = True
    event = SDL_Event()
    while SDL_PollEvent(ctypes.byref(event)) != 0:

        # 設定されたフック関数を実行
        if g.event_hooker:
            g.event_hooker(event)

        # 閉じるボタン
        if event.type == SDL_QUIT:
            retval = False

        # ここからキーボード入力
        elif event.type == SDL_KEYDOWN:
            # キーが押されたらフラグを立てる
            sym = event.key.keysym.sym
            g.key_flags[sym] = True

        elif event.type == SDL_KEYUP:
            # キーが離されたらフラグを折る
            sym = event.key.keysym.sym
            g.key_flags[sym] = False

        # ここからマウス入力
        elif event.type == SDL_MOUSEMOTION:
            g.mouse_x = event.motion.x
            g.mouse_y = event.motion.y

        elif event.type == SDL_MOUSEBUTTONDOWN:
            g.mouse_button_flags[event.button.button] = True
            g.mouse_x = event.button.x
            g.mouse_y = event.button.y

        elif event.type == SDL_MOUSEBUTTONUP:
            g.mouse_button_flags[event.button.button] = False
            g.mouse_x = event.button.x
            g.mouse_y = event.button.y

    return retval


def check_key(keycode):
    """
    SDL_Keycodeで指定したキーが押されているかを調べる

    Args:
        keycode: SDLK_*

    Returns:
        bool: True:押されている False:押されていない  
    """
    return g.key_flags[keycode]


def check_mouse_button(code):
    """
    マウスボタンが押されているか調べる

    Args:
        code: 調べるボタンのコード(SDL_BUTTON_LEFT SDL_BUTTON_MIDDLE SDL_BUTTON_RIGHT SDL_BUTTON_X1 SDL_BUTTON_X2)

    Returns:
        bool: True: 押されている False:押されていない
    """
    return g.mouse_button_flags[code]


def get_mouse_position():
    """
    Window内のマウスの座標を得る  
     
    Returns:
        tuple (int, int): 座標のタプル(x , y) 
    """
    return g.mouse_x, g.mouse_y


def set_event_hooker(hooker):
    """
    イベント処理を独自に行うためのフック関数を登録する

    hooker-> 第一引数にSDL_Eventオブジェクトをもつ関数
    """
    g.event_hooker = hooker


def clear_screen():
    """
    メインウィンドウのスクリーンを黒で塗りつぶす
    
    Returns:
        bool: True:成功 False: 失敗
    """
    ret = True
    # レンダラの描画色を保存しておく
    red = ctypes.c_uint8()
    green = ctypes.c_uint8()
    blue = ctypes.c_uint8()
    alpha = ctypes.c_uint8()
    res = SDL_GetRenderDrawColor(g.main_window_renderer,
                                 ctypes.byref(red), ctypes.byref(green),
                                 ctypes.byref(blue), ctypes.byref(alpha))
    if res < 0:
        log.write("clear_screen() failed. error={}".format(SDL_GetError()))
        ret = False
    # レンダラのブレンドモードを保存しておく
    mode = SDL_BlendMode()
    res = SDL_GetRenderDrawBlendMode(g.main_window_renderer, ctypes.byref(mode))
    if res < 0:
        log.write("clear_screen() failed. error={}".format(SDL_GetError()))
        ret = False

    # 黒で塗りつぶし
    res = SDL_SetRenderDrawColor(g.main_window_renderer, 0, 0, 0, 255)
    if res < 0:
        log.write("clear_screen() failed. error={}".format(SDL_GetError()))
        ret = False
    res = SDL_RenderClear(g.main_window_renderer)
    if res < 0:
        log.write("clear_screen() failed. error={}".format(SDL_GetError()))
        ret = False

    # レンダラの設定を元に戻す
    res = SDL_SetRenderDrawBlendMode(g.main_window_renderer, mode)
    if res < 0:
        log.write("clear_screen() failed. error={}".format(SDL_GetError()))
        ret = False
    res = SDL_SetRenderDrawColor(g.main_window_renderer, red, green, blue, alpha)
    if res < 0:
        log.write("clear_screen() failed. error={}".format(SDL_GetError()))
        ret = False

    return ret


def update_screen():
    """
    メインウィンドウの変更を表示する
    """
    SDL_RenderPresent(g.main_window_renderer)


def set_num_channel(num):
    """
    サウンド再生のチャンネル数を設定する

    Args:
        num (int): チャンネル数
    """
    Mix_AllocateChannels(num)


def stop_all_sounds():
    """
    すべてのサウンドの再生を止める
    """
    Mix_HaltChannel(-1)
