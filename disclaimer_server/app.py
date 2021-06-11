from flask import Flask
from gevent.pywsgi import WSGIServer
import getopt
import html
import requests
import sys
import xml.etree.ElementTree as ET

app = Flask(__name__)
disclaimers = dict()
parameters = dict()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hdi:f:p:", ["ip=", "feed=", "port="])
    except getopt.GetoptError:
        print('python app.py -f <xml_feed_url> -i <ip> -p <port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('python app.py -f <xml_feed_url> -i <ip> -p <port>')
            sys.exit()
        elif opt in ("-i", "--ip"):
            parameters["ip"] = arg
        elif opt in ("-f", "--feed"):
            parameters["feed_url"] = arg
        elif opt in ("-p", "--port"):
            parameters["port"] = arg
        elif opt == "-d":
            parameters["debug"] = True
    if "feed_url" not in parameters:
        print('missing required feed_url parameter')
        sys.exit(2)
    print("parameters=", parameters)
    if parameters.get("debug", False):
        app.run(
            debug=True,
            host=parameters.get("ip", "127.0.0.1"),
            port=parameters.get("port", 5000),
        )
    else:
        http_server = WSGIServer((
            parameters.get("ip", ""),
            parameters.get("port", 5000)
        ), app)
        http_server.serve_forever()


def reloadListings():
    resp = requests.get(parameters["feed_url"])
    listings = ET.fromstring(resp.text)
    print("reloading listings from", parameters["feed_url"])
    disclaimers.clear()
    count = 0
    for listing in listings:
        vehicle_offer_id = listing.find('vehicle_offer_id').text
        offer_disclaimer = listing.find('offer_disclaimer').text
        if len(offer_disclaimer) > 0:
            # special processing since the user's xml double escaped content
            disclaimers[vehicle_offer_id] = html.unescape(offer_disclaimer)
            count += 1
    print(count, "disclaimers loaded")


def lookupDisclaimer(vehicle_offer_id: str) -> str:
    if not disclaimers or vehicle_offer_id not in disclaimers:
        reloadListings()
    return disclaimers.get(vehicle_offer_id)


@app.route('/disclaimer/<vehicle_offer_id>')
def routeDisclaimer(vehicle_offer_id):
    disclaimerContent = lookupDisclaimer(vehicle_offer_id)
    if not disclaimerContent:
        return ''
    # TODO: adjust CSS here
    return html.unescape(disclaimerContent)


if __name__ == "__main__":
    main(sys.argv[1:])
