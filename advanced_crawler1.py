import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os

# --- Configuration ---
CSV_INPUT_FILE = 'universities.csv'
CSV_OUTPUT_FILE = 'fyup_advanced_scan_results.csv'
KEYWORDS = [
    'Four-Year Undergraduate Programme',
    'FYUP',
    '4-year degree'
]
MAX_PAGES_PER_SITE = 100

# --- Main Crawler Logic ---
def crawl_and_get_context(base_url):
    """
    Crawls a website, finds all occurrences of keywords, and extracts the context.
    """
    pages_to_visit = [base_url]
    visited_pages = set()
    found_data = []
    page_count = 0
    base_domain = urlparse(base_url).netloc
    
    print(f"\n🚀 Scanning: {base_domain}")

    while pages_to_visit and page_count < MAX_PAGES_PER_SITE:
        current_url = pages_to_visit.pop(0)

        if current_url in visited_pages:
            continue
            
        visited_pages.add(current_url)
        page_count += 1
        
        try:
            response = requests.get(current_url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Search through specific tags to find the paragraph/sentence
            text_elements = soup.find_all(['p', 'li', 'td', 'span', 'h1', 'h2', 'h3'])
            
            for element in text_elements:
                element_text = element.get_text().strip()
                for keyword in KEYWORDS:
                    if keyword.lower() in element_text.lower():
                        print(f"  ✅ Found '{keyword}' on page {page_count}")
                        found_data.append({
                            'University': base_domain,
                            'Page_URL': current_url,
                            'Keyword_Found': keyword,
                            'Context': element_text.replace('\n', ' ').replace('\r', ' ')
                        })

            # Find new links to visit
            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(base_url, link['href'])
                if urlparse(absolute_url).netloc == base_domain and absolute_url not in visited_pages:
                    pages_to_visit.append(absolute_url)

        except requests.exceptions.RequestException:
            continue
            
    if not found_data:
        print(f"  ❌ No keywords found after scanning {page_count} pages.")
        
    return found_data

# --- Main Execution Block ---
if __name__ == "__main__":
    try:
        url_df = pd.read_csv(CSV_INPUT_FILE)
        start_urls = url_df['University_URL'].dropna().tolist()
        print(f"✅ Loaded {len(start_urls)} URLs from '{CSV_INPUT_FILE}'.")
    except (FileNotFoundError, KeyError):
        print(f"❗️ ERROR: Could not load URLs from '{CSV_INPUT_FILE}'. Please check the file.")
        start_urls = []

    if start_urls:
        total_sites = len(start_urls)
        print(f"--- Starting Advanced Crawler for {total_sites} Universities ---")
        
        file_exists = os.path.isfile(CSV_OUTPUT_FILE)
        
        for i, url in enumerate(start_urls):
            print(f"\n--- Processing University {i+1} of {total_sites} ---")
            results_for_site = crawl_and_get_context(url)
            
            if results_for_site:
                results_df = pd.DataFrame(results_for_site)
                if not file_exists:
                    results_df.to_csv(CSV_OUTPUT_FILE, index=False, mode='w')
                    file_exists = True
                else:
                    results_df.to_csv(CSV_OUTPUT_FILE, index=False, mode='a', header=False)
            
            time.sleep(1)

    print(f"\n\n🎉 Scan complete! Detailed results saved to '{CSV_OUTPUT_FILE}'")