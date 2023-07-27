import tkinter as tk
from tkinter import colorchooser
import json




def calculate_unicode_colors(color_text, unicode_unformatted_text):
    # Get the text entered in the 'Entry' widget
    text = unicode_unformatted_text.get()
    color_text = gradient_listbox.get(0, tk.END)

    formatted_text.delete("0.0", tk.END)
    nbt_segment = f'{{"extra":['
    formatted_text.insert("0.0", nbt_segment)
    for i in range(len(text)):
        character = text[i]
        char_color = color_text[i]
        # Do something with the character here
        color_the_unicode(character, char_color)
    formatted_text.delete("end-2c")
    nbt_segment = f'], "text": ""}}'
    formatted_text.insert(tk.END, nbt_segment)
def color_the_unicode(unicode_character, color_hex):

    nbt_segment = f'{{"bold":false,"italic":false,"color":"{color_hex}", "text":"{unicode_character}"}},'
    formatted_text.insert(tk.END, nbt_segment)


    #{"extra":[{"bold":false,"italic":false,"color":"#FFFF00","text":"𝙶"}],"text":""}



def render_color_boxes(color_list, start_row=0, start_column=0):

    max_columns = 6  # You can adjust the number of columns here
    box_width = 6
    box_height = 3
    padding_x = 50
    padding_y = 55

    # Clear any existing colored boxes from the window
    for box in color_boxes:
        box.destroy()

    for i, color in enumerate(color_list):
        row, column = divmod(i, max_columns)

        # Calculate the starting position without padding
        x_pos = (column * (box_width + padding_x)) + (start_column * (box_width + padding_x))
        y_pos = (row * (box_height + padding_y)) + (start_row * (box_height + padding_y))

        # Create a colored box as a label widget and add it to the window using place()
        box = tk.Label(root, bg=color, width=box_width, height=box_height, borderwidth=4, relief="ridge")
        box.place(x=x_pos, y=y_pos)
        color_boxes.append(box)


def calculate_gradients():
    global start_color
    global end_color
    global num_steps

    # Get the value from num_steps_text and handle errors
    num_steps_str = num_steps_text.get().strip()
    if not num_steps_str:
        print("Error: Number of steps cannot be empty.")
        return

    try:
        num_steps = int(num_steps_str)
        if num_steps <= 0:
            raise ValueError("Number of steps must be a positive integer.")
    except ValueError as e:
        print("Error:", e)
        return

    gradient_list = interpolate_hex_color(start_color, end_color, num_steps)
    gradient_listbox.delete(0, tk.END)  # Clear previous items in the listbox
    for color in gradient_list:
        gradient_listbox.insert(tk.END, color)

    def get_color_list_from_listbox(gradient_list):
        color_list = []
        for index in range(gradient_list.size()):
            color = gradient_list.get(index)
            color_list.append(color)
        return color_list

    color_list = get_color_list_from_listbox(gradient_listbox)

    # Update the height of the Listbox based on the number of items in the gradient_list
    num_items = gradient_listbox.size()
    listbox_height = min(num_items, 40)  # Set a maximum height of 40 items
    gradient_listbox.config(height=listbox_height)

    # Call render_color_boxes with the desired starting row and column values.
    # The starting columns and rows act as coordinates for the boxes, and are the reason they are so precise.
    render_color_boxes(color_list, start_row=1.73,start_column=6.45)

    calculate_unicode_colors(gradient_list, unicode_unformatted_text)

def update_start_color():
    global start_color
    start_color = colorchooser.askcolor()[1]
    start_color_rectangle.config(bg=start_color)
    start_hex_text.delete(0, tk.END)
    start_hex_text.insert(0, start_color)
    calculate_gradients()

def update_end_color():
    global end_color
    end_color = colorchooser.askcolor()[1]
    end_color_rectangle.config(bg=end_color)
    end_hex_text.delete(0, tk.END)
    end_hex_text.insert(0, end_color)
    calculate_gradients()

def interpolate_hex_color(gradient_start_color, gradient_end_color, gradient_steps):
    def hex_to_rgb(hex_color):
        return tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))

    def rgb_to_hex(rgb_color):
        return '#{0:02x}{1:02x}{2:02x}'.format(*rgb_color)

    gradient_end_rgb = hex_to_rgb(gradient_end_color)
    gradient_start_rgb = hex_to_rgb(gradient_start_color)

    gradient_r_step = (gradient_end_rgb[0] - gradient_start_rgb[0]) / (gradient_steps - 1)
    gradient_g_step = (gradient_end_rgb[1] - gradient_start_rgb[1]) / (gradient_steps - 1)
    gradient_b_step = (gradient_end_rgb[2] - gradient_start_rgb[2]) / (gradient_steps - 1)

    gradient = []
    for i in range(gradient_steps):
        gradient_r = int(gradient_start_rgb[0] + gradient_r_step * i)
        gradient_g = int(gradient_start_rgb[1] + gradient_g_step * i)
        gradient_b = int(gradient_start_rgb[2] + gradient_b_step * i)
        gradient.append(rgb_to_hex((gradient_r, gradient_g, gradient_b)))

    return gradient

def update_interpolation_length():
    txt_len = len(unicode_unformatted_text.get())

    num_steps_text.delete(0, tk.END)
    num_steps_text.insert(0, txt_len)  # Remove the extra closing parenthesis here
    slider.set(txt_len)

num_steps = 30
color_boxes = []  # Initialize the list of colored boxes

# Create the main window
root = tk.Tk()
root.title("Color Picker")
root.configure(bg="#151619")
ui_color = "#1d1d1f"
text_color = "#ffffff"

# Set the position of the window
start_color = "#1d1d1f"
end_color = "#1d1d1f"
window_width = 1920
window_height = 1080
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (-8)  # Centered horizontally
y_position = (0)  # Centered vertically

root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Color Rectangle
start_color_rectangle = tk.Label(root, width=20, height=5, bg="#FFFFFF")
start_color_rectangle.place(x=50, y=100)
start_color_rectangle.configure(bg=ui_color)


# Second Color Rectangle
end_color_rectangle = tk.Label(root, width=20, height=5, bg="#FFFFFF")
end_color_rectangle.place(x=210, y=100)
end_color_rectangle.configure(bg=ui_color)

# Color Picker Button
start_pick_color_button = tk.Button(root, text="Pick a Color", command=update_start_color)
start_pick_color_button.place(x=50, y=190)
start_pick_color_button.configure(bg=ui_color)
start_pick_color_button.configure(fg=text_color)


# Set # to text length
set_text_len_button = tk.Button(root, text="Set # To Text Length", command=update_interpolation_length)
set_text_len_button.place(x=235, y=230)
set_text_len_button.configure(bg=ui_color)
set_text_len_button.configure(fg=text_color)
set_text_len_button.config(highlightbackground="#0088ff", highlightcolor="#0088ff")

# Second Color Picker Button
end_pick_color_button = tk.Button(root, text="Pick a Color", command=update_end_color)
end_pick_color_button.place(x=210, y=190)
end_pick_color_button.configure(bg=ui_color)
end_pick_color_button.configure(fg=text_color)

# Editable Text Box for Hex Color
start_hex_text = tk.Entry(root, width=10)
start_hex_text.place(x=135, y=190)
start_hex_text.configure(bg=ui_color)
start_hex_text.configure(fg=text_color)

# Editable Text Box for Second Hex Color
end_hex_text = tk.Entry(root, width=10)  # Added the variable for the second hex text box
end_hex_text.place(x=290, y=190)  # Adjusted the x position for the second hex text box
end_hex_text.configure(bg=ui_color)
end_hex_text.configure(fg=text_color)

# Editable Text Box for Unicode
unicode_unformatted_text = tk.Entry(root, width=106)
unicode_unformatted_text.insert(0, "𝐔𝐍𝐈𝐂𝐎𝐃𝐄 𝐃𝐀𝐓𝐀 𝐆𝐎𝐄𝐒 𝐇𝐄𝐑𝐄")  # Initialize the textbox
unicode_unformatted_text.place(x=50.5, y=70)
unicode_unformatted_text.configure(bg=ui_color)
unicode_unformatted_text.configure(fg=text_color)

# Editable Text Box for Final Product
formatted_text = tk.Text(root, width=140, height=42)  # You can change the height as desired
formatted_text.pack(fill=tk.BOTH, expand=True)
formatted_text.place(x=697, y=70)
formatted_text.configure(bg=ui_color)
formatted_text.configure(fg=text_color)


import tkinter as tk

# Assuming you have defined the root and ui_color variables.

# Canvas for displaying software guide
canvas = tk.Canvas(root, width=180, height=640)
canvas.pack()
canvas_x = 173
canvas_y = 265
canvas.place(x=canvas_x, y=canvas_y)
canvas.configure(bg=ui_color)

# Text To Go In Canvas
text_x_coordinate = 94
text_y_coordinate = 320
text_to_display = '''
How to use: Click "Pick A Color" to select the first color in the gradient, then do the same for the ending color of the gradient by using the second button. Then enter the string of unicode you want to color into the box at the top. The"Set # to text length" button sets the gradient length to the length of your string so you can fit it perfectly into the text. If you want to have different number of colors, you can set it with the slider or text box. The colored boxes show how many colors you currently have. When you're done you can copy your code from the box on the left into your NBT edit client in Minecraft. Please note that the output you are given is NOT A MINECRAFT command. It is a piece of nbt formatting meant to be used in combination with the NBT edit mod.
'''
text_wrap_length = 180  # Set the desired wrap length (adjust as needed)

canvas.create_text(text_x_coordinate, text_y_coordinate, text=text_to_display, font=("Arial", 12), fill="white", width=text_wrap_length)

def on_slider_change(value):
    num_steps_text.delete(0, tk.END)
    num_steps_text.insert(0, value)
    print("Slider value:", value)
    calculate_gradients()

slider_value = tk.DoubleVar()  # You can use tk.IntVar() for integer values
slider = tk.Scale(root, variable=slider_value, from_=2, to=84, orient=tk.HORIZONTAL, command=on_slider_change)
slider.set(50)  # Set the initial value to 50
global read_slider_value
read_slider_value = slider.get()
slider.place(x=130, y=216)
slider.configure(bg=ui_color)
slider.configure(fg=text_color)

def on_entry_change(*args):
    # This function will be called whenever the entry text is changed
    global slider
    try:
        # Get the value from the text box
        value = float(num_steps_text_var.get())
        # Set the value to the slider
        slider.set(value)
    except ValueError:
        pass  # If the value in the text box is not a valid float, do nothing

num_steps_text = tk.Entry(root, width=10)
num_steps_text.place(x=50, y=235)
# Bind the <<Modified>> event to the on_entry_change function using trace
num_steps_text_var = tk.StringVar()
num_steps_text.config(textvariable=num_steps_text_var)
num_steps_text_var.trace("w", on_entry_change)
num_steps_text.configure(bg=ui_color)
num_steps_text.configure(fg=text_color)

# Editable Text Box for Gradient Interpolation Steps

# Initialize the textbox with the default value of num_steps
num_steps_text_var.set(str(num_steps))

#####LISTBOX#####
# Create the Listbox to display the gradient colors
gradient_listbox = tk.Listbox(root, width=20, height=10)
gradient_listbox.place(x=50, y=265)
gradient_listbox.configure(bg=ui_color)
gradient_listbox.configure(fg=text_color)

# Call calculate_gradients initially to populate the Listbox with the default gradient
calculate_gradients()

root.mainloop()
