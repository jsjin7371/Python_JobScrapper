from bs4 import BeautifulSoup
from requests import get


def extract_wwr_jobs(keyword):
  base_url = "https://weworkremotely.com/remote-jobs/search?term="

  response = get(f"{base_url}{keyword}")
  results = []

  if response.status_code != 200:
    print("Can't request website")

  else:

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = soup.find_all('section', class_="jobs")

    for job_section in jobs:
      job_posts = job_section.find_all('li')
      job_posts.pop(-1)

      for post in job_posts:
        anchors = post.find_all('a')
        anchor = anchors[1]

        anchor['href']

        company, kind, location = anchor.find_all('span', class_="company")

        position = anchor.find('span', class_="title")
        link = anchor['href']

        if company:
          company = company.string.strip()
        if position:
          position = position.string.strip()
        if location:
          location = location.string.strip()
        if link:
          link = f"https://weworkremotely.com{link}"
        if company and position and location and link:
          job = {
              'company': company,
              'position': position,
              'location': location,
              'link': link
          }
          results.append(job)

  return results
