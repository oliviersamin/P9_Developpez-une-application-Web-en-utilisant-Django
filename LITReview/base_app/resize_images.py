from PIL import Image as Pi
from PIL import ImageTk as PIk
import argparse
from resizeimage import resizeimage
import os


class ResizeImage:
    def __init__(self):
        self.original_image = ""
        self.original_image_name = ""
        self.scale = None
        self.new_image = ""
        self.new_image_name = ""
        self.directory = ""
        self.args = ""

    def __parse_arguments(self):
        parser = argparse.ArgumentParser(description='Resize images')
        parser = argparse.ArgumentParser()
        parser.add_argument("-d", "--directory", required=False, help="Enter the path of the directory "
                                                      "to save the new image into")
        parser.add_argument("-i", "--image", required=True, help="Enter the path of the image to work with")
        parser.add_argument("-n", "--name", required=False, help="Enter the name of the new image with its extension")
        parser.add_argument("-s", "--scale", help="Enter the scale in pourcentage to resize the image."
                                                  "It keeps the proportions", type=int, choices=range(1, 101))
        parser.add_argument("-max_w", "--max_width", help="Enter the maximum width of the new image in pixels")
        parser.add_argument("-max_h", "--max_height", help="Enter the maximum height of the new image in pixels")
        self.args = parser.parse_args()
        if (self.args.scale is None) and (self.args.max_width is None) and (self.args.max_height is None):
            print("You must choose the method to resize the image between scale, max_width and max_height")
            return False
        else:
            return True

    def __resize_image_scale(self, image):
        self.original_image = Pi.open(image)
        # print(self.original_image)
        if (self.args.scale is None) and (self.scale is None):
            print("There is no scale to resize the image")
            print(self.original_image.size)
        else:
            if self.scale is None:
                self.scale = float(self.args.scale)/100.
            resolution = (int(round(self.original_image.size[0] * self.scale)),
                          int(round(self.original_image.size[1] * self.scale)))
            self.new_image = resizeimage.resize_thumbnail(self.original_image, resolution)
            try:
                os.chdir(self.directory)
                self.new_image.save(self.new_image_name)
            except FileNotFoundError:
                print("Wrong directory name, please verify it and try again\nThe new image has not been saved")

    def __resize_image_pixels(self, image, position):
        self.original_image = Pi.open(image)
        if position == self.args.max_width:
            self.scale = float(self.args.max_width)/self.original_image.size[0]
        elif position == self.args.max_height:
            self.scale = float(self.args.max_height)/self.original_image.size[1]
        self.__resize_image_scale(image)

    def resize(self):
        if self.__parse_arguments():
            self.__get_directory_and_image_name(self.args.image)
            self.__initialize_attributes(self.args.image)
            if self.args.scale is not None:
                self.__resize_image_scale(self.args.image)
            elif self.args.max_width is not None:
                self.__resize_image_pixels(self.args.image, self.args.max_width)
            elif self.args.max_height is not None:
                self.__resize_image_pixels(self.args.image, self.args.max_height)

    def __get_directory_and_image_name(self, image):
        """ image is an attribute of Ticket in models.py of base_app """
        image_name = image[::-1][:image[::-1].find('/')]
        directory = image[::-1][image[::-1].find('/')+1:]
        return {'image_name': image_name[::-1], 'directory': directory[::-1]}

    def __initialize_attributes(self, image):
        """ use the dict from self.__get_directory_and_image_name  to give values to the attributes"""
        dico = self.__get_directory_and_image_name(image)
        self.original_image_name = dico['image_name']
        self.new_image_name = self.original_image_name[:self.original_image_name.find('.')] + "_resized" + \
                         self.original_image_name[self.original_image_name.find('.'):]
        self.directory = dico['directory']


if __name__ == "__main__":
    ResizeImage().resize()
