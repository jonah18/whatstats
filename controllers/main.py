from flask import *
from collections import OrderedDict
from datetime import datetime, timedelta

main = Blueprint('main', __name__, template_folder='templates')

# Update number of posts stats
def calcPostStats(author, stats):

    if author in stats:
        stats[author] += 1
    else:
        stats[author] = 1

# Update number of words stats
def calcWordStats(author, message, stats):

    if author not in stats:
        stats[author] = 0

    # Add one word for image/video post
    if "<" in message:
        stats[author] += 1

    for _ in message:
        stats[author] += 1

# Update number of media stats
def calcMediaStats(author, message, stats):

    if author not in stats:
        stats[author] = 0

    if "<" in message:
        stats[author] += 1

def parseMessage(line, chat, metric, stats):
    split = line.split(":")

    if len(split) < 5:
        return False

    date = line.split(",")[0]
    timestamp = line.split("M:")[0].split(", ")[1]

    author = split[3][1:]
    message = split[4][1:]

    if metric == "posts":
        calcPostStats(author, stats)

    elif metric == "words":
        calcWordStats(author, message, stats)

    elif metric == "media":
        calcMediaStats(author, message, stats)

    chat["author"] = author
    chat["message"] = message
    chat["date"] = date
    chat["timestamp"] = timestamp + "M"

    return True

# If date range is set, checks if message falls within range
def validMessageDate(line, beginDate):
    split = line.split(":")

    if len(split) < 5:
        return False

    date = line.split(",")[0]
    splitDate = date.split("/")

    dateTime = datetime(int('20' + splitDate[2]), int(splitDate[0]), int(splitDate[1]))

    if dateTime < beginDate:
        return False

    return True


@main.route('/', methods=['GET', 'POST'])
def main_route():
    options = {}

    if request.method == 'GET':
        return render_template("home.html")

    elif request.method == 'POST':

        if request.files['file'].filename == '':
            options['message'] = "No File"

            return render_template("home.html", **options)

        chats = []
        stats = {}
        rangeSet = False

        metric = request.form['metric']
        file = request.files['file']
        timeUnit = request.form['time-unit']

        # Check if time range is set
        if timeUnit != "all":
            rangeSet = True

            now = datetime.now()
            timeNumber = int(request.form['time-number'])

            # Determine beginning range for date
            if timeUnit == "year":
                timeDelta = timedelta(days=365*timeNumber)

            elif timeUnit == "month":
                timeDelta = timedelta(days=30*timeNumber)

            else:
                timeDelta = timedelta(weeks=timeNumber)

            beginDate = now - timeDelta

        numChats = 0
        for line in file.readlines():
            chat = {}
            line = line.decode('utf-8')

            if rangeSet:
                if not validMessageDate(line, beginDate):
                    continue

            if parseMessage(line, chat, metric, stats):
                chats.append(chat)
            numChats += 1

        stats = OrderedDict(sorted(stats.items(), key=lambda x: x[1], reverse=True))

        options['message'] = "Success"
        options['stats'] = stats

    return render_template("stats.html", **options)
