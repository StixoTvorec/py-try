from PIL import Image, ImageOps
import pytesseract


def decoder(file):
    image = Image.open(file).convert('RGB')
    image = ImageOps.invert(image)
    image = ImageOps.grayscale(image)
    image = ImageOps.autocontrast(image)
    return pytesseract.image_to_string(image)
