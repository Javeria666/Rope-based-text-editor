import tkinter as tk
from tkinter import filedialog, messagebox
from rope import make_rope, insert, delete

# Global variable to hold the rope structure for text
text_rope = make_rope()

def update_text_widget(text_widget):
    global text_rope
    text_value = text_rope[0]
    text_widget.delete("1.0", tk.END)
    text_widget.insert(tk.END, text_value)

def handle_insert(text_widget):
    global text_rope
    text_content = text_widget.get("1.0", tk.END).strip()  # Get the entire text content
    sentences = text_content.split(".")  # Split into sentences (assuming sentences end with period)

    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            text_rope = insert(text_rope, len(text_rope[0]), sentence)

    # Update the text widget and display the Rope structure in the terminal
    update_text_widget(text_widget)
    print("Current Rope Structure:")
    print(text_rope)

def open_file(text_widget):
    global text_rope
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            content = file.read()
            text_rope = make_rope(content)
            update_text_widget(text_widget)

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        text_value = text_rope[0]
        with open(file_path, "w") as file:
            file.write(text_value)

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
text_widget = tk.Text(root, wrap="word", height=20, width=80)
text_widget.pack(padx=10, pady=10)

# Bind key events to text widget
text_widget.bind("<Return>", lambda event: handle_insert(text_widget))  # Press Enter to insert text

# Create buttons for opening, saving files and word count
open_button = tk.Button(root, text="Open File", command=lambda: open_file(text_widget))
open_button.pack(side=tk.LEFT, padx=(10, 5), pady=10)

save_button = tk.Button(root, text="Save File", command=save_file)
save_button.pack(side=tk.LEFT, padx=(5, 10), pady=10)

word_count_button = tk.Button(root, text="Word Count", command=count_words)
word_count_button.pack(side=tk.LEFT, padx=10, pady=10)

# Run the main event loop
root.mainloop()
