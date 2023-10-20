
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


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    weaving_pattern = request.form['weaving_pattern']

    if len(weaving_pattern) > 15:
        error = "Warp pattern should be up to 12 characters long."
        return render_template('index.html', error=error)

    epi = int(request.form['epi'])
    ppi = int(request.form['ppi'])
    epi_color = hex_to_rgb(request.form['epi_color'])
    ppi_color = hex_to_rgb(request.form['ppi_color'])

    if epi > 40 or ppi > 40:
        error = "EPI and PPI should not exceed 40."
        return render_template('index.html', error=error)

    # Increase the size of the unit square for better visibility
    square_size = 50

    # size of each segment based on the warp pattern and square size
    segment_size = square_size // len(weaving_pattern)

    # unit square pattern based on the warp pattern
    unit_square = np.zeros((square_size, square_size, 3), dtype=np.uint8)

    for i, val in enumerate(weaving_pattern):
        val = int(val)
        color = epi_color if val == 1 else ppi_color  # useing EPI color for warp threads
        start_x = i * segment_size
        end_x = (i + 1) * segment_size
        unit_square[:, start_x:end_x] = color

    # final warp fabric image by replicating the unit square
    fabric_width = square_size * epi  #
    fabric_height = square_size * ppi
    fabric_image = np.zeros((fabric_height, fabric_width, 3), dtype=np.uint8)

    for i in range(ppi):
        for j in range(epi):
            fabric_image[i * square_size: (i + 1) * square_size,
                         j * square_size: (j + 1) * square_size] = unit_square

    image = Image.fromarray(fabric_image)

    image_path = 'patterns/warp_fabric_pattern.png'
    image.save(image_path)
    return send_file(image_path, mimetype='image/png')


if __name__ == '__main__':
    app.run()

