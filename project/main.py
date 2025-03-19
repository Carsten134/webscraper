import sys
import pandas as pd

def main(mode:str) -> None:
  if mode == "Spiegel":
    # start and run spiegel scraper agent
    print("spiegel scraper should run now")

  elif mode == "X":
    # start and run X scraper agent
    df = pd.DataFrame({"test": [1,2,3,4]})
    df.to_csv("./project/data/X/test.csv")
    print("X scraper should run now")
  
  else:
    raise RuntimeError(f"Passed mode {mode} does not belong to any agent. Make sure to use one of 'X'| 'Spiegel'")
    
if __name__ == "__main__":
  if len(sys.argv) < 2:
    raise RuntimeError("No scraper mode provided!")
  
  main(sys.argv[1])
