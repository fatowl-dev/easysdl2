# -*- coding: utf-8 -*-
"""
easysdl2モジュール内で使うエラーログに関するモジュールです。
"""

import datetime

_log_file_name = ""
_print_flag = True


def enable_console(flag):
    """
    コンソール出力フラグを設定

    Args:
        flag (bool): True:ログメッセージをコンソールにも出力。 False:コンソールには出力しない。
    """
    _print_flag = flag


def set_file_name(filename):
    """
    ログファイル名を指定する
    
    Note:
        ファイル名が""ならログファイルを出力しない 

    Args:
        filename (str): ログファイル名
    """
    _log_file_name = filename


def write(message):
    """
    ログファイルに1行書き込む
   
    Note:
        初期設定ではコンソール出力のみ。ファイル出力したい場合はset_log_file()でファイル名を指定する。

    Args:
        messsage (str): 書き込む文字列
    """
    if _print_flag: print(message)
    if _log_file_name:
        now = datetime.now()
        nowstr = now.strftime("[%Y/%m/%d %H:%M:%S]")
        with open(_log_file_name, "a") as f:
            f.write(nowstr + ":" + message + "\n")


def error_log(message="", method="", classname="", trgfile=""):
    """
    エラーログを決まった形式で出力する

    Args:
        message (str): エラーメッセージ
        method (str): エラーが起きたメソッド名
        classname (str): エラーが起こったクラス名
        trgfile (str): 読み込み等でエラーが起こったファイル名
    """
    text = ""
    if message: text += "message='" + str(message) + "' "
    if method: text += "method='" + str(method) + "' "
    if classname: text += "class='" + str(classname) + "' "
    if trgfile: text += "file='" + str(trgfile) + "' "
    write(text)
