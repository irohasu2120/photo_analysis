from matplotlib import pyplot, font_manager
import matplotlib_fontja
from pprint import pprint


class LensPieChart:
    """
    使用レンズの割合を円グラフで作成するクラス
    """

    def generate_pie_chart(self, photo_exifs: list[dict]):
        """
        使用レンズの割合を円グラフで作成するメソッド
        """
        lens_count_dict = self.extract_lens_info(photo_exifs)
        self.create_pie_chart(lens_count_dict)

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

        return lens_count_dict

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
        fig, ax = pyplot.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        fig.savefig("aaa.png")