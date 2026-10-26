import sys
from crawl import get_html

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

   print(get_html(url))

if __name__ == "__main__":
    main()