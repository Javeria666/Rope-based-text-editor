import tkinter as tk
from tkinter import filedialog, messagebox
from rope2 import make_rope, insert, delete

# Global variable to hold the rope structure for text
text_rope = make_rope()


def open_file():
    global text_rope
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_rope = (content, None, None, len(content))
            update_text_widget()


def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        text_rope_value = text_rope[0]
        with open(file_path, "w") as file:
            file.write(text_rope_value)


def update_text_widget():
    global text, text_rope
    text_rope_value = text_rope[0]
    text.delete("1.0", tk.END)
    text.insert(tk.END, text_rope_value)


def handle_key(event):
    global text, text_rope
    if event.keysym == "BackSpace":
        # Handle Backspace key press
        cursor_pos = int(text.index(tk.INSERT).split(".")[1])
        # Delete character before cursor using rope structure
        text_rope = delete(text_rope, cursor_pos - 1, cursor_pos)
        update_text_widget()
    elif event.keysym == "Left":
        # Move cursor left
        text.mark_set(tk.INSERT, f"1.{int(text.index(tk.INSERT).split('.')[1]) - 1}")
    elif event.keysym == "Right":
        # Move cursor right
        text.mark_set(tk.INSERT, f"1.{int(text.index(tk.INSERT).split('.')[1]) + 1}")
    else:
        # Handle other key presses by inserting characters using rope structure
        cursor_pos = int(text.index(tk.INSERT).split(".")[1])
        char = event.char
        text_rope = insert(text_rope, cursor_pos, char)
        update_text_widget()


def count_words():
    global text_rope
    text_content = text_rope[0]
    words = text_content.split()
    word_count = len(words)
    messagebox.showinfo("Word Count", f"Total Words: {word_count}")


# Create the main window
root = tk.Tk()
root.title("Simple Text Editor")

# Create a text widget for text editing
text = tk.Text(root, wrap="word", height=20, width=80)
text.pack(padx=10, pady=10)

# Bind key events to text widget
text.bind("<Key>", handle_key)
text.bind("<BackSpace>", handle_key)

# Create buttons for opening, saving files and word count
open_button = tk.Button(root, text="Open File", command=open_file)
open_button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

save_button = tk.Button(root, text="Save File", command=save_file)
save_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

word_count_button = tk.Button(root, text="Word Count", command=count_words)
word_count_button.pack(side=tk.LEFT, padx=10, pady=10)

# Run the main event loop
root.mainloop()
