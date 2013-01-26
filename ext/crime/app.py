import flask
app = flask.Flask(__name__)

import datetime
import json
import urllib2
import operator

import collections

KEYS = {"category", }

CATEGORIES = {
    "anti-social-behaviour": "AntiSocial Behaviour",

}

LOCATIONS = {}

NEIGHS = {}

def get_neighbourhood(nid):
    if len(NEIGHS) == 0:
        data = get_json("http://policeapi2.rkh.co.uk/api/leicestershire/neighbourhoods")
        NEIGHS.update(dict((n["id"], n["name"]) for n in data))
    return NEIGHS[nid]


CACHE = {}
def get_json(url):
    if url not in CACHE:
        CACHE[url] = json.loads(urllib2.urlopen(url).read())
    return CACHE[url]


@app.route("/api/data.json")
def base():
    lat = flask.request.args["lat"]
    lon = flask.request.args["long"]
    cat = flask.request.args["cat"]

    providers = ["crime", "life", "paygap"]
    datasets = []
    return {
        "title": "Shoreditch",
        "datasets": datasets
    }


def location(lat, lon):
    url = ("http://policeapi2.rkh.co.uk/api/locate-neighbourhood?q=%s,%s" %
        (lat, lon))
    data = get_json(url)
    return data["neighbourhood"]


REGION_DATA = {
    (u'52.629729', u'-1.131592'): 1660
}

def fetch_region(lat, lon, date):
    neigh_id = location(lat, lon)
    url = ("http://policeapi2.rkh.co.uk/api/leicestershire/%s/crime" %
        (neigh_id))
    info = get_json(url)
    total = 0
    for date in info["crimes"].values():
        for cat in date.values():
            total += cat["total_crimes"]
    return total


def get_region(lat, lon, date):
    if (lat, lon) not in REGION_DATA:
        REGION_DATA[lat, lon] = fetch_region(lat, lon, date)
    return REGION_DATA[lat, lon]


STREET_DATA = {
    (u'52.629729', u'-1.131592'): {u'public-disorder-weapons': 61, u'vehicle-crime': 82, u'robbery': 12, u'shoplifting': 117, u'drugs': 30, u'other-crime': 28, u'anti-social-behaviour': 305, u'criminal-damage-arson': 93, u'burglary': 62, u'other-theft': 273, u'violent-crime': 177}
}


def fetch_data(lat, lon, date):
    url = ("http://policeapi2.rkh.co.uk/api/crimes-street/all-crime?date=%s&lat=%s&lng=%s" %
        (date, lat, lon))
    data = get_json(url)
    cats = collections.defaultdict(int)
    for item in data:
        cats[item["category"]] += 1
    return cats


@app.route("/api/crime/<lat>/<lon>/")
def get_data(lat, lon):
    date = datetime.datetime.today().strftime("2012-09")
    if (lat, lon) not in STREET_DATA:
        STREET_DATA[lat, lon] = fetch_data(lat, lon, date)

    region_total = get_region(lat, lon, date)
    
    data = STREET_DATA[lat, lon]

    cat_total = sum(data.values())

    cat_percent = dict((c, int(100 * (d/float(cat_total)) )) 
                        for c,d in data.iteritems())
    out_data = sorted(cat_percent.items(), key=operator.itemgetter(1), reverse=True)[:4]
    out_data[-1] = ("rape", out_data[-1][1])
    return flask.render_template("hi.html", total=region_total, data=out_data)


@app.route("/api/location/<lat>/<lon>/")
def get_location(lat, lon):
    url = "http://www.uk-postcodes.com/latlng/%s,%s.json" % (51.52251,-0.085208)
    data = get_json(url)
    return json.dumps({
        "postcode": data["postcode"],
        "name": data["administrative"]["ward"]["title"],
        "connurbation": "London"
        })
    return json.dumps()

if __name__ == "__main__":
    try:
        get_neighbourhood[0]
    except:
        pass
    app.run(debug=True)