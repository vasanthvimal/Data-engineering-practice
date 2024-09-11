import requests
import os
import zipfile
urls = [
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip',
    'https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip'
]

# path = 'C:\\Users\\Vasanth\\Downloads\\pythonDownload'
path = 'downloads'

def creating_folder():
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print(f"The new folder {path} created!")

def downloading_files(urls):
    for url in urls:
        file_name = url.split("/")[-1]
        response = requests.get(url)
        status = response.status_code
        print("File Name :", file_name, " Status:", status)
        if status == 200:
            completeName = os.path.join(path, file_name)
            with open(completeName, 'wb') as file:
                file.write(response.content)
            print(completeName, " Downloaded")
            with zipfile.ZipFile(completeName,'r') as zip_file:
                zip_file.extractall(path)
                print(zip_file, " Unzip Completed")
            if os.path.exists(completeName):
                os.remove(completeName)
                print(completeName, " Zip File Removed")
            else:
                print("File Not Available")
        else:
            print("Invalid Url, skipping to next file")
    print("All process Completed Successfully !!")
def main():
    creating_folder()
    downloading_files(urls)
if __name__ == '__main__':
    main()
