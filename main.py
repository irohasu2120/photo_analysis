from fractions import Fraction
import pathlib
import glob
from pprint import pprint
import exifread
from matplotlib import pyplot, font_manager
import matplotlib_fontja
import numpy as np
import sys
import os


class Main:
    """
    メインクラス
    """

    def main_routine(self, argv: list[str]):
        """
        メインルーチン
        Args:
            argv: コマンドライン引数
        """
        # 入力パスの正当性確認
        if not self.validate_input_path(argv):
            return

        # 指定フォルダ内の画像を読み込む
        picture_info_list = self.read_image_in_folder(argv[1])
        # print(len(picture_info_list))
    
    def read_image_in_folder(self, source_path: str) -> list[dict]:
        """
        指定フォルダ内の画像を読み込むメソッド
        Args:
            source_path: 画像フォルダパス
        Returns:
            list[dict]: 画像情報リスト
        """
        picture_info_list = []
        pathlib_path = pathlib.Path(source_path)

        # TODO 絶対パスに変換する必要ある？
        pathlib_path = pathlib_path.resolve()

        pprint(list(pathlib_path.rglob("*.JPG")))




    def validate_input_path(self, argv: list[str]) -> bool:
        """
        入力パスの正当性を確認するメソッド
        Args:
            argv: コマンドライン引数
        Returns:
            bool: 正当性確認結果
        """
        if len(argv) < 2:
            print("エラー：引数が不足しています。")
            return False
        if not os.path.exists(argv[1]):
            print(f"エラー：指定されたパス '{argv[1]}' は存在しません。")
            return False
        return True


if __name__ == "__main__":
    main = Main()
    main.main_routine(sys.argv)
