from typing import List


def read_encoded_image(filename: str) -> List[int]:
    with open(filename, 'r') as f:
        tmp = f.read()
    
    return [int(val) for val in tmp]


def decode_image(image_width: int, image_height: int, encoded_image: List[int]) -> List[List[List[int]]]:
    image_layers = []

    number_of_pixels = len(encoded_image)

    for base_pixel in range(0, number_of_pixels, image_width * image_height):
        this_layer = []
        for row in range(image_height):
            this_row = []
            for col in range(image_width):
                this_row.append(encoded_image[base_pixel + col + row * image_width])
            this_layer.append(this_row)
        image_layers.append(this_layer)

    return image_layers


def check_image(image: List[List[List[int]]]) -> int:

    # layer_with_fewest_zeros = -1
    fewest_zeros = 1000000
    check_value = 0

    # for layer_number, layer in enumerate(image):
    for layer in image:

        num_0 = 0
        num_1 = 0
        num_2 = 0

        for row in layer:
            for col in row:
                if col == 0:
                    num_0 += 1
                elif col == 1:
                    num_1 += 1
                elif col == 2:
                    num_2 += 1
        
        if num_0 < fewest_zeros:
            fewest_zeros = num_0
            # layer_with_fewest_zeros = layer_number
            check_value = num_1 * num_2
    
    return check_value


def render_image(decoded_image: List[List[List[int]]]) -> List[List[int]]:
    image_height = len(decoded_image[0])
    image_width = len(decoded_image[0][0])
    n_layers = len(decoded_image)

    rendered_image = [[0 for _ in range(image_width)] for _ in range(image_height)]

    for row in range(image_height):
        for col in range(image_width):
            for layer_number in range(n_layers):
                if decoded_image[layer_number][row][col] == 2:
                    continue
                else:
                    break
            rendered_image[row][col] = decoded_image[layer_number][row][col]
    
    return rendered_image


def print_image(rendered_image: List[List[int]]):

    for row in rendered_image:
        print(' '.join(str(val) for val in row))


if __name__ == '__main__':

    image_width = 3
    image_height = 2

    test_image = [int(val) for val in '123456789012']

    decoded_image = decode_image(image_width, image_height, test_image)
    assert decoded_image[0][1][1] == 5
    assert decoded_image[1][0][2] == 9

    image_width = 25
    image_height = 6

    encoded_image = read_encoded_image('./inputs/day08.txt')

    decoded_image = decode_image(image_width, image_height, encoded_image)
    check_value = check_image(decoded_image)
    print(f"The image check value is {check_value}")

    rendered_image = render_image(decoded_image)
    print_image(rendered_image)
