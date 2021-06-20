# tap-cmc

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [CoinMarketCap](https://coinmarketcap.com/)
- Extracts the following resources from the listing of the top 50 coins on coinmarketcap's website:
  - `name`
  - `symbol`
  - `cmc_rank`
  - `price`
  - `last_updated`
  - `market_cap`
  - `volume_24h`
  - `timestamp`
 - Outputs the schema for each resource

# Schema of the data getting pulled down
```
{
  "name":         {"type": "string"},
  "symbol":       {"type": "string"},
  "cmc_rank":     {"type": "integer"},
  "price":        {"type": "number"},
  "last_updated": {"type": "string", "format": "date-time"},
  "market_cap":   {"type": "integer"},
  "volume_24h":   {"type": "integer"},
  "timestamp":    {"type": "string", "format": "date-time"}
}
```
# Prerequisites

1. Access to [CoinMarketCap API key](https://coinmarketcap.com/api/) 
2. [Python 3](https://www.python.org/downloads/)
3. Python virtualenv (optional)


# Build steps to get the tap running
1. Clone the repo

&emsp;&emsp;&emsp;&emsp;  $ `git clone git@github.com:kafagy/tap-cmc.git`

2. Add the CoinMarketCap API key in the `config.json` file
3. Install the project as a python package

&emsp;&emsp;&emsp;&emsp; $ `sudo pip3 install -e .`

4. Run the tap in discovery mode

&emsp;&emsp;&emsp;&emsp; $ `tap-cmc -c config.json --discover > catalog.json`

5. Edit the `catalog.json` to select the `cmc_listings_stream` 

&emsp;&emsp;&emsp;&emsp; Add the key value pair `"selected": true` under the `schema` key. 

6. Run the tap in sync mode

&emsp;&emsp;&emsp;&emsp; $ `tap-cmc -c config.json --catalog catalog.json`