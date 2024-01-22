import numpy as np
import os
from PIL import Image
import cv2 as cv2
import shutil
import xml.etree.ElementTree as ElementTree
from pascal_voc_writer import Writer


class FormatImage:

    def __init__(self):
        self.IMAGE_ORIGINAL_WIDTH = 4608
        self.IMAGE_ORIGINAL_HEIGHT = 3456
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

    def crop_xml(self, nameOfXml, nameOfImage, nameOfNewXml):
        elementTree = ElementTree.parse('images/selecteds/{}.xml'.format(nameOfXml))
        root = elementTree.getroot()
        newXmlFile = self.create_xml_file(nameOfImage)

        for member in root.findall('object'):
            class_name = member[0].text

            # bbox coordinates
            xMin = int(member[4][0].text)
            yMin = int(member[4][1].text)
            xMax = int(member[4][2].text)
            yMax = int(member[4][3].text)

            auxXMin = self.calculate_x(xMin)
            auxYMin = self.calculate_y(yMin)
            auxXMax = self.calculate_x(xMax)
            auxYMax = self.calculate_y(yMax)

            # if auxXMin < self.IMAGE_SIZE and auxYMin > 0 and auxXMax < self.IMAGE_SIZE and auxYMax > 0:
            # self.add_object_to_xml(newXmlFile, class_name, auxXMin, auxYMin, auxXMax, auxYMax)

            if auxXMin > self.IMAGE_SIZE and auxYMin < 0 and auxXMax > self.IMAGE_SIZE and auxYMax < 0:
                print("entrou aqui")
                continue

            # print("passou aqui")
            # if auxXMin > self.IMAGE_SIZE:
            #     auxXMin = self.IMAGE_SIZE
            #
            # if auxYMin < 0:
            #     auxYMin = 0
            #
            # if auxXMax > self.IMAGE_SIZE:
            #     auxXMax = self.IMAGE_SIZE
            #
            # if auxYMax < 0:
            #     auxYMax = 0

            # if auxXMin > self.IMAGE_SIZE:
            #     auxXMin = self.IMAGE_SIZE
            #     if auxYMin < 0:
            #         auxYMin = 0
            #         if auxXMax > self.IMAGE_SIZE:
            #             auxXMax = self.IMAGE_SIZE
            #             if auxYMax < 0:
            #                 continue
            #             else:
            print("aqui")
            self.add_object_to_xml(newXmlFile, class_name, auxXMin, auxYMin, auxXMax, auxYMax)

            # print("class_name", class_name)
            # print("xmin", xMin)
            # print("ymin", yMin)
            # print("xmax", xMax)
            # print("ymax", yMax)

        self.save_xml_file(nameOfNewXml, newXmlFile)

    def calculate_y(self, yMin):
        return self.IMAGE_SIZE - yMin

    def calculate_x(self, xMin):
        return self.IMAGE_ORIGINAL_WIDTH - xMin

    def create_xml_file(self, nameOfImage):
        # create pascal voc writer (image_path, width, height)
        return Writer('images/selecteds/finisheds/{}.jpg'.format(nameOfImage), 448, 448)

    def add_object_to_xml(self, newXmlFile, className, xMin, yMin, xMax, yMax):
        # add objects (class, xmin, ymin, xmax, ymax)
        return newXmlFile.addObject(className, xMin, yMin, xMax, yMax)

    def save_xml_file(self, nameOfXml, newXmlFile):
        # write to file
        newXmlFile.save('images/croppeds/{}.xml'.format(nameOfXml))

    def delete_images(self, path):
        dirs = os.listdir(path)
        for fileName in dirs:
            image = Image.open('{}/{}'.format(path, fileName))
            width, height = image.size
            image.close()

            if height != 448:
                os.remove('{}/{}'.format(path, fileName))

    def delete_xml_files(self):
        dirs = os.listdir('images/croppeds')
        for fileName in dirs:
            print("a", '.xml' in fileName)
            if '.xml' in fileName:
                os.remove('{}/{}'.format('images/croppeds', fileName))

    def crop_xml_to_all_images(self, nameOfXml):
        for image in os.listdir('images/croppeds'):
            nameOfImage = image.replace('.jpg', '')
            self.crop_xml(nameOfXml, nameOfImage, nameOfImage)


if __name__ == '__main__':
    # FormatImage().crop_image('47a88ca8-P4130464', 'images/croppeds')
    # FormatImage().delete_images('images/croppeds')
    FormatImage().crop_xml('47a88ca8-P4130464', '47a88ca8-P4130464-X0Y0', '47a88ca8-P4130464-X0Y0')
    # FormatImage().crop_xml_to_all_images('47a88ca8-P4130464')
    # FormatImage().delete_xml_files()
