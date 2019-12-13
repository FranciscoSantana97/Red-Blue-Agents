from flask import Flask, send_from_directory
import os, sys

app = Flask(__name__)

@app.route("/download", methods=["GET"])
def download():
    base = os.path.join(os.path.dirname(__file__))
    name = "rat"
    return send_from_directory(directory = base, filename = name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print ("Run this script with a parameter that denotes a port number")
        sys.exit(0)
    try:
        port = int(sys.argv[1])
    except ValueError:
        print ("Please specify a valid port number")
        sys.exit(0)

    #TODO : Catch exceptions with a kind error message :)
    app.run(debug = True, host="0.0.0.0", port=port)
