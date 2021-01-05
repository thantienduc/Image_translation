import os, io
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import translate_v2 as translate
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
#import binascii
import sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'image-translation-1-8558e0089908.json'

client = vision.ImageAnnotatorClient()

file_name = 'img_4.jpg'
folder_path = '/Users/ducthantien/Documents/Image_translation/images'
with io.open(os.path.join(folder_path,file_name),'rb') as image_file:
    content = image_file.read()
#img = Image.open(folder_path+'/'+file_name)
image = vision.types.Image(content=content)

respond = client.text_detection(image = image)
annotations = respond.text_annotations

min_y = min(annotations[0].bounding_poly.vertices[0].y,annotations[0].bounding_poly.vertices[1].y,
annotations[0].bounding_poly.vertices[2].y,annotations[0].bounding_poly.vertices[3].y)
max_y = max(annotations[0].bounding_poly.vertices[0].y,annotations[0].bounding_poly.vertices[1].y,
annotations[0].bounding_poly.vertices[2].y,annotations[0].bounding_poly.vertices[3].y)
lines = annotations[0].description.split('\n')
count=len(lines)
font_size = int((max_y-min_y)/(count*1.33))
#print(int(font_size))

img = Image.open(folder_path+'/'+file_name)

#print(img.size)
#img = Image.frombytes('RGBA', (size,size), content, 'raw')
draw = ImageDraw.Draw(img)
#print(type(img))
font = ImageFont.truetype('Arial.ttf', font_size)
temp = annotations[0].description.split(' ')[0]
for annotation in annotations:
    if temp == annotation.description:
        start_x = annotation.bounding_poly.vertices[0].x
        start_y = annotation.bounding_poly.vertices[0].y
        break

draw.text((start_x, start_y), "hello", (255, 255, 255), font=font)
#current_y = start_y

for line in lines:

    translate_client = translate.Client()
    result = translate_client.translate(line,target_language = 'vi')
    #print(result)
    draw.text((start_x, current_y), result['translatedText'], (255, 255, 255), font=font)
    current_y += font_size*1.33

img.save('img_5.jpg')
