import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import font
# Rope data structure for efficient text manipulation
# Rope data structure for efficient text manipulation
def build_rope(string):

    #Base case: If the length of the string is small (keeping it less than or equal to 11), represent it directly as a leaf node to optimize memory usage and simplify operations
    if len(string) <= 11:
        return [string, None, None, len(string)] #Return a list representing leaf node: No left or Right children
    
    mid = len(string) // 2 #find midpoint
    while mid < len(string) and string[mid] != " ": #Loop until a suitable split point is found(at space) /the end of the string is reached
        mid+=1

    #Splitting the string into left and right substrings
    left_substring = string[:mid]

    if mid<len(string):
        right_substring = string[mid:]

    #If no desired split point found (e.g., no space found in the remaining string), we represent the entire string directly as a leaf node to avoid unnecessary splitting
    if left_substring== string or mid==len(string):
         return [string, None, None, len(string)]
    else:
        #Recursively build Rope structures for left and right substrings
        left = build_rope(left_substring)
        right = build_rope(right_substring)
    
    #Calculating the total weight of the current Rope node
    weight = len(string)
    #Return a new Rope node with left and right children and total weight
    return [None, left, right, weight]

def rope_to_string(rope):
    if rope is None:
        return ""  # Return empty string if rope is None (as there is nothing to convert)
    
    value, left, right, _ = rope
    
    if value is not None:
        return value    

    # Recursively process left and right nodes if value is None (which means current node is not a leaf node, rather it is an internal node)
    left_string = rope_to_string(left)
    right_string = rope_to_string(right)
    
    #Concatenating the strings obtained from the left and right child nodes to form the final string representation of the Rope
    return left_string + right_string

def concatenate(rope1, rope2):
    if rope1[0] is None: #If rope1 is empty, return rope2. There's no need for concatenation.
        return rope2
    if rope2[0] is None: # If rope2 is empty, return rope1. There's no need for concatenation.
        return rope1
    

    #If both rope1 and rope2 contain data, we need to create a new Rope node to represent their concatenation
    #The new node will have None as its value (indicating an internal node),
    #rope1 as its left child, rope2 as its right child,
    #and the total weight of rope1 and rope2 as the weight of the new node
    new_root = [None, rope1, rope2, rope1[3] + rope2[3]]
    
    return new_root #returning new node after concatenation.

def split(rope, index):
    value, left, right, weight = rope
    # If index is at the beginning, split into two ropes with the first being empty and the second being the original rope
    if index == 0:
        return [None, None, rope, 0], rope
    # If index is at the end, split into two ropes with the first being the original rope and the second being empty
    if index == weight:
        return rope, [None, rope, None, 0]
    
    
    if left is None: #If there's no left child node, split the right subtree
        left_split = [None, None, None, 0]
        right_split = rope
    
    
    elif index < left[3]: #iIf the index is within the left subtree
        # Recursively split the left subtree
        left_split, right_split = split(left, index)
        left = right_split
    
    elif index > left[3]: # If the index is within the right subtree
        #recursively split the right subtree
        left_split, right_split = split(right, index - left[3])
        right = left_split

    if right is None: #if there's no right child node, create an empty right subtree
        right_split = [None, None, None, 0]
    
    #ccheck if left or right is None before accessing their weights
    left_weight = left[3] if left else 0
    right_weight = right[3] if right else 0
    weight = left_weight + right_weight
    
    return [None, left, right, weight], [None, left, right, weight] #new nodes w updated weights

def insert(rope, index, new_string):
    #split the rope at the specified index
    left, right = split(rope, index)
    #build a new rope from the new string
    new_rope = concatenate(left, build_rope(new_string))
    #join or concatenate the left split rope, new rope, and right split rope
    return concatenate(new_rope, right)

def delete(rope, start_index, end_index):
    #split the rope at the start index
    left, right = split(rope, start_index) #left = portion before deletion, right = portion after deletion start
    
    _, right = split(right, end_index - start_index) #right = portion after deletion end, end index-start index gives length of the substring which needs to be deleted
    #concatenate the left split rope and the right split rope 
    return concatenate(left, right)

def replace_all(text, search_word, replace_word):
    index = 0
    #loop until all occurrences of the search word are replaced
    while True:
        #ffind the next occurrence of the search word
        index = text.find(search_word, index)
        #ifno more occurrences are found, break the loop
        if index == -1:
            break
        #replace the search word with the replace word in the text
        text = text[:index] + replace_word + text[index + len(search_word):]
        # Move the index forward by the length of the replace word
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
        self.selected_font = tk.StringVar()
        self.selected_font.set("Arial")  # Default font
        
        self.create_widgets()
        self.update_word_count()  # Initial word count
        self.bind("<Control-z>", self.undo)
        self.bind("<Key>", self.on_text_change)
        self.bind("<Delete>", self.on_delete_key_press)  # Bind Delete key press event
    
    def create_widgets(self):
        self.text_area = tk.Text(self, wrap="word")
        self.text_area.pack(expand=True, fill="both")
        self.text_area.bind("<Key>", self.on_text_change)
        
        font_label = tk.Label(self, text="Font:")
        font_label.pack(side=tk.LEFT, padx=(10, 0))
        
        font_options = font.families()
        self.font_menu = tk.OptionMenu(self, self.selected_font, *font_options, command=self.change_font)
        self.font_menu.pack(side=tk.LEFT)
        
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
        edit_menu.add_separator()
        edit_menu.add_command(label="Bold", command=self.toggle_bold)
        edit_menu.add_command(label="Italic", command=self.toggle_italic)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        
        self.config(menu=menu_bar)

    
    def toggle_bold(self):
    # Get the current font style of the selected text
        font_style = font.Font(font=self.text_area.tag_cget(tk.SEL, "font"))
        
        # Check if the selected text is already bold
        if font_style.actual()['weight'] == 'bold':
            # If bold, reset to normal weight (non-bold)
            font_style.configure(weight='normal')
        else:
            # If not bold, set to bold weight
            font_style.configure(weight='bold')
        
        # Apply the updated font style to the selected text
        self.text_area.tag_configure("bold_style", font=font_style)
        self.text_area.tag_add("bold_style", tk.SEL_FIRST, tk.SEL_LAST)

    def toggle_italic(self):
        # Get the current font style of the selected text
        font_style = font.Font(font=self.text_area.tag_cget(tk.SEL, "font"))
        
        # Check if the selected text is already italic
        if font_style.actual()['slant'] == 'italic':
            # If italic, reset to normal slant (non-italic)
            font_style.configure(slant='roman')
        else:
            # If not italic, set to italic slant
            font_style.configure(slant='italic')
        
        # Apply the updated font style to the selected text
        self.text_area.tag_configure("italic_style", font=font_style)
        self.text_area.tag_add("italic_style", tk.SEL_FIRST, tk.SEL_LAST)


    def apply_text_style(self, font_style):
        # Get the current selection range
        start_index = self.text_area.index(tk.SEL_FIRST)
        end_index = self.text_area.index(tk.SEL_LAST)
        
        # Apply the updated font style to the selected text
        self.text_area.tag_configure("text_style", font=font_style)
        self.text_area.tag_add("text_style", start_index, end_index)

    def change_font(self, *args):
        selected_font = (self.selected_font.get(), 12)  # 12 is the default font size
        font_style = font.Font(font=self.text_area['font'])
        font_style.configure(family=self.selected_font.get())
    
        # Get the current selection range
        start_index = self.text_area.index(tk.SEL_FIRST)
        end_index = self.text_area.index(tk.SEL_LAST)
        
        # Apply the selected font to the selected text
        self.text_area.tag_configure("selected", font=font_style)
        self.text_area.tag_add("selected", start_index, end_index)

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

        search_count_label = tk.Label(search_window, text="Searched Word Count: 0")
        search_count_label.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        def update_search_count():
            search_word = search_entry.get()
            if search_word:
                text = self.text_area.get("1.0", tk.END)
                search_count = text.count(search_word)
                search_count_label.config(text=f"Searched Word Count: {search_count}")
            else:
                search_count_label.config(text="Searched Word Count: 0")

        def on_search_key_press(event):
            update_search_count()

        search_entry.bind("<KeyRelease>", on_search_key_press)
        search_entry.bind("<Key>", on_search_key_press)



        def replace():
            search_word = search_entry.get()
            replace_word = replace_entry.get()
            text = self.text_area.get("1.0", tk.END)
            new_text = replace_all(text, search_word, replace_word)
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert("1.0", new_text)
            search_window.destroy()

        replace_button = tk.Button(search_window, text="Replace", command=replace)
        replace_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        cancel_button = tk.Button(search_window, text="Cancel", command=search_window.destroy)
        cancel_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def on_delete_key_press(self, event):
        # Capture the deleted characters before updating the text_rope
        deleted_characters = self.get_deleted_characters()
        if deleted_characters:
            self.undo_stack.append(deleted_characters)



if __name__ == "__main__":
    app = TextEditorApp()
    app.mainloop()
