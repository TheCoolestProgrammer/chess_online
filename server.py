from flask import Flask, request
import json

app = Flask(__name__)

last_sender = "black"
last_way = [None, None]


@app.route("/")
def result():
    global last_sender, last_way

    method = request.args.get("method")
    if method == "SET":
        sender = request.args.get("sender")

        new_pos = request.args.get("new_pos")
        if new_pos:
            new_pos = new_pos.split(";")

        pos = request.args.get("pos")
        if pos:
            pos = pos.split(";")

        if sender != last_sender:
            last_sender = sender
            last_way = [pos, new_pos]
    else:
        sender = request.args.get("sender")
        if sender == last_sender:
            return json.dumps([0])
    print(last_way)
    answer = last_way
    answer = json.dumps(answer)
    return answer



def main():
    # port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
