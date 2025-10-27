# Web-Scraper 🚀
An intuitive desktop application for extracting data from any website without writing complex code.

Built with Python, Tkinter, and BeautifulSoup.

This tool was created to simplify web scraping. Instead of writing complex scripts, you can configure your CSS selectors through a simple interface, specifying whether you want to extract the visible text or a specific attribute (such as a link href or image src).

✨ Main Features
*Simple Graphical Interface*: website inspection skills are required. All configuration is done through a point-and-click interface.

*Flexible Selection (Text vs. Attribute)*: The real strength of this app. You can choose whether to extract:

  - *Text*: The textual content of a tag (e.g., "Product Title").

  - *Attribute*: A hidden value in a tag (e.g., extracting `href` from an `<a>` link).

*Asynchronous Scraping (No-Freeze)*: Scraping runs in a separate thread. The UI will never freeze while the app is processing.

*Automatic Link Resolution*: If you extract a relative link (e.g., /page.html), the app will automatically convert it to an absolute link (e.g., https://site.com/page.html).

*Column Configuration*: Define the data you want to extract as columns (e.g., "Title," "Price," "Link"), just like in a spreadsheet.

🚀 Quick Start
1. Paste the URL of the site you want to extract data from.
2. Add columns by pressing "Add Selector Row" for each data item you need.
3. Define the CSS Selector to find the element (e.g., h2.product-title).
4. Choose the Type:
  - Click "Text" to extract the text.
  - Click "Attribute" to extract an attribute and enter its name (e.g., href).
5. Start scraping by pressing "Run Scraping."
6. The results will appear in the text area below!

# 🛠️ Installation and Startup
To run this application on your computer:

1. Clone the Repository

Bash
- `git clone https://github.com/RoccoFerrari/web-scraper`
- `cd REPO_NAME`

2. (Recommended) Create a Virtual Environment

Bash
  **On macOS/Linux**
- `python3 -m venv venv`
- `source venv/bin/activate`

  **On Windows**
- `python -m venv venv`
- .\venv\Scripts\activate`

3. Use the `requirements.txt` file to install dependencies

Bash
- `pip install -r requirements.txt`

4. Start the Application

Bash
- `python main_gui.py # Or the name of your main Python file`

💻 Technologies Used
  Python 3.x

  Tkinter: For the graphical user interface (GUI).

  BeautifulSoup4: For HTML parsing.

  Requests: For downloading web pages.

  Threading: For asynchronous scraping.
