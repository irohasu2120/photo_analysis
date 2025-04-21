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
        image_file_list = self.get_image_files_path(argv[1])
        # pprint(str(image_file_list[0]))
        # print(len(picture_info_list))
        # pprint(image_file_list)
        self.read_exif_data(image_file_list)

    def get_image_files_path(self, source_path: str) -> list[pathlib.Path]:
        """
        指定フォルダ内の画像ファイルパスを取得するメソッド
        Args:
            source_path: 画像フォルダパス
        Returns:
            list: 画像ファイルパスリスト
        """
        # pathlib_path =

        # # TODO 絶対パスに変換する必要ある？
        pathlib_path = pathlib.Path(source_path).resolve()

        # TODO exif情報を持ってないjpgファイルも想定する
        # TODO 拡張子がjpegのファイルも想定する

        # 画像ファイルリストを取得（再帰的）
        # return list(pathlib.Path(pathlib_path).rglob("*.JPG"))
        return list(pathlib_path.rglob("*.JPG"))

    def read_exif_data(self, file_path_list: list[pathlib.Path]):
        """
        指定フォルダ内の画像を読み込むメソッド
        Args:
            file_path_list: 画像ファイルパスリスト
        Returns:
            dict: EXIFデータ
        """
        picture_info_list = []
        for file_path in file_path_list:
            with open(file_path, "rb") as file:
                picture_info = {}
                tags = exifread.process_file(file, details=False)
                for tag, value in tags.items():
                    if tag.startswith("Image ") or tag.startswith("EXIF "):
                        picture_info[tag] = value
                picture_info_list.append(picture_info)

        return picture_info_list

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
