from pprint import pprint
from fractions import Fraction
from matplotlib import pyplot, font_manager
import matplotlib_fontja
import numpy as np
from reportlab.platypus import BaseDocTemplate, SimpleDocTemplate, Paragraph, Image, frames, PageTemplate
from reportlab.lib.pagesizes import A4, mm, landscape, portrait
import datetime


class GeneratePDF:
    """
    PDF生成クラス
    """
    # PDFファイル名テンプレート
    FILE_NAME_TEMPLATE = "photograph_analysis_report_{generate_timestamp}.pdf"

    def generate(self, image_exif_list: list[dict]):
        """
        PDF生成
        Args:
            image_exif_list: 画像EXIF情報リスト
        """
        # pprint(image_exif_list)
        self.ini_pdf()
        pass

    def ini_pdf(self):
        """
        PDF初期化処理
        """
        generate_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = self.FILE_NAME_TEMPLATE.format(
            generate_timestamp=generate_timestamp)
        doc = BaseDocTemplate(
            file_name,
            pagesize=portrait(A4),
            # rightMargin=72,
            # leftMargin=72,
            # topMargin=72,
            # bottomMargin=18,
        )
        frame_list = [
            frames.Frame(25 * mm, 120*mm, 150*mm, 50*mm, showBoundary=1)
        ]
        page_template = PageTemplate("test", frames=frame_list)
        doc.addPageTemplates(page_template)

        flowables = []
        doc.multiBuild(flowables)
