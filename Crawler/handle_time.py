import database

def parse_time(time_str):
    time_str = time_str.strip()
    new_time = None
    if time_str.startswith("(") and time_str.endswith(")"):
        time_array = time_str[1:-1].split(",")
        month_day = time_array[0].strip().split(" ")
        year = time_array[1].strip()
        month = month_day[0]
        day = month_day[1]
        new_time = year + "-" + parse_month(month) + "-" + day
    elif '-' in time_str:
        time_array = time_str.split("-")
        year = time_array[0].strip()
        month = time_array[1].strip()
        day = time_array[2].strip()
        new_time = year + "-" + parse_month(month) + "-" + day
    elif '.' in time_str:
        time_str = time_str.split(".")[0]
        year = time_str[:4]
        month = time_str[4:6]
        day = time_str[6:]
        new_time = year + "-" + month + "-" + day
    print(new_time)
    return new_time

def parse_month(month):
    return {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12',
    }.get(month, None)

def update_all_date():
    values = []
    db = database.connectdb()
    cursor = db.cursor()
    sql = "SELECT id,date FROM library_versions where parsed_date is null"
    query_result = database.querydb(db, sql)
    for entry in query_result:
        id = entry[0]
        date = entry[1]
        new_date = parse_time(date)
        if new_date is not None:
            print(str(id) + " : " + new_date)
            values.append((id, new_date))
        if len(values) == 5000:
            cursor.executemany(
                'INSERT INTO library_versions (id,parsed_date) value (%s,%s) on duplicate key update parsed_date = values(parsed_date)',
                values)
            db.commit()
            values = []
        # break
    cursor.executemany(
        'INSERT INTO library_versions (id,parsed_date) value (%s,%s) on duplicate key update parsed_date = values(parsed_date)',
        values)
    db.commit()

# parse_time("(Nov 08, 2005) ")
# parse_time("20170419.022402")
update_all_date()
# 20170419.022402
