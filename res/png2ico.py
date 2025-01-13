# pic 2 ico

from PIL import Image
import os

def png2ico(png_path, ico_path):
    im = Image.open(png_path)
    im.save(ico_path, 'ICO')
    print('png2ico success')

if __name__ == '__main__':
   # res\Designer.png
    png_path = os.path.join(os.path.dirname(__file__), 'Designer.png')
    ico_path = os.path.join(os.path.dirname(__file__), 'Designer.ico')
    png2ico(png_path, ico_path)