from flask import Flask, render_template, request, send_file
import numpy as np
from PIL import Image

app = Flask(__name__)


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    return [r, g, b]


def generate_fabric_image(screen_width, screen_height, weaving_pattern, epi, ppi, epi_color, ppi_color):
    # Adjust the square size to ensure even division
    square_size = min(screen_width, screen_height) // max(epi, ppi)

    fabric_width = screen_width // square_size
    fabric_height = screen_height // square_size

    fabric_image = np.zeros((fabric_height, fabric_width, 3), dtype=np.uint8)

    for i in range(fabric_width):  # column position
        for j in range(fabric_height):  # row position
            # Calculate the pattern index based on the position
            pattern_index = (i * epi // square_size + j * ppi //
                             square_size) % len(weaving_pattern)

            # Check the weaving pattern
            if weaving_pattern[pattern_index] == '1':
                fabric_image[j, i] = epi_color
            else:
                fabric_image[j, i] = ppi_color

    thickened_fabric_image = np.kron(fabric_image, np.ones(
        (square_size, square_size, 1), dtype=np.uint8))

    image = Image.fromarray(thickened_fabric_image)
    return image, None


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    weaving_pattern = request.form['weaving_pattern']
    epi = int(request.form['epi'])
    ppi = int(request.form['ppi'])
    epi_color = hex_to_rgb(request.form['epi_color'])
    ppi_color = hex_to_rgb(request.form['ppi_color'])

    # if epi or ppi exceeds the limit (40)
    if epi > 40 or ppi > 40:
        error = "EPI and PPI should not exceed 40."
        return render_template('index.html', error=error)

    # screen resolution
    screen_width, screen_height = 800, 600
    image, error = generate_fabric_image(
        screen_width, screen_height, weaving_pattern, epi, ppi, epi_color, ppi_color)

    if error:
        return render_template('index.html', error=error)

    image_path = 'patterns/fabric_pattern.png'
    image.save(image_path)
    return send_file(image_path, mimetype='image/png')


if __name__ == '__main__':
    app.run()
