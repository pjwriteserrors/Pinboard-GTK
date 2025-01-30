from PIL import ImageGrab, Image


def get_image():
    # grab the image from the clipboard and return size and file if there is image in clipboard
    img = ImageGrab.grabclipboard()
    if isinstance(img, Image.Image):
        return img.size[0], img.size[1], img