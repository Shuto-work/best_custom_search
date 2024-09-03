# README
## Custom Search API Scraping with Streamlit
This project provides a web interface using Streamlit for interacting with the Google Custom Search Engine (CSE) API. Users can input search queries and retrieve a list of phone numbers and company names from the search results, which are then output as a CSV file.

### What is Streamlit !?
It is Python library
https://docs.streamlit.io/

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

### How to get CSE_ID & API_key
For Japanese
https://www.system-exe.co.jp/kotohajime15/

### CSE
https://programmablesearchengine.google.com/intl/ja_jp/about/

## Usage
### 1, Run the Streamlit app:
```bash
streamlit run app.py
```
### 2, Input your search parameters:
- Search Keyword: The term you want to search for.
- Start Page: The starting page number for search results.
- End Page: The ending page number for search results.
- Sort Order: Choose between "Relevance" and "date".
- CSV Filename: The name of the output CSV file.
- Download the CSV file once the search is complete.
### 3, Download the CSV File 
Download the CSV File once the search is complete.

## Description
This section outlines the parameters you can set when using the Streamlit app:

- Search Keyword: The term or phrase you want to search.
- Start Page: The page number from which to start retrieving results.
- End Page: The page number at which to stop retrieving results.
- Sort Order: The sorting method for search results, either by "Relevance" or "date".
- CSV Filename: The name of the CSV file where results will be saved.
