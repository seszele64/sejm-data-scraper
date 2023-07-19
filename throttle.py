import random
import time
import logging


class Throttle:
    def __init__(self, mean):
        self.mean = mean

    def wait(self):
        # Adjust standard deviation as per your needs
        delay = random.normalvariate(self.mean, self.mean/3)
        delay = max(delay, 0)
        time.sleep(delay)

    # try a few times to get a response from server, use browser_manager
    def try_get_response(self, url, browser):
        for _ in range(5):
            # wait max 5 seconds for a response
            try:
                browser.get(url)
                return
            except Exception:
                logging.info("No response from server. Retrying...")
                self.wait()
        self.no_response()
    # detect no response from server -> exit program

    def no_response(self):

        exit_message = """
        No response from server. Exiting program...
        Please check your internet connection and try again. You might also want to try using a proxy.
        Program will continue scraping from the last MP index.
        """

        logging.info(exit_message)
        print(exit_message)

        exit()
