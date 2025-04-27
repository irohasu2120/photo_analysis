from logging import getLogger, INFO, DEBUG, Formatter, FileHandler
import io
from matplotlib import pyplot
from matplotlib.ticker import FixedLocator, MultipleLocator
import matplotlib_fontja


class GenerateFAndFocalLengthScatterChart:
    a4 = (8.27, 11.69)  # A4サイズのインチ数
    mm = 0.0393701  # インチからmmへの変換係数

    logger = getLogger(__name__)

    def __init__(self):
        """
        コンストラクタ
        """
        # log出力設定
        self.logger.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # ファイルへ出力するハンドラーを定義
        fh = FileHandler(filename='./logs/logging.log', encoding='utf-8')
        fh.setLevel(DEBUG)
        fh.setFormatter(formatter)
        # rootロガーにハンドラーを登録
        self.logger.addHandler(fh)

    def sub_routine(self, photo_exifs: list[dict]) -> io.BytesIO:
        """
        F値と焦点距離の関係を三府図グラフで作成するメソッド
        """
        f_and_focal_length_infos = self.extract_f_and_focal_length_info(
            photo_exifs)
        return self.create_f_and_focal_length_scatter_chart(f_and_focal_length_infos)

    def extract_f_and_focal_length_info(self, photo_exifs: list[dict]) -> dict:
        """
        F値と焦点距離の情報を抽出するメソッド
        Args:
            photo_exifs: 画像EXIF情報リスト
        Returns:
            dict: F値と焦点距離の関係性dict
        """
        # F値と焦点距離を抽出
        f_and_focal_length_infos = []
        for image in photo_exifs:
            if "EXIF FNumber" in image and "EXIF FocalLengthIn35mmFilm" in image:
                f_and_focal_length_infos.append(
                    (float(str(image["EXIF FNumber"])), int(str(image["EXIF FocalLengthIn35mmFilm"]))))
        return f_and_focal_length_infos

    def create_f_and_focal_length_scatter_chart(self, f_and_focal_length_infos: list[tuple]) -> io.BytesIO:
        """
        F値と焦点距離の関係を三府図グラフで表示するメソッド
        Args:
            f_and_focal_length_infos: F値と焦点距離dict
        Return:
            buf: 画像データ
        """
        fig, ax = pyplot.subplots(
            layout="constrained",
            figsize=(self.a4[0] - (40*self.mm), (self.a4[1] - (40*self.mm))/4), dpi=350)

        ax.scatter(
            [info[0] for info in f_and_focal_length_infos],
            [info[1] for info in f_and_focal_length_infos],
            alpha=0.5
        )
        ax.grid(True)
        ax.set_xlabel("F値")
        ax.set_ylabel("焦点距離 (35mm換算)")

        # x_labels = [1.0,1.1,1.2,1.4,1.6,1.8,2,2.2,2.5,2.8,3.2,3.5,4,4.5,5.0,5.6,6.3,7.1,8,9,10,11,13,14,16,18,20,22,25,29,32]# 1/3段ごと
        x_labels = [1.0, 2, 2.8, 4, 5.6, 8, 11, 16, 22, 32]  # 間引き

        ax.set_xticks(x_labels)
        pyplot.xticks(rotation=90)
        ax.set_xticklabels(x_labels)

        # 画像出力
        buf = io.BytesIO()
        pyplot.savefig(buf, format='png')
        buf.seek(0)
        pyplot.close(fig)
        return buf
