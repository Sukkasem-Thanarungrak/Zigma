import cv2
import pytesseract

# In order to use tesseract OCR library, you have to install the tesseract executable
# from https://github.com/ub-mannheim/tesseract/wiki
# and edit the PATH where you install the program.
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\TesseractOCR\tesseract.exe'
    

def ocr_core(img):
    text = pytesseract.image_to_string(img)
    return text


img = cv2.imread('test1.png')


# get grayscale image
def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# noise removal
def remove_noise(image):
    return cv2.medianBlur(image, 5)


# thresholding
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]


img = get_grayscale(img)
img = thresholding(img)
img = remove_noise(img)

print(ocr_core(img))


