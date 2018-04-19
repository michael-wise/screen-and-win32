from PIL import ImageGrab
import os
import time
 
def screenGrab():
    # box = (157,346,796,825)
    box = ()
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +
'.png', 'PNG')
 
def main():
    screenGrab()
    print 'test'
 
if __name__ == '__main__':
    main()