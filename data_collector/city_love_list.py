from bs4 import BeautifulSoup
import requests
import json

session = requests.Session()

def request_handler(url:str):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.content
    except requests.HTTPError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.reason}")
    except requests.RequestException as e:
        print(f"Error: {e}")
    return None

def extract_businesses(soup):
    businesses_dict = {}
    headers = soup.find_all('h2')
    for i in range(len(headers)-1):
        header = headers[i]
        business_type_span = header.find("span", {"style": "color:#F442F8"})
        if business_type_span:
            business_type = business_type_span.text
            businesses_dict[business_type] = []

            i += 1
            while i < len(headers) and not headers[i].find("span", {"style": "color:#F442F8"}):
                current_header = headers[i]
                if not current_header.text:
                    i += 1
                    continue

                link_element = current_header.find("a")
                link = link_element['href'] if link_element else None
                name = current_header.text
                location_text = extract_location(current_header, headers, i)
                
                businesses_dict[business_type].append(create_business_entry(name, business_type, link, location_text))
                i += 1
    return businesses_dict

def extract_location(current_header, headers, index):
    parent_text = current_header.parent.text
    next_header_text = headers[index + 1].text if index + 1 < len(headers) else ""
    location = parent_text.split(current_header.text)[1].split(next_header_text)[0]
    return location

def create_business_entry(name, business_type, link, location_text):
    social_media = {
        "instagram": link if link and "instagram" in link else None,
        "twitter": link if link and "twitter" in link else None,
        "facebook": link if link and "facebook" in link else None,
        "other": link,
    }
    return {
        "name": name,
        "business_type": business_type,
        "black_owned": True,
        "ratings": None,
        "chill_score": None,
        "activity_type": None,
        "weekend_only": False,
        "business_url": link,
        "social_media": social_media,
        "location": {
            "location_raw": location_text.strip(),
            "location_raw2": parent.split(head.text)[1].split( headers[i + 1].text or headers[i + 2].text )[0],
            "address": None,
            "metro": "DFW",
            "state": "Texas",
            "longitude": None,
            "latitude": None,
        },
    }

def main(url:str):
    html_content = request_handler(url)
    if html_content:
        soup = BeautifulSoup(html_content, 'lxml')
        businesses = extract_businesses(soup)
        with open('../DATA/locations.json', 'w') as file:
            json.dump(businesses, file, indent=4)
    else:
        print("Failed to retrieve or parse HTML content.")

if __name__ == "__main__":
    url = 'https://www.citylovelist.com/post/100-black-owned-businesses-to-support-around-dfw-this-black-history-month-and-beyond'
    main(url)
