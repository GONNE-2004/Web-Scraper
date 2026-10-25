import unittest
from crawl import ( 
  normalize_url, 
  get_heading_from_html, 
  get_first_paragraph_from_html,
  get_urls_from_html,
  get_images_from_html,
  extract_page_data
  
)


class TestCrawl(unittest.TestCase):
  def test_normalize_url_protocol(self) -> None:
    input_url = "https://www.boot.dev/blog/path"    
    actual = normalize_url(input_url)
    expected = "www.boot.dev/blog/path"
    self.assertEqual(actual, expected)

  def test_normalize_url_slash(self) -> None:
    input_url = "https://www.boot.dev/blog/path/"
    actual = normalize_url(input_url)
    expected = "www.boot.dev/blog/path"
    self.assertEqual(actual, expected)

  def test_normalize_url_capital(self) -> None:
    input_url = "https://WWW.BOOT.DEV/blog/path/"
    actual = normalize_url(input_url)
    expected = "www.boot.dev/blog/path"
    self.assertEqual(actual, expected)

  def test_normalize_url_http(self) -> None:
    input_url = "http://WWW.BOOT.DEV/blog/path/"
    actual = normalize_url(input_url)
    expected = "www.boot.dev/blog/path"
    self.assertEqual(actual, expected)
    
  #testing html tags extraction
  def test_get_heading_from_html_basic(self):
    input_body = "<html><body><h1>Test Title</h1></body></html>"
    actual = get_heading_from_html(input_body)
    expected = "Test Title"
    self.assertEqual(actual, expected)

  def test_get_heading_from_html_h2(self):
    input_body = "<html><body><h2>Test Title</h2></body></html>"
    actual = get_heading_from_html(input_body)
    expected = "Test Title"
    self.assertEqual(actual, expected)

  def test_get_heading_from_main_priority(self):
    input_body = """<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>"""
    actual = get_first_paragraph_from_html(input_body)
    expected = "Main paragraph."
    self.assertEqual(actual, expected)
  
  def test_get_heading_from_html_with_whitespace(self) -> None:
      input_body = "<html><body><h1>   Whitespace Title   </h1></body></html>"
      actual = get_heading_from_html(input_body)
      expected = "Whitespace Title"
      self.assertEqual(actual, expected)

  def test_get_first_paragraph_from_html_no_paragraph(self) -> None:
      input_body = "<html><body><h1>No paragraphs here</h1></body></html>"
      actual = get_first_paragraph_from_html(input_body)
      expected = ""
      self.assertEqual(actual, expected)


  #Extracting links(href) within the page
  def test_get_urls_from_html_absolute(self):
      input_url = "https://crawler-test.com"
      input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
      actual = get_urls_from_html(input_body, input_url)
      expected = ["https://crawler-test.com"]
      self.assertEqual(actual, expected)

  def test_get_urls_from_html_without_href(self):
      input_url = "https://crawler-test.com"
      input_body = '<html><body><a><span>Boot.dev</span></a></body></html>'
      actual = get_urls_from_html(input_body, input_url)
      expected = []
      self.assertEqual(actual, expected)

  def test_get_urls_from_html_multiple_url(self):
      input_url = "https://crawler-test.com"
      input_body = """
      <html><body>
      <a href="https://crawler-test.com" ><span>Boot.dev</span></a>
      <a href="https://crawl-test.com" ><span>Bot.dev</span></a>
      </body></html>"""
      actual = get_urls_from_html(input_body, input_url)
      expected = ["https://crawler-test.com", "https://crawl-test.com"]
      self.assertEqual(actual, expected)


  #Extracting imgage(src) within the page
  def test_get_images_from_html_relative(self):
      input_url = "https://crawler-test.com"
      input_body = '<html><body><img src="/logo.png" alt="Logo"></body></html>'
      actual = get_images_from_html(input_body, input_url)
      expected = ["https://crawler-test.com/logo.png"]
      self.assertEqual(actual, expected)  

  def test_get_images_from_html_without_src(self):
      input_url = "https://crawler-test.com"
      input_body = '<html><body><img alt="Logo"></body></html>'
      actual = get_images_from_html(input_body, input_url)
      expected = []
      self.assertEqual(actual, expected)

  def test_get_images_from_html_multiple_src(self):
      input_url = "https://crawler-test.com"
      input_body = """
      <html><body>
      <img src="/logo.png" alt="Logo">
      <img src="/Gogo.png" alt="Logger">
      </body></html>"""
      actual = get_images_from_html(input_body, input_url)
      expected = [
        "https://crawler-test.com/logo.png", "https://crawler-test.com/Gogo.png"
      ]
      self.assertEqual(actual, expected)


  # Extracting page data
  def test_extract_page_data_basic(self):
      input_url = "https://crawler-test.com"
      input_body = """<html><body>
          <h1>Test Title</h1>
          <p>This is the first paragraph.</p>
          <a href="/link1">Link 1</a>
          <img src="/image1.jpg" alt="Image 1">
      </body></html>"""
      actual = extract_page_data(input_body, input_url)
      expected = {
          "url": "https://crawler-test.com",
          "heading": "Test Title",
          "first_paragraph": "This is the first paragraph.",
          "outgoing_links": ["https://crawler-test.com/link1"],
          "image_urls": ["https://crawler-test.com/image1.jpg"],
      }
      self.assertEqual(actual, expected)
   
   
if __name__ == "__main__":
    unittest.main() 