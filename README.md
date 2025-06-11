# Wikipedia Scraper 


This project demonstrates how to collect structured and semi-structured data from an open API and enrich it with data scraped from Wikipedia.

You will retrieve historical political leaders for several countries using a REST API, then scrape their biographies using BeautifulSoup. Finally, the data is saved locally for further use in data science workflows.



## Prerequisites

Make sure you have **Python 3.12.10** installed.

- Download from: https://www.python.org/downloads/release/python-31210/
- Add Python to your system PATH.

>  This project was tested with Python 3.12.10. Other versions may cause compatibility issues (e.g., with pandas or ipykernel).


## Environment Setup

This project uses a virtual environment (`.venv`) to isolate its dependencies.

### Why use a virtual environment?

- Prevents conflicts between Python packages
- Ensures consistency across machines
- Keeps your system Python clean

### Setup Instructions

Run the following commands in a Bash-compatible terminal (e.g., Git Bash):

```bash
chmod +x setup-env.sh
./setup-env.sh
```

## Running the Application

You can run the project either via **Jupyter Notebook** or as a **standalone script**.

### Run in Notebook Mode

1. Open `wikipedia_scraper.ipynb` in **VS Code**
2. Select the `.venv` kernel
3. Run each cell step by step


### Run in Script Mode (recommended)

This mode uses `main.py` to launch the full scraping pipeline.

```bash
chmod +x run-main.sh
./run-main.sh
```
## Technologies Used

- **Python 3.12.10**  
  The main programming language used for building the entire scraping pipeline.

- **`requests`**  
  For sending HTTP requests to APIs and web pages to retrieve data.

- **`beautifulsoup4`**  
  Used for parsing and navigating HTML content from Wikipedia pages.

- **`pandas`**  
  Powerful library for manipulating and organizing data into structured DataFrames.

- **`json`**  
  Native Python module to serialize and deserialize JSON data (used for saving final output).

- **`re` (regex)**  
  Python's built-in regular expressions module for text pattern matching and data cleaning.

- **`multiprocessing`** *(optional)*  
  For parallelizing API requests or processing multiple items simultaneously to improve performance.

## Feature Completion Table (**this is not yet accurate - implementation pending**)

| Feature                                                                                                    | Required Type  | Implemented |
|------------------------------------------------------------------------------------------------------------|----------------------|-------------|
| Create a virtual environment using `venv`                                                                  | Mandatory      | ✅ Yes |
| Install required packages via `requirements.txt`                                                           | Mandatory      | ✅ Yes |
| Call an external API using `requests`                                                                      | Mandatory      | ✅ Yes |
| Handle cookies to access the API                                                                           | Mandatory      | ✅ Yes |
| Retrieve list of countries via `/countries` endpoint                                                       | Mandatory      | ✅ Yes |
| Retrieve list of leaders via `/leaders` endpoint                                                           | Mandatory      | ✅ Yes |
| Retrieve and parse Wikipedia bio from `wikipedia_url`                                                     | Mandatory       | ✅ Yes |
| Extract first paragraph using `BeautifulSoup`                                                              | Mandatory      | ✅ Yes |
| Save results in a structured JSON file                                                                     | Mandatory      | ✅ Yes |
| Create a custom exception with proper handling                                                             | Mandatory      | ✅ Yes |
| Provide a Jupyter notebook (`wikipedia_scraper.ipynb`) that shows the workflow                            | Mandatory       | ✅ Yes |
| Refactor into a Python module `leaders_scraper.py` with OOP design (`WikipediaScraper` class)             | Mandatory       | ✅ Yes |
| Implement the `WikipediaScraper` class with all required attributes & methods                             | Mandatory       | ✅ Yes |
| Provide a `main.py` script to run the scraper                                                              | Mandatory      | ✅ Yes |
| Create a GitHub repository with meaningful name and clean folder structure                                 | Mandatory      | ✅ Yes |
| Write a clear README with description, installation, usage, visuals, etc.                                  | Mandatory      | ✅ Yes |
| Use `requests.Session()` instead of `requests.get()`                                                       | Optional       | ✅ Yes |
| Implement CSV export option                                                                                | Optional       | ❌ No  |
| Speed up scraping using multiprocessing                                                                    | Optional       | ❌ No  |
| Use regex to clean text data                                                                               | Optional       | ✅ Yes |
| Organize must-have and nice-to-have code in separate Git branches                                          | Optional       | ❌ No  |


## License
This project is for educational purposes as part of the BeCode data science curriculum.