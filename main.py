from SiteUrlCrawler import SiteUrlCrawler


def main():
    # Create a site crawler with 5 threads and allowing logging
    crawler = SiteUrlCrawler("https://strongscot.com", 5, True)

    # Get all the URLs and print them
    for url in crawler.crawl():
        print("Found: " + url)


if __name__ == '__main__':
    main()
