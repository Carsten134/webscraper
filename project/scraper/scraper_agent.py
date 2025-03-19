from selenium import webdriver

class ScraperAgent:
  """
  Overarching Interface with Scraper Agents of different kind
  """
  def __init__(self):
    return self


class ZeeschuimerScraperAgent(ScraperAgent):
  """
  Implementation of a ScraperAgent using Zeeschuimer to scraper from social media
  """

  def __init__(self, social_media):
      self = super()
      self.driver = webdriver.Firefox()
  