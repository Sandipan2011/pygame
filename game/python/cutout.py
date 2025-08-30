from PIL import Image

img = Image.open("car.png")
img_cropped = img.crop(img.getbbox())
img_cropped.save("car_cropped.png")
