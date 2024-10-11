import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

base_url = "https://www.consumerfinance.gov/enforcement/actions/"
response = requests.get(base_url)
soup = BeautifulSoup(response.content, 'html.parser')
pagination_input = soup.find('input', id='m-pagination__current-page-0')
if pagination_input:
    max_page_number = int(pagination_input['max'])
else:
    max_page_number = 20
print("Scraping up to page", max_page_number)

page_number = 1
all_content = []
# max_page_number = 1

while page_number <= max_page_number:
    url = f"{base_url}?page={page_number}"
    print(f"Scraping {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    posts = soup.find_all(class_='o-post-preview')
    if not posts:
        break

    for post in posts:
        content = {
            "title": "",
            "link": "",
            "date": "",
            "summary": "",
            "description": "",
            "related_documents": [],
            "press_release": "",
            "case_docket": "",
            "forum": [],
            "docket_number": "",
            "initial_filing_date": "",
            "status": "",
            "products": []
        }

        content["title"] = post.find('h3', class_='o-post-preview__title').get_text(strip=True)
        content["link"] = post.find('a')['href']
        content["date"] = post.find('time')['datetime']
        content["summary"] = post.find('div', class_='o-post-preview__description').get_text(strip=True)
        content["summary"] = " ".join(content["summary"].split())

        # Navigate to the post's link
        post_url = f"https://www.consumerfinance.gov{content['link']}"
        content["link"] = post_url
        post_response = requests.get(post_url)
        post_soup = BeautifulSoup(post_response.content, 'html.parser')

        # Scrape the content from the page
        content_div = post_soup.find('div', class_='o-full-width-text-group')

        # Extract summary
        summary_paragraph = content_div.find('div', class_='m-full-width-text')
        if summary_paragraph:
            first_paragraph = summary_paragraph.find('p')
            if first_paragraph:
                content["description"] = first_paragraph.get_text(strip=True)
                content["description"] = " ".join(content["description"].split())
                
        # Extract related documents
        related_documents_section = content_div.find('h5', id='related-documents')
        if related_documents_section:
            for link in related_documents_section.find_next_siblings('p'):
                if not link.find('a'):
                    continue
                doc_link = link.find('a')['href']
                doc_text = link.find('a').get_text(strip=True)
                content["related_documents"].append({"text": doc_text, "link": doc_link})

        # Extract press release
        press_release_section = content_div.find('h5', id='press-release')
        if press_release_section:
            press_release_link = press_release_section.find_next_sibling('p').find('a')['href']
            content["press_release"] = f"https://www.consumerfinance.gov{press_release_link}"

        # Extract case docket
        case_docket_section = content_div.find('h5', id='case-docket')
        if case_docket_section:
            case_docket_link = case_docket_section.find_next_sibling('p').find('a')['href']
            content["case_docket"] = f"https://www.consumerfinance.gov{case_docket_link}"

        # Extract forum, docket number, initial filing date, status, and products from sidebar
        sidebar = post_soup.find('aside', class_='u-layout-grid__sidebar')
        if sidebar:
            metadata_items = sidebar.find_all('div', class_='m-related-metadata__item-container')
            for item in metadata_items:
                label_h3 = item.find('h3', class_='h4')
                if label_h3:
                    label = label_h3.get_text(strip=True)
                    if label == "Forum":
                        values = item.find_all('li', class_='m-list__item')
                        for value in values:
                            content["forum"].append(value.get_text(strip=True))
                    elif label == "Docket number":
                        value = item.find('p')
                        if value:
                            content["docket_number"] = value.get_text(strip=True)
                    elif label == "Initial filing date":
                        value = item.find('time')
                        if value:
                            content["initial_filing_date"] = value.get_text(strip=True)
                    elif label == "Status":
                        value = item.find('div')
                        if value:
                            content["status"] = value.get_text(strip=True)
                    elif label == "Products":
                        tag_group = item.find('ul', class_='m-tag-group')
                        if tag_group:
                            tags = tag_group.find_all('li')
                            for tag in tags:
                                tag_text = tag.find('span', class_='a-tag-topic__text')
                                if tag_text:
                                    content["products"].append(tag_text.get_text(strip=True))

        all_content.append(content)

    page_number += 1

# Print first description
#print(all_content[0]["description"])

# Print to json file
print("Writing to json file")
with open('data/enforcement_actions/cfpb_enforcement_actions.json', 'w') as f:
    json.dump(all_content, f, indent=2)

# Print to csv file
print("Writing to csv file")
df = pd.DataFrame(all_content)
df.to_csv('data/enforcement_actions/cfpb_enforcement_actions.csv', index=False)

# Loop through the content and download any related documents that are pdfs
for content in all_content:
    for doc in content["related_documents"]:
        if doc["link"].endswith('.pdf'):
            doc_response = requests.get(doc["link"])
            # Extract the filename from the link
            filename = doc["link"].split('/')[-1].replace('.pdf', '')
            print(f"Downloading {filename}.pdf")
            with open(f"data/enforcement_actions/documents/cfpb/{filename}.pdf", 'wb') as f:
                f.write(doc_response.content)