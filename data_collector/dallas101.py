from bs4 import BeautifulSoup
import requests
import re
import json

session = requests.Session()


def request_handler(url:str):
    try:
        response = session.get(url)
        response.raise_for_status()
        return response.content
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None


def parse_business_details(section):
    businesses = []
    business_type = None
    for elem in section.find_all(['h2', 'h3', 'p'], recursive=False):
        if elem.name in ['h2', 'h3']:
            business_type = elem.get_text().strip()
        elif elem.name == 'p' and business_type:
            text = elem.get_text(separator='|').split('|')
            name, location = text[0].strip(), text[-1].strip()
            social_links = {a['href'] for a in elem.find_all('a', href=True)}
            business = create_business_dict(name, location, business_type, social_links)
            businesses.append(business)
    return businesses


def create_business_dict(name, location, business_type, links):
    social_media = {
        "instagram": next((link for link in links if "instagram" in link), None),
        "twitter": next((link for link in links if "twitter" in link), None),
        "facebook": next((link for link in links if "facebook" in link), None),
        "other": next((link for link in links if all(social not in link for social in ["instagram", "twitter", "facebook"])), None)
    }
    return {
        "name": name,
        "business_type": business_type,
        "black_owned": True,
        "ratings": None,
        "chill_score": None,
        "activity_type": None,
        "weekend_only": False,
        "business_url": None,
        "social_media": social_media,
        "location": {
            "location": location,
            "address": None,
            "metro": "DFW",
            "state": "Texas",
            "longitude": None,
            "latitude": None
        }
    }


def extract_businesses(html):
    soup = BeautifulSoup(html, 'html.parser')
    sections = soup.find_all('section')[2:6] 
    all_businesses = {}
    for section in sections:
        businesses = parse_business_details(section)
        for business in businesses:
            business_type = business['business_type']
            if business_type not in all_businesses:
                all_businesses[business_type] = []
            all_businesses[business_type].append(business)
    return all_businesses


def main(url:str):
    html = request_handler(url)
    if html:
        businesses = extract_businesses(html)
        with open('../DATA/dallas101_list.json', 'w') as f:
            json.dump(businesses, f, indent=4)
    else:
        print("Failed to retrieve HTML content.")


if __name__ == "__main__":
    url = 'https://www.dallasites101.com/blog/post/guide-black-owned-businesses-dallas/'
    main(url)

            
            
# out2={}
# sec2 = dom.xpath('/html/body/div[1]/div[2]/div[3]/div/div/main/div/div[2]/div/div/div/div[3]/section')[0]
# elements2 = list(sec2.iterdescendants())
# i = 0
# while i<len(elements2):
#     if elements2[i].tag == 'h2' and elements2[i].text != None:
#         type_ = elements2[i].text
#         print(elements2[i].text)
#         out2[type_] = []
#         # i+=1
#         while elements2[i+1].tag != 'h2':

#             if all([elements2[i].text!='\xa0', list(elements2[i].itertext())!=[], elements2[i].tag =='p']):
#                 print(list(elements2[i].itertext()), elements2[i].tag)
#                 name, location, *rest = elements2[i].itertext()
#                 link = elements2[i].find('a').get('href')
#                 out[type_]+=[{
#                 "name": name,
#                 "business_type": type_,
#                 "black_owned": True,
#                 "ratings": None,
#                 "chill_score": None,
#                 "activity_type": None,
#                 "weekend_only": False,
#                 "business_url": None,
#                 "social_media": {
#                     "instagram": link if "instagram" in link else None,
#                     "twitter": link if "twitter" in link else None,
#                     "facebook": link if "facebook" in link else None,
#                     "other": link,
#                 },
#                 "location": {
#                             "location": location.replace('\xa0| ', ''),
#                             "address": None,
#                             "metro": "DFW",
#                             "state": "Texas",
#                             "longitude": None,
#                             "latitude": None
#                     }
#             }]
        
#             i+=1
#     i+=1
    

# for i, elem in enumerate(sec.iterdescendants()):
#     print(f'{elem.tag} => {elem.text}')
#     if elem.find('h3') is not None:
#         type_= elem.find('h3').text
#     elif elem.find('a') is not None:
#         break
#         name = elem.find('a').text
#         link = elem.find('a').get('href')
        


# soup.find('h3')
