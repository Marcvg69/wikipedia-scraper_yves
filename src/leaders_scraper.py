# src/leaders_scraper.py

import requests
from bs4 import BeautifulSoup
import re
import json
from urllib.parse import unquote
from utils.print_utils import PrintUtils, BgColor, Color
from concurrent.futures import ThreadPoolExecutor



class WikipediaScraper:
    def __init__(self):
        # Base URL for the API that provides information about country leaders
        self.base_url = "https://country-leaders.onrender.com"

        # URL endpoint to fetch a valid session cookie
        self.cookie_url = f"{self.base_url}/cookie"

        # URL endpoint to retrieve the list of countries
        self.country_endpoint = f"{self.base_url}/countries"

        # URL endpoint to retrieve the leaders for a given country
        self.leaders_endpoint = f"{self.base_url}/leaders"

        # Create a reusable requests session for all HTTP calls (more efficient than multiple requests)
        self.session = requests.Session()

        # Retrieve and store cookies needed for API access
        self.cookie = self._get_cookies()

        # Will store leaders per country with summaries
        self.leaders_data = {}  

    def refresh_cookie(self):
        """
        Public method to refresh and return a new session cookie.

        This method is an alias for the internal _get_cookies() method.
        Returns:
        - requests.cookies.RequestsCookieJar: refreshed cookie object
        """
        self.cookie = self._get_cookies()
        return self.cookie

    def get_countries(self):
        """
        Retrieve the list of countries supported by the API.

        Returns:
        - list[str]: List of ISO country codes (e.g., ['us', 'fr', 'be'])
        """
        response = self.session.get(self.countries_url, cookies=self.cookies)
        return response.json()

    def get_leaders(self, country):
        """
        Fetch the list of political leaders for a given country.

        Parameters:
        - country (str): ISO country code (e.g., 'us', 'fr')

        Returns:
        - list[dict]: List of leaders with their metadata (excluding Wikipedia summary)
        """
        params = {"country": country}
        response = self.session.get(self.leaders_url, cookies=self.cookies, params=params)
        return response.json()


    def _get_cookies(self):
        """
        Retrieve a fresh set of cookies from the API.

        This is typically required before making further requests,
        as the API expects valid cookies for authentication or session handling.

        Returns:
        - requests.cookies.RequestsCookieJar: cookies object to be reused in subsequent API calls
        """

        # Send a GET request to the /cookie endpoint using the session
        response = self.session.get(self.cookie_url)

        # Return the cookies received in the response
        return response.cookies


    def get_first_paragraph(self, wikipedia_url):
        """
        Fetch and clean the first paragraph of a Wikipedia article.

        This method:
        - Sends a GET request to the provided Wikipedia URL
        - Parses the HTML content using BeautifulSoup
        - Finds the first meaningful paragraph (<p>) with more than 80 characters
        - Removes citation markers like [1], [2], etc. using regex
        - Returns the cleaned paragraph as a string

        Parameters:
        - wikipedia_url (str): The URL of the Wikipedia article

        Returns:
        - str: Cleaned first paragraph text, or empty string if none found
        """

        # Cyrillic or Arabic characters may display incorrectly
        # Print the human-readable URL (for debugging purposes)
        print(unquote(wikipedia_url))

        # Send HTTP GET request to the Wikipedia page
        response = self.session.get(wikipedia_url)

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Iterate over all paragraph elements
        for p in soup.find_all("p"):
            text = p.get_text(strip=True)  # Extract text and strip leading/trailing whitespace

            # Skip short or empty paragraphs
            if len(text) > 80:
                # Remove citation references like [1], [2], etc.
                cleaned = re.sub(r"\[[0-9]+\]", "", text)
                return cleaned

        # Return empty string if no suitable paragraph was found
        return ""


    def enrich_leader(self, leader):
        """
        Enrich a single leader dictionary with a cleaned Wikipedia URL and a summary paragraph.

        This method:
        - Decodes the Wikipedia URL to ensure proper character display (e.g., Cyrillic, accents)
        - Fetches and adds the first meaningful paragraph from the leader's Wikipedia page

        Parameters:
        - leader (dict): A dictionary representing a political leader, containing at least a 'wikipedia_url' key

        Returns:
        - dict: The updated leader dictionary, now including a 'summary' field (if URL was valid)
        """
        if "wikipedia_url" in leader and leader["wikipedia_url"]:
            # Decode percent-encoded characters (e.g., %D0%9F → П)
            leader["wikipedia_url"] = unquote(leader["wikipedia_url"])
            
            # Extract and attach the first paragraph of the Wikipedia page
            leader["summary"] = self.get_first_paragraph(leader["wikipedia_url"])
        
        return leader
    
    def enrich_all_leaders(self, leaders, use_multithreading=False):
        """
        Enrich a list of leaders with decoded Wikipedia URLs and summaries.

        Parameters:
        - leaders (list[dict]): list of leader dictionaries to enrich
        - use_multithreading (bool): whether to use threads for parallel enrichment

        Returns:
        - list[dict]: enriched leader dictionaries
        """
        if use_multithreading:
            with ThreadPoolExecutor() as executor:
                return list(executor.map(self.enrich_leader, leaders))
        else:
            return [self.enrich_leader(leader) for leader in leaders]


    def fetch_leaders(self, limit_per_country=None, verbose=False, use_multithreading=False):
        """
        Fetch leaders per country and enrich with Wikipedia summaries.

        Parameters:
        - limit_per_country (int or None): max number of leaders to fetch per country
        - verbose (bool): if True, print a sample of the enriched results

        Returns:
        - dict: mapping of country code to list of leader dictionaries (with Wikipedia summaries)
        """

        # Fetch the list of countries using the API and store it as a list of country codes
        countries = self.session.get(self.country_endpoint, cookies=self.cookie).json()

        # Initialize a dictionary to hold leaders grouped by country
        leaders_per_country = {}

        # Loop through each country to fetch its leaders
        for country in countries:
            # Set the country parameter for the API request
            params = {"country": country}
            
            # Fetch the list of leaders for the current country
            res = self.session.get(self.leaders_endpoint, cookies=self.cookie, params=params)
            leaders_data = res.json()

            # Optionally limit the number of leaders per country if a limit is specified
            if limit_per_country is not None:
                leaders_data = leaders_data[:limit_per_country]

            # Enrich each leader with decoded URL and Wikipedia summary
            #leaders_data = [self.enrich_leader(leader) for leader in leaders_data]

            # Enrich all leaders using multithreading if requested
            leaders_data = self.enrich_all_leaders(leaders_data, use_multithreading=use_multithreading)            

            # Store the enriched leader data in the dictionary, keyed by country
            leaders_per_country[country] = leaders_data

        # If verbose is True, print a sample of the collected data for inspection
        if verbose:
            for country, leaders in list(leaders_per_country.items())[:3]:  # Show only first 3 countries
                print(f"\nCountry: {country}")
                for leader in leaders[:5]:  # Show up to 5 leaders per country
                    summary = leader.get("summary", "")
                    print(f"- {leader.get('first_name')} {leader.get('last_name')}: {summary[:100]}...")

        # Return the full dictionary of leaders grouped by country
        self.leaders_data = leaders_per_country
        return leaders_per_country


    def to_json_file(self, filepath="leaders.json"):
        """
        Save the leaders_data attribute to a JSON file.

        Parameters:
        - filepath (str): The file path where the JSON will be written. Default is 'leaders.json'.

        This method writes the internal `self.leaders_data` dictionary to a file in JSON format.
        The output is encoded in UTF-8 and prettified for readability.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            # Serialize the dictionary to a UTF-8 encoded JSON file
            # ensure_ascii=False: keeps special characters (e.g., é, ñ, Ж, ع) intact
            # indent=2: formats the output for better readability
            json.dump(self.leaders_data, f, ensure_ascii=False, indent=2)

        # Print confirmation message in green
        PrintUtils.print_color(f"\nData saved to {filepath}", Color.GREEN)

