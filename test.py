from PIL import Image
import numpy as np

# Run me with python3 -i test.py

if __name__ == "__main__":
    w, h = 1024, 512
    data = np.zeros((h, w, 3), dtype=np.uint8)
    for i in range(512):
        data[i,i] = [i, i, i]

    img = Image.fromarray(data, 'RGB')
    img.save('my.png')
    img.show()


