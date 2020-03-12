## Description

A super simple multi-threaded website URL crawler. Returns a Python array of all found URLs. It can be configured to
return either internal urls, external urls or both.

**Please Note:** This does **NOT** attempt to crawl external URLs, this isn't Google.

## Dependencies

- pip install requests
- pip install beautifulsoup4

## Features

- Super simple; two lines of code to get a list of URLs on a website.
- Multi-threaded.
- Enable or disable logging.
- Can return internal, external or both URLs.
- Not much else.

## Usage

The following code sample will scan site "strongscot.com", using 5 threads and hiding all logging information.

### Find Internal and External URLs

```
crawler = SiteUrlCrawler("https://strongscot.com", 5, False)

# Print the found URLs
for url in crawler.crawl(SiteUrlCrawler.Mode.ALL):
    print("Found: " + url)
```

Will output something similar to this:

```
Found: https://strongscot.com/
Found: https://strongscot.com/projects/
Found: https://strongscot.com/cv/
Found: https://strongscot.com/contact/
Found: https://strongscot.com/blog/20/03/03/simple-site-crawler.html
Found: https://strongscot.com/blog/20/02/19/birthday.html
Found: https://strongscot.com/blog/19/12/09/new-site.html
Found: https://strongscot.com/blog/19/09/09/body-goals.html
Found: https://strongscot.com/blog/19/09/09/cool-dropdown-ui.html
Found: https://strongscot.com/blog/19/09/09/flying-in-a-flight-machine.html
```

### Find Only Internal URLs

```
crawler = SiteUrlCrawler("https://strongscot.com", 5, False)

# Print the found URLs
for url in crawler.crawl(SiteUrlCrawler.Mode.INTERNAL):
    print("Found: " + url)
```

### Find Only External URLs

```
crawler = SiteUrlCrawler("https://strongscot.com", 5, False)

# Print the found URLs
for url in crawler.crawl(SiteUrlCrawler.Mode.EXTERNAL):
    print("Found: " + url)
```


## Author

@strongscot

## License

MIT
