import cv2
import numpy as np
from matplotlib import pyplot as plt


class TemplateMatcher:

    def __init__(self):
        self.mandatory_sign = cv2.imread('template/template_nakaz_mask.png', 0)
        self.prohibition_sign = cv2.imread('template/template_zakaz_mask.png', 0)
        self.warning_sign = cv2.imread('template/template_ostrzegawczy_mask.png', 0)
        self.information_sign = cv2.imread('template/template_informacyjny_mask.png', 0)

        #self.mandatory_sign = cv2.imread('template/template_nakaz.png', 0)
        #self.prohibition_sign = cv2.imread('template/template_zakaz.png', 0)
        #self.warning_sign = cv2.imread('template/template_ostrzegawczy.png', 0)
        #self.information_sign = cv2.imread('template/template_informacyjny.png', 0)

    def temp_select(self, temp_key):
        if temp_key == 'nakaz':
            template = self.mandatory_sign
        if temp_key == 'zakaz':
            template = self.prohibition_sign
        if temp_key == 'ostrzegawczy':
            template = self.warning_sign
        if temp_key == 'informacyjny':
            template = self.information_sign

        return template

    def template_single_conv(self, image, template):

        img = image.copy()
        resized_template = template.copy()
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # img_gray = image.copy()
        matchList = []
        imageList = []
        imgWidth = int(image.shape[1])
        imgHeight = int(image.shape[0])
        scale_percent = 30
        width = int(template.shape[1] * scale_percent / 100)
        height = int(template.shape[0] * scale_percent / 100)
        # while imgWidth < width or imgHeight < height:
        #     scale_percent -= 5  # percent of original size
        #     width = int(template.shape[1] * scale_percent / 100)
        #     height = int(template.shape[0] * scale_percent / 100)

#        print('Original Template Dimensions : ', template.shape)
#        print('Sign Dimensions : ', img_gray.shape)
        while width < imgWidth and height < imgHeight:
            dim = (width, height)
            # resize image
            resized_template = cv2.resize(template, dim, interpolation=cv2.INTER_AREA)
            # print('Resized Dimensions : ', img_rgb.shape)
            res = cv2.matchTemplate(img_gray, resized_template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            highest_score = max_val
            #print(highest_score)
            top_left = max_loc
            bottom_right = (top_left[0] + width, top_left[1] + height)
            # img = self.contour_detection(img)
            img = cv2.rectangle(img, top_left, bottom_right, 255, 2)
            matchList.append(highest_score)
            imageList.append(img)
            img = image.copy()
            scale_percent += 1
            width = int(template.shape[1] * scale_percent / 100)
            height = int(template.shape[0] * scale_percent / 100)
        # print(bottom_right[1], top_left[1], top_left[0], bottom_right[0])
        #print(matchList)
        
        highest_score = max(matchList)
        index = matchList.index(highest_score)
        img = imageList[index]

        return img, highest_score

    def offline_test(self, img_rgb, temp_key):
        # img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = self.temp_select(temp_key)
        img_detect, score = self.template_single_conv(img_rgb, template)
        return img_detect, score

    def display(self, image, temp_key):
        cv2.imshow('winname', image)
        cv2.imshow('temp', self.temp_select(temp_key))
        cv2.waitKey(0)

if __name__ == "__main__":
    tm = TemplateMatcher()
    # Tutaj wczytuje znak do rozpoznania
    img_rgb = cv2.imread('znaki/nakazRondo.png')

    print("Dopasowanie za znakiem nakazu")
    mandatory_img, mandatory_value = tm.offline_test(img_rgb, 'nakaz')
    print("Dopasowanie za znakiem zakazu")
    prohibition_img, prohibition_value = tm.offline_test(img_rgb, 'zakaz')
    print("Dopasowanie za znakiem ostrzegawczym")
    warning_img, warning_value = tm.offline_test(img_rgb, 'ostrzegawczy')
    print("Dopasowanie za znakiem informacyjnym")
    information_img, information_value = tm.offline_test(img_rgb, 'informacyjny')
    results = [mandatory_value, prohibition_value, warning_value, information_value]
    winner = max(results)
    if winner == mandatory_value:
        winner_name = "nakaz"
        winner_img = mandatory_img
    if winner == prohibition_value:
        winner_name = "zakaz"
        winner_img = prohibition_img
    if winner == warning_value:
        winner_name = "ostrzegawczy"
        winner_img = warning_img
    if winner == information_value:
        winner_name = "informacyjny"
        winner_img = information_img

    print("Rozpoznano: " + winner_name)
    print("Wyniki to: ")
    print("znak nakazu: " + str(results[0] * 100))
    print("znak zakazu: " + str(results[1] * 100))
    print("znak ostrzegawczy: " + str(results[2] * 100))
    print("znak informacyjny: " + str(results[3] * 100))

    print("\nZnaleziony rodzaj znaku: " + winner_name)
    tm.display(winner_img, winner_name)

