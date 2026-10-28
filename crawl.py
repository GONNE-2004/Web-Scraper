from urllib.parse import urlsplit, urljoin
from bs4 import BeautifulSoup, Tag
from typing import TypedDict
from types import TracebackType
import asyncio
import aiohttp
   

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


class AsyncCrawler():
  def __init__(self, base_url: str, max_concurrency= 10, max_pages: int = 20) -> None:    
    """Concurrently crawls a website within a single domain, collecting page data.

    Uses an aiohttp.ClientSession to fetch pages asynchronously, an
    asyncio.Semaphore to cap the number of simultaneous in-flight requests
    (max_concurrency), and an asyncio.Lock to guard shared mutable state
    (`visited` and `page_data`) against race conditions between concurrent
    tasks. Must be used as an async context manager so the underlying
    HTTP session is properly opened and closed.

    Attributes:
        base_url: The starting URL for the crawl.
        base_domain: The netloc of base_url; only same-domain pages are crawled.
        page_data: Maps normalized URLs to their extracted PageData.
        visited: Normalized URLs already scheduled/crawled, to avoid duplicates.
        lock: Guards concurrent access to `visited` and `page_data`.
        max_concurrency: Maximum number of simultaneous HTTP requests.
        semaphore: Enforces the max_concurrency limit.
        session: The aiohttp session used for all requests, set on __aenter__.
    """
    self.base_url = base_url
    parsed_url = urlsplit(self.base_url)
    self.base_domain = parsed_url.netloc
    self.page_data: dict[str, PageData] = {}
    self.visited: set[str] = set()
    self.lock = asyncio.Lock()
    self.max_concurrency = max_concurrency
    self.max_pages = max_pages
    self.semaphore = asyncio.Semaphore(self.max_concurrency)
    self.should_stop: bool = False
    self.all_tasks = set()
    self.session: aiohttp.ClientSession | None = None

  async def __aenter__(self) -> "AsyncCrawler":
    """Open the aiohttp session and return self for use in `async with`."""
    self.session = aiohttp.ClientSession()
    return self  

  async def __aexit__(
    self, 
    exc_type: type[BaseException] | None, 
    exc_val: BaseException | None, 
    exc_tb: TracebackType | None
  ) -> None:
    """Close the aiohttp session when exiting the `async with` block."""
    if self.session is not None:
      await self.session.close()

  async def add_page_visit(self, normalized_url) -> bool:
    """Atomically mark a URL as visited; return False if already visited.""" 
      
    async with self.lock:
      if normalized_url in self.visited:
        return False
      if self.should_stop is True:
        return False   
      if len(self.visited) >= self.max_pages:
        self.should_stop = True
        print("Reached maximum number of pages to crawl.")
        print(f"DEBUG: visited count = {len(self.visited)}, max_pages = {self.max_pages}")
        return False      
      self.visited.add(normalized_url)      

      return True


  async def get_html(self, url: str) -> str | None:
    """Fetch a URL's HTML, returning None on request, status, or content-type errors."""
    if self.session is None:
      return None
    try:
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as response:
            if response.status >= 400:
              print(f"Error: HTTP {response.status} for {url}")
              return None

            content_type = response.headers.get("content-type", "")
            if "text/html" not in content_type:
              print(f"Error: Non-HTML content {content_type} for {url}")
              return None
              
            return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None

  async def crawl_page(self, current_url):
    """Crawl a single page (if new and same-domain), then recursively crawl its links."""
    current_task = asyncio.current_task()
    try:
      if self.should_stop is True:
        return      
      current_url_obj = urlsplit(current_url)   
      if current_url_obj.netloc != self.base_domain:
        return
        
      normalized_url = normalize_url(current_url)
      
      is_new = await self.add_page_visit(normalized_url)
      if not is_new:
          return
          
      async with self.semaphore:
          print(
              f"Crawling {current_url} (Active: {self.max_concurrency - self.semaphore._value})"
          )
          html = await self.get_html(current_url)
          if html is None:
              return
              
          page_info = extract_page_data(html, current_url)
          async with self.lock:
              self.page_data[normalized_url] = page_info
  
          next_urls = page_info["outgoing_links"]
  
      tasks: list[asyncio.Task[None]] = []
      for next_url in next_urls:
        child_task = asyncio.create_task(self.crawl_page(next_url))
        self.all_tasks.add(child_task)
        tasks.append(child_task)
  
      if tasks:
        await asyncio.gather(*tasks)  
    finally:
      self.all_tasks.discard(current_task)

  async def crawl(self):
    """Start crawling from base_url and return the collected page_data dict."""
    await self.crawl_page(self.base_url)
    return self.page_data

async def crawl_site_async( base_url: str, max_concurrency: int, max_pages: int):
  """Crawl an entire site starting at base_url using an AsyncCrawler, returning page_data."""
  async with AsyncCrawler(base_url, max_concurrency, max_pages) as crawler:
      return await crawler.crawl()