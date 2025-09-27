# FYUP Implementation Web Scraper

This project contains the tools and methodology used to identify Indian universities implementing the Four-Year Undergraduate Programme (FYUP) as prescribed by the National Education Policy (NEP) 2020. The core of the project is a robust Python web crawler designed to run on a cloud server to systematically gather data from over a thousand university websites.
---
## Tech Stack 💻

* **Language:** Python 3
* **Core Libraries:** `requests`, `BeautifulSoup4`, `pandas`
* **Cloud Platform:** AWS EC2 (`t2.micro`)
* **Operating System:** Ubuntu Server
* **Tools:** `screen` (for persistent terminal sessions), `nano` (for server-side editing)


---
## Project Structure
.
├── advanced_crawler1.py             # The main, robust Python scraper script.
├── universities.csv                 # The input file with the master list of university URLs.
└── fyup_advanced_scan_results.csv   # The output file where results are incrementally saved.



---
## Methodology Overview 🗺️

The information gathering process was executed in three distinct phases:

1.  **Source Aggregation & Data Enrichment:** A master list of university URLs was created by first manually copying the university data table from the official UGC portal. This raw text was then processed by a Large Language Model (LLM) to parse and find the official website for each institution, resulting in a clean CSV file.
2.  **Data Extraction via Web Crawler:** A custom Python script was developed to crawl each university website from the master list. It was designed to be resilient and to extract not just keywords, but the specific context in which they appeared.
3.  **Cloud-Based Execution:** To handle the long-running nature of the task, the entire scraping process was deployed and run on a free-tier AWS EC2 instance, allowing for continuous, unattended operation.

---

---

## Setup and Usage 🚀

1.  **Cloud Server Setup:**
    * Launch a free-tier `t2.micro` EC2 instance with Ubuntu Server on AWS.
    * Configure its Security Group to allow SSH (Port 22) from your IP.
    * Connect and create a 4GB swap file for stability.

2.  **Project Setup on Server:**
    * Upload `advanced_crawler1.py` and `universities.csv`.
    * Install necessary system packages: `sudo apt install python3-pip python3.12-venv -y`
    * Create and activate a Python virtual environment: `python3 -m venv scraper_env && source scraper_env/bin/activate`
    * Install required Python libraries: `pip install pandas requests beautifulsoup4`

3.  **Running the Scraper:**
    * Edit `advanced_crawler1.py` to add your Discord Webhook URL.
    * Start a `screen` session: `screen`
    * Run the script: `python3 advanced_crawler1.py`
    * Detach from the session: **`Ctrl+A`**, then **`D`**.





---
## Results and Analysis 📊

The automated web crawling process was executed on a list of over 1200 university URLs. The script successfully scanned approximately **930 unique university websites** before the process was concluded for analysis. The scan yielded a rich dataset of keyword matches, providing significant insight into the adoption of the Four-Year Undergraduate Programme (FYUP) across India.

---
### **Quantitative Findings**

An analysis of a sample of the results provides a clear indication of the widespread implementation of NEP 2020's guidelines.

* **Positive Implementations:** From the analyzed sample of results, **22 unique universities** showed direct evidence of implementing or planning for the FYUP and its related policies.

* **Keyword Frequency:** The scraper found a total of 87 individual keyword matches within the sample. The distribution is as follows:
    * `Multiple Entry`: 42 occurrences
    * `FYUP`: 40 occurrences
    * `Four-Year Undergraduate Programme`: 4 occurrences
    * `4-year degree`: 1 occurrence

This distribution shows that universities are actively using terms like "FYUP" and "Multiple Entry" in their official communications and course descriptions.

---
### **Qualitative Analysis: Examples of Implementation**

The contextual data extracted by the scraper is crucial for verifying the status of implementation. The following examples demonstrate the clarity of the data collected:

#### Example 1: Clear Policy Statement (Amity University)
> *Context: "As per new structure and duration of undergraduate programmes proposed by NEP 2020, Amity University Mumbai is offering Four-Year Undergraduate degree programmes for the students to experience full range of holistic and multidisciplinary education."*

**Analysis:** This is a direct confirmation from the university that it is actively offering four-year degree programs in direct alignment with NEP 2020.

#### Example 2: Official University Documentation (Raja Mahendra Pratap Singh State University)
> *Context: "Curricular & Credit Framework for Four Year Undergraduate Programme (FYUP) एन०ई०पी० यू०जी० एवं पी०जी० अध्यादेश के सम्बन्ध में | Dated: 24-Jul-2025"*

**Analysis:** This finding points to official university ordinances and framework documents for the FYUP, which is a strong indicator of formal adoption at an administrative level.

#### Example 3: Adoption of Flexible Structures (K. K. University)
> *Context: "As per new structure and duration of undergraduate programmes proposed by NEP 2020, K. K. University is offering 1 year Certification, 2 Years Diploma, 3 Years Bachelor and 4 Year Bachelor with Honours programmes... with multiple entry/exit during this period..."*

**Analysis:** This demonstrates a full embrace of the flexible academic structure proposed by NEP 2020, including multiple entry/exit points and a clear path to a four-year honors degree.

---
### **Summary of Results**

The automated data collection methodology proved to be highly effective. The findings, combining both the significant number of universities with positive matches and the explicit nature of the contextual evidence, strongly indicate a widespread trend towards the adoption of the Four-Year Undergraduate Programme across Indian higher education institutions.


---
## Challenges Faced and Solutions 🛠️

Several technical challenges were encountered and overcome during the project's development.

* **Challenge: Dynamic Content and Bot Detection**
    * **Problem:** The initial attempt to scrape the UGC portal for a list of universities failed because the website used JavaScript to load its data and had measures in place to block automated scripts.
    * **Solution:** This was solved by using the **Selenium** library with **selenium-stealth** to automate a full web browser. This allowed the script to mimic human interaction (like clicking buttons) and hide its automated nature, enabling the successful aggregation of all university URLs.

* **Challenge: Server Memory Limitations**
    * **Problem:** The script was repeatedly terminated ("Killed") by the operating system on the low-RAM (`1 GB`) `t2.micro` cloud server, even after the workload was reduced to 10 pages per site.
    * **Solution:** A multi-pronged approach fixed this. A **4 GB swap file** was created to act as virtual memory. A **memory leak** was diagnosed and fixed by adding an explicit garbage collection call (`gc.collect()`) to the script's main loop, forcing it to release memory after processing each university.

* **Challenge: Script Resilience and Data Loss**
    * **Problem:** An error on a single website (e.g., bad HTML, connection timeout) would crash the entire multi-day process, and all previously collected data would be lost.
    * **Solution:** The script was re-architected to include **incremental saving**, appending results to the output CSV file after each site. A robust `try...except` block was also wrapped around the main loop to log errors and continue processing the remaining URLs, ensuring the job would run to completion.

* **Challenge: Cross-Platform Environment Setup**
    * **Problem:** Connecting to the cloud server via SSH proved difficult due to file permission errors on Windows (`icacls`) vs. WSL (`chmod`) and network timeouts caused by dynamic IP addresses being blocked by the AWS firewall.
    * **Solution:** OS-specific commands were used to set the correct key file permissions. A clear guide for updating the AWS Security Group to allow the user's current IP address was followed, resolving all connection issues.