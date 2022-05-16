from enum import Enum

import requests
import threading

from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


class SiteUrlCrawler:
    class Mode(Enum):
        ALL = 0
        INTERNAL = 1
        EXTERNAL = 2

    def __init__(self, site_base_url, max_threads=10, logging_enabled=False):
        """
        Constructor for SiteCrawler.
        :param site_base_url:
        :param max_threads:
        :param logging_enabled:
        """
        self.site_base_url = site_base_url
        self.site_hostname = urlparse(site_base_url).hostname
        self.logging_enabled = logging_enabled
        self.mode = self.Mode.ALL.value

        self.max_threads = max_threads
        self.thread_pool = []
        self.urls_to_search_lock = threading.Lock()
        self.found_url_lock = threading.Lock()

        self.urls_to_search = list()
        self.found_urls = []
        self.callback = None

    def crawl(self, mode=None, callback=None):
        """
        Begins the crawling process.
        :return:
        """
        self.mode = self.Mode.ALL if mode is None else mode
        self.callback = callback

        # Build initial starting point URLs to crawl
        for url in CrawlerThread(self, self.mode).find_all_urls_on_page(self.site_base_url, False):
            self.found_url(url)

        while len(self.thread_pool) < self.max_threads:
            thread = CrawlerThread(self, self.mode)
            self.thread_pool.append(thread)
            self.log("Creating new thread, " + thread.getName())

        for thread in self.thread_pool:
            thread.start()

        # Using list comprehension, wait on all threads completing
        [t.join() for t in self.thread_pool]

        self.log("All threads completed.")

        self.thread_pool.clear()

        return self.found_urls

    def get_work_item(self):
        """
        Returns a work url for a worker thread.
        :return:
        """
        self.log("----------------------------")
        self.log("URLs to check: " + str(len(self.urls_to_search)))
        self.log("Found URLs: " + str(len(self.found_urls)))

        if len(self.urls_to_search) > 0:
            return self.urls_to_search.pop()

        return None

    def found_url(self, url):
        """
        Report a new found url.
        :param url:
        :return:
        """
        self.found_url_lock.acquire()

        if url not in self.found_urls:
            self.found_urls.append(url)
            self.urls_to_search.append(url)

            self.log("Found URL \"" + url + "\".")

            if self.callback is not None:
                self.callback(url)

        self.found_url_lock.release()

    def log(self, message):
        """
        Logging
        :param message:
        :return:
        """
        if self.logging_enabled:
            print("SiteCrawler:" + message)


class CrawlerThread(threading.Thread):
    def __init__(self, site_crawler, mode):
        """
        Constructor for worker thread.
        :param site_crawler:
        :param mode:
        """
        super(CrawlerThread, self).__init__()
        self.site_crawler = site_crawler
        self.mode = mode

    def run(self) -> None:
        """
        Perform the actual work of popping a url from the shared url queue and then checking the url for any other urls
        that we can additionally check.
        :return:
        """
        while True:
            # Keep things in sync
            self.site_crawler.urls_to_search_lock.acquire()
            url = self.site_crawler.get_work_item()
            self.site_crawler.urls_to_search_lock.release()

            if url is None:
                break

            if self.is_internal_url(url) is False:
                self.log("Skipping URL \"" + url + "\" cause its external and we dont want to index the internet.")
                break

            self.log("Checking URL \"" + url + "\".")
            self.find_all_urls_on_page(url, True)

        self.log("Completed.")

    def find_all_urls_on_page(self, url, use_callback=True):
        """
        Finds all links referenced by a particular URL.
        :param url:
        :param use_callback:
        :return:
        """
        found_urls = []

        # Only operate on pages with a content-type header
        if requests.head(url).headers.get('content-type') is None:
            return found_urls

        # Only handle HTML files
        if "text/html" not in requests.head(url).headers.get('content-type'):
            return found_urls

        soup = BeautifulSoup(requests.get(url).content, "html.parser")

        for a in soup.findAll("a"):
            a_href = a.attrs.get("href")

            # Skip empty urls
            if a_href is None or len(a_href) == 0:
                continue

            # If the url is relative, make it absolute
            if a_href[0] == '/':
                a_href = urljoin(url, a_href)

            if a_href[:a_href.find(":")] not in ("http", "https"):
                continue

            # If its an external url, skip it
            if self.mode == SiteUrlCrawler.Mode.INTERNAL:
                if not self.is_internal_url(a_href):
                    continue
            elif self.mode == SiteUrlCrawler.Mode.EXTERNAL:
                if self.is_internal_url(a_href):
                    continue
            elif self.mode == SiteUrlCrawler.Mode.ALL:
                pass

            # Clean the url
            url_parts = urlparse(a_href)
            a_href = url_parts.scheme + '://' + url_parts.netloc + url_parts.path

            if url_parts.query:
                a_href += "?" + url_parts.query

            if use_callback is True:
                self.site_crawler.found_url(a_href)
            else:
                found_urls.append(a_href)

        return found_urls

    def is_internal_url(self, url):
        """
        Checks if a URL is internal or external pointing.
        :param url:
        :return:
        """
        return self.site_crawler.site_hostname in url

    def log(self, message):
        """
        Logging.
        :param message:
        :return:
        """
        if self.site_crawler.logging_enabled:
            print(self.getName() + " (CrawlerThread): " + message)
