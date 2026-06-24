import pandas as pd
import json
import gpxpy
import os


def standardize_timestamp(ts):
    try:
        return pd.to_datetime(ts)
    except:
        return pd.NaT


def process_csv(filepath):
    df = pd.read_csv(filepath)
    return df


def process_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    df = pd.json_normalize(data)
    return df


def process_gpx(filepath):
    with open(filepath, "r") as f:
        gpx = gpxpy.parse(f)

    rows = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                rows.append({
                    "latitude": point.latitude,
                    "longitude": point.longitude,
                    "elevation": point.elevation,
                    "timestamp": point.time
                })

    return pd.DataFrame(rows)


def ingest(filepath):

    if not os.path.exists(filepath):
        return {"error": "File not found"}

    if os.path.getsize(filepath) == 0:
        return {"error": "Uploaded file is empty"}

    try:
        ext = filepath.split(".")[-1].lower()

        if ext == "csv":
            df = process_csv(filepath)

        elif ext == "json":
            df = process_json(filepath)

        elif ext == "gpx":
            df = process_gpx(filepath)

        else:
            return {"error": f"Unsupported file type: {ext}"}

        total_rows = len(df)

        missing_count = int(df.isna().sum().sum())

        timestamp_col = None

        for col in df.columns:
            if "time" in col.lower() or "date" in col.lower():
                timestamp_col = col
                break

        start_time = None
        end_time = None

        if timestamp_col:

            before_missing = df[timestamp_col].isna().sum()

            df[timestamp_col] = df[timestamp_col].apply(
                standardize_timestamp
            )

            after_missing = df[timestamp_col].isna().sum()

            missing_count += (after_missing - before_missing)

            valid_times = df[timestamp_col].dropna()

            if len(valid_times) > 0:
                valid_times = valid_times.sort_values()

                start_time = valid_times.iloc[0].strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                end_time = valid_times.iloc[-1].strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                df[timestamp_col] = df[timestamp_col].dt.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

        gps_missing = 0

        if "latitude" in df.columns:
            gps_missing += df["latitude"].isna().sum()

        if "longitude" in df.columns:
            gps_missing += df["longitude"].isna().sum()

        summary = {
            "total_rows_processed": total_rows,
            "missing_or_corrupted_data_points":
                int(missing_count + gps_missing),
            "start_timestamp": start_time,
            "end_timestamp": end_time,
            "columns": list(df.columns)
        }

        print("\n===== DATA INGESTION SUMMARY =====")
        print(summary)

        print("\n===== CLEANED DATA PREVIEW =====")
        print(df.head())

        return summary

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":

    filepath = input("Enter file path: ").strip()

    result = ingest(filepath)

    if "error" in result:
        print("\nError:", result["error"])