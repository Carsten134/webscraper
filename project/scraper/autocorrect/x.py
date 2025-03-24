"""
Autocorrections for the XScraper object
"""
from functools import wraps

from autocorrect.specifications.base import AndSpecification, OrSpecification
from autocorrect.specifications import x as XSpec

def search_autocorrect(search):
  @wraps(search)
  def wrapped_search(*args, **kwargs):
    # checking conditions

    # fixing if necessary
    
    search(*args, **kwargs)
  
  return wrapped_search