from database import connect

def merge_sort(values):
    if len(values) <= 1:
        return values
    middle = len(values) // 2
    left = merge_sort(values[:middle])
    right = merge_sort(values[middle:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    return result + left[i:] + right[j:]

def binary_search(values, target):
    low, high = 0, len(values) - 1
    while low <= high:
        middle = (low + high) // 2
        if values[middle] == target:
            return middle
        if values[middle] < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1

def analyze_traffic():
    connection = connect()
    records = connection.execute("SELECT * FROM traffic ORDER BY id").fetchall()
    connection.execute("DELETE FROM anomalies")

    if not records:
        connection.commit()
        connection.close()
        return {"anomalies": 0}

    packet_values = [record["packets"] for record in records]
    ordered = merge_sort(packet_values)
    mean = sum(packet_values) / len(packet_values)
    standard_deviation = (
        sum((value - mean) ** 2 for value in packet_values) / len(packet_values)
    ) ** 0.5

    found = 0
    for index, record in enumerate(records):
        start = max(0, index - 2)
        end = min(len(records), index + 3)
        window = [records[j]["packets"] for j in range(start, end) if j != index]
        local_average = sum(window) / len(window) if window else mean

        score = max(0, (record["packets"] - local_average) / (standard_deviation or 1))
        reasons = []

        if record["packets"] > mean + 2 * standard_deviation:
            reasons.append("global traffic spike")
        if record["packets"] > local_average * 2.5:
            reasons.append("local traffic spike")
        if record["bytes"] > record["packets"] * 1800:
            reasons.append("high bytes per packet")

        if reasons:
            severity = "High" if score >= 3 else ("Medium" if score >= 2 else "Low")
            connection.execute(
                """INSERT INTO anomalies
                   (traffic_id,timestamp,source_ip,packets,bytes,score,severity,reason)
                   VALUES (?,?,?,?,?,?,?,?)""",
                (record["id"], record["timestamp"], record["source_ip"],
                 record["packets"], record["bytes"], round(score, 2),
                 severity, "; ".join(reasons))
            )
            found += 1

    connection.commit()
    connection.close()
    return {
        "anomalies": found,
        "mean": round(mean, 2),
        "median": ordered[len(ordered)//2],
        "std_dev": round(standard_deviation, 2)
    }
