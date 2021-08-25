from random import randint
from PIL import Image, ImageFont, ImageDraw
import os

def paint_grid(grid, w, h, filename):
    with Image.new('RGB',(w, h)) as painting:
        for i in range(h):
            for j in range(w):
                painting.putpixel((j, i), grid[i*w + j])

        if not os.path.exists(f'./{filename}/'):
            os.mkdir(f'./{filename}/')
        painting.save(f"./{filename}/{filename}.png", "PNG")
        print(f"Created {filename}.png")

def paint_text_grid(grid, w, h, colors, bg, filename):
    pixel = 10  # consider not hard-coding this

    # we need colors for all digits
    # pad with random colors
    while len(colors) < 10:
        colors[str(len(colors))] = tuple(randint(0,255) for _ in range(3))

    # I don't want white; replace with grey
    for key, value in colors.items():
        if all(x > 200 for x in value):
            colors[key] = (196, 196, 196)

    with Image.new('RGB', (pixel*w, pixel*h)) as painting:
        for i in range(pixel*h):
            for j in range(pixel*w):
                painting.putpixel((j, i), bg)
        
        draw = ImageDraw.Draw(painting)
        font = ImageFont.load_default() # consider changing to a specific font later
        for i in range(h):
            for j in range(w):
                draw.text((pixel*j, pixel*i), grid[i*w+j], font=font, fill=colors[grid[i*w+j]])

        if not os.path.exists(f'./{filename}/'):
            os.mkdir(f'./{filename}/')
        painting.save(f"./{filename}/{filename}-prime-painting.png", "PNG")
        print(f"Created {filename}-prime-painting.png")
    

if __name__ == '__main__':
    grid = input()
    colors = {(7, 36, 82): '1', (68, 124, 174): '0', (249, 250, 251): '2'}
    invert = {value: key for key,value in colors.items()}
    paint_text_grid(grid, 50, 50, invert, (255,255,255), "fixed-logo")