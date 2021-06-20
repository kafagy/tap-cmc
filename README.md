# tap-cmc

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from [CoinMarketCap](https://coinmarketcap.com/)
- Extracts the following resources from the listing of the top 50 coins on coinmarketcap's website:
  - name
  - symbol
  - cmc_rank
  - price
  - last_updated
  - market_cap
  - volume_24h
  - timestamp
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

# Build steps to get the tap running
## Clone the repo

$ `git clone git@github.com:kafagy/tap-cmc.git`

## Install the project as a python package

$ `pip3 install -e .`

## Run the tap in discovery mode

$ `tap-cmc -c config.json --discover > catalog.json`

## Edit `catalog.json` to select stream
 Edit the `catalog.json` to select the `cmc_listings_stream` by adding the key value pair `"selected": true` under the `schema` key. 

## Run the tap in sync mode

$ `tap-cmc -c config.json --catalog catalog.json`