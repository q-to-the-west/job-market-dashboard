from bs4 import BeautifulSoup
import requests
import json

def extract(website):
    try:
        # Fetching the URL and transforming it into text
        html_text = requests.get(website).text

        # Parse the HTML
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup
    except requests.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def find_jobs(soup):
    if soup is None:
        return {}

    # Get the class col-md-11
    job_cards = soup.find_all("div", class_="col-md-11")

    # Create a dictionary
    jobs_dict = {}

    # Extract job details
    for job_element in job_cards:
        title_element = job_element.find(class_="no-margin-top")
        company_element = job_element.find(class_="color-black")
        location_element = job_element.find("span", class_="color-white-mute")
        description_element = job_element.find("p")

        # Ensure that all elements are found
        if title_element and company_element and location_element and description_element:
            title = title_element.get_text().strip()
            company = company_element.get_text().strip()
            location = location_element.get_text().strip()
            description = description_element.get_text().strip()

            jobs_dict[title] = {
                "company": company,
                "location": location,
                "description": description
            }

    return jobs_dict

def display_jobs(jobs_dict):
    # Loop through the dictionary
    for title, details in jobs_dict.items():
        company = details['company']
        location = details['location']
        description = details['description']

        # Display jobs
        print(f"Company: {company}")
        print(f"Title: {title}")
        print(f"Location: {location}")
        print(f"Description: {description}\n")

def save(filename, data):
    # Save to a file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    print(f"Data saved successfully to {filename}")

def load(filename):
    try:
        # Load the file
        with open(filename, 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return None

def main():
    url = "https://www.remotepython.com/jobs/?q=Python"

    # Step 1: Extract the HTML content from the URL
    soup = extract(url)

    # Step 2: Parse and find relevant job information
    jobs = find_jobs(soup)

    if jobs:
        # Step 3: Save the parsed job data to a JSON file
        save("jobs.txt", jobs)

        # Step 4: Load the saved job data from the file
        jobs_dict = load("jobs.txt")

        if jobs_dict:
            # Step 5: Display the job data
            display_jobs(jobs_dict)
        else:
            print("Failed to load job data.")
    else:
        print("No jobs found.")


if __name__ == "__main__":
    main()
