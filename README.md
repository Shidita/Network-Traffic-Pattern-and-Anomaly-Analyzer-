# Network Traffic Pattern & Anomaly Analyzer

An interactive **Network Traffic Pattern & Anomaly Analyzer** developed as a DAA mini-project using **Python, Flask, SQLite, HTML, CSS, and JavaScript**. The application analyzes network traffic records, identifies unusual traffic behavior, calculates anomaly scores, and presents the results through an interactive web interface.

## 📌 Project Overview

Network traffic can contain unusual patterns such as sudden packet spikes, abnormal data volumes, or unexpected traffic behavior. Manually identifying these patterns in large datasets can be difficult.

This project provides a web-based solution for loading network traffic data from a CSV file, storing the information in an SQLite database, analyzing traffic patterns using algorithmic techniques, and identifying potential anomalies.

The project combines **Data Structures and Algorithms (DAA)** concepts with a practical network traffic analysis application.

## ✨ Features

- Interactive web-based dashboard
- Upload network traffic data using CSV files
- Store and manage traffic data using SQLite
- Display traffic records in an organized table
- Detect potential network traffic anomalies
- Calculate anomaly scores and severity levels
- Identify global traffic spikes
- Identify local traffic spikes
- Detect unusually high bytes per packet
- Display top source IP addresses by packet volume
- Analyze traffic trends
- Analyze traffic by network protocol
- REST API endpoint for dashboard data
- Clean and responsive web interface

## 🧠 Algorithms & DAA Concepts

The project demonstrates several important algorithmic concepts.

### 1. Merge Sort

Merge Sort is implemented to sort packet-volume values efficiently.

**Time Complexity:**  
- Best Case: O(n log n)
- Average Case: O(n log n)
- Worst Case: O(n log n)

The sorted values are also used to determine the median traffic value during analysis.

### 2. Binary Search

Binary Search is implemented as an algorithmic searching technique over sorted values.

**Time Complexity:** O(log n)

It demonstrates how efficient searching can be performed after data has been ordered.

### 3. Sliding Window / Local Analysis

The analyzer examines neighboring traffic records around each record to calculate a local average.

This helps identify traffic spikes that may not appear unusual when compared only with the entire dataset.

### 4. Statistical Anomaly Detection

The system calculates:

- Mean packet count
- Standard deviation
- Median packet count
- Local average
- Anomaly score

A traffic record can be identified as anomalous when it satisfies one or more detection conditions.

## 🚨 Anomaly Detection Rules

The analyzer currently checks several conditions.

### Global Traffic Spike

A record is considered suspicious when:

`packets > mean + 2 × standard deviation`

### Local Traffic Spike

A record is considered suspicious when its packet count is significantly higher than the average of nearby records.

### High Bytes per Packet

The system also checks whether:

`bytes > packets × 1800`

These conditions generate reasons for the detected anomaly.

## 📊 Severity Levels

Detected anomalies are assigned a severity based on their anomaly score.

| Score | Severity |
|---|---|
| Score ≥ 3 | High |
| Score ≥ 2 | Medium |
| Score < 2 | Low |

## 🛠️ Technologies Used

### Programming Language
- Python

### Framework
- Flask

### Database
- SQLite

### Frontend
- HTML
- CSS
- JavaScript

### Data Processing
- Python CSV module
- Statistical calculations

### Algorithms
- Merge Sort
- Binary Search
- Sliding Window / Local Analysis
- Statistical anomaly scoring

## 📁 Project Structure

```text
Network-Traffic-Pattern-and-Anomaly-Analyzer/
│
├── app.py
├── analyzer.py
├── database.py
├── network_traffic.db
├── requirements.txt
├── README.md
│
├── data/
│   └── network_traffic.csv
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── traffic.html
│   ├── anomalies.html
│   ├── analysis.html
│   └── upload.html
│
└── static/
    ├── css/
    │   └── style.css
    │
    └── js/
        └── app.js
```

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Shidita/Network-Traffic-Pattern-and-Anomaly-Analyzer-.git
```

### 2. Open the Project Folder

```bash
cd Network-Traffic-Pattern-and-Anomaly-Analyzer-
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

## ▶️ Running the Application

Start the Flask application:

```bash
python app.py
```

The application will run locally at:

```text
http://127.0.0.1:5000/
```

Open the address in your web browser.

## 📂 CSV Dataset Format

The application expects a CSV file containing the following columns:

```text
timestamp
source_ip
destination_ip
port
packets
bytes
protocol
```

Example:

```csv
timestamp,source_ip,destination_ip,port,packets,bytes,protocol
2026-01-01 10:00:00,192.168.1.10,10.0.0.5,80,120,15000,TCP
```

## 🔄 Application Workflow

```text
CSV Traffic Dataset
        ↓
CSV Upload
        ↓
Data Validation
        ↓
SQLite Database
        ↓
Traffic Analysis
        ↓
Merge Sort
        ↓
Statistical Analysis
        ↓
Sliding Window Analysis
        ↓
Anomaly Detection
        ↓
Anomaly Score
        ↓
Severity Classification
        ↓
Interactive Dashboard
```

## 🖥️ Main Application Sections

### Dashboard

The dashboard provides an overview of:

- Total traffic records
- Number of unique source IPs
- Total packets
- Total bytes
- Number of detected anomalies
- Top source IPs

### Traffic Records

Displays stored network traffic records including:

- Timestamp
- Source IP
- Destination IP
- Port
- Packets
- Bytes
- Protocol

### Anomalies

Displays detected anomalies with:

- Timestamp
- Source IP
- Packet count
- Byte count
- Anomaly score
- Severity
- Reason for detection

### Upload

Users can upload a CSV dataset through the web interface. The uploaded data is stored in SQLite and analyzed automatically.

## 🔌 API

The application also provides a dashboard API endpoint:

```text
/api/dashboard
```

The endpoint returns dashboard information in JSON format, including:

- Traffic statistics
- Anomaly count
- Traffic trends
- Protocol statistics

## 🗄️ Database

The project uses **SQLite** with two primary tables:

### `traffic`

Stores network traffic information such as:

- Timestamp
- Source IP
- Destination IP
- Port
- Packet count
- Byte count
- Protocol

### `anomalies`

Stores detected anomalies including:

- Traffic record ID
- Timestamp
- Source IP
- Packet count
- Byte count
- Anomaly score
- Severity
- Detection reason

## 🎯 Objectives

The main objectives of this project are:

1. Analyze network traffic data efficiently.
2. Demonstrate practical applications of DAA concepts.
3. Detect unusual network traffic patterns.
4. Implement sorting and searching algorithms.
5. Apply local and statistical analysis to traffic data.
6. Store and retrieve network data using SQLite.
7. Provide an easy-to-use web interface for analysis.
8. Present detected anomalies in an understandable format.

## 🔮 Future Enhancements

Possible future improvements include:

- Real-time network packet monitoring
- Machine learning based anomaly detection
- Additional network protocols and traffic features
- Advanced visualization and charts
- User authentication
- Export anomaly reports to CSV/PDF
- Configurable anomaly thresholds
- Network security alert notifications
- Integration with live packet capture tools such as Wireshark/tcpdump

## 🎓 Academic Purpose

This project demonstrates how **Data Structures and Algorithms** can be applied to a practical cybersecurity and network traffic analysis problem.

The implementation combines algorithmic techniques with a Flask web application and SQLite database to create an interactive network traffic analysis system.

## 👩‍💻 Author

**Shidita Tiwari**

GitHub:  
https://github.com/Shidita

## 📄 License

This project is developed for educational and academic purposes.
