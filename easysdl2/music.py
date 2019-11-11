# -*- coding: utf-8 -*-
"""
音楽を扱うクラスを定義します。
"""

from sdl2.sdlmixer import *

from . import log


class Music():
    """
    音楽を扱うクラス。
    
    Note:
        ストリーミングされるのでBGM等の長い音声はこちらで再生する
    """

    # --- static metods ---

    @staticmethod
    def set_volume(volume):
        """
        音量を設定。
        
        Note: 
            すべてのMusicに適用される
        
        Args:
            volume (int): 0〜128
        """
        Mix_VolumeMusic(volume)

    @staticmethod
    def get_volume():
        """
        音楽の音量を調べる
        
        Returns:
            int: 現在の音量
        """
        ret = Mix_VolumeMusic(-1)
        return ret

    @staticmethod
    def stop():
        """
        音楽を停止する
        """
        Mix_HaltMusic()

    # --- methods ---

    def __init__(self, filename=""):
        """
        filenameを指定しなければ何もしない
        """
        self.__music = None
        if filename:
            if not self.load(filename):
                log.write("__init__() in Music object failed.")

    def __del__(self):
        """
        delされたらmusicを開放
        """
        if self.__music:
            Mix_FreeMusic(self.__music)

    def load(self, filename):
        """
        音楽ファイルを読み込む
        
        Args:
            filename (str): ファイルのパス(utf-8)
        
        Returns:
            bool: True:成功 False:失敗
        """
        if self.__music:
            Mix_FreeMusic(self.__music)
            self.__music = None

        music = Mix_LoadMUS(filename.encode("utf-8"))
        if not music:
            log.write("load('{}') in Music object failed. error={}".format(filename, Mix_GetError()))
            return False
        self.__music = music
        return True

    def play(self, loops=-1):
        """
        音楽を再生する

        Args:
            loops (int): ループ回数。-1で無限ループ
        
        Returns:
            bool: True:成功 False:失敗
        """
        if not self.__music:
            log.write("play() in Music object failed. Not loaded.")
            return False

        res = Mix_PlayMusic(self.__music, loops)
        if res == -1:
            log.write("play() in Music object failed. error={}".format(Mix_GetError()))
            return False

        return True
