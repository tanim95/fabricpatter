from flask import Flask, render_template, request
import numpy as np
from PIL import Image, ImageTk

app = Flask(__name__)


def generate_fabric_image(epi, ppi, weaving_pattern, yarn_count):
    if yarn_count > 500:
        message = f"Yarn count is too high: {yarn_count}"
        return message

    fabric_image = np.zeros((ppi, epi, 3), dtype=np.uint8)

    # RGB values based on the weaving pattern and yarn count
    for i in range(ppi):
        for j in range(epi):
            if weaving_pattern[i % len(weaving_pattern)] == '1':
                if (i % 2 == 0 and j % 2 == 0) or (i % 2 != 0 and j % 2 != 0):
                    fabric_image[i, j] = [255, 0, 0]  # Red color for weave
                else:
                    # Blue color for non-weave
                    fabric_image[i, j] = [0, 0, yarn_count]
            else:
                # White color for non-weave
                fabric_image[i, j] = [255, 255, 255]

    return fabric_image


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    epi = int(request.form['epi'])
    ppi = int(request.form['ppi'])
    weaving_pattern = request.form['weaving_pattern']
    yarn_count = int(request.form['yarn_count'])

    if yarn_count > 500:
        error = f"Yarn count is too high: {yarn_count}"
        return render_template('index.html', error=error)

    colors = []
    for i in range(ppi):
        if weaving_pattern[i % len(weaving_pattern)] == '1':
            if (i % 2 == 0):
                colors.append('red')
            else:
                colors.append(f'rgb(0, 0, {yarn_count})')
        else:
            colors.append('white')

    return render_template('result.html', colors=colors)


if __name__ == '__main__':
    app.run()
