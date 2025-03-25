from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import uuid
import time
import json
import os

from config import ZEESCHUIMER_ID
from autocorrect.x import search_autocorrect

class XScraper:
  def __init__(self, run_config:dict):
    """
    XScraper: The object for scraping the social media platform X.

    Input:
      run_config(dict): Config for full run of scraping. See directory "./scraper/run-configs" for examples.

    Returns:
      XScraper instance. To start the run call the `.run()` method.    
    """
    self.username = run_config["user"]["name"]
    self.mail = run_config["user"]["name"]
    self.password = run_config["user"]["password"]

    self.run_config = run_config
    
    # stuff for activating zeeschuimer
    options = Options()
    add_on_id_dynamic = str(uuid.uuid4())
    options.set_preference('extensions.webextensions.uuids',
                            json.dumps({ZEESCHUIMER_ID: add_on_id_dynamic}))

    self.zeeschuimer_url = f"moz-extension://{add_on_id_dynamic}/popup/interface.html"
    
    # set download dir
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.dir", f"{os.getcwd()}\data\X")
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-ndjson,application/json")


    # instantiating firefox and navigating to zeeschuimer
    self.driver = webdriver.Firefox(options=options)
    self.driver.install_addon("./extensions/zeeschuimer-v1.12.3.zip", temporary=True)
    self.driver.get(self.zeeschuimer_url)

    # toggle X
    x_toggle_input = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[for="zs-enabled-twitter.com"]')))
    x_toggle_input.click()
  
  def run(self):
    """
    Run the scraping.
    """
    self.login()

    for search_term in self._resolve_search_terms(self.run_config["searchTerms"]):
        time.sleep(1)
        self.search(search_term)
        self.scroll(self.run_config["scrollsPerSearch"],
                    self.run_config["scrollsOffset"],
                    self.run_config["secBetweenScrolls"])
    
    self.download_posts()
  
  def login(self):
    self.driver.get("https://x.com/i/flow/login")

    usermail = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[autocomplete="username"]')))
    usermail.send_keys(self.mail)
    usermail.send_keys(Keys.ENTER)

    time.sleep(1)
    ActionChains(self.driver).send_keys(self.username + Keys.ENTER).perform()

    password = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[name="password"]')))
    password.send_keys(self.password)
    password.send_keys(Keys.ENTER)

  @search_autocorrect
  def search(self, text):
    search = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[placeholder="Search"]')))
    
    # make sure the search field is empty
    search.clear()
    search.send_keys(text + Keys.ENTER)

  def download_posts(self):
    self.driver.get(self.zeeschuimer_url)
    download_button = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'button[class="download-ndjson"][data-platform="twitter.com"]')))
    download_button.click()
  
  def scroll(self, times, offset = 300, sleep = 1):
    try:
      # wait until posts are loaded
      WebDriverWait(self.driver, 10)\
          .until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'article')))
      for _ in range(times):
        time.sleep(sleep)
        ActionChains(self.driver).scroll_by_amount(0, offset).perform()
    except TimeoutException:
      # if no posts are loaded, do nothing since there is nothing to scroll
      return None
    
    

  def _resolve_search_terms(self, search_terms):
    if type(search_terms) == list and len(search_terms) > 0:
      if type(search_terms[0]) == list:
        # do cartesian product of the lists provided
        temp = []
        for first in search_terms[0]:
          for second in search_terms[1]:
            temp.append(first + second)
        return temp
      # if just list of search terms was given return it
      return search_terms
        
    raise RuntimeError("No searchterms provided in run config")