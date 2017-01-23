import argparse

from blackjack.server import app


parser = argparse.ArgumentParser(description='Blackjack server')
parser.add_argument('-a', '--host', help='Host address', required=False, default="localhost")
parser.add_argument('-p', '--port', help='Port number', required=False, default=5000, type=int)
parser.add_argument('-d', '--verbose', help='Verbose mode', action='store_true')
args = parser.parse_args()


if __name__ == '__main__':
    app.run(host=args.host, port=args.port, debug=args.verbose)
