import os
import database

def collect_update_entry():
    db = database.connectdb()
    sql = "SELECT id,project_id,prev_commit,curr_commit,prev_type_id,curr_type_id FROM lib_update WHERE prev_type_id is not null and curr_type_id is not null"
    query_result = database.querydb(db, sql)
    for entry in query_result:
        print(entry)

collect_update_entry()