from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def dashboard():
    return render_template("dashboard.html", 
                          address="0x5df3d175dfedc08bfd0fb93912f9162926fb2e1",
                          balance=60,
                          tx_count=3,
                          node_status="Idle")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
