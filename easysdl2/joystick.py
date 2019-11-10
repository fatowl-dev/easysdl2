# -*- coding: utf-8 -*-
"""
ジョイスティックを扱うクラスを定義します。
"""

from sdl2 import *

from . import log


class Joystick():
    """
    ジョイスティックを扱うクラス
    """

    @staticmethod
    def get_num():
        """
        使えるジョイスティックの数を得る

        Returns:
            int: ジョイスティックの数、エラー時-1
        """
        res = SDL_NumJoysticks()
        if res < 0:
            log.write("Joystick.get_num() failed. error={}".format(SDL_GetError()))
            return -1
        return res

    def __init__(self, index=-1):
        """
        初期化
       
        Args:
            index (int): ジョイスティックの番号。-1なら開かずにインスタンスのみ生成する 
        """
        self.__joystick = None
        if index >= 0:
            if not self.open(index):
                log.write("__init__() in Joystick object failed.")

    def __del__(self):
        """
        delされたらジョイスティックを開放
        """
        if self.__joystick:
            if SDL_WasInit(SDL_INIT_JOYSTICK):
                SDL_JoystickClose(self.__joystick)

    def open(self, index):
        """
        ジョイスティックを開く
       
        Args:
            index (int): ジョイスティックの番号。
        
        Returns:
            bool: True:成功 False:失敗
        """
        if self.__joystick:
            SDL_JoystickClose(self.__joystick)
            self.__joystick = None
        joystick = SDL_JoystickOpen(index)
        if not joystick:
            log.write("open() in Joystick object failed. error={}".format(SDL_GetError()))
            return False
        self.__joystick = joystick
        return True

    def get_num_axes(self):
        """
        軸の数を得る
        
        Returns:
            int: 軸の数。失敗は-1
        """
        if not self.__joystick:
            log.write("get_num_axes() in Joystick object failed. Not Opened.")
            return -1

        res = SDL_JoystickNumAxes(self.__joystick)
        if res < 0:
            log.write("get_num_axes() in Joystick object failed. error={}".format(SDL_GetError()))
            return -1
        return res

    def get_num_balls(self):
        """
        トラックボールの数を得る

        Returns:
            int: トラックボールの数。失敗は-1
        """
        if not self.__joystick:
            log.write("get_num_balls() in Joystick object failed. Not opened.")
            return -1

        res = SDL_JoystickNumBalls(self.__joystick)
        if res < 0:
            log.write("get_num_balls() in Joystick object failed. error={}".format(SDL_GetError()))
        return res

    def get_num_buttons(self):
        """
        ボタンの数を得る

        Returns:
            int: ボタンの数
        """
        if not self.__joystick:
            log.write("get_num_buttons() in Joystick object failed. Not opened.")
            return -1

        res = SDL_JoystickNumButtons(self.__joystick)
        if res < 0:
            log.write("get_num_buttons() in Joystick object failed. error={}".format(SDL_GetError()))
        return res

    def get_num_hats(self):
        """
        POVハットの数を得る

        Returns:
            int: POVハットの数。失敗は-1
        """
        if not self.__joystick:
            log.write("get_num_hats() in Joystick object failed. Not opened.")
            return -1

        res = SDL_JoystickNumHats(self.__joystick)
        if res < 0:
            log.write("get_num_hats() in Joystick object failed. error={}".format(SDL_GetError()))
        return res

    def get_name(self):
        """
        ジョイスティックの名前を得る

        Returns:
            str: ジョイスティックの名前。失敗は""
        """
        if not self.__joystick:
            log.write("get_name() in Joystick object failed. Not opened.")
            return -1

        res = SDL_JoystickName(self.__joystick)
        if not res:
            log.write("get_name in Joystick object failed. error={}".format(SDL_GetError()))
            return ""
        return res.decode("ascii")

    def get_axis(self, axis):
        """
        軸の傾きを得る
        
        Args:
            axis (int): 軸番号。通常は0がX軸、1がY軸らしい。追加のボタンが3、4になることもある。
        
        Returns:
            int: 成功:傾き(-32768～32767)
        """
        if not self.__joystick:
            log.write("get_axis() in Joystick object failed. Not opened.")
        res = SDL_JoystickGetAxis(self.__joystick, axis)
        # if res == 0: #リファレンスには0が失敗って書いてるけどそんなことなさそう
        #    log.write("get_axis() in Joystick object failed. error={}".format(SDL_GetError()))
        return res

    def get_ball(self, ball):
        """
        ボールの位置の前回習得との差を得る

        Args:
            ball (int): ボールの番号

        Returns:
            int: x軸の差
            int: y軸の差
        """
        if not self.__joystick:
            log.write("get_ball() in Joystick object failed. Not opened.")
            return 0, 0
        x = ctypes.c_int()
        y = ctypes.c_int()
        res = SDL_JoystickGetBall(self.__joystick, ball, ctypes.byref(x), ctypes.byref(y))
        if res < 0:
            log.write("get_ball() in Joystick object failed. error={}".format(SDL_GetError()))
            return 0, 0

        return x.value, y.value

    def get_button(self, button):
        """
        ボタンの状態を得る

        Aargs:
            button (int): ボタン番号

        Returns:
            bool: True:押されている False:押されていない
        """
        if not self.__joystick:
            log.write("get_button() in Joystick object failed. Not opened.")
            return False

        res = SDL_JoystickGetButton(self.__joystick, button)
        return (res != 0)

    def get_hat(self, hat):
        """
        POVハットの状態を得る

        Aargs:
            hat (int): POVハットの番号

        Returns:
            int: POVハットの状態を表す定数(SDL_HAT_***) 
        """
        return SDL_JoystickGetHat(self.joystick, hat)
