import io
# import matplotlib
from matplotlib import pyplot, font_manager
import matplotlib_fontja
from pprint import pprint
# from reportlab.lib.pagesizes import A4, landscape, portrait
import numpy as np


class GenerateLensPieChart:
    """
    使用レンズの割合を円グラフで作成するクラス
    """
    a4 = (8.27, 11.69)  # A4サイズのインチ数
    mm = 0.0393701  # インチからmmへの変換係数

    # def __init__(self):
    #     matplotlib.use('Agg')

    def generate_lens_pie_chart(self, photo_exifs: list[dict]):
        """
        使用レンズの割合を円グラフで作成するメソッド
        """
        lens_count_dict = self.extract_lens_info(photo_exifs)
        return self.create_pie_chart(lens_count_dict)

    def extract_lens_info(self, photo_exifs: list[dict]) -> dict:
        """
        使用レンズの情報を抽出するメソッド
        Args:
            photo_exifs: 画像EXIF情報リスト
        Returns:
            dict: レンズ名と出現回数の辞書
        """
        # 使用レンズを抽出
        lens_infos = []
        for image in photo_exifs:
            if "EXIF LensModel" in image:
                lens_infos.append(image["EXIF LensModel"])

        # レンズ名をキーに出現回数をカウント
        lens_count_dict = {}
        for lens in lens_infos:
            lens_name = str(lens)
            if lens_name in lens_count_dict:
                lens_count_dict[lens_name] += 1
            else:
                lens_count_dict[lens_name] = 1

        # 上位5位まではそのまま、その他はまとめる
        lens_chart_dict = dict(
            sorted(lens_count_dict.items(), key=lambda x: x[1], reverse=True)[:5])
        others_sum = sum(
            value for key, value in lens_count_dict.items() if key not in lens_chart_dict)
        lens_chart_dict['その他'] = others_sum  # その他を追加
        return lens_chart_dict

    def create_pie_chart(self, lens_count_dict: dict):
        """
        円グラフを作成するメソッド
        Args:
            lens_count_dict: レンズ名と出現回数の辞書
        """
        # 円グラフのデータを準備
        labels = list(lens_count_dict.keys())
        data = list(lens_count_dict.values())

        # 円グラフを作成
        fig, ax = pyplot.subplots(
            # layout="constrained", figsize=(self.a4[0] - (40*self.mm), (self.a4[1] - (40*self.mm))/5), dpi=350)
            subplot_kw=dict(aspect="equal"), figsize=(self.a4[0] - (40*self.mm), (self.a4[1] - (40*self.mm))/5), dpi=350)

        wedges, texts = ax.pie(
            # sizes, labels=None, autopct='%1.1f%%', startangle=90, counterclock=False,)
            data, wedgeprops=dict(width=0.5), startangle=-40, )
        # ax.legend(labels, title="凡例", loc='lower left',
        #           fontsize=8, )

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2.0 + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(labels[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)

        buffer = io.BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        pyplot.close(fig)  # グラフを閉じる

        return buffer
