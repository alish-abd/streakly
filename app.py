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

    # Преобразуем список дат в множество для быстрого поиска
    activity_dates = set(data['dates'])
    
    # Опциональные параметры: year и month, если не переданы — берем текущий месяц
    try:
        year = int(data.get('year', datetime.today().year))
        month = int(data.get('month', datetime.today().month))
    except ValueError:
        return jsonify({"error": "year and month should be integers."}), 400

    # Получаем календарь месяца (каждая неделя — список из 7 чисел, 0 означает, что в эту ячейку не попадает число месяца)
    month_weeks = calendar.monthcalendar(year, month)
    
    # Заголовок с названиями дней недели (Пн - Вс)
    header = "Пн Вт Ср Чт Пт Сб Вс"

    # Формирование строк календаря:
    rows = []
    for week in month_weeks:
        week_cells = []
        for day in week:
            if day == 0:
                week_cells.append("   ")  # пустая ячейка (3 пробела для выравнивания)
            else:
                # Формируем дату в формате YYYY-MM-DD
                date_str = f"{year}-{month:02d}-{day:02d}"
                # Если дата есть в activity_dates, заменяем на эмодзи, иначе показываем номер дня
                cell = "✅" if date_str in activity_dates else f"{day:2d}"
                week_cells.append(cell)
        rows.append(" ".join(week_cells))
    
    calendar_text = f"Календарь активностей для {year}-{month:02d}:\n{header}\n" + "\n".join(rows)
    
    return Response(calendar_text, mimetype='text/plain')

if __name__ == '__main__':
    # Railway задает порт через переменную окружения PORT, иначе используем 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
