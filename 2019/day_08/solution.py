import numpy as np
image_data = open('data.txt').read()

size = (6, 25)

def layer_split(image_data, size):
    layers = []
    length = size[0]*size[1]
    assert len(image_data) % length == 0
    for i in range(int(len(image_data)/length)):
        layers.append(image_data[i*length:(i+1)*length])
    return layers

layers = layer_split(image_data, size)

def get_layer_with_less_zeros(layers):
    min_ = len(layers[0])
    index_min = 0
    for index, layer in enumerate(layers):
        if layer.count("0") < min_:
            min_ = layer.count("0")
            index_min = index
    return layers[index_min]

layer = get_layer_with_less_zeros(layers)
print(layer.count("1")*layer.count("2"))
print(len(layers))

test_layers = layer_split("0222112222120000", (2, 2))

# 0 is black, 1 is white, 2 is transparent
def compute_image(layers, size):
    image = np.zeros(size[0]*size[1]).astype(int)
    for pixel in range(len(layers[0])):
        index = 0
        while True and index < len(layers):
            layer = layers[index]
            if layer[pixel] != "2":
                image[pixel] = layer[pixel]
                break
            index += 1
        else:
            image[pixel] = "2"

    return image.reshape(size)

print(compute_image(test_layers, (2, 2)))
print(compute_image(layers, size))