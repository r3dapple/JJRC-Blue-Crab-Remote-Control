import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import binascii

with open('rgb.txt', 'rb') as f:
    hexdata = binascii.hexlify(f.read())

hexdata = hexdata.decode()
n = 2
hexlist = [hexdata[i:i+n] for i in range(0, len(hexdata), n)]

height = 720
width = 1280
depth = 3
array = np.zeros((height,width,depth), dtype=float)

counter = 0
for y in range(0,height):
    for x in range(0,width):
        for z in range(0,depth):
            array[y][x][z] = float(int(hexlist[counter], 16))
            counter = counter + 1



test_image = image.array_to_img(array)
imgplot = plt.imshow(test_image)