import requests
import csv
from bs4 import BeautifulSoup

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
