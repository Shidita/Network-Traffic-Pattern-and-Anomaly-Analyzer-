from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

from database import init_db, load_csv, query
from analyzer import analyze_traffic


# --------------------------------------------------
# FLASK APPLICATION
# --------------------------------------------------

app = Flask(__name__)

# Secret key for Flask flash messages
app.secret_key = "network-traffic-analyzer-secret"

# Initialize database
init_db()


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

@app.route("/")
def dashboard():

    stats = query("""
        SELECT
            COUNT(*) AS records,
            COUNT(DISTINCT source_ip) AS unique_ips,
            COALESCE(SUM(packets), 0) AS packets,
            COALESCE(SUM(bytes), 0) AS bytes
        FROM traffic
    """)[0]

    anomaly_count = query("""
        SELECT COUNT(*) AS c
        FROM anomalies
    """)[0]["c"]

    top_ips = query("""
        SELECT
            source_ip,
            SUM(packets) AS packets
        FROM traffic
        GROUP BY source_ip
        ORDER BY packets DESC
        LIMIT 7
    """)

    return render_template(
        "dashboard.html",
        stats=stats,
        anomaly_count=anomaly_count,
        top_ips=top_ips
    )


# --------------------------------------------------
# TRAFFIC RECORDS
# --------------------------------------------------

@app.route("/traffic")
def traffic():

    rows = query("""
        SELECT *
        FROM traffic
        ORDER BY timestamp DESC
        LIMIT 250
    """)

    return render_template(
        "traffic.html",
        rows=rows
    )


# --------------------------------------------------
# ANOMALIES PAGE
# --------------------------------------------------

@app.route("/anomalies")
def anomalies():

    rows = query("""
        SELECT *
        FROM anomalies
        ORDER BY score DESC, timestamp DESC
    """)

    return render_template(
        "anomalies.html",
        rows=rows
    )


# --------------------------------------------------
# UPLOAD CSV
# --------------------------------------------------

@app.route("/upload", methods=["GET", "POST"])
def upload():

    if request.method == "POST":

        file = request.files.get("file")

        # Check file
        if not file or file.filename == "":
            flash(
                "Please select a CSV file.",
                "error"
            )
            return redirect(url_for("upload"))

        # Check extension
        if not file.filename.lower().endswith(".csv"):
            flash(
                "Only CSV files are allowed.",
                "error"
            )
            return redirect(url_for("upload"))

        # Temporary upload location
        path = "/tmp/network_traffic_upload.csv"

        try:

            # Save uploaded file
            file.save(path)

            # Load CSV into database
            load_csv(path)

            # Run anomaly analysis
            result = analyze_traffic()

            flash(
                f"Dataset loaded successfully — "
                f"{result['anomalies']} anomalies found.",
                "success"
            )

        except Exception as exc:

            flash(
                f"Could not process the file: {exc}",
                "error"
            )

        return redirect(url_for("dashboard"))

    return render_template("upload.html")


# --------------------------------------------------
# RUN ANALYSIS
# --------------------------------------------------

@app.route("/analyze")
def analyze():

    try:

        result = analyze_traffic()

        flash(
            f"Analysis complete — "
            f"{result['anomalies']} anomalies found.",
            "success"
        )

    except Exception as exc:

        flash(
            f"Analysis failed: {exc}",
            "error"
        )

    return redirect(url_for("anomalies"))


# --------------------------------------------------
# DAA ANALYSIS PAGE
# --------------------------------------------------

@app.route("/analysis")
def analysis():

    return render_template(
        "analysis.html"
    )


# --------------------------------------------------
# DASHBOARD API
# --------------------------------------------------

@app.route("/api/dashboard")
def api_dashboard():

    # Basic statistics
    stats = query("""
        SELECT
            COUNT(*) AS records,
            COUNT(DISTINCT source_ip) AS unique_ips,
            COALESCE(SUM(packets), 0) AS packets,
            COALESCE(SUM(bytes), 0) AS bytes
        FROM traffic
    """)[0]

    # Total anomalies
    anomalies = query("""
        SELECT COUNT(*) AS c
        FROM anomalies
    """)[0]["c"]

    # Traffic trend
    trend = query("""
        SELECT
            substr(timestamp, 1, 13) AS hour,
            SUM(packets) AS packets
        FROM traffic
        GROUP BY hour
        ORDER BY hour
    """)

    # Protocol distribution
    protocols = query("""
        SELECT
            protocol,
            SUM(packets) AS packets
        FROM traffic
        GROUP BY protocol
        ORDER BY packets DESC
    """)

    return jsonify({

        "stats": dict(stats),

        "anomalies": anomalies,

        "trend": [
            dict(row)
            for row in trend
        ],

        "protocols": [
            dict(row)
            for row in protocols
        ]

    })


# --------------------------------------------------
# ERROR HANDLERS
# --------------------------------------------------

@app.errorhandler(404)
def page_not_found(error):

    return """
    <div style="
        font-family: Arial;
        text-align: center;
        margin-top: 100px;
    ">

        <h1>404</h1>

        <h2>Page Not Found</h2>

        <p>
            The requested page does not exist.
        </p>

        <a href="/">
            Go back to Dashboard
        </a>

    </div>
    """, 404


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )