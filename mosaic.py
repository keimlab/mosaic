import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

class Mosaic:
    def __init__(self, image):
        self.img = cv2.imread(image)
        self.img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)

        self.img_height = self.img.shape[0]
        self.img_width = self.img.shape[1]

    def __ave_rgb(self, image, height, width):
        ave_c_per_row = np.mean(image, axis=0)
        ave_c = np.mean(ave_c_per_row, axis=0)
        ave_c_int = np.uint8(ave_c)

        return np.array([[ave_c_int] * width] * height)

    def size(self, mos_height, mos_width):
        for i in range(0, self.img_width, mos_width):
            if i + mos_width > self.img_width:
                width = self.img_width - i
            else:
                width = mos_width

            for j in range(0, self.img_height, mos_height):
                if j+mos_height > self.img_height:
                    height = self.img_height - j
                else:
                    height = mos_height

                mos_block = self.img_rgb[j:j + height, i:i + width]
                mos_ave = self.__ave_rgb(mos_block, height, width)

                self.img_rgb[j:j + height, i:i + width] = mos_ave[0:height, 0:width]

    def show(self):
        plt.imshow(self.img_rgb)
        plt.show()

    def save(self, filename):
        plt.imsave(filename, self.img_rgb)

def main():
    parser = argparse.ArgumentParser(description='画像ファイルにモザイク処理をかけるプログラム')

    parser.add_argument('-s', help='ソースファイル名を指定')
    parser.add_argument('-d', help='書き出すファイル名を指定')
    parser.add_argument('-m', type=int, default = 100, help='モザイクのサイズを指定:default=100')

    args = parser.parse_args()
    if (args.s == None or args.d == None):
        parser.print_help()
    else:
        img = Mosaic(args.s)
        img.size(args.m, args.m)
        img.save(args.d)

if __name__ == "__main__":
    main()
