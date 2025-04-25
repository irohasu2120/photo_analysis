import sys
import os
import pathlib
from pprint import pprint
from fractions import Fraction
from typing import Tuple
import exifread
import numpy as np
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Image, frames, PageTemplate
from reportlab.lib.pagesizes import A4, mm, landscape, portrait
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics, cidfonts
import datetime

from chart.lens_bar_chart import GenerateLensBarChart


class GeneratePDF:
    """
    PDF生成クラス
    """
    # 引数 画像フォルダパスインデックス
    PHOTO_DIR_INDEX = 2
    # PDFファイル出力先
    FILE_OUTPUT_PATH = "out"
    # PDFファイル名テンプレート
    FILE_NAME_TEMPLATE = "photograph_analysis_report_{generate_timestamp}.pdf"

    def __init__(self):
        """
        コンストラクタ
        """
        # フォント登録
        pdfmetrics.registerFont(cidfonts.UnicodeCIDFont("HeiseiKakuGo-W5"))

    def main(self, argv: list[str]):
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

        # PDFテンプレートを作成
        doc, contents = self.initialize_pdf_template()
        # 使用レンズ割合の棒グラフを作成
        self.create_lens_bar_chart(doc, contents, photo_exifs)

        # PDF生成
        doc.build(contents)

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

    def initialize_pdf_template(self) -> Tuple[BaseDocTemplate, list]:
        """
        PDF初期化処理
        """
        # ファイル名生成
        generate_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = self.FILE_NAME_TEMPLATE.format(
            generate_timestamp=generate_timestamp)

        # PDFファイル出力先
        file_path = str(
            (pathlib.Path(self.FILE_OUTPUT_PATH) / file_name).resolve())

        # PDFテンプレートを作成
        doc = SimpleDocTemplate(
            file_path,
            pagesize=portrait(A4),
            rightMargin=(10*mm),
            leftMargin=(10*mm),
            topMargin=(5*mm),
            bottomMargin=(5*mm),
        )
        contents = []
        return doc, contents

    def create_lens_bar_chart(self, doc: BaseDocTemplate, contents: list, photo_exifs: dict):
        """
        棒グラフを作成するメソッド
        Args:
            photo_exifs: 画像EXIF情報リスト
        """
        generate_lens_bar_chart = GenerateLensBarChart()
        img = generate_lens_bar_chart.sub_routine(photo_exifs)
        lens_bar_chart_image = Image(
            img,
            width=doc.pagesize[0] - 20*mm,
            height=doc.pagesize[1] - 20*mm,
            kind="proportional",
            # hAlign="CENTER",
            # vAlign="MIDDLE",
        )
        contents.append(lens_bar_chart_image)


if __name__ == "__main__":
    generate_pdf = GeneratePDF()
    generate_pdf.main(sys.argv)
