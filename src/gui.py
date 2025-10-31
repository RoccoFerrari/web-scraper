import tkinter as tk
import threading
import scraper_logic as sl
from queue import Queue, Empty
from tkinter import ttk
from tkinter import scrolledtext
from class_selectors import GUIRef, AbstractSelector, TagSelector, AttributeSelector
from typing import List
from tkinter import scrolledtext, filedialog
from data_handler import save_data

class WebScraperGUI:
    """
    This class creates the Graphical User Interface (GUI) for a 
    web scraper using Tkinter.
    
    It allows adding dynamic selectors, distinguishing between
    extracting tag text content or a specific attribute.
    It does NOT contain any business logic (scraping, saving).
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper GUI")
        self.root.geometry("700x600")
        
        # --- Style ---
        self.style = ttk.Style()
        self.style.theme_use('clam') 

        
        # Queue used to receive results from the scraping thread
        self.result_queue = Queue()

        self.last_results = None # Memory of last results
        self.save_button = None # Reference to the Save button
        self.run_button = None

        self.save_dialog_configs = {
            'csv': {
                'filetypes': [('CSV files', '*.csv'), ('All files', '*.*')],
                'defaultextension': '.csv'
            },
            'json': {
                'filetypes': [('JSON files', '*.json'), ('All files', '*.*')],
                'defaultextension': '.json'
            }
            # Future formats can be added here
        }

        # Track dynamic selector rows (initialized before creating selector UI)
        self.selector_rows = []

        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Build GUI Sections ---
        self.create_url_section(main_frame)
        self.create_selectors_section(main_frame)
        self.create_run_section(main_frame)
        self.create_results_section(main_frame)
        self.create_save_section(main_frame)

    def create_url_section(self, parent_frame):
        """Creates the URL input section."""
        url_frame = ttk.Frame(parent_frame, padding=(0, 5))
        url_frame.pack(fill='x')

        url_label = ttk.Label(url_frame, text="URL:", width=10)
        url_label.pack(side=tk.LEFT, padx=(0, 5))

        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(fill='x', expand=True, side=tk.LEFT)

    def create_selectors_section(self, parent_frame):
        """Creates the main container for dynamic selectors."""
        # Use a LabelFrame for visual grouping
        self.selectors_main_frame = ttk.LabelFrame(parent_frame, text="Selectors", padding="10")
        self.selectors_main_frame.pack(fill='x', pady=5)

        # Add the first selector row as required
        self.add_selector_row(is_first_row=True)

    def add_selector_row(self, is_first_row=False):
        """
        Adds a new row (a Frame) with all widgets needed
        to define a single selector (selector string, type, and attribute).
        """
        row_frame = ttk.Frame(self.selectors_main_frame)
        row_frame.pack(fill='x', pady=2)

        # 1. Label
        selector_label = ttk.Label(row_frame, text="Selector:", width=10)
        selector_label.pack(side=tk.LEFT, padx=(0, 5))

        # 2. Selector Entry
        selector_entry = ttk.Entry(row_frame)
        selector_entry.pack(fill='x', expand=True, side=tk.LEFT, padx=5)

        # 3. Toggle Button (Text / Attribute)
        # This button controls the extraction type
        toggle_button = ttk.Button(row_frame, text="Text", width=10)
        toggle_button.pack(side=tk.LEFT, padx=5)

        # 4. Attribute Name Entry (e.g., "href") - Starts disabled
        attr_entry = ttk.Entry(row_frame, width=15, state='disabled')
        attr_entry.pack(side=tk.LEFT, padx=5)
        
        # 5. Add (+) or Remove (x) Button
        if is_first_row:
            action_button = ttk.Button(
                row_frame, 
                text="+", 
                width=3, 
                command=lambda: self.add_selector_row(is_first_row=False)
            )
        else:
            # Subsequent rows get a 'x' button to remove themselves
            action_button = ttk.Button(
                row_frame, 
                text="x", 
                width=3,
                # Lambda passes the specific frame to be destroyed
                command=lambda rf=row_frame: self.remove_selector_row(rf)
            )
        action_button.pack(side=tk.LEFT, padx=5)
        
        # Configure the toggle button's command AFTER creating attr_entry
        toggle_button.config(
            command=lambda b=toggle_button, e=attr_entry: self.toggle_extraction_type(b, e)
        )

        # Store references to the widgets for data collection
        self.selector_rows.append({
            "frame": row_frame,
            "selector": selector_entry,
            "type_button": toggle_button,
            "attribute": attr_entry
        })

    def remove_selector_row(self, row_frame):
        """Removes a selector row from the GUI and the tracking list."""
        row_to_remove = None
        # Find the corresponding item in our tracking list
        for row in self.selector_rows:
            if row["frame"] == row_frame:
                row_to_remove = row
                break
        
        if row_to_remove:
            # 1. Remove widgets from GUI
            row_frame.destroy()
            # 2. Remove reference from tracking list
            self.selector_rows.remove(row_to_remove)

    def toggle_extraction_type(self, button, attribute_entry):
        """
        Pure GUI logic: Toggles the button text and enables/disables
        the attribute entry field.
        """
        current_text = button['text']
        if current_text == "Text":
            # Switch to Attribute mode
            button.config(text="Attribute")
            attribute_entry.config(state='normal')
            attribute_entry.insert(0, "href") # Insert a common default
        else:
            # Switch back to Text mode
            button.config(text="Text")
            attribute_entry.delete(0, tk.END) # Clear the entry
            attribute_entry.config(state='disabled')

    def create_run_section(self, parent_frame):
        """Creates the 'Run' button."""
        run_frame = ttk.Frame(parent_frame, padding=(0, 10))
        run_frame.pack(fill='x')

        self.run_button = ttk.Button(
            run_frame, 
            text="Run", 
            command=self.execute_connector # Connects to the data gathering function
        )
        self.run_button.pack()

    def create_results_section(self, parent_frame):
        """Creates the text area for results, with a scrollbar."""
        # Use a LabelFrame for visual grouping
        results_frame = ttk.LabelFrame(parent_frame, text="Output", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        # ScrolledText is a compound widget that includes a Text widget
        # and a Scrollbar, managing them automatically.
        self.results_text = scrolledtext.ScrolledText(
            results_frame, 
            height=10, 
            wrap=tk.WORD, # Wrap lines at word boundaries
            state='disabled' # Start as read-only
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)


    def create_save_section(self, parent_frame):
        """Creates the save options (CSV/JSON Radio buttons)."""
        save_frame = ttk.Frame(parent_frame, padding=(0, 5))
        save_frame.pack(fill='x')

        save_label = ttk.Label(save_frame, text="Save as:", width=10)
        save_label.pack(side=tk.LEFT, padx=(0, 5))

        # Tkinter control variable to store the selected value
        self.save_format_var = tk.StringVar(value="csv") # Default to 'csv'

        csv_radio = ttk.Radiobutton(
            save_frame, 
            text="CSV", 
            variable=self.save_format_var, 
            value="csv"
        )
        csv_radio.pack(side=tk.LEFT, padx=5)

        json_radio = ttk.Radiobutton(
            save_frame, 
            text="JSON", 
            variable=self.save_format_var, 
            value="json"
        )
        json_radio.pack(side=tk.LEFT, padx=5)

        self.save_button = ttk.Button(
            save_frame,
            text="Save Results",
            command=self.save_results, 
            state='disabled'          
        ) 
        self.save_button.pack(side=tk.RIGHT, padx=10)

    def execute_connector(self):
        """
        This function is connected to the 'Run' button.
        It collects and validates all data from the GUI to build the GUIRef object.
        
        It writes to the output area ONLY if a validation error occurs.
        The actual scraping logic should be called at the end of this function.
        """
        
        # Prepare the text area (clear it, ready for results or errors)
        self.results_text.config(state='normal')
        self.results_text.delete('1.0', tk.END)

        self.last_results = None # 
        self.save_button.config(state='disabled')
        self.run_button.config(state='disabled')

        # Flag to track validation errors
        has_errors = False

        # Collect URL and Format 
        url = self.url_entry.get()
        save_format = self.save_format_var.get()
        
        # Validate URL
        if not url:
            self.results_text.insert(tk.END, "Error: The URL field is required.\n")
            has_errors = True
        
        # Build Selector Objects 
        cols_to_extract: List[AbstractSelector] = [] # Typo fixed (extratc -> extract)

        for i, row in enumerate(self.selector_rows):
            selector_str = row["selector"].get()
            scrape_type = row["type_button"]["text"]
            
            if not selector_str:
                continue

            try:
                if scrape_type == "Text":
                    job = TagSelector(selector_str)
                    cols_to_extract.append(job)
                
                elif scrape_type == "Attribute":
                    attr_name = row["attribute"].get()
                    if not attr_name:
                        # Validation Error: Attribute name is missing
                        self.results_text.insert(tk.END, f"Error Row {i+1}: 'Attribute' type selected, but attribute name is missing.\n")
                        has_errors = True
                        continue
                    
                    job = AttributeSelector(attr_name, selector_str)
                    cols_to_extract.append(job)
            
            except Exception as e:
                 # This is likely a programming error, but we show it
                 self.results_text.insert(tk.END, f"Error processing row {i+1}: {e}\n")
                 has_errors = True
        
        # Validate that at least one selector was added
        if not cols_to_extract and not has_errors:
            # Only show this if no other errors were found
            self.results_text.insert(tk.END, "Error: No valid selectors were configured.\n")
            has_errors = True
        
        # Stop if any validation errors were found 
        if has_errors:
            self.results_text.insert(tk.END, "\nPlease fix the errors and try again.")
            self.results_text.config(state='disabled') # Lock the text area
            self.run_button.config(state='normal')
            return # Stop the function

        # Create the GUIRef object 
        # At this point, we know the input data is valid.
        try:
            gui_data_object = GUIRef(url=url, format=save_format, selectors=cols_to_extract)
        except Exception as e:
            self.results_text.insert(tk.END, f"\n--- Critical Error ---\nCould not create data object: {e}\n")
            self.results_text.config(state='disabled')
            self.run_button.config(state='normal')
            return
        
        #### Scraping function logic
        self.results_text.insert(tk.END, f"Scraping from {gui_data_object.url}...\n")

        job_thread = threading.Thread(
            target=sl.execute_scraping,
            args=(gui_data_object, self.result_queue)
        )
        job_thread.daemon = True # Allow the app to close even if the thread is executing
        job_thread.start()

        self.root.after(100, self.process_queue)

        self.results_text.config(state='disabled')

    def process_queue(self):
        """
        Controlls resulting_queue with no blocking GUI
        """
        try:
            # Try to get an elem from queue without stop the process
            result = self.result_queue.get_nowait()

            self.run_button.config(state='normal')

            # Reset and prepare the results text area
            self.results_text.config(state='normal')
            self.results_text.delete('1.0', tk.END)

            if isinstance(result, Exception):
                self.results_text.insert(tk.END, f"--- Scraping failed ---\n\n{result}")
                self.last_results = None
                self.save_button.config(state='disabled')

            else:
                self.results_text.insert(tk.END, "--- Scraping results ---\n\n")
                if not result:
                    self.results_text.insert(tk.END, "No data found with those selectors")
                    self.last_results = None
                    self.save_button.config(state='disabled')
                
                else:
                    self.last_results = result 
                    self.save_button.config(state='normal') 
                
                    for row in result:
                        cleaned_row = [str(item) if item is not None else "N/A" for item in row]
                        self.results_text.insert(tk.END, " : ".join(cleaned_row) + "\n")

            # Lock the text area again
            self.results_text.config(state='disabled')

        except Empty:
            self.root.after(100, self.process_queue)

    def save_results(self):
        """
        Called when the "Save Results" button is clicked.
        This function handles saving the last scraped results
        """
        # Check if there are results to save
        if not self.last_results:
            self.results_text.config(state='normal')
            self.results_text.insert(tk.END, "\n--- No data to save ---")
            self.results_text.config(state='disabled')
            return
            
        # Get selected format
        save_format = self.save_format_var.get()
        
        # Get the dialog configuration from the registry
        dialog_config = self.save_dialog_configs.get(save_format)
        
        # Handle missing dialog configuration
        if not dialog_config:
            self.results_text.config(state='normal')
            self.results_text.insert(tk.END, f"\n--- Error: configuration not found '{save_format}' ---")
            self.results_text.config(state='disabled')
            return
            
        # Opnen the Save As dialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=dialog_config['defaultextension'],
            filetypes=dialog_config['filetypes'],
            title="Save results as..."
        )
        
        # Check if the user provided a filepath
        if not filepath:
            return 
            
        # Call the saving logic
        try:
            save_data(self.last_results, save_format, filepath)
            
            self.results_text.config(state='normal')
            self.results_text.insert(tk.END, f"\n--- Results found in: {filepath} ---")
            self.results_text.config(state='disabled')
            
        except Exception as e:
            self.results_text.config(state='normal')
            self.results_text.insert(tk.END, f"\n--- Error during saving: {e} ---")
            self.results_text.config(state='disabled')