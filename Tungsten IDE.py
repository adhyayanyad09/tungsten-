import tkinter as tk
from tkinter import filedialog
import re

# Symbol table to store variables
variables = {}

# Define the version of Tungsten IDE
TUNGSTEN_VERSION = "1.1"

# Interpreter for Tungsten language
def run_tungsten_code(code):
    output = ""
    lines = code.strip().split("\n")

    for line in lines:
        line = line.strip()

        if line.startswith("print("):
            output += handle_print(line) + "\n"
        elif line.startswith("let"):
            output += handle_variable(line) + "\n"
        elif line.startswith("for"):
            output += handle_for_loop(line)
        elif line.startswith("if"):
            output += handle_if_statement(line) + "\n"
    
    return output.strip()

# Handle print statement (e.g., print("Hi") or print(x))
def handle_print(line):
    # Extract content inside print() (it can be a string or variable)
    match = re.match(r'print\((.*)\)', line)
    if match:
        content = match.group(1).strip()  # Get the content inside print()

        # If it's a variable, we need to retrieve its value
        if content in variables:
            return variables[content]
        
        # If it's a string, return the string
        if content.startswith('"') and content.endswith('"'):
            return content[1:-1]  # Remove quotes
        
        return "Error: Invalid print statement"
    return "Error: Invalid print statement"

# Handle variable declaration and assignment (e.g., let x = 5)
def handle_variable(line):
    match = re.match(r'let (\w+) = (.+)', line)
    if match:
        var_name = match.group(1)
        value = match.group(2).strip()
        
        # If the value is a number, store it as an integer
        if value.isdigit():
            variables[var_name] = value
        # If the value is a variable, get its value
        elif value in variables:
            variables[var_name] = variables[value]
        else:
            return "Error: Invalid variable value"

        return f"{var_name} = {variables[var_name]}"  # Show the variable assignment in output
    return "Error: Invalid variable declaration"

# Handle for loop (e.g., for i in 1 to 5:)
def handle_for_loop(line):
    match = re.match(r'for (\w+) in (\d+) to (\d+):', line)
    if match:
        var_name = match.group(1)
        start = int(match.group(2))
        end = int(match.group(3))

        loop_output = ""
        for i in range(start, end + 1):
            variables[var_name] = str(i)
            loop_output += f"{i}\n"  # Directly print the loop value (no need for handle_print)

        return loop_output
    return "Error: Invalid for loop"

# Handle if statements (e.g., if x == 5 then:)
def handle_if_statement(line):
    match = re.match(r'if (.*) then:', line)
    if match:
        condition = match.group(1).strip()
        # Check if the condition is in the form of "x == 5"
        if condition == "x == 5" and "x" in variables and variables["x"] == "5":
            return "Condition met: x is 5"
        return "Condition not met"
    return "Error: Invalid if statement"

# GUI setup for the Tungsten IDE using Tkinter
class TungstenIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("Tungsten IDE")
        
        # Create text area for code input
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack()

        # Create Run button to execute code
        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack()

        # Create Version button to show the version
        self.version_button = tk.Button(self.root, text="Version", command=self.show_version)
        self.version_button.pack()

        # Create Save button to save the code
        self.save_button = tk.Button(self.root, text="Save", command=self.save_code)
        self.save_button.pack()

        # Create Load button to load code from a file
        self.load_button = tk.Button(self.root, text="Load", command=self.load_code)
        self.load_button.pack()

        # Create output text area
        self.output_text = tk.Text(self.root, height=10, width=50, state=tk.DISABLED)
        self.output_text.pack()

    def run_code(self):
        code = self.text_area.get("1.0", "end-1c")  # Get the code from the text area
        output = run_tungsten_code(code)  # Execute the Tungsten code
        self.display_output(output)  # Show the output in the output area

    def display_output(self, output):
        # Enable output text area to display result
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)  # Clear previous output
        self.output_text.insert(tk.END, output)  # Insert the new output
        self.output_text.config(state=tk.DISABLED)  # Disable editing output text area

    def show_version(self):
        # Display the version of the Tungsten IDE
        version_message = f"Tungsten IDE Version: {TUNGSTEN_VERSION}"
        self.display_output(version_message)

    def save_code(self):
        # Open a file dialog to choose where to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".tungsten", filetypes=[("Tungsten Files", "*.tungsten"), ("Text Files", "*.txt")])
        
        if file_path:
            # Get the code from the text area and save to the chosen file
            code = self.text_area.get("1.0", "end-1c")
            with open(file_path, 'w') as file:
                file.write(code)
            self.display_output(f"Code saved to: {file_path}")

    def load_code(self):
        # Open a file dialog to choose a file to load
        file_path = filedialog.askopenfilename(defaultextension=".tungsten", filetypes=[("Tungsten Files", "*.tungsten"), ("Text Files", "*.txt")])
        
        if file_path:
            # Read the code from the file and insert into the text area
            with open(file_path, 'r') as file:
                code = file.read()
            self.text_area.delete("1.0", tk.END)  # Clear the text area
            self.text_area.insert(tk.END, code)  # Load the code into the text area
            self.display_output(f"Code loaded from: {file_path}")

# Run the Tungsten IDE
if __name__ == "__main__":
    root = tk.Tk()
    ide = TungstenIDE(root)
    root.mainloop()
