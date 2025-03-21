from flask import Flask, request, jsonify, Response
import calendar
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/calendar', methods=['POST'])
def generate_calendar():
    data = request.get_json()
    if not data or 'dates' not in data:
        return jsonify({"error": "Please provide 'dates' array in JSON."}), 400

    # Extract dates from request
    activity_dates = set(data['dates'])
    
    # Get year & month, default to current if not provided
    try:
        year = int(data.get('year', datetime.today().year))
        month = int(data.get('month', datetime.today().month))
    except ValueError:
        return jsonify({"error": "year and month should be integers."}), 400

    # Ensure Monday (0) is the first day of the week
    cal = calendar.TextCalendar(firstweekday=0)

    # Get weeks (each row contains 7 days, with 0 for padding)
    month_weeks = cal.monthdayscalendar(year, month)

    # Russian header for weekdays (Пн - Вс)
    header = "Пн Вт Ср Чт Пт Сб Вс"

    rows = []
    for week in month_weeks:
        week_cells = []
        for day in week:
            if day == 0:
                week_cells.append("  ")  # Two spaces for empty days
            else:
                date_str = f"{year}-{month:02d}-{day:02d}"
                cell = "✅" if date_str in activity_dates else f"{day:2d}"
                week_cells.append(cell)
        rows.append(" ".join(week_cells))

    # Construct final Telegram-friendly calendar
    calendar_text = (
        f"📅 **Календарь активностей для {year}-{month:02d}:**\n"
        f"```"
        f"\n{header}\n" + "\n".join(rows) + "```"
    )

    return Response(calendar_text, mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
