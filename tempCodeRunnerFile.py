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
    warp_pattern = request.form['warp_pattern']
    weft_pattern = request.form['weft_pattern']
    weaving_pattern = request.form['weaving_pattern']

    if len(warp_pattern) != len(weft_pattern) or len(warp_pattern) > 12 or len(weft_pattern) > 12:
        error = "Warp and weft patterns should be up to 12 characters long and have the same length."
        return render_template('index.html', error=error)

    epi = int(request.form['epi'])
    ppi = int(request.form['ppi'])
    epi_color = hex_to_rgb(request.form['epi_color'])
    ppi_color = hex_to_rgb(request.form['ppi_color'])

    if epi > 50 or ppi > 50:
        error = "EPI and PPI should not exceed 50."
        return render_template('index.html', error=error)

    square_size = 50

    fabric_width = square_size * epi
    fabric_height = square_size * ppi
    fabric_image = np.zeros((fabric_height, fabric_width, 3), dtype=np.uint8)

    for i in range(ppi):
        for j in range(epi):
            # Calculate the pattern index based on the position
            pattern_index = (i * epi // square_size + j * ppi //
                             square_size) % len(weaving_pattern)
            warp_char = warp_pattern[j]
            weft_char = weft_pattern[i]

            # Check the weaving pattern
            if weaving_pattern[pattern_index] == '1':
                fabric_image[i * square_size: (i + 1) * square_size,
                             j * square_size: (j + 1) * square_size] = epi_color if warp_char == '1' else ppi_color
            else:
                fabric_image[i * square_size: (i + 1) * square_size,
                             j * square_size: (j + 1) * square_size] = epi_color if weft_char == '1' else ppi_color

    image = Image.fromarray(fabric_image)

    image_path = 'patterns/fabric_pattern.png'
    image.save(image_path)
    return send_file(image_path, mimetype='image/png')


if __name__ == '__main__':
    app.run()