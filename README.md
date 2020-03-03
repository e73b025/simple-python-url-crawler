## Description

Super simple multi-thread site URL crawler. Returns a Python array of all found URLs.

## Dependencies

- pip install requests
- pip install beautifulsoup4

## Features

- Super simple; two lines of code to get a list of URLs on a website.
- Multi-threaded.
- Enable or disable logging.
- Not much else.

## Usage

The following code sample will scan site "strongscot.com", using 5 threads and output all logging information.

```
    crawler = SiteUrlCrawler("https://strongscot.com", 5, True)
    found_urls = crawler.crawl()
    
    # Print the found URLs
    for url in found_urls:
        print("Found: " + url)
```

## Author

@strongscot

## License

MIT
