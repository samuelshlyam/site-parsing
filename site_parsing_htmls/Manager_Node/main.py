import os
import pandas as pd
import requests
import uvicorn
from sqlalchemy import create_engine,text
from fastapi import FastAPI, BackgroundTasks

pwd_value = str(os.environ.get('MSSQLS_PWD'))
pwd_str =f"Pwd={pwd_value};"
global conn
conn = "DRIVER={ODBC Driver 17 for SQL Server};Server=35.172.243.170;Database=luxurymarket_p4;Uid=luxurysitescraper;" + pwd_str
global engine
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % conn)
app = FastAPI()

@app.post("/submit_job")
async def brand_single(job_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_single_parser, job_id)

    return {"message": "Notification sent in the background"}

@app.post("/job_complete")
async def brand_batch_endpoint(job_id: str, resultUrl:str,logUrl:str,count:int,background_tasks: BackgroundTasks):
    background_tasks.add_task(update_sql_job, job_id, resultUrl, logUrl, count)

    return {"message": "Notification sent in the background"}


def update_sql_job(job_id, resultUrl, logUrl, count):
    sql = (
            f"Update utb_BrandScanJobs Set ParsingResultUrl = '{resultUrl}',\n"
            f"ParsingLogURL = '{logUrl}',\n"
            f"ParsingCount =  {count},\n"
            f" ParsingEnd = getdate()\n"
            f" Where ID = {job_id}"
           )
    if len(sql) > 0:
        ip = requests.get('https://api.ipify.org').content.decode('utf8')
        print('My public IP address is: {}'.format(ip))

        connection = engine.connect()
        sql = text(sql)
        print(sql)
        connection.execute(sql)
        connection.commit()
        connection.close()
def run_single_parser(job_id):

    df=fetch_job_details(job_id)
    brand_id = str(df.iloc[0, 0])
    source_url = df.iloc[0, 1]
    response_status = submit_job_post(job_id, brand_id, source_url)
def submit_job_post(job_id,brand_id,url):

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'job_id': f"{job_id}",
        'brand_id':f"{brand_id}",
        'scan_url':f"{url}" ,
    }

    response = requests.post(f"{os.environ.get('AGENT_BASE_URL')}/run_parser", params=params, headers=headers)
    return response.status_code
def fetch_job_details(job_id):
    update_job_status(job_id)
    sql_query = (f"Select BrandId, ResultUrl from utb_BrandScanJobs where ID = {job_id}")
    print(sql_query)
    df = pd.read_sql_query(sql_query, con=engine)
    print(df)
    engine.dispose()
    return df
def update_job_status(job_id):
    sql = (f"Update utb_BrandScanJobs\n"
           f"Set ParsingStart = getdate()\n"
           f"Where ID = {job_id}")
    if len(sql) > 0:
        ip = requests.get('https://api.ipify.org').content.decode('utf8')
        print('My public IP address is: {}'.format(ip))

        connection = engine.connect()
        sql = text(sql)
        print(sql)
        connection.execute(sql)
        connection.commit()
        connection.close()
if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, host="0.0.0.0", log_level="info")
