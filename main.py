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
    IMAGE_DIR_INDEX = 2

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
        image_exif_list = self.read_exif_data(image_file_list)

        # PDF生成
        generate_pdf = GeneratePDF()
        generate_pdf.generate(image_exif_list)
        # pprint(image_exif_list)

    def get_image_files_path(self, source_path: str) -> list[pathlib.Path]:
        """
        指定フォルダ内の画像ファイルパスを取得するメソッド
        Args:
            source_path: 画像フォルダパス
        Returns:
            list: 画像ファイルパスリスト
        """
        pathlib_path = pathlib.Path(source_path).resolve()

        # TODO 拡張子がjpegのファイルも想定する

        # 画像ファイルリストを取得（再帰的）
        return list(pathlib_path.rglob("*.JPG"))

    def read_exif_data(self, file_path_list: list[pathlib.Path]) -> list[dict]:
        """
        指定フォルダ内の画像を読み込むメソッド
        Args:
            file_path_list: 画像ファイルパスリスト
        Returns:
            dict: EXIFデータ
        """
        # TODO exif情報を持ってないjpgファイルも想定する
        picture_info_list = []
        for file_path in file_path_list:
            try:
                with open(file_path, "rb") as file:
                    picture_info = {}
                    tags = exifread.process_file(file, details=False)
                    for tag, value in tags.items():
                        if tag.startswith("Image ") or tag.startswith("EXIF "):
                            picture_info[tag] = value
                    picture_info_list.append(picture_info)
            except Exception as e:
                # エラーは握り潰して見なかったことにするのだ
                pass
        
        # F値を小数点表記に変換
        for i, val in enumerate(picture_info_list):
            picture_info_list[i]["EXIF FNumber"] = float(Fraction(str(val["EXIF FNumber"])))
        return picture_info_list

    def validate_input_path(self, argv: list[str]) -> bool:
        """
        入力パスの正当性を確認するメソッド
        Args:
            argv: コマンドライン引数
        Returns:
            bool: 正当性確認結果
        """
        if len(argv) < self.IMAGE_DIR_INDEX:
            print("エラー：引数が不足しています。")
            return False
        if not os.path.exists(argv[1]):
            print(f"エラー：指定されたパス '{argv[1]}' は存在しません。")
            return False
        return True


if __name__ == "__main__":
    main = Main()
    main.main_routine(sys.argv)
