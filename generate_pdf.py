import pathlib
from pprint import pprint
from fractions import Fraction
import numpy as np
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Image, frames, PageTemplate
from reportlab.lib.pagesizes import A4, mm, landscape, portrait
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics, cidfonts
import datetime

from chart.lens_pie_chart import LensPieChart


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
        self.create_pdf_template()
        # 使用レンズ割合の円グラフを作成
        lens_pie_chart = LensPieChart()
        lens_pie_chart.generate_pie_chart(image_exifs)

    def create_pdf_template(self):
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

        doc = BaseDocTemplate(
            file_path,
            pagesize=portrait(A4),
            # rightMargin=72,
            # leftMargin=72,
            # topMargin=72,
            # bottomMargin=18,
        )
        width, height = A4

        show = 1
        frame_list = [
            frames.Frame(15*mm, 15*mm, width-30*mm,
                         height-30*mm, showBoundary=0),
        ]
        page_template = PageTemplate("test", frames=frame_list)
        doc.addPageTemplates(page_template)

        flowables = []

        style = ParagraphStyle(
            name="Normal",
            fontName="HeiseiKakuGo-W5",
            fontSize=12,
            leading=14,
            spaceAfter=10,
            alignment=1,
        )
        para = Paragraph("使用レンズの割合", style)
        flowables.append(para)

        # PDF出力
        # TODO buildメソッドとの違いは何？
        # doc.multiBuild(flowables)

