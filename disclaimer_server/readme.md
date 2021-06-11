# Disclaimer Server

Example web server to dynamically server xml content.

## Requirements

* Python 3
* Requests library (pip3 install requests)
* Flask library (pip3 install flask)
* gevent library (pip3 install gevent)

### Parameters

 * -d = debug mode (default: false)
 * -f = feed url (required)
 * -i = serving host (default: 127.0.0.1 or localhost)
 * -p = serving port (default: 5000)

## Usage:

```
python3 app.py -f "https://www.example.com/offer.xml"

# use browser to visit
#   (first visit may be slow since it lazily loads the xml, after initial loading, it is cached in memory)
#  http://localhost:5000/disclaimer/<vehicle_offer_id>
#  http://localhost:5000/disclaimer/CUT202017_500
#  http://localhost:5000/disclaimer/CUT202013_501
```
