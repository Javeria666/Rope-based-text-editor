import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Rope data structure for efficient text manipulation
def build_rope(string):
    if len(string) <= 11:
        return [string, None, None, len(string)]
    
    mid = len(string) // 2
    while mid < len(string) and string[mid] != " ":
        mid+=1
    left_substring = string[:mid]#.strip()
    if mid<len(string):
        right_substring = string[mid:]#.strip()
    if left_substring== string or mid==len(string):
         return [string, None, None, len(string)]
    else:
        left = build_rope(left_substring)
        right = build_rope(right_substring)
    
    weight = len(string)
    
    return [None, left, right, weight]

def rope_to_string(rope):
    if rope is None:
        return ""  # Return empty string if rope is None
    
    if len(rope) != 4:
        return ""  # Return empty string if rope structure is invalid
    
    value, left, right, _ = rope
    
    if value is not None:
        return value
    
    # Recursively process left and right nodes
    left_string = rope_to_string(left) if left else ""
    right_string = rope_to_string(right) if right else ""
    
    return left_string + right_string

def concatenate(rope1, rope2):
    if rope1[0] is None:
        return rope2
    if rope2[0] is None:
        return rope1
    
    new_root = [None, rope1, rope2, rope1[3] + rope2[3]]
    
    return new_root

def split(rope, index):
    value, left, right, weight = rope
    if index == 0:
        return [None, None, rope, 0], rope
    if index == weight:
        return rope, [None, rope, None, 0]
    
    if left is None:
        left_split = [None, None, None, 0]
        right_split = rope
    elif index < left[3]:
        left_split, right_split = split(left, index)
        left = right_split
    elif index > left[3]:
        left_split, right_split = split(right, index - left[3])
        right = left_split
    
    if right is None:
        right_split = [None, None, None, 0]
    
    # Check if left or right is None before accessing their weights
    left_weight = left[3] if left else 0
    right_weight = right[3] if right else 0
    weight = left_weight + right_weight
    
    return [None, left, right, weight], [None, left, right, weight]

def insert(rope, index, new_string):
    left, right = split(rope, index)
    new_rope = concatenate(left, build_rope(new_string))
    # print(rope, "insert")
    return concatenate(new_rope, right)

def delete(rope, start_index, end_index):
    left, right = split(rope, start_index)
    _, right = split(right, end_index - start_index)
    return concatenate(left, right)

def replace_all(text, search_word, replace_word):
    index = 0
    while True:
        index = text.find(search_word, index)
        if index == -1:
            break
        text = text[:index] + replace_word + text[index + len(search_word):]
        index += len(replace_word)
    return text

# Create Tkinter application
class TextEditorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Editor")
        
        self.text_rope = build_rope("")
        self.word_count = tk.StringVar()
        self.undo_stack = []
        
        self.create_widgets()
        self.update_word_count()  # Initial word count
        self.bind("<Control-z>", self.undo)
        self.bind("<Key>", self.on_text_change)
        self.bind("<Delete>", self.on_delete_key_press)  # Bind Delete key press event
    
    def create_widgets(self):
        self.text_area = tk.Text(self, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<Key>", self.on_text_change)
        
        self.status_bar = tk.Label(self, textvariable=self.word_count, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        
        self.create_menu()
        
        self.update_status_bar()

    def create_menu(self):
        menu_bar = tk.Menu(self)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Search and Replace", command=self.search_and_replace)
        edit_menu.add_command(label="Undo", command=self.undo)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        self.config(menu=menu_bar)
    def update_status_bar(self):
        undo_text = f"Undo Stack Size: {len(self.undo_stack)}"
        self.status_bar.config(text=undo_text)

    def update_word_count(self, event=None):
        # print("Updating word count...")
        word_count = self.count_words_in_rope(self.text_rope)
        # print(f"Word count: {word_count}")
        self.word_count.set(f"Words: {word_count}")
        # print("Word count updated.")

    def count_words_in_rope(self, rope):
        if rope is None:
            return 0
        
        value, left, right, _ = rope
        
        if value is not None:
            # print(value)
            # Count words in the text segment represented by this leaf node
            words = value.split()
            
            return len(words)
        
        # Recursively count words in the left and right child nodes
        return self.count_words_in_rope(left) + self.count_words_in_rope(right)

    def on_text_change(self, event=None):
        deleted_characters = self.get_deleted_characters()
        if deleted_characters:
            self.undo_stack.append(deleted_characters)
        
        self.undo_stack.append(self.text_rope)
        # Get current text content from the text area
        current_text = self.text_area.get("1.0", tk.END)
        
        # Update the rope structure to reflect the new text content
        self.text_rope = build_rope(current_text)
        # Update word count based on the new rope structure
        self.update_word_count()
        self.update_status_bar()
        print("Current Rope Structure:")
        self.print_rope_structure(self.text_rope)

    def get_deleted_characters(self):
        # Get the text before and after the cursor position
        cursor_index = self.text_area.index(tk.INSERT)
        current_text = self.text_area.get("1.0", tk.END)
        
        # Determine the position of the cursor within the text
        line, col = map(int, cursor_index.split("."))
        offset = len("\n".join(current_text.splitlines()[:line-1])) + col
        
        # Determine the character(s) that were deleted (if any)
        deleted_characters = current_text[offset - 1:offset]
        return deleted_characters
    
    def print_rope_structure(self, rope, indent=""):
        if rope is None:
            print(indent + "None")
            return
        
        value, left, right, weight = rope
        
        if value is not None:
            print(indent + f"Value: '{value}', Weight: {weight}")
        else:
            print(indent + f"Weight: {weight}")
        
        if left is not None:
            print(indent + "Left:")
            self.print_rope_structure(left, indent + "  ")
        
        if right is not None:
            print(indent + "Right:")
            self.print_rope_structure(right, indent + "  ")

    def undo(self, event=None):
         if self.undo_stack:
            self.text_rope = self.undo_stack.pop()
            self.refresh_text_area()
            self.update_word_count() 
            self.update_status_bar()
    
    def refresh_text_area(self):
        text = rope_to_string(self.text_rope)
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert("1.0", text)
        
    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                text = file.read()
                self.text_rope = build_rope(text)
                self.refresh_text_area()
                self.update_word_count()
    
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            text = rope_to_string(self.text_rope)  # Convert rope to string
            with open(file_path, "w") as f:
                f.write(text)  # Write the text to the file
            messagebox.showinfo("Save", "File saved successfully.")
    
    def search_and_replace(self):
        search_window = tk.Toplevel(self)
        search_window.title("Search and Replace")
        
        search_label = tk.Label(search_window, text="Search:")
        search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        search_entry = tk.Entry(search_window)
        search_entry.grid(row=0, column=1, padx=5, pady=5)
        
        replace_label = tk.Label(search_window, text="Replace:")
        replace_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        replace_entry = tk.Entry(search_window)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)
        
        def replace():
            search_word = search_entry.get()
            replace_word = replace_entry.get()
            text = self.text_area.get("1.0", tk.END)
            new_text = replace_all(text, search_word, replace_word)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_text)
            search_window.destroy()
        
        replace_button = tk.Button(search_window, text="Replace", command=replace)
        replace_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        cancel_button = tk.Button(search_window, text="Cancel", command=search_window.destroy)
        cancel_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    def on_delete_key_press(self, event):
        # Capture the deleted characters before updating the text_rope
        deleted_characters = self.get_deleted_characters()
        if deleted_characters:
            self.undo_stack.append(deleted_characters)



if __name__ == "__main__":
    app = TextEditorApp()
    app.mainloop()
