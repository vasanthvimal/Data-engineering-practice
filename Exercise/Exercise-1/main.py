import asyncio
import time
import os
import aiohttp
import zipfile
from concurrent.futures import ThreadPoolExecutor

start = time.perf_counter()

urls = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]

#path = 'C:\\Users\\Vasanth\\Downloads\\pythonDownload\\combined'
path = 'downloads'
def creating_folder():
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"The new folder {path} created!")

def extract_and_remove_zip(file_path):
    try:
        with open(file_path, 'rb') as file:
            zipfile.ZipFile(file).extractall(path=path)
            print(file_path, " Unzip Completed")
        os.remove(file_path)
        print(file_path, " Zip File Removed")
    except Exception as e:
        print(f"Error extracting or removing {file_path}: {e}")

async def downloading_files(session, url, executor):
    file_name = url.split("/")[-1]
    print(f"Downloading {url}")
    
    async with session.get(url) as response:
        print("File Name :", file_name, " Status:", response.status)
        if response.status == 200:
            complete_name = os.path.join(path, file_name)
            with open(complete_name, 'wb') as f:
                f.write(await response.read())  
            print(complete_name, " Downloaded")
           
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(executor, extract_and_remove_zip, complete_name)
        else:
            print(f"Invalid URL: {url}, skipping to next file")



async def main():
    creating_folder()
    executor = ThreadPoolExecutor(max_workers=5)  
    async with aiohttp.ClientSession() as session:
        tasks = [downloading_files(session, url, executor) for url in urls]
        await asyncio.gather(*tasks,return_exceptions=True)

asyncio.run(main())

print(f"Total time: {time.perf_counter() - start}")