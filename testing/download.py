import requests

url = "https://occ.gov/static/enforcement-actions/eaAA-ENF-2024-77.pdf"
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

response = requests.get(url, headers=headers)
print(response.status_code)