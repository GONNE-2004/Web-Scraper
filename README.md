# Python Web Crawler

A multi-threaded web crawler built in Python that traverses a website, counts internal link occurrences, and outputs a formatted crawl report.

## Features

- **Recursive Crawling**: Discovers and visits all internal links starting from a base URL.
- **Domain Restriction**: Stays within the target domain to avoid crawling external websites.
- **URL Normalization**: Strips protocols and trailing slashes to accurately deduplicate and count links.
- **Concurrency**: Employs asynchronous fetching/threading to crawl pages concurrently and efficiently.
- **Formatted Reporting**: Sorts and displays visited pages ordered by link count.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>

2. (Optional) Set up a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

3. Install required dependencies:
pip install -r requirements.txt

4. Usage
Run the crawler by passing the target URL as an argument to the main entry point:

python3 main.py <target_url> [max_concurrency] [max_pages]


Here is a clean, standard README.md template tailored to the web crawler project. You can customize the placeholders (like repository URLs and specific CLI flags if yours differ) before adding it to your repository:

# Python Web Crawler

A multi-threaded web crawler built in Python that traverses a website, counts internal link occurrences, and outputs a formatted crawl report.

## Features

- **Recursive Crawling**: Discovers and visits all internal links starting from a base URL.
- **Domain Restriction**: Stays within the target domain to avoid crawling external websites.
- **URL Normalization**: Strips protocols and trailing slashes to accurately deduplicate and count links.
- **Concurrency**: Employs asynchronous fetching/threading to crawl pages concurrently and efficiently.
- **Formatted Reporting**: Sorts and displays visited pages ordered by link count.

## Prerequisites

- Python 3.10 or higher
- `pip` (Python package manager)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/<your-username>/<your-repo-name>.git
   cd <your-repo-name>

(Optional) Set up a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

Install required dependencies:

pip install -r requirements.txt

Usage
Run the crawler by passing the target URL as an argument to the main entry point:

python3 main.py <target_url> [max_concurrency] [max_pages]

Example
python3 main.py https://wagslane.dev 5 25

Sample Output
=============================
  REPORT for https://wagslane.dev
=============================
Found 15 internal links to https://wagslane.dev
Found 8 internal links to https://wagslane.dev/tags
Found 4 internal links to https://wagslane.dev/about
Found 2 internal links to https://wagslane.dev/posts

Running Tests
To run the unit test suite:
python3 -m unittest discover