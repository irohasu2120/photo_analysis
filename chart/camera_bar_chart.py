from logging import getLogger, INFO, DEBUG, Formatter, FileHandler
import io
from matplotlib import pyplot
import matplotlib_fontja


class GenerateCameraBarChart:
    a4 = (8.27, 11.69)  # A4サイズのインチ数
    mm = 0.0393701  # インチからmmへの変換係数

    logger = getLogger(__name__)

    def __init__(self):
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
        使用カメラの割合を棒グラフで作成するメソッド
        """
        camera_chart_dict = self.extract_camera_info(photo_exifs)
        return self.create_camera_bar_chart(camera_chart_dict)

    def extract_camera_info(self, photo_exifs: list[dict]) -> dict:
        """
        使用カメラの情報を抽出するメソッド
        Args:
            photo_exifs: 画像EXIF情報リスト
        Returns:
            dict: カメラ名と出現回数dict
        """
        # 使用カメラを抽出
        camera_infos = []
        for image in photo_exifs:
            if "Image Model" in image and "Image Make" in image:
                camera_infos.append(
                    f"{str(image['Image Make']).strip()}_{str(image['Image Model']).strip()}")

        # カメラ名をキーに出現回数をカウント
        camera_count_dict = {}
        for camera in camera_infos:
            camera_name = str(camera)
            if camera_name in camera_count_dict:
                camera_count_dict[camera_name] += 1
            else:
                camera_count_dict[camera_name] = 1
        self.logger.debug(f"カメラ情報: {camera_count_dict}")

        # 上位5位まではそのまま、その他はまとめる
        camera_chart_dict = dict(
            sorted(camera_count_dict.items(), key=lambda x: x[1], reverse=True)[:5])
        others_sum = sum(
            value for key, value in camera_count_dict.items() if key not in camera_chart_dict)
        camera_chart_dict['その他'] = others_sum  # その他を追加
        return camera_chart_dict

    def create_camera_bar_chart(self, camera_count_dict: dict) -> io.BytesIO:
        """
        カメラ使用回数を棒グラフで表示するメソッド
        Args:
            camera_count_dict: カメラ名と出現回数dict
        Return:
            buf: 画像データ
        """
        # 棒グラフのデータを準備
        labels = list(camera_count_dict.keys())
        data = list(camera_count_dict.values())
        bar_colors = ["tab:red", "tab:blue", "tab:green",
                      "tab:orange", "tab:purple", "tab:brown"]

        fig, ax = pyplot.subplots(
            layout="constrained",
            figsize=(self.a4[0] - (40*self.mm), (self.a4[1] - (40*self.mm))/5), dpi=350)

        bar = ax.barh(labels, data, color=bar_colors, zorder=2)
        # バー内部のラベル色を白に変更し、最前面に配置
        ax.bar_label(bar, color="white", label_type="center",
                     fontsize=10, zorder=3)
        # 目盛りラベル（レンズ名）のフォントサイズを変更
        ax.tick_params(axis="y", labelsize=8)
        # グリッド線を有効にし、最背面に配置
        ax.grid(axis='x', linestyle='--', zorder=0, alpha=0.5)
        # y軸を反転
        ax.invert_yaxis()

        # 画像出力
        buf = io.BytesIO()
        pyplot.savefig(buf, format='png')
        buf.seek(0)
        pyplot.close(fig)
        return buf
