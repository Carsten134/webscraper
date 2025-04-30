import sys
import pandas as pd
import json
import os
from scraper.x import XScraper
"""
This file is the entrypoint for a new docker container
and therefore the highest level of abstraction for this programm.
"""


RUN_JSON_X_DIR = "./project/scraper/run-configs/"

def main(mode:str, run_name) -> None:
  if mode == "Spiegel":
    # start and run spiegel scraper agent
    print("spiegel scraper is not implemented yet")

  elif mode == "X":
    with open(RUN_JSON_X_DIR + run_name) as f:
      run_json = json.load(f)
    
    # start scraper
    x = XScraper(run_json)
    x.run()
  
  else:
    raise RuntimeError(f"Passed mode {mode} does not belong to any agent. Make sure to use one of 'X'| 'Spiegel'")
    
if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise RuntimeError("No scraper mode provided!")
  
  main(sys.argv[1], sys.argv[2])
