import json
import time
import random
import urllib.request
from textwrap import wrap

from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne


def get_thought():
    url = 'https://www.reddit.com/r/Showerthoughts/top/.json?t=hour&limit=1'
    try:
        with urllib.request.urlopen(url) as f:
            parsed_json = json.loads(f.read())
            thought = parsed_json['data']['children'][0]['data']['title']
            return thought
    except urllib.error.HTTPError as e:
        return e


def render(thought):
    inky_display = InkyPHAT("red")
    inky_display.set_border(inky_display.RED)
    img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(img)

    bg_colour = random.choice([inky_display.RED, inky_display.BLACK])
    for y in range(0, inky_display.height):
        for x in range(0, inky_display.width):
            img.putpixel((x, y), bg_colour)

    thought_list = wrap(thought, 30)

    text_font = ImageFont.truetype(FredokaOne, 14)
    line_margin = 15

    if len(thought_list) >= 9:
        text_font = ImageFont.truetype(FredokaOne, 12)
        thought_list = wrap(thought, 35)
        line_margin = 13
    elif len(thought_list) == 8:  # DONE
        thought_list = wrap(thought, 32)
        text_font = ImageFont.truetype(FredokaOne, 13)

    y_pos = 2
    font_colour = inky_display.WHITE
    for thought_line in thought_list:
        draw.text((5, y_pos), thought_line, font_colour, text_font)
        y_pos += line_margin

    inky_display.set_image(img)
    inky_display.show()


if __name__ == '__main__':
    thought = get_thought()

    # loop to "handle" the 'Too many requests' error
    while '429' in str(thought):
        print(f'{thought} - retrying...')
        time.sleep(5)
        thought = get_thought()
    render(thought)
