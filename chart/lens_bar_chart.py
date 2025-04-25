import io
from matplotlib import pyplot
import matplotlib_fontja
from pprint import pprint


class GenerateLensBarChart:
    a4 = (8.27, 11.69)  # A4サイズのインチ数
    mm = 0.0393701  # インチからmmへの変換係数

    def sub_routine(self, photo_exifs: list[dict]) -> io.BytesIO:
        """
        使用レンズの割合を棒グラフで作成するメソッド
        """
        lens_count_dict = self.extract_lens_info(photo_exifs)
        return self.create_lens_bar_chart(lens_count_dict)

    def extract_lens_info(self, photo_exifs: list[dict]) -> dict:
        """
        使用レンズの情報を抽出するメソッド
        Args:
            photo_exifs: 画像EXIF情報リスト
        Returns:
            dict: レンズ名と出現回数dict
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

    def create_lens_bar_chart(self, lens_count_dict: dict) -> io.BytesIO:
        """
        レンズ使用回数を棒グラフで表示するメソッド
        Args:
            lens_count_dict: レンズ名と出現回数dict
        Return:
            buf: 画像データ
        """
        # 棒グラフのデータを準備
        labels = list(lens_count_dict.keys())
        data = list(lens_count_dict.values())
        bar_colors = ["tab:red", "tab:blue", "tab:green", "tab:orange", "tab:purple", "tab:brown"]

        fig, ax = pyplot.subplots(
            layout="constrained",
            figsize=(self.a4[0] - (40*self.mm), (self.a4[1] - (40*self.mm))/5), dpi=350)

        bar = ax.barh(labels, data, color=bar_colors, zorder=2)
        ax.bar_label(bar, color="white", label_type="center", fontsize=10, zorder=3)
        # ax.legend(title="レンズ名")

        # グリッド線を有効
        ax.grid(axis='x', linestyle='--', zorder=0, alpha=0.5)
        # y軸を反転
        ax.invert_yaxis()
        
        # 画像出力
        buf = io.BytesIO()
        pyplot.savefig(buf, format='png')
        buf.seek(0)
        pyplot.close(fig)
        return buf