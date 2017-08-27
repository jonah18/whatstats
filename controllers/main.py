from flask import *

main = Blueprint('main', __name__, template_folder='templates')

fullChat = {}

chats = []
stats = {}


def updatePostStats(author):
    if author in stats:
        stats[author] += 1
    else:
        stats[author] = 1


# Update group messaging statistics
def updateWordCountStats(author, message):

    if author not in stats:
        stats[author] = 0

    # Add one word for image/video post
    if "<" in message:
        stats[author] += 1

    for _ in message:
        stats[author] += 1


def parseMessage(line, chat, metric):
    split = line.split(":")

    if len(split) < 5:
        return False

    date = line.split(",")[0]
    timestamp = line.split("M:")[0].split(", ")[1]

    author = split[3][1:]
    message = split[4][1:]

    if metric == "posts":
        updatePostStats(author)

    else:
        updateWordCountStats(author, message)

    chat["author"] = author
    chat["message"] = message
    chat["date"] = date
    chat["timestamp"] = timestamp + "M"

    return True


@main.route('/', methods=['GET', 'POST'])
def main_route():
    options = {}

    if request.method == 'POST':

        metric = request.form['metric']
        file = request.files['file']

        numChats = 0
        for line in file.readlines():
            chat = {}
            line = str(line)

            if parseMessage(line, chat, metric):
                chats.append(chat)
            numChats += 1
        options['stats'] = stats

    return render_template("stats.html", **options)
