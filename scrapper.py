import requests
# from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import time


# #We first set the headers to mimic a browser request

# # HEADERS = {
# #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
# #     'Accept-Language': 'en-US,en;q=0.9',
# #     'Accept-Encoding': 'gzip, deflate, br',
# #     'Connection': 'keep-alive'
# # }

# HEADERS = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
#         'Accept-Language': 'en-US,en;q=0.9',
#         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
#         'Referer': 'https://www.google.com/'
#     }



# #Set the base url for the website we want to scrape
# BASE_URL = 'https://it.indeed.com/jobs'




# #Function to scrape job listings from a given page

# def get_job_listing(city, keywrod="studente"):
    
#     print(f"Scraping jobs for '{keywrod}' in '{city}'...")
#     params = {
#         'q': keywrod,
#         'l': city,
#         # 'start': 'date'
#     }
    
#     session = requests.Session()
    
#     response = session.get(BASE_URL, headers=HEADERS, params=params)
    
#     # Check if the request was successful
#     if response.status_code != 200:
#         print(f"❌ Failed to retrieve data: {response.status_code}")
#         print("🔍 Response Headers:", response.headers)
#         print("🔍 Response Text (first 300 chars):", response.text[:300])
#         return []

#     soup = BeautifulSoup(response.text, 'html.parser')
#     job_cards = soup.find_all('div', class_='job_seen_beacon')

        
#     jobs = [
#             {
#                 'title': card.find('h2', class_='jobTitle').get_text(strip=True),
#                 'company': card.find('span', class_='companyName').get_text(strip=True),
#                 'location': card.find('div', class_='companyLocation').get_text(strip=True),
#                 'link': f"https://it.indeed.com{card.find('a')['href']}",
#                 'source': 'Indeed'
#             }
#             for card in job_cards
#             if card.find('h2', class_='jobTitle')
#         ]
    
#     return jobs

# # Function to save jobs to a JSON file
# def save_jobs_to_json(jobs, filename='data/jobs.json'):
#     with open(filename, 'w', encoding='utf-8') as f:
#         json.dump(jobs, f, ensure_ascii=False, indent=2)
#         print(f"Jobs saved to {len(jobs)} jobs to {filename}")

# ...existing code...



# ...existing code...
    
    
    
    
    # ...existing code...

# def get_jobs_for_types(city, job_types):
#     """
#     Scrape jobs for multiple job types in a given city.
#     """
#     all_jobs = []
#     for job_type in job_types:
#         print(f"Scraping jobs for '{job_type}' in '{city}'...")
#         params = {
#             'q': job_type,
#             'l': city
#         }
#         response = requests.get(BASE_URL, headers=HEADERS, params=params)
#         if response.status_code != 200:
#             print(f"Failed to retrieve data for {job_type}: {response.status_code}")
#             continue

#         soup = BeautifulSoup(response.text, 'html.parser')
#         job_cards = soup.find_all('div', class_='job_seen_beacon')

#         for card in job_cards:
#             title = card.find('h2', class_='jobTitle').get_text(strip=True)
#             company = card.find('span', class_='companyName').get_text(strip=True)
#             location = card.find('div', class_='companyLocation').get_text(strip=True)
#             link = card.find('a')['href']
#             all_jobs.append({
#                 'title': title,
#                 'company': company,
#                 'location': location,
#                 'link': f"https://it.indeed.com{link}",
#                 'type': job_type
#             })
#     return all_jobs

# # Example usage:
# job_types = ["part-time", "information technology", "restaurant", "hotel", "flexible"]
# jobs = get_jobs_for_types("Udine", job_types)
# print(jobs)

# ...existing code...




    # jobs = []
    
    # for card in job_cards:
    #     title = card.find('h2', class_='jobTitle').get_text(strip=True)
    #     company = card.find('span', class_='companyName').get_text(strip=True)
    #     location = card.find('div', class_='companyLocation').get_text(strip=True)
    #     link = card.find('a')['href']
        
    #     jobs.append({
    #         'title': title,
    #         'company': company,
    #         'location': location,
    #         'link': f"https://it.indeed.com{link}"
    #     })
    
    
    
    

def get_jobs_with_playwright(city, keyword="studente"):
    jobs = []
    print(f"Scraping with Playwright: '{keyword}' in {city}")

    url = f"https://it.indeed.com/jobs?q={keyword}&l={city}&sort=date"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)  # wait for content to load

        job_cards = page.locator(".job_seen_beacon")
        count = job_cards.count()

        for i in range(count):
            card = job_cards.nth(i)
            title = card.locator("h2.jobTitle").inner_text()
            company = card.locator("span.companyName").inner_text()
            location = card.locator("div.companyLocation").inner_text()
            link = card.locator("a").get_attribute("href")

            jobs.append({
                "title": title.strip(),
                "company": company.strip(),
                "location": location.strip(),
                "link": f"https://it.indeed.com{link}",
                "source": "Indeed"
            })

        browser.close()

    return jobs

def save_jobs_to_file(jobs, filename="jobs.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(jobs)} jobs to {filename}")
