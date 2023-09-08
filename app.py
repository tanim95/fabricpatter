
# from flask import Flask, render_template, request, send_file
# import numpy as np
# from PIL import Image
# import tkinter as tk

# app = Flask(__name__)


# def get_screen_resolution():
#     root = tk.Tk()
#     screen_width = root.winfo_screenwidth()
#     screen_height = root.winfo_screenheight()
#     root.destroy()
#     return screen_width, screen_height


# def generate_fabric_image(screen_width, screen_height, weaving_pattern, yarn_count, epi, ppi):
#     if yarn_count > 500:
#         return None

#     square_size = 10

#     fabric_width = screen_width // square_size
#     fabric_height = screen_height // square_size

#     fabric_image = np.zeros((fabric_height, fabric_width, 3), dtype=np.uint8)

#     for i in range(fabric_width):
#         for j in range(fabric_height):
#             if weaving_pattern[(i * epi // square_size) % len(weaving_pattern)] == '1':
#                 if (i * ppi // square_size) % 2 == 0 and (j * ppi // square_size) % 2 == 0:
#                     # Yellow color for weave
#                     fabric_image[j, i] = [255, 255, 0]
#                 else:
#                     # Green color for non-weave
#                     fabric_image[j, i] = [0, 128, 0]
#             else:
#                 # White color for non-weave
#                 fabric_image[j, i] = [255, 255, 255]

#     thickened_fabric_image = np.kron(fabric_image, np.ones(
#         (square_size, square_size, 1), dtype=np.uint8))

#     # line thickness based on yarn count
#     line_thickness = yarn_count // 10
#     thickened_fabric_image[:, :, 1] = np.where(
#         thickened_fabric_image[:, :, 1] > 0, line_thickness, 0)

#     image = Image.fromarray(thickened_fabric_image)
#     return image, None


# @app.route('/')
# def home():
#     return render_template('index.html')


# @app.route('/generate', methods=['POST'])
# def generate():
#     weaving_pattern = request.form['weaving_pattern']
#     yarn_count = int(request.form['yarn_count'])
#     epi = int(request.form['epi'])
#     ppi = int(request.form['ppi'])

#     screen_width, screen_height = get_screen_resolution()
#     image, error = generate_fabric_image(
#         screen_width, screen_height, weaving_pattern, yarn_count, epi, ppi)

#     if error:
#         return render_template('index.html', error=error)

#     image_path = 'patterns/fabric_pattern.png'
#     image.save(image_path)
#     return send_file(image_path, mimetype='image/png')


# if __name__ == '__main__':
#     app.run(debug=True)

# ..................................................................
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
    square_size = 10

    fabric_width = screen_width // square_size
    fabric_height = screen_height // square_size

    fabric_image = np.zeros((fabric_height, fabric_width, 3), dtype=np.uint8)

    for i in range(fabric_width):
        for j in range(fabric_height):
            if weaving_pattern[(i * epi // square_size) % len(weaving_pattern)] == '1':
                if (i * ppi // square_size) % 2 == 0 and (j * ppi // square_size) % 2 == 0:
                    fabric_image[j, i] = epi_color
                else:
                    fabric_image[j, i] = ppi_color
            else:
                fabric_image[j, i] = [0, 0, 0]  # Non weave color

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

    # Check if epi or ppi exceeds the limit (40)
    if epi > 40 or ppi > 40:
        error = "EPI and PPI should not exceed 40."
        return render_template('index.html', error=error)

    #  screen resolution
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
