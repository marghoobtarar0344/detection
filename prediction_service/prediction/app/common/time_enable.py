from common.db_connection import db_conn
from common.sql_to_dict import mssql_result2dict
from common.exception_detections import get_error
from config.global_variables import DB_NAME
from config.global_variables import (START_HR,END_HR)
def time_eligibility(timezone,camera_id):
    try:
        from datetime import datetime
        import pytz
        utcmoment_naive = datetime.utcnow()
        utcmoment = utcmoment_naive.replace(tzinfo=pytz.utc)
        
        localDatetime = utcmoment.astimezone(pytz.timezone(timezone))
        db = db_conn()
        query = f'''
        SELECT TOP(1) * FROM [{DB_NAME}].dbo.[notification_time_configurations] 
        where start_date<=? and end_date>=? and camera_id = ? and
        ( deleted_date IS NULL OR deleted_date<? )
        '''
        db.execute(query,localDatetime,localDatetime,camera_id,localDatetime)
        results_alarm = mssql_result2dict(db)
        print('alarm result==>',results_alarm)

        if len(results_alarm):
            print(localDatetime.hour , results_alarm[0]['daily_monitor_start_time'].hour ,localDatetime.hour ,results_alarm[0]['daily_monitor_end_time'].hour)
            if localDatetime.time() <= results_alarm[0]['daily_monitor_start_time'] or localDatetime.time() >= results_alarm[0]['daily_monitor_end_time']:
                
                return False,1
            else:
                return True,0
        else:
            if localDatetime.hour <=START_HR  or localDatetime.hour >= END_HR:
                
                return False,1
            else:
                return True,0
            
                        
    except Exception as e:
        error = get_error(e)
        print('here is error',error)
        raise RuntimeError(error)
