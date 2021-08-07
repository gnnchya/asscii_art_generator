# A very simple Flask Hello World app for you to get started with...
from flask import Flask, render_template, request
import requests
from io import BytesIO
from PIL import Image

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("main_page.html")

@app.route("/", methods=["POST"])
def assccii():
    ASCII_CHARS = ['@','#','%','?','S','+','=','*',':',',','.']

    if request.form['submit'] == 'Submit URL' :
        pic = request.form['imageURL']
        r = requests.get(pic)
        image = Image.open(BytesIO(r.content)).convert('L')

    elif request.form['submit'] == 'Submit File' :
        image = Image.open(request.files['imageFile']).convert('L')


    #Convert to 300 px
    w = image.size[0]
    h = image.size[1]
    if w < h:
        ratio = h/w
        h = int(ratio*300)
        w = 300
    elif w == h:
        w = 300
        h = 300

    elif w>h :
        ratio = w/h
        h = 300
        w = int(ratio*300)

    range_width = 25
    #resize the image
    image = image.resize((w,h))
    #get all pixel values and put them into the list
    pixel_in_image = (list(image.getdata()))
    #convert each pixel into character according to the tone of the pixel
    #in greyscale we have 255 tones and we assign each 25 tones to 1 character
    #create a list that contains each pixel that converted into character
    pixels_to_chars = [ASCII_CHARS[int(pixel_value/range_width)] for pixel_value in pixel_in_image]
    pixels_to_chars = "".join(pixels_to_chars)
    len_pixels_to_chars = len(pixels_to_chars)

    #divide the characters into lines
    if w <= h:
        image_ascii = [pixels_to_chars[index: index + w] for index in range(0, len_pixels_to_chars, w)]
    else:
        image_ascii = [pixels_to_chars[index: index + w] for index in range(0, len_pixels_to_chars, w)]

    x = "\n".join(image_ascii)


    return render_template("result.html", x=x)
