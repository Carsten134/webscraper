from autocorrect.specifications.base import PageSpecification
import re

class OnXHome(PageSpecification):
  def is_satisfied(self):
    # checks if current url contains the home page url
    home_sub_str = re.findall(self.candidate_driver.current_url, "$https://x.com/home")
    return bool(len(home_sub_str))

class OnXSearch(PageSpecification):
  def is_satisfied(self):
    # checks current url for search url substring
    search_sub_str = re.findall(self.candidate_driver.current_url, "$https://x.com/search")
    return bool(len(search_sub_str))

