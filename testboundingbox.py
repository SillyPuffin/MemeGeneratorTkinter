from PIL import Image, ImageDraw, ImageFont

# Create a blank image
image = Image.new("RGB", (400, 300), (255, 255, 255))
draw = ImageDraw.Draw(image)

# Load a font
font = ImageFont.truetype('Fonts/ComicSans.ttf',size=50)

# Set text and position
text = "Hello World sigma boi"
xy = (350, 0)

# Get bounding box
bbox = draw.multiline_textbbox(xy, text, font=font, anchor="la")
print("Bounding box:", bbox)

# Draw the bounding box
draw.rectangle(bbox, outline="red", width=2)

# Draw the text
draw.multiline_text(xy, text, fill="black", font=font, anchor="la")

# Show the image
image.show()
