import os
import requests
import uvicorn
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from fastapi import FastAPI, BackgroundTasks
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv
import json
from requests.adapters import HTTPAdapter
from sqlalchemy import create_engine,text
from urllib3.util.retry import Retry
import pandas as pd
import datetime

load_dotenv()
pwd_value = str(os.environ.get('MSSQLS_PWD'))
pwd_str =f"Pwd={pwd_value};"
global conn
conn = "DRIVER={ODBC Driver 17 for SQL Server};Server=35.172.243.170;Database=luxurymarket_p4;Uid=luxurysitescraper;" + pwd_str
global engine
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % conn)
app = FastAPI()

@app.post("/submit_job")
async def brand_single(job_id: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_single_api, job_id)

    return {"message": "Notification sent in the background"}
def run_single_api(job_id):

    df=fetch_job_details(job_id)
    brand_id = str(df.iloc[0, 0])
    response_status = submit_job_post(job_id, brand_id)
def submit_job_post(job_id,brand_id):

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = {
        'job_id': f"{job_id}",
        'brand_id':f"{brand_id}"
    }

    response = requests.post(f"{os.environ.get('AGENT_BASE_URL')}/run_parser", params=params, headers=headers)
    return response.status_code
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
def fetch_job_details(job_id):
    update_job_status(job_id)
    sql_query = (f"Select BrandId, ResultUrl from utb_BrandScanJobs where ID = {job_id}")
    print(sql_query)
    df = pd.read_sql_query(sql_query, con=engine)
    print(df)
    engine.dispose()
    return df



if __name__ == "__main__":
    uvicorn.run("api:app", port=8006, log_level="info")