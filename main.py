import pyttsx3
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os

class PDFToAudioConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF to Audio Converter - Multiple Files")
        self.root.geometry("700x500")
        
        # Initialize text-to-speech engine
        self.tts_engine = pyttsx3.init()
        self.selected_files = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF to Audio Converter", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        files_frame = ttk.LabelFrame(main_frame, text="PDF Files", padding="10")
        files_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Buttons for file management
        button_frame = ttk.Frame(files_frame)
        button_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        add_files_button = ttk.Button(button_frame, text="Add PDF Files", command=self.add_files)
        add_files_button.grid(row=0, column=0, padx=(0, 10))
        
        remove_files_button = ttk.Button(button_frame, text="Remove Selected", command=self.remove_selected)
        remove_files_button.grid(row=0, column=1, padx=(0, 10))
        
        clear_all_button = ttk.Button(button_frame, text="Clear All", command=self.clear_all_files)
        clear_all_button.grid(row=0, column=2)
        
        # File list
        list_frame = ttk.Frame(files_frame)
        list_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # Listbox with scrollbar
        self.files_listbox = tk.Listbox(list_frame, height=6, selectmode=tk.MULTIPLE)
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.files_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Voice settings
        settings_frame = ttk.LabelFrame(main_frame, text="Voice Settings", padding="10")
        settings_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Speech rate
        ttk.Label(settings_frame, text="Speech Rate:").grid(row=0, column=0, sticky=tk.W)
        self.rate_var = tk.StringVar(value="200")
        rate_scale = ttk.Scale(settings_frame, from_=100, to=300, 
                              variable=self.rate_var, orient=tk.HORIZONTAL, length=200)
        rate_scale.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=10)
        self.rate_label = ttk.Label(settings_frame, text="200 WPM")
        self.rate_label.grid(row=0, column=2)
        rate_scale.configure(command=self.update_rate_label)
        
        # Voice selection
        ttk.Label(settings_frame, text="Voice:").grid(row=1, column=0, sticky=tk.W, pady=(10, 0))
        self.voice_var = tk.StringVar()
        self.voice_combo = ttk.Combobox(settings_frame, textvariable=self.voice_var, 
                                       state="readonly", width=30)
        self.voice_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=10, pady=(10, 0))
        self.populate_voices()
        
        # Output options
        output_frame = ttk.LabelFrame(main_frame, text="Output Options", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Conversion mode
        self.conversion_mode = tk.StringVar(value="separate")
        ttk.Radiobutton(output_frame, text="Create separate audio file for each PDF", 
                       variable=self.conversion_mode, value="separate").grid(row=0, column=0, sticky=tk.W)
        ttk.Radiobutton(output_frame, text="Combine all PDFs into one audio file", 
                       variable=self.conversion_mode, value="combined").grid(row=1, column=0, sticky=tk.W)
        
        # Output prefix/name
        ttk.Label(output_frame, text="Output Name/Prefix:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        self.output_name = tk.StringVar(value="converted_audio")
        output_entry = ttk.Entry(output_frame, textvariable=self.output_name, width=30)
        output_entry.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Convert button
        self.convert_button = ttk.Button(main_frame, text="Convert to Audio", 
                                        command=self.start_conversion)
        self.convert_button.grid(row=4, column=0, columnspan=3, pady=20)
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to convert - Add PDF files to begin")
        self.status_label.grid(row=6, column=0, columnspan=3, pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        files_frame.columnconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        output_frame.columnconfigure(0, weight=1)
    
    def add_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        for file_path in file_paths:
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                filename = os.path.basename(file_path)
                self.files_listbox.insert(tk.END, filename)
        
        self.update_status()
    
    def remove_selected(self):
        selected_indices = self.files_listbox.curselection()
        for index in reversed(selected_indices):  # Remove from end to maintain indices
            self.files_listbox.delete(index)
            self.selected_files.pop(index)
        
        self.update_status()
    
    def clear_all_files(self):
        self.files_listbox.delete(0, tk.END)
        self.selected_files.clear()
        self.update_status()
    
    def update_status(self):
        count = len(self.selected_files)
        if count == 0:
            self.status_label.config(text="Ready to convert - Add PDF files to begin")
        elif count == 1:
            self.status_label.config(text="1 PDF file ready for conversion")
        else:
            self.status_label.config(text=f"{count} PDF files ready for conversion")
    
    def populate_voices(self):
        voices = self.tts_engine.getProperty('voices')
        voice_names = []
        for voice in voices:
            name = voice.name if hasattr(voice, 'name') else str(voice.id)
            voice_names.append(name)
        
        self.voice_combo['values'] = voice_names
        if voice_names:
            self.voice_combo.current(0)
    
    def update_rate_label(self, value):
        self.rate_label.config(text=f"{int(float(value))} WPM")
    
    def start_conversion(self):
        if not self.selected_files:
            messagebox.showerror("Error", "Please select at least one PDF file!")
            return
        
        if not self.output_name.get().strip():
            messagebox.showerror("Error", "Please enter an output name/prefix!")
            return
        
        # Start conversion in separate thread
        self.convert_button.config(state="disabled")
        self.progress.config(mode='determinate', maximum=100)
        self.progress['value'] = 0
        
        thread = threading.Thread(target=self.convert_pdfs_to_audio)
        thread.daemon = True
        thread.start()
    
    def convert_pdfs_to_audio(self):
        try:
            # Configure TTS engine
            rate = int(float(self.rate_var.get()))
            self.tts_engine.setProperty('rate', rate)
            
            # Set voice if selected
            voices = self.tts_engine.getProperty('voices')
            if self.voice_combo.current() >= 0:
                selected_voice = voices[self.voice_combo.current()]
                self.tts_engine.setProperty('voice', selected_voice.id)
            
            mode = self.conversion_mode.get()
            total_files = len(self.selected_files)
            
            if mode == "combined":
                self.convert_combined()
            else:
                self.convert_separate()
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", 
                            f"An error occurred: {str(e)}"))
            self.root.after(0, lambda: self.status_label.config(text="Conversion failed!"))
        
        finally:
            # Re-enable button
            self.root.after(0, lambda: self.convert_button.config(state="normal"))
            self.root.after(0, lambda: self.progress.config(value=100))
    
    def convert_combined(self):
        """Combine all PDFs into one audio file"""
        self.root.after(0, lambda: self.status_label.config(text="Combining all PDFs..."))
        
        combined_text = ""
        total_files = len(self.selected_files)
        
        for i, file_path in enumerate(self.selected_files):
            try:
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    filename = os.path.basename(file_path)
                    
                    # Add filename as separator
                    combined_text += f"\n\nReading from {filename}.\n\n"
                    
                    for page_num, page in enumerate(pdf_reader.pages):
                        text = page.extract_text()
                        clean_text = text.strip().replace('\n', ' ')
                        combined_text += clean_text + " "
                
                # Update progress
                progress = int((i + 1) / total_files * 80)  # Use 80% for reading
                self.root.after(0, lambda p=progress: self.progress.config(value=p))
                self.root.after(0, lambda f=filename: 
                              self.status_label.config(text=f"Processed: {f}"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showwarning("Warning", 
                                f"Error reading {os.path.basename(file_path)}: {str(e)}"))
        
        if combined_text.strip():
            self.root.after(0, lambda: self.status_label.config(text="Generating combined audio file..."))
            output_file = f"{self.output_name.get()}_combined.wav"
            self.tts_engine.save_to_file(combined_text, output_file)
            self.tts_engine.runAndWait()
            
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                            f"Combined audio file saved as: {output_file}"))
            self.root.after(0, lambda: self.status_label.config(text="Combined conversion completed!"))
        else:
            self.root.after(0, lambda: messagebox.showerror("Error", 
                            "No text found in any PDF files!"))
    
    def convert_separate(self):
        """Convert each PDF to a separate audio file"""
        total_files = len(self.selected_files)
        successful_conversions = 0
        
        for i, file_path in enumerate(self.selected_files):
            try:
                filename = os.path.basename(file_path)
                base_name = os.path.splitext(filename)[0]
                
                self.root.after(0, lambda f=filename: 
                              self.status_label.config(text=f"Converting: {f}"))
                
                with open(file_path, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    full_text = ""
                    
                    for page in pdf_reader.pages:
                        text = page.extract_text()
                        clean_text = text.strip().replace('\n', ' ')
                        full_text += clean_text + " "
                    
                    if full_text.strip():
                        output_file = f"{self.output_name.get()}_{base_name}.wav"
                        self.tts_engine.save_to_file(full_text, output_file)
                        self.tts_engine.runAndWait()
                        successful_conversions += 1
                    else:
                        self.root.after(0, lambda f=filename: messagebox.showwarning("Warning", 
                                        f"No text found in: {f}"))
                
                # Update progress
                progress = int((i + 1) / total_files * 100)
                self.root.after(0, lambda p=progress: self.progress.config(value=p))
                
            except Exception as e:
                self.root.after(0, lambda f=filename, err=str(e): messagebox.showwarning("Warning", 
                                f"Error converting {f}: {err}"))
        
        # Show completion message
        if successful_conversions > 0:
            self.root.after(0, lambda: messagebox.showinfo("Success", 
                            f"Successfully converted {successful_conversions} out of {total_files} PDF files!"))
            self.root.after(0, lambda: self.status_label.config(text=f"Conversion completed! {successful_conversions}/{total_files} successful"))
        else:
            self.root.after(0, lambda: messagebox.showerror("Error", 
                            "No PDF files were successfully converted!"))

def main():
    root = tk.Tk()
    app = PDFToAudioConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()