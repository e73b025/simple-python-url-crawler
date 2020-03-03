from SiteUrlCrawler import SiteUrlCrawler


def main():
    crawler = SiteUrlCrawler("https://strongscot.com", 5, True)
    found_urls = crawler.crawl()

    print()
    print("Found: " + str(len(found_urls)) + " URLs.")

    for url in found_urls:
        print("Found: " + url)


if __name__ == '__main__':
    main()
