from flask import Flask

app = Flask(__name__)

@app.route("/")  # ✅ Add this route
def home():
    return "BlueprintIQ is running!"

if __name__ == "__main__":
    app.run(debug=True)
