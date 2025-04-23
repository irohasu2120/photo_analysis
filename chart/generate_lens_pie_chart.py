import io
from matplotlib import pyplot, font_manager
import matplotlib_fontja
from pprint import pprint


class GenerateLensPieChart:
    """
    使用レンズの割合を円グラフで作成するクラス
    """

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
        sizes = list(lens_count_dict.values())

        # 円グラフを作成
        fig, ax = pyplot.subplots(figsize=(7, 3), dpi=300)
        wedges, texts, autotexts = ax.pie(
            sizes, labels=None, autopct='%1.1f%%', startangle=90, counterclock=False,)
        ax.legend(labels, title="凡例", loc='lower left',
                  fontsize=8, bbox_to_anchor=(1, 0, 0.5, 1))
        # ax.axis('equal')
        pyplot.setp(autotexts, size=8, weight="bold", color="white")
        # ax.set_title("使用レンズの割合", fontsize=12)
        
        # ジャストフィットさせる
        pyplot.tight_layout()

        # グラフを出力
        buf = io.BytesIO()
        with io.BytesIO() as buf:
            pyplot.savefig(buf, format='png')
            buf.seek(0)
            graph_image = buf.getvalue()
            buf.close()
        return  graph_image
