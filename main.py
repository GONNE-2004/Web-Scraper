import sys
import asyncio
from crawl import crawl_site_async
from json_report import write_json_report

async def main() -> None:
   args = sys.argv   
   if len(args) < 4:
     print("no website provided")
     sys.exit(1)
   elif len(args) > 4:
     print( "too many arguments provided")
     sys.exit(1)
  
   url = args[1]   
   max_concurrency = int(args[2])
   max_pages = int( args[3])
   
   print(f"starting crawl of: {url}...")
   page_data = await crawl_site_async(url, max_concurrency, max_pages)
   
   print(f"Crawling complete. Found {len(page_data)} pages.")
   
   write_json_report(page_data)
   
if __name__ == "__main__":
     asyncio.run(main())