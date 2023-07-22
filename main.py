import numpy as np
import os
from PIL import Image
import cv2 as cv2
import shutil


class FormatImage:

    def __init__(self):
        self.IMAGE_SIZE = 448
        self.INITIAL_AXLE = 0
        self.DEFAULT_WALK_HEIGHT = 403
        self.DEFAULT_WALK_WIDTH = 436

    def crop_image(self, nameOfImage, pathToSave):
        image = cv2.imread('images/selecteds/{}.jpg'.format(nameOfImage))
        height = self.IMAGE_SIZE
        width = self.IMAGE_SIZE
        axleX = self.INITIAL_AXLE  # equals width
        axleY = self.INITIAL_AXLE  # equals height
        shutil.move('images/selecteds/{}.jpg'.format(nameOfImage),
                    'images/selecteds/finisheds/{}.jpg'.format(nameOfImage))
        for i in range(10):
            for j in range(7):
                crop = image[axleX:width, axleY:height]

                cv2.imwrite('{}/{}-X{}Y{}.jpg'.format(pathToSave, nameOfImage, axleX, axleY), crop)
                height = height + self.DEFAULT_WALK_HEIGHT
                axleY = axleY + self.DEFAULT_WALK_HEIGHT
            width = width + self.DEFAULT_WALK_WIDTH
            axleX = axleX + self.DEFAULT_WALK_WIDTH
            height = self.IMAGE_SIZE
            axleY = self.INITIAL_AXLE



    def delete_image(self, path):
        dirs = os.listdir(path)
        for fileName in dirs:
            image = Image.open('{}/{}'.format(path, fileName))
            width, height = image.size
            image.close()

            if height != 448:
                os.remove('{}/{}'.format(path, fileName))


if __name__ == '__main__':
    # FormatImage().crop_image('26-0002', 'images/croppeds')
    FormatImage().delete_image('images/croppeds')


