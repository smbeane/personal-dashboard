import urllib
from PIL import Image
from letters import letters_temp

def setURLImage(canvas, albumCover, x_length, y_length, x_start, y_start):
  dirPath = "/home/smbeane5235/spotify/testing/albumCover.png"
  urllib.request.urlretrieve(albumCover, dirPath)

  image = Image.open(dirPath)
  image = image.resize((24, 24))

  setImage(canvas, image, 24, 24, 2, 4)  
  
  return image
def setImage(canvas, image, length_x, length_y, start_x, start_y):
  if(image.mode != "RGB"):
    image = image.convert("RGB")

  allpixels = list(image.getdata())

  for y in range(0, length_y):
    for x in range(0, length_x):
      color = allpixels[y * length_x + x]
      canvas.SetPixel(x + start_x, y + start_y, color[0], color[2], color[1]) 
  
def setBubbles(canvas, bubblesFilled ):
  bubbleCount = 0

  for x in range(0, 35):
    for y in range(0, 5):
      #Border for duration bubbles
      if (y == 0 or y == 4 or x == 0 or x == 34):
        canvas.SetPixel(x + 27, y + 21, 255, 255, 255)
      else: 
        if(bubbleCount < bubblesFilled):
          canvas.SetPixel(x + 27, y + 21, 255, 255, 255)
          bubbleCount += 1
        else: 
          canvas.SetPixel(x + 27, y + 21, 0, 0, 0)
              
def setText(canvas, text, start_x, start_y, max_chars, r_on, g_on, b_on):
  char_count = 0
  text = text.lower()
  

  for char in text:
    if char not in letters_temp:
      continue
    if char_count >= max_chars:
      break
    for y in range(5):
      for x in range(3):
        if letters_temp[char][y][x] == 1:
          r, g, b = r_on, g_on, b_on
        else:
          r, g, b = 0, 0, 0
        canvas.SetPixel(start_x + x + char_count * 4, start_y + y, r, b, g)
    char_count += 1

def setDivider(canvas, start_x, start_y, length, r, g, b):
        for y in range(start_y, start_y + length):
          canvas.SetPixel(start_x, y, r, b, g)
