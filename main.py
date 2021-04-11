
import argparse
from chonk_api import ChonkMarketApiClient

parser = argparse.ArgumentParser(description='A basic example api client for chonk.market')
parser.add_argument(
    '--apibaseurl',
    default='https://chonk.market/api',
    help='The base url for the chonk.market api. You is rarely something you would need to set.',
    required=False
)
parser.add_argument(
    '-t',
    '--token',
    required=True,
    help='The auth token from your chonk.market account, you can copy this from the API settings page'
)
parser.add_argument(
    '--verifytoken',
    default=True,
    help='If enabled this client will verify the identity token before submitting to the chonk.market api. This is mostly to make it easy to notice if it was copied wrong',
    required=False
)
parser.add_argument(
    '--ssl_verification',
    default=False,
    help='If disabled the client will not verify the ssl certificate for the chonk.market API. This is mostly for development testing.',
    required=False
)
parser.add_argument(
    '-v',
    '--verbose',
    default=False,
    help='If enabled this client will log more information.',
    action='store_true',
    required=False
)
parser.add_argument(
    '--fetch_day',
    default="4/6/2021",
    help='Which date to fetch data for',
    required=False
)
parser.add_argument(
    '--fetch_data',
    default=False,
    help='Fetch all of the data for the given date and print it out',
    required=False
)
parser.add_argument(
    '--fetch_tickers',
    default=False,
    help='Fetch all of the available tickers and print them out',
    required=False
)
parser.add_argument(
    '--stream_test_data',
    default=False,
    help='Stream test data for the given date',
    required=False
)
parser.add_argument(
    '--stream_data',
    default=False,
    help='Stream live data flowing in now',
    required=False
)
parser.add_argument(
    '--ticker',
    default='SPY',
    help='The ticker we are going to get data for',
    required=False
)

args = parser.parse_args()

client = ChonkMarketApiClient(
    args.apibaseurl,
    args.token,
    args.verifytoken,
    args.verbose,
    args.ssl_verification)

if (args.fetch_tickers):
    client.fetch_tickers()

if (args.fetch_data):
    client.fetch_quotes("spy", args.fetch_day)

if (args.stream_test_data or args.stream_data):
    print("This will print out data points as they flow in")
    if (args.stream_test_data):
        messages = client.stream_data(symbol=args.ticker, testmode=True, date=args.fetch_day)

    if (args.stream_data):
        messages  = client.stream_data(symbol=args.ticker)

    for msg in messages:
        print(msg)
