![jobsearch](jobsearch.jpg)
 
# GlassDoor Entry-Level Cybersecurity Job Web Scraper

FoxtrotWebScraper is a Python scraper developed to collect job postings data from the Glassdoor API for Cyber Security jobs and exports the data to a CSV file. The jobs are filtered based on location, country (US), and entry-level seniority. The resulting data includes the job title, employer, location, job description, date posted, remote work type, and a link to the job listing.

## Set Up and Prerequisites

To begin, select your choice of platform (e.g. VirtualStudio, Google CoLab, Pycharm etc.) and open a new file. To run the particular script, you'll need to have the following Python libraries installed: 
- [requests](https://pypi.org/project/requests/) to allow the script to send HTTP requests,
- [csv](https://docs.python.org/3/library/csv.html) to write the output data in a csv file
and
- [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) to process and clean up HTML content in job descriptions.

```python
import requests
import csv
from bs4 import BeautifulSoup
```
## API Configuration

The script uses the Glassdoor Jobs Scraper API hosted on RapidAPI. You will need to sign up on RapidAPI and obtain your own API key.

Update the x-rapidapi-key in the script with your API key:
```python
headers = {
   "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
   "x-rapidapi-host": "glassdoor-jobs-scraper-api.p.rapidapi.com",
   "Content-Type": "application/json"
}
```

## Usage
1. Configure Filters
The payload allows you to specify job filters such as:

Country: Currently set to "us" (United States).
Keyword: Currently set to "Cyber Security".
Seniority Level: Currently set to "entrylevel".

You can modify these filters within the [payload](https://pypi.org/project/payload-api/) dictionary in the script.

2. Run the Script
Once the script is configured, run the code as shown below:

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

## Notes and Considerations

- Ensure your API key has sufficient credits to make the required number of requests
- Ensure you're within the API's rate limits to avoid being blocked or facing penalties. If the code is making frequent requests, consider implementing a rate limiter or using a task queue to spread out requests.
- The script currently fetches a maximum of 20 job listings per run. You can modify the [maxRows] field in the [payload] to increase or decrease this limit.
- This code relies on a RapidAPI endpoint for scraping Glassdoor jobs. Using scraping tools on websites can be against their terms of service. It's recommended to check Glassdoor's terms before running this code. There might be official APIs available for job searches.
- Regularly review and update the code to address changes in the API, website structure, or your requirements.
- Ensure that you're complying with the terms of service of the API provider and any websites you're scraping. Some websites may have restrictions on scraping or require explicit permission. Be mindful of privacy laws and regulations. Avoid collecting or storing personally identifiable information (PII) unless it's necessary and you have appropriate consent.
- Implement checks to ensure that the scraped data is consistent and accurate. For example, verify that dates are in the correct format, locations are valid, and job descriptions are not empty. If necessary, clean the scraped data to remove noise, inconsistencies, or formatting issues. This might involve tasks like removing HTML tags, correcting typos, or standardizing data formats.
- Implement try-except blocks to catch potential exceptions like network errors, API errors, or parsing issues. This will help prevent the code from crashing and allow you to handle errors gracefully.
- If you need to process a large number of jobs, consider using parallel processing or asynchronous programming to improve performance. For large datasets, consider storing the scraped data in a database for efficient querying and analysis.

## Credits

This project was worked on by Mr. Roger Barrow and Mr. Marlon Forde.



