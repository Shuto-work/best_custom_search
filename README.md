# README
## Custom Search API Scraping with Streamlit
This project provides a web interface using Streamlit for interacting with the Google Custom Search Engine (CSE) API. Users can input search queries and retrieve a list of phone numbers and company names from the search results, which are then output as a CSV file.

## Features
Search Functionality: Search using custom keywords and retrieve results from Google CSE.
Pagination: Specify which pages of search results to retrieve.
Sort Order: Choose between relevance-based and date-based sorting.
CSV Output: Export search results to a CSV file.

## Installation
Clone the repository:
```bash
git clone <repository-url>
```
## Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
Create a secrets.toml file with your API key and CSE ID:
```toml
api_key = "YOUR_API_KEY"
cse_id = "YOUR_CSE_ID"
```

## Usage
### 1, Run the Streamlit app:
```bash
streamlit run app.py
```
### 2, Input your search parameters:
Search Keyword: The term you want to search for.
Start Page: The starting page number for search results.
End Page: The ending page number for search results.
Sort Order: Choose between "Relevance" and "date".
CSV Filename: The name of the output CSV file.
Download the CSV file once the search is complete.