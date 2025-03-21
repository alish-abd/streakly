from flask import Flask, request, jsonify, Response
import calendar
from datetime import datetime
import os

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello from Flask!"

@app.route('/calendar', methods=['POST'])
def generate_calendar():
    data = request.get_json()
    if not data or 'dates' not in data:
        return jsonify({"error": "Please provide 'dates' array in JSON."}), 400

    # Convert list of dates to a set for quick membership checks
    activity_dates = set(data['dates'])
    
    # Optional year/month params; default to current if not provided
    try:
        year = int(data.get('year', datetime.today().year))
        month = int(data.get('month', datetime.today().month))
    except ValueError:
        return jsonify({"error": "year and month should be integers."}), 400

    # Get a matrix of weeks for the given month (each row is a week, each cell is a day or 0 if not in that month)
    month_weeks = calendar.monthcalendar(year, month)
    
    # Day-of-week header (Russian, Monday-Sunday)
    header = "Пн Вт Ср Чт Пт Сб Вс"

    rows = []
    for week in month_weeks:
        week_cells = []
        for day in week:
            if day == 0:
                # No day in this cell (padding)
                week_cells.append("   ")
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                # Mark with ✅ if in activity_dates, else just day number
                cell = "✅" if date_str in activity_dates else f"{day:2d}"
                week_cells.append(cell)
        rows.append(" ".join(week_cells))
    
    calendar_text = (
        f"Календарь активностей для {year}-{month:02d}:\n"
        f"{header}\n" +
        "\n".join(rows)
    )

    # Return as plain text
    return Response(calendar_text, mimetype='text/plain')

if __name__ == "__main__":
    # Railway sets PORT as an env var. Default to 5000 if not set.
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
