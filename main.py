from fractions import Fraction
import pathlib
from pprint import pprint
import exifread
import sys
import os

from generate_pdf import GeneratePDF


class Main:
    """
    メインクラス
    """
    # 画像フォルダパスインデックス
    PHOTO_DIR_INDEX = 2

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
        photo_files = self.get_photo_files_path(argv[1])
        photo_exifs = self.read_exif_data(photo_files)

        # PDF生成
        generate_pdf = GeneratePDF()
        generate_pdf.generate(photo_exifs)
        # pprint(image_exif_list)

    def get_photo_files_path(self, source_path: str) -> list[pathlib.Path]:
        """
        指定フォルダ内の画像ファイルパスを取得するメソッド
        Args:
            source_path: 画像フォルダパス
        Returns:
            list: 画像ファイルパスリスト
        """
        pathlib_path = pathlib.Path(source_path).resolve()
        paths = list(pathlib_path.rglob("*.*"))
        return [f for f in paths if f.suffix.lower() in [".jpg", ".jpeg", ".tiff"]]

    def read_exif_data(self, file_paths: list[pathlib.Path]) -> list[dict]:
        """
        指定フォルダ内の画像を読み込むメソッド
        Args:
            file_paths: 画像ファイルパスリスト
        Returns:
            dict: EXIFデータ
        """
        picture_infos = []
        for file_path in file_paths:
            try:
                with open(file_path, "rb") as file:
                    picture_info = {}
                    tags = exifread.process_file(file, details=False)
                    for tag, value in tags.items():
                        if tag.startswith("Image ") or tag.startswith("EXIF "):
                            picture_info[tag] = value
                    picture_infos.append(picture_info)
            except Exception as e:
                # エラーは握り潰して見なかったことにするのだ
                pass
        # F値を小数点表記に変換
        for i, val in enumerate(picture_infos):
            picture_infos[i]["EXIF FNumber"] = float(
                Fraction(str(val["EXIF FNumber"])))
        return picture_infos

    def validate_input_path(self, argv: list[str]) -> bool:
        """
        入力パスの正当性を確認するメソッド
        Args:
            argv: コマンドライン引数
        Returns:
            bool: 正当性確認結果
        """
        if len(argv) < self.PHOTO_DIR_INDEX:
            print("エラー：引数が不足しています。")
            return False
        if not os.path.exists(argv[1]):
            print(f"エラー：指定されたパス '{argv[1]}' は存在しません。")
            return False
        return True


if __name__ == "__main__":
    main = Main()
    main.main_routine(sys.argv)
