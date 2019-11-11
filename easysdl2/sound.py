# -*- coding: utf-8 -*-
"""
テクスチャ（画像）を扱うクラスを定義します。
"""
from . import log
from .functions import *


class Sound:
    """
    サウンド（SE)を扱うクラス
    
    Note: 
        一時停止などはMix_PauseなどのSDL_Mixierの関数を直接使う。
        多重再生は自動化すると煩雑で無駄が多いため使用者が管理することにする
    """

    def __init__(self, filename=""):
        """
        コンストラクタ

        Note:
            ファイル名を指定しなければインスタンスのみ生成し、後でload()できる。
        """
        self.__chunk = None
        self.__volume = 128
        self.__channel = -1
        if filename:
            if not self.load(filename):
                log.write("__init__ in Sound object failed.")

    def __del__(self):
        """
        デストラクタ

            delされたらチャンクを開放する
        """
        Mix_FreeChunk(self.__chunk)

    def load(self, filename):
        """
        ファイルからサウンドファイルを読み込む

        Args:
            filename (str): 読み込むサウンドファイルのパス(utf-8)
        
        Returns:
            bool: True:成功 False:失敗
        """
        if self.__chunk:
            Mix_FreeChunk(self.__chunk)
            self.__chunk = None

        chunk = Mix_LoadWAV(filename.encode("utf-8"))
        if not chunk:
            log.write("load('{}') in Sound object failed. error={}".format(filename, Mix_GetError()))
            return False
        self.__chunk = chunk
        Mix_VolumeChunk(self.__chunk, self.__volume)
        return True

    def play(self, channel=0, loops=0):
        """
        サウンドを再生する

        Note:
            効果音を多重再生したい場合は違うチャネルを指定すること。
            ゲームでは効果音を多数同時に鳴らすので-1指定による自動設定はすぐにチャネルが枯渇するため推奨しない。
        
        Args:
            channel (int): 再生するチャネル。-1で空いているチャネルを使う
            loops (int): ループ回数、-1なら無限ループ、0なら1回、1なら2回再生される
        
        Returns:
            int: 再生されるチャネル。失敗時-1 
        """
        if not self.__chunk:
            log.write("play() in Sound object failed. Not loaded.")
            return -1

        res = Mix_PlayChannel(channel, self.__chunk, loops)
        if res == -1:
            log.write("play() in Sound object failed. error={}".format(Mix_GetError()))
        return int(res)

    def set_volume(self, volume):
        """
        サウンド再生時のボリュームを設定する

        Args:
            volume (int): ボリューム(0-128)
        """
        if not self.__chunk:
            log.write("set_voume() in Sound object failed. Not loaded.")
            return
        self.__volume = volume
        Mix_VolumeChunk(self.__chunk, volume)

    def get_chunk(self):
        """
        読み込まれたMix_Chunkオブジェクトを得る

        Returns:
            Mix_Chunk:  読み込まれたMix_Chunkオブジェクト。失敗はNone
        """
        return self.__chunk
