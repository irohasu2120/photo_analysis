import sys
import os
import datetime
import pathlib
from pprint import pprint
from typing import Tuple

from fractions import Fraction
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, Table
from reportlab.lib.pagesizes import A4, portrait
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics, cidfonts
import exifread
import numpy as np

from chart.lens_bar_chart import GenerateLensBarChart


class GeneratePdf:
    """
    PDF生成クラス
    """
    # 引数 画像フォルダパスインデックス
    PHOTO_DIR_INDEX = 2
    # PDFファイル出力先
    FILE_OUTPUT_PATH = "out"
    # PDFファイル名テンプレート
    FILE_NAME_TEMPLATE = "photograph_analysis_report_{generate_timestamp}.pdf"

    paragraph_sample_style = None

    def __init__(self):
        """
        コンストラクタ
        """
        # フォント登録
        pdfmetrics.registerFont(cidfonts.UnicodeCIDFont("HeiseiKakuGo-W5"))
        # ParagraphStyleのテンプレートを取得
        self.paragraph_sample_style = getSampleStyleSheet()
        self.paragraph_sample_style["Title"].fontName = "HeiseiKakuGo-W5"
        self.paragraph_sample_style["Heading2"].fontName = "HeiseiKakuGo-W5"
        self.paragraph_sample_style["Heading3"].fontName = "HeiseiKakuGo-W5"

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
        photo_files = self.collect_photo_files_path(argv[1])
        photo_exifs = self.read_exif_data(photo_files)

        # exif情報が取得出来ない場合は処理を終了
        if len(photo_exifs) == 0:
            print("EXIF情報が取得できませんでした。処理を終了します。")
            return

        # PDFテンプレートを作成
        doc, contents = self.initialize_pdf_template()

        # PDFタイトルを描画
        # TODO cloneした方がよいか？
        paragraph_title = self.paragraph_sample_style["Title"]
        paragraph_title.underlineWidth = 1
        title = Paragraph(
            "<u>撮影スタイルレポート</u>",
            style=paragraph_title,
        )
        contents.append(title)
        contents.append(Spacer(1, 12))

        # テーブル情報を描画
        self.create_table_info(doc, contents, photo_exifs)

        # 使用レンズ割合の棒グラフを描画
        self.create_lens_bar_chart(doc, contents, photo_exifs)
        contents.append(Spacer(1, 12))

        # PDF生成
        doc.build(contents)

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

    def collect_photo_files_path(self, source_path: str) -> list[pathlib.Path]:
        """
        指定フォルダ内の画像ファイルパスを収集するメソッド
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
        対象の画像ファイルからEXIF情報を読み込むメソッド
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
                print(f"エラー：画像のEXIF情報を読込中にエラーが発生しました。画像パス：{file_path} {e}")
        # F値を小数点表記に変換
        for i, val in enumerate(picture_infos):
            picture_infos[i]["EXIF FNumber"] = float(
                Fraction(str(val["EXIF FNumber"])))
        return picture_infos

    def initialize_pdf_template(self) -> Tuple[SimpleDocTemplate, list]:
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

    def create_table_info(self, doc: SimpleDocTemplate, contents: list, photo_exifs: dict):
        """
        テーブル情報を描画するメソッド
        Args:
            doc: PDFドキュメント
            contents: PDFコンテンツ
            photo_exifs: 画像EXIF情報リスト
        """
        # 撮影期間を取得
        period_start = None
        period_end = None
        for image in photo_exifs:
            if "EXIF DateTimeOriginal" in image:
                date_str = str(image["EXIF DateTimeOriginal"])
                date = datetime.datetime.strptime(
                    date_str, "%Y:%m:%d %H:%M:%S")
                if period_start is None:
                    period_start = date
                else:
                    if period_start > date:
                        period_start = date
                if period_end is None:
                    period_end = date
                else:
                    if period_end < date:
                        period_end = date
        period_start_str = period_start.strftime("%Y/%m/%d")
        period_end_str = period_end.strftime("%Y/%m/%d")

        data = [
            ["レポート対象画像", len(photo_exifs), "レポート対象期間",
             f"{period_start_str}～{period_end_str}"],
        ]
        table = Table(data, colWidths=[30*mm, 40*mm, 30*mm, 60*mm])
        table.setStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, "black"),
            ("BACKGROUND", (0, 0), (0, 0), "palegreen"),
            ("BACKGROUND", (1, 0), (1, 0), "white"),
            ("BACKGROUND", (2, 0), (2, 0), "palegreen"),
            ("BACKGROUND", (3, 0), (3, 0), "white"),
            ("TEXTCOLOR", (0, 0), (-1, -1), "black"),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME", (0, 0), (-1, -1), "HeiseiKakuGo-W5"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
        ])
        contents.append(table)

    def create_lens_bar_chart(self, doc: SimpleDocTemplate, contents: list, photo_exifs: dict):
        """
        使用レンズ回数を示す棒グラフを作成するメソッド
        Args:
            doc: PDFドキュメント
            contents: PDFコンテンツ
            photo_exifs: 画像EXIF情報リスト
        """
        header_style = self.paragraph_sample_style["Heading2"]
        header_style.underlineWidth = 1
        header = Paragraph(
            "<u>使用レンズ回数</u>",
            style=header_style,
        )
        contents.append(header)
        contents.append(Spacer(1, 4))

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
    generate_pdf = GeneratePdf()
    generate_pdf.main(sys.argv)
