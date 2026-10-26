from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
import requests


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

def normalize_url(url: str) -> str :
  parsed_url = urlsplit(url)
  full_path = f"{parsed_url.netloc}{parsed_url.path}"
  full_path = full_path.rstrip("/")
  return full_path.lower() 

def get_heading_from_html(html: str) -> str:
  soup = BeautifulSoup(html, "html.parser")  
  h_tag = soup.find("h1") or soup.find("h2") 
  return h_tag.get_text(strip=True) if isinstance(h_tag, Tag) else ""

def get_first_paragraph_from_html(html: str) -> str:
  soup = BeautifulSoup(html, "html.parser")
  
  main_tag = soup.find("main")
  if isinstance(main_tag, Tag):
    f_tag = main_tag.find("p")
  else:
    f_tag = soup.find("p")
  return f_tag.get_text(strip=True) if isinstance(f_tag, Tag) else ""


def get_urls_from_html(html, base_url):
  urls = []
  soup = BeautifulSoup(html, "html.parser")
  anchors = soup.find_all("a")
  
  for anchor in anchors:
    if not isinstance(anchor, Tag):
      continue
    href = anchor.get("href")
    if isinstance(href, str) and href:
      try:
        absolute = urljoin(base_url, href)
        urls.append(absolute)
      except Exception as e:
        print(f"{str(e)}: {href}")     
        
  return urls


def get_images_from_html(html, base_url):
  image_urls = []
  soup = BeautifulSoup(html, "html.parser")
  images = soup.find_all("img")
  
  for image in images:
    if not isinstance(image, Tag):
      continue
    src = image.get("src")
    if isinstance(src, str) and src:
      try:
        absolute = urljoin(base_url, src)
        image_urls.append(absolute)
      except Exception as e:
        print(f"{str(e)}: {src}")     
        
  return image_urls


def extract_page_data(html: str, page_url: str) -> PageData:
  return {
         "url": page_url,
         "heading": get_heading_from_html(html),
         "first_paragraph": get_first_paragraph_from_html(html),
         "outgoing_links":get_urls_from_html(html, page_url),
         "image_urls": get_images_from_html(html, page_url),
     }


def get_html(url: str):
  """Fetch HTML content from a URL.  
      Raises an Exception if the request fails, the status code indicates an
      error (>= 400), or the response content is not HTML.
  """
  try:  
    response = requests.get(
      url,
      headers= {"User-Agent": "BootCrawler/1.0"}
    )
  except Exception as e:
    raise Exception(f"network error while fetching {url}: {e}")
  
  if response.status_code >= 400:
      raise Exception(f"got HTTP error: {response.status_code}")

  content_type = response.headers.get("content-type", "")
  if "text/html" not in content_type:
    raise Exception(f"got non-HTML response: {content_type}")

  return response.text


def crawl_page(base_url, current_url=None, page_data=None, max_pages=30):
  """Recursively crawl pages on a domain and collect their data."""
  if current_url is None:
    current_url = base_url
  if page_data is None:
    page_data = {}
  
  if len(page_data) >= max_pages:
      return page_data
      
  parsed_base_url = urlsplit(base_url)
  parsed_current_url = urlsplit(current_url)
  dom_base = parsed_base_url.netloc
  dom_current = parsed_current_url.netloc  
  if dom_current != dom_base:
    return page_data
    
  normalized_url = normalize_url(current_url)
  if normalized_url in page_data:
    return page_data
    
  print(f"crawling {current_url}")
  html = safe_get_html(current_url)
  if html is None:
      return page_data
  
  page_info = extract_page_data(html, current_url)
  page_data[normalized_url] = page_info

  next_urls = page_info["outgoing_links"]
  for next_url in next_urls:
    if len(page_data) >= max_pages:
                break
    page_data = crawl_page(base_url, next_url, page_data, max_pages)

  return page_data


def safe_get_html(url: str) -> str | None:
    """Fetch HTML without crashing if the request fails."""
    try:
        return get_html(url)
    except Exception as e:
        print(f"{e}")
        return None