import unittest
from crawl import normalize_url, get_heading_from_html, get_first_paragraph_from_html

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
    
  #testing html extraction
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
   
   
if __name__ == "__main__":
    unittest.main() 