# from scrapper import *
# import time


# if __name__ == "__main__":
#     # Example usage
#     all_jobs = []
#     for city in ["Udine", "Trieste", "Pordenone", "Gorizia"]:
#         jobs = get_job_listing(city)
#         all_jobs.extend(jobs)
#         time.sleep(3)
       
       
       
from scrapper import get_jobs_with_playwright, save_jobs_to_file
import time

if __name__ == "__main__":
    all_jobs = []
    for city in ["Udine", "Trieste", "Pordenone", "Gorizia"]:
        jobs = get_jobs_with_playwright(city)
        all_jobs.extend(jobs)
        time.sleep(2)

    save_jobs_to_file(all_jobs)
