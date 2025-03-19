# X and Spiegel Scraper
This repository is part of the project ["Diskurs Energiewende"](https://jonasrieger.github.io/2024/09/03/bmwk.html) and provides code for scraping posts from [X](https://X.com) and [Spiegel Debatte](https://www.spiegel.de/debatten) related to the energy transition and social inequality.

To achieve this, let us first introduce the scraper-agent. A scraper-agent is an programm, which emulates a normal user, browsing the web. One scraper-agent is indepent of other scraper-agents and operates in an environemnt that has it's on OS, IP-Adress, browser etc.. We achieve this, by running each scraper-agent in a docker-container which can be easily instantiated from our `scraper-agent` image.

## Setup
To run this setup locally, make sure you have [docker desktop](https://www.docker.com/) installed.

Clone the repo and run from the root directory:
```
docker build . -t scraper-agent
```
Then instantiate scraper-agents through the run command
```
docker run -it -v data scraper-agent X | Spiegel
```

## Underlying Architecture
![Software-Architecture](./assets/architecture.svg)

