import tkinter as tk
from PIL import Image, ImageDraw, ImageOps
import numpy as np
from tensorflow.keras.models import load_model

#  Here this part for Load trained model
model = load_model("digit_model.h5")

# To Create main window
window = tk.Tk()
window.title("Digit Recognizer")
# for height and weight 
canvas_width = 300
canvas_height = 300
pen_width = 15
pen_color = "black"

# For Canvas to draw
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()

# Image for PIL drawing
image1 = Image.new("L", (canvas_width, canvas_height), color=255)
draw = ImageDraw.Draw(image1)

# Drawing function
def paint(event):
    x1, y1 = (event.x - pen_width), (event.y - pen_width)
    x2, y2 = (event.x + pen_width), (event.y + pen_width)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline=pen_color)
    draw.ellipse([x1, y1, x2, y2], fill=0)  # Always draw black in model image

canvas.bind("<B1-Motion>", paint)

# Clear function
def clear():
    canvas.delete("all")
    draw.rectangle([0, 0, canvas_width, canvas_height], fill=255)
    result_label.config(text="Draw a digit and click Predict.")
    feedback_label.config(text="")

# Predict on button click
def predict():
    resized = image1.resize((28, 28))
    inverted = ImageOps.invert(resized)
    img_array = np.array(inverted) / 255.0
    img_array = img_array.reshape(1, 28, 28, 1)

    prediction = model.predict(img_array, verbose=0)
    predicted_digit = np.argmax(prediction)
    result_label.config(text=f"Predicted Digit: {predicted_digit}")
    feedback_label.config(text="Was this correct?")

# User feedback buttons
def mark_correct():
    feedback_label.config(text="✅ Marked as Correct")

def mark_wrong():
    feedback_label.config(text="❌ Marked as Wrong")

#  pen size
def set_pen_size(size):
    global pen_width
    pen_width = size

#  pen color
def set_pen_color(color):
    global pen_color
    pen_color = color

# Buttons and UI
btn_clear = tk.Button(window, text="Clear", command=clear)
btn_clear.pack(pady=5)

btn_predict = tk.Button(window, text="Predict", command=predict)
btn_predict.pack(pady=5)

# Pen size buttons
pen_frame = tk.Frame(window)
tk.Label(pen_frame, text="Pen Size:").pack(side=tk.LEFT)
tk.Button(pen_frame, text="Thin", command=lambda: set_pen_size(8)).pack(side=tk.LEFT)
tk.Button(pen_frame, text="Thick", command=lambda: set_pen_size(20)).pack(side=tk.LEFT)
pen_frame.pack(pady=5)

# Pen color buttons
color_frame = tk.Frame(window)
tk.Label(color_frame, text="Pen Color:").pack(side=tk.LEFT)
colors = {
    "Red": "red", "Orange": "orange", "Yellow": "yellow",
    "Green": "green", "Blue": "blue", "Indigo": "indigo", "Violet": "violet"
}
for name, hexcode in colors.items():
    tk.Button(color_frame, bg=hexcode, width=2, command=lambda c=hexcode: set_pen_color(c)).pack(side=tk.LEFT, padx=2)
color_frame.pack(pady=5)

# Result label
result_label = tk.Label(window, text="Draw a digit and click Predict.", font=("Arial", 14))
result_label.pack(pady=5)

# Correct/Wrong buttons
feedback_buttons = tk.Frame(window)
tk.Button(feedback_buttons, text="✅ Correct", command=mark_correct).pack(side=tk.LEFT, padx=10)
tk.Button(feedback_buttons, text="❌ Wrong", command=mark_wrong).pack(side=tk.LEFT, padx=10)
feedback_buttons.pack(pady=5)

feedback_label = tk.Label(window, text="", font=("Arial", 12))
feedback_label.pack()

# Start app
window.mainloop()
