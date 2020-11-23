## Description

A super simple multi-threaded website URL crawler. Returns a Python array of all found URLs. It can be configured to
return either internal urls, external urls or both.

## Dependencies

- pip install requests
- pip install beautifulsoup4

## Features

- Super simple; two lines of code to get a list of URLs on a website.
- Multi-threaded.
- Enable or disable logging.
- Can return internal, external or both URLs.
- Can provide optional callback method for LIVE URL finds.
- Not much else.

## Usage

The following code sample will scan site "strongscot.com", using 5 threads and hiding all logging information.

### Find Internal and External URLs

```python
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
Found: https://github.com/strongscot
Found: https://strongscot.com/blog/20/03/03/simple-site-crawler.html
Found: https://strongscot.com/blog/20/02/19/birthday.html
Found: https://strongscot.com/blog/19/12/09/new-site.html
Found: https://strongscot.com/blog/19/09/09/body-goals.html
Found: https://strongscot.com/blog/19/09/09/cool-dropdown-ui.html
Found: https://strongscot.com/blog/19/09/09/flying-in-a-flight-machine.html
Found: https://github.com/strongscot/simple-python-url-crawler
```

### Find Only Internal URLs

```python
crawler = SiteUrlCrawler("https://strongscot.com")

# Print the found URLs
for url in crawler.crawl(SiteUrlCrawler.Mode.INTERNAL):
    print("Found: " + url)
```

### Find Only External URLs

```python
crawler = SiteUrlCrawler("https://strongscot.com")

# Print the found URLs
for url in crawler.crawl(SiteUrlCrawler.Mode.EXTERNAL):
    print("Found: " + url)
```

Will output:

```
Found: https://github.com/strongscot
Found: https://twitter.com/thestrongscot
```

## Using Callback (getting live URL finds as they happen)

If you wish to get each URL as it is found rather than at the end in an array, you can pass an optional argument to the
``crawl()`` method that will do exactly that. For example:

```python
crawler = SiteUrlCrawler("https://strongscot.com")

def callback(url):
    print("Found: " + url)

# Get ALL urls and print them
crawler.crawl(SiteUrlCrawler.Mode.ALL, callback)
```

## Bad-Tip

Want to make it a small Google Bot? Comment-out lines ``134`` - ``136`` in file ``SiteUrlCrawler.py`` and it will trawl even external links.

## Author

@strongscot

## License

MIT
