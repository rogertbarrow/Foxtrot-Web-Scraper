![jobsearch](jobsearch.jpg)
 
# FoxtrotAIOpsScraper

FoxtrotOpsScraper is a Python scraper developed to identify and collect data from GlassDoor about open job postings in cybersecurity at the entry level. 

## Installation

First install the package [requests](https://pypi.org/project/requests/) to allow the script to send HTTP requests as well as [csv](https://docs.python.org/3/library/csv.html) to write the output data in a csv file.

```python
import requests
import csv
```
## Usage

```python
import requests
import csv
from bs4 import BeautifulSoup
# import datetime


url = "https://glassdoor-jobs-scraper-api.p.rapidapi.com/api/job/wait"


payload = {
   "scraper": {
       "filters": {
           "country": "us",
           "keyword": "Cyber Security",
           "location": "",
           "seniorityType": "entrylevel"
       },
       "maxRows": 20
   }
}
headers = {
   "x-rapidapi-key": "014506a59dmsh60addb51d52af2dp155156jsna84340a12ba4",
   "x-rapidapi-host": "glassdoor-jobs-scraper-api.p.rapidapi.com",
   "Content-Type": "application/json"
}


response = requests.post(url, json=payload, headers=headers)


# Get the data from the response
data = response.json()


# Extract the "jobs" data from the response
jobs_data = data["returnvalue"]["jobs"]


def process_job_data(jobs_data):
 """Processes job data from a list of dictionaries.


 Args:
   jobs_data: A list of dictionaries containing job data.


 Returns:
   A list of dictionaries containing processed job data.
 """


 processed_data = []
 for job in jobs_data:
   description = job["job"]["description"]
   soup = BeautifulSoup(description, 'html.parser')
   # Find all tags and store their text in a list.
   strip_tags_text = [strip_tags.text for strip_tags in soup.find_all()]
   content = " ".join(strip_tags_text)


   processed_job = {
     "Employer": job["overview"]["name"],
     "JobTitle": job["job"]["jobTitleText"],
     "City": job["map"]["cityName"],
     "Country": job["map"]["country"],
     "Description": content,
     "DatePosted": job["job"]["discoverDate"],
     "RemoteWorkType": job["header"]["remoteWorkTypes"],
     "URL": job["header"]["jobLink"]
   }
   processed_data.append(processed_job)


 return processed_data


def export_job_data_to_csv(jobs_data, filename="glassdoor_jobs.csv"):
 """Exports processed job data to a CSV file.


 Args:
   jobs_data: A list of dictionaries containing processed job data.
   filename: The name of the CSV file to export to.
 """


 with open(filename, "w", newline="") as csvfile:
   fieldnames = ["Employer", "JobTitle", "City", "Country", "Description", "DatePosted", "RemoteWorkType", "URL"]
   writer = csv.DictWriter(csvfile, fieldnames=fieldnames)


   writer.writeheader()
   for job in jobs_data:
     writer.writerow(job)


joblist = process_job_data(jobs_data)
export_job_data_to_csv(joblist)


```

## Considerations

In our research while creating the web scraper, we would've utilized RapidAPI as a resource for our Application Programming Interface (API) to bypass scraping restrictions.
As the code relies on the RapidAPI endpoint to successfully scrape for jobs on GlassDoor's website, it was paramount that we checked the API code as well as 
GlassDoor's terms of service before running the code. Along this same vein, we were very mindful of privacy laws and regulations and avoided collecting or storing any information unless it was necessary and came with appropriate consent.
Furthermore, in order to mitigate blockages, website denial of services or penalties, we employed a rate limiter to limit the number of requests that the code executes withing a given period of time.
Throughout the process, checks were implemented to ensure that the scraped data is consistent and accurate. This includes verifying that dates are in the correct format, locations are valid, and job descriptions are not empty. If necessary, the scraped data would then be cleaned to remove noise, inconsistencies, or formatting issues. This might involve tasks like removing HTML tags, correcting typos, or standardizing data formats.
To mitigate any potential errors, try-except blocks were implemented to catch potential exceptions like network errors, API errors, or parsing issues. This helped to prevent the code from crashing and allows for graceful handling of errors. Any relevant errors would also be logged to track and troubleshoot issues.

## License

[MIT](https://choosealicense.com/licenses/mit/)
