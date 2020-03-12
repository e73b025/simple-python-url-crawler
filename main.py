from SiteUrlCrawler import SiteUrlCrawler


def main():
    # Create a site crawler with 5 threads and allowing logging
    crawler = SiteUrlCrawler("https://strongscot.com", 5, False)

    # Get ALL urls and print them
    for url in crawler.crawl(SiteUrlCrawler.Mode.ALL):
        print("Found: " + url)

    # Get INTERNAL urls ONLY and print them
    for url in crawler.crawl(SiteUrlCrawler.Mode.INTERNAL):
        print("Found: " + url)

    # Get EXTERNAL urls ONLY and print them
    for url in crawler.crawl(SiteUrlCrawler.Mode.EXTERNAL):
        print("Found: " + url)


if __name__ == '__main__':
    main()
