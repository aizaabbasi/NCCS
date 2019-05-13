try:
    import PIL
    import PIL.Image as PILimage
    from PIL import ImageDraw, ImageFont, ImageEnhance
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError as err:
    exit(err)


class Worker(object):
    def __init__(self, img):
        self.img = img
        self.get_exif_data()
        self.date =self.get_date_time()
        self.make = self.get_make()
        self.model = self.get_model()
        self.software = self.get_software()
        self.focalLength = self.get_focal_length()
        self.shutterSpeed= self.get_shutter_speed()
        self.width = self.get_width()
        self.height = self.get_height()
        self.colorSpace = self.get_colorspace()
        super(Worker, self).__init__()

    def get_exif_data(self):
        exif_data = {}
        info = self.img._getexif()
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                if decoded == "GPSInfo":
                    gps_data = {}
                    for t in value:
                        sub_decoded = GPSTAGS.get(t, t)
                        gps_data[sub_decoded] = value[t]

                    exif_data[decoded] = gps_data
                else:
                    exif_data[decoded] = value
        self.exif_data = exif_data
        # return exif_data 

    def get_date_time(self):
        if 'DateTime' in self.exif_data:
            date_and_time = self.exif_data['DateTime']
            return date_and_time 


    def get_make(self):
        if 'Make' in self.exif_data:
            make = self.exif_data['Make']
            return make 

    def get_model(self):
        if 'Model' in self.exif_data:
            model = self.exif_data['Model']
            return model 

    def get_software(self):
        if 'Software' in self.exif_data:
            software = self.exif_data['Software']
            return software

    def get_focal_length(self):
        if 'FocalLength' in self.exif_data:
            focalLength = self.exif_data['FocalLength']
            return focalLength

    def get_width(self):
        if 'ExifImageWidth' in self.exif_data:
            width = self.exif_data['ExifImageWidth']
            return width


    def get_height(self):
        if 'ExifImageHeight' in self.exif_data:
            height = self.exif_data['ExifImageHeight']
            return height


    def get_colorspace(self):
        if 'ColorSpace' in self.exif_data:
            colorSpace = self.exif_data['ColorSpace']
            return colorSpace
 
    def get_shutter_speed(self):
        if 'ShutterSpeedValue' in self.exif_data:
            shutterSpeed = self.exif_data['ShutterSpeedValue']
            return shutterSpeed


def main():
   # date = image.date
  #  print(date)

#if __name__ == '__main__':
    try:
        img = PILimage.open('555.jpg')
        image = Worker(img)
        date = image.date
        make = image.make
        model= image.model
        software= image.software
        focalLength= image.focalLength
        width= image.width
        height= image.height
        colorSpace= image.colorSpace
        shutterSpeed= image.shutterSpeed
                

        print("Date and Time > "+ date)
        print("Make > "+make)
        print("Model > "+model)
        print("Software > "+software)
        print("FocalLength > "+str(focalLength))
        print("ShutterSpeedValue > "+str(shutterSpeed))
        print("ExifImageWidth > "+str(width))
        print("ExifImageHeight > "+str(height))
        print("ColorSpace > "+str(colorSpace))



    except Exception as e:
        print(e)

