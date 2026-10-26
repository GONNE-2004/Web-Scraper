import sys
from crawl import crawl_page

def main():
   args = sys.argv
   url = args[1]
   
   if len(args) < 2:
     print("no website provided")
     sys.exit(1)
   elif len(args) > 2:
     print( "too many arguments provided")
     sys.exit(1)
   else:
     print(f"starting crawl of: {url}")
  
   
   print(f"starting crawl of: {url}...")
    
   page_data = crawl_page(url)
  
   print(f"Found {len(page_data)} pages:")
   for page in page_data.values():
     print(f"- {page['url']}: {len(page['outgoing_links'])} outgoing links")


if __name__ == "__main__":
    main()