import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from openai import OpenAI
import os
import threading

class OpenAIDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🦜🔗 OpenAI Desktop App")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Variables
        self.api_key_var = tk.StringVar()
        self.temperature_var = tk.DoubleVar(value=0.7)
        self.max_tokens_var = tk.IntVar(value=500)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🦜🔗 OpenAI Desktop App", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # API Key section
        ttk.Label(main_frame, text="OpenAI API Key:").grid(row=1, column=0, sticky=tk.W, pady=5)
        api_key_entry = ttk.Entry(main_frame, textvariable=self.api_key_var, 
                                 show="*", width=50)
        api_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(5, 0))
        
        # Load API key from environment if available
        env_key = os.getenv('OPENAI_API_KEY')
        if env_key:
            self.api_key_var.set(env_key)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="5")
        settings_frame.grid(row=1, column=2, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        
        # Temperature
        ttk.Label(settings_frame, text="Temperature:").grid(row=0, column=0, sticky=tk.W)
        temp_scale = ttk.Scale(settings_frame, from_=0.0, to=2.0, 
                              variable=self.temperature_var, orient=tk.HORIZONTAL)
        temp_scale.grid(row=0, column=1, sticky=(tk.W, tk.E))
        temp_label = ttk.Label(settings_frame, text="0.7")
        temp_label.grid(row=0, column=2)
        
        # Max tokens
        ttk.Label(settings_frame, text="Max Tokens:").grid(row=1, column=0, sticky=tk.W)
        tokens_spinbox = ttk.Spinbox(settings_frame, from_=50, to=2000, 
                                    textvariable=self.max_tokens_var, width=10)
        tokens_spinbox.grid(row=1, column=1, sticky=tk.W)
        
        # Update temperature label
        def update_temp_label(*args):
            temp_label.config(text=f"{self.temperature_var.get():.1f}")
        self.temperature_var.trace('w', update_temp_label)
        
        # Input text area
        ttk.Label(main_frame, text="Enter your prompt:").grid(row=2, column=0, sticky=(tk.W, tk.N), pady=(10, 5))
        self.input_text = scrolledtext.ScrolledText(main_frame, height=8, wrap=tk.WORD)
        self.input_text.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                            pady=(10, 5), padx=(5, 0))
        self.input_text.insert('1.0', 'What are the three key pieces of advice for learning how to code?')
        
        # Submit button
        self.submit_btn = ttk.Button(main_frame, text="Generate Response", 
                                    command=self.generate_response_threaded)
        self.submit_btn.grid(row=3, column=1, pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=3, column=2, sticky=(tk.W, tk.E), pady=10, padx=(10, 0))
        
        # Output text area
        ttk.Label(main_frame, text="AI Response:").grid(row=4, column=0, sticky=(tk.W, tk.N), pady=(10, 5))
        self.output_text = scrolledtext.ScrolledText(main_frame, height=10, wrap=tk.WORD, 
                                                    state=tk.DISABLED)
        self.output_text.grid(row=4, column=1, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), 
                             pady=(10, 5), padx=(5, 0))
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Menu bar
        self.setup_menu()
        
    def setup_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Clear Input", command=self.clear_input)
        file_menu.add_command(label="Clear Output", command=self.clear_output)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
    def clear_input(self):
        self.input_text.delete('1.0', tk.END)
        
    def clear_output(self):
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete('1.0', tk.END)
        self.output_text.config(state=tk.DISABLED)
        
    def show_about(self):
        messagebox.showinfo("About", 
                           "OpenAI Desktop App\n\nA simple desktop interface for OpenAI API\n\nBuilt with Python & Tkinter")
        
    def generate_response_threaded(self):
        # Run in separate thread to prevent GUI freezing
        thread = threading.Thread(target=self.generate_response)
        thread.daemon = True
        thread.start()
        
    def generate_response(self):
        try:
            # Validate API key
            api_key = self.api_key_var.get().strip()
            if not api_key or not api_key.startswith('sk-'):
                messagebox.showerror("Error", "Please enter a valid OpenAI API key!")
                return
            
            # Get input text
            input_text = self.input_text.get('1.0', tk.END).strip()
            if not input_text:
                messagebox.showerror("Error", "Please enter some text!")
                return
            
            # Update UI
            self.submit_btn.config(state=tk.DISABLED)
            self.progress.start()
            self.status_var.set("Generating response...")
            
            # Clear previous output
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete('1.0', tk.END)
            self.output_text.config(state=tk.DISABLED)
            
            # Make API call
            client = OpenAI(api_key=api_key)
            response = client.completions.create(
                model="gpt-3.5-turbo-instruct",
                prompt=input_text,
                max_tokens=self.max_tokens_var.get(),
                temperature=self.temperature_var.get()
            )
            
            # Display response
            response_text = response.choices[0].text.strip()
            self.output_text.config(state=tk.NORMAL)
            self.output_text.insert('1.0', response_text)
            self.output_text.config(state=tk.DISABLED)
            
            self.status_var.set("Response generated successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate response:\n{str(e)}")
            self.status_var.set("Error occurred")
            
        finally:
            # Reset UI
            self.submit_btn.config(state=tk.NORMAL)
            self.progress.stop()

def main():
    root = tk.Tk()
    app = OpenAIDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
