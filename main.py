from SiteUrlCrawler import SiteUrlCrawler


def main():
    crawler = SiteUrlCrawler("https://strongscot.com", 5, True)

    for url in crawler.crawl():
        print("Found: " + url)


if __name__ == '__main__':
    main()
