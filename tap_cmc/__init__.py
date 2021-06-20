#!/usr/bin/env python3
import os
import json
import singer
import json
import singer
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from singer import utils
from singer.catalog import Catalog, CatalogEntry
from singer.schema import Schema


REQUIRED_CONFIG_KEYS = ["url", "api_key", "start", "limit", "convert"]
LOGGER = singer.get_logger()


def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)


def load_schemas():
    """ Load schemas from schemas folder """
    schemas = {}
    for filename in os.listdir(get_abs_path('schemas')):
        path = get_abs_path('schemas') + '/' + filename
        file_raw = filename.replace('.json', '')
        with open(path) as file:
            schemas[file_raw] = Schema.from_dict(json.load(file))
    return schemas


def discover():

    raw_schemas = load_schemas()
    streams = []
    for stream_id, schema in raw_schemas.items():
        # TODO: populate any metadata and stream's key properties here..
        stream_metadata = []
        key_properties = []
        streams.append(
            CatalogEntry(
                tap_stream_id=stream_id,
                stream=stream_id,
                schema=schema,
                key_properties=key_properties,
                metadata=stream_metadata,
                replication_key=None,
                is_view=None,
                database=None,
                table=None,
                row_count=None,
                stream_alias=None,
                replication_method=None,
            )
        )
    return Catalog(streams)


def sync(config, state, catalog):
    """ Sync data from tap source """
    print(config)
    for stream in catalog.get_selected_streams(state):
        LOGGER.info("Syncing stream:" + stream.tap_stream_id)

        LOGGER.info(stream.tap_stream_id)
        LOGGER.info(stream.schema)
        LOGGER.info(stream.key_properties)
        singer.write_schema(
            stream_name=stream.tap_stream_id,
            schema=stream.schema.to_dict(),
            key_properties=stream.key_properties,
        )

        url = config['url']
        parameters = {
            'start': config['start'],
            'limit': config['limit'],
            'convert': config['convert']
        }

        headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config['api_key']
        }

        session = Session()
        session.headers.update(headers)
        try:
            response = session.get(url, params=parameters)
            coins = json.loads(response.text)
            for coin in coins['data']:
                name = coin['name']
                rank = coin['cmc_rank']
                symbol = coin['symbol']
                last_updated = coin['quote']['USD']['last_updated']
                price = coin['quote']['USD']['price']
                market_cap = int(coin['quote']['USD']['market_cap'])
                volume_24h = int(coin['quote']['USD']['volume_24h'])
                singer.write_records(stream.tap_stream_id,[{
                    'name': name,
                    'rank': rank,
                    'symbol': symbol,
                    'last_updated': last_updated,
                    'price': price,
                    'market_cap': market_cap,
                    'volume_24h': volume_24h
                }])
        except(ConnectionError, Timeout, TooManyRedirects) as e:
            LOGGER.error(e)
    return


@utils.handle_top_exception(LOGGER)
def main():
    # Parse command line arguments
    args = utils.parse_args(REQUIRED_CONFIG_KEYS)

    # If discover flag was passed, run discovery mode and dump output to stdout
    if args.discover:
        catalog = discover()
        catalog.dump()
    # Otherwise run in sync mode
    else:
        if args.catalog:
            catalog = args.catalog
        else:
            catalog = discover()
        sync(args.config, args.state, catalog)


if __name__ == "__main__":
    main()
