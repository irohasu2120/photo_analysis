from fractions import Fraction
import glob
import exifread
from matplotlib import pyplot, font_manager
import matplotlib_fontja
import numpy as np
import sys


def generate(source_path):
    # 指定フォルダ内の画像を読み込む
    picture_info_list = []
    file_path_list = glob.glob(source_path + "\\*.JPG", recursive=True)
    for file_path in file_path_list:
        with open(file_path, "rb") as file:
            picture_info = {}
            tags = exifread.process_file(file, details=False)
            for tag, value in tags.items():
                if tag.startswith("Image ") or tag.startswith("EXIF "):
                    picture_info[tag] = value
            picture_info_list.append(picture_info)

    # f値を小数点表記に変換
    for i, val in enumerate(picture_info_list):
        picture_info_list[i]["EXIF FNumber"] = float(Fraction(str(val["EXIF FNumber"])))
        # print(val["EXIF DateTimeOriginal"])

    
    
    # 画像生成
    flg, ax = pyplot.subplots()

    fnumber_extractor = lambda x: x["EXIF FNumber"]
    f_numbers = [fnumber_extractor(info) for info in picture_info_list]
    x_labels = list(set(f_numbers))
    print(x_labels)
    print(f_numbers)


    bottom = np.zeros(len(x_labels))
    ax.set_xticks(x_labels)
    ax.set_yticks([i for i in range(0, 20)])
    for val in f_numbers:
        p = ax.bar(val, val,)
        bottom += 1
    # ax.bar(x_labels, f_numbers, label="f値")
    # ax.legend()
    # ax.plot()
    flg.savefig("test.png")


if __name__ == "__main__":
    generate(sys.argv[1])
    # generate("C:\\Users\\halo1\\Downloads\\しまうまプリント用")
