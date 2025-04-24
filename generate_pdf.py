import pathlib
from pprint import pprint
from fractions import Fraction
import numpy as np
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Image, frames, PageTemplate
from reportlab.lib.pagesizes import A4, mm, landscape, portrait
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics, cidfonts
import datetime

from chart.generate_lens_bar_chart import GenerateLensBarChart
from chart.generate_lens_pie_chart import GenerateLensPieChart


class GeneratePDF:
    """
    PDF生成クラス
    """
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

    def generate(self, image_exifs: list[dict]):
        """
        PDF生成
        Args:
            image_exifs: 画像EXIF情報リスト
        """
        # pprint(image_exif_list)
        # PDFテンプレートを作成
        doc, contents = self.create_pdf_template()
        # # 使用レンズ割合の円グラフを作成
        # self.create_lens_pie_chart(doc, contents, image_exifs)
        # 使用レンズ割合の棒グラフを作成
        self.create_lens_bar_chart(doc, contents, image_exifs)

    def create_pdf_template(self) -> BaseDocTemplate | list:
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

        # simpleDocTemplate
        contents = []
        doc = SimpleDocTemplate(
            file_path,
            pagesize=portrait(A4),
            rightMargin=(10*mm),
            leftMargin=(10*mm),
            topMargin=(5*mm),
            bottomMargin=(5*mm),
        )
        # contents.append(Paragraph("テスト", style=ParagraphStyle(
        #     name="title", fontName="HeiseiKakuGo-W5",)))
        return doc, contents

    def create_lens_pie_chart(self, doc: BaseDocTemplate, contents: list, image_exifs: dict):
        """
        円グラフを作成するメソッド
        Args:
            image_exifs: 画像EXIF情報リスト
        """
        generate_lens_pie_chart = GenerateLensPieChart()
        img = generate_lens_pie_chart.generate_lens_pie_chart(
            image_exifs)
        # 円グラフをPDFに貼り付ける
        lens_pie_chart_image = Image(
            img,
            width=doc.pagesize[0] - 20*mm,
            height=doc.pagesize[1] - 20*mm,
            kind="proportional",
            # hAlign="CENTER",
            # vAlign="MIDDLE",
        )
        contents.append(lens_pie_chart_image)
        doc.build(contents)

    def create_lens_bar_chart(self, doc: BaseDocTemplate, contents: list, image_exifs: dict):
        """
        棒グラフを作成するメソッド
        Args:
            image_exifs: 画像EXIF情報リスト
        """
        generate_lens_bar_chart = GenerateLensBarChart()
        img = generate_lens_bar_chart.generate_lens_bar_chart(
            image_exifs)
        # 棒グラフをPDFに貼り付ける
        lens_bar_chart_image = Image(
            img,
            width=doc.pagesize[0] - 20*mm,
            height=doc.pagesize[1] - 20*mm,
            kind="proportional",
            # hAlign="CENTER",
            # vAlign="MIDDLE",
        )
        contents.append(lens_bar_chart_image)
        doc.build(contents)