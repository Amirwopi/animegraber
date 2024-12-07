import requests
from bs4 import BeautifulSoup
import json


# Function to fetch anime data (ID, title, description) from the API
def fetch_anime_data():
    all_anime_data = []

    for page in range(1, 27):
        response = requests.get(f'https://aiofilm.com/wp-json/wp/v2/anime/?categories=39&per_page=100&page={page}')

        if response.status_code == 200:
            anime_list = response.json()

            for anime in anime_list:
                anime_id = anime['id']
                title = anime['title']['rendered']
                description = anime['content']['rendered']

                # Fetch download links for this anime
                download_links = fetch_download_links(anime_id)

                all_anime_data.append({
                    'ID': anime_id,
                    'Title': title,
                    'Description': description,
                    'Download Links': download_links
                })
        else:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")

    return all_anime_data


# Function to fetch download links from a specific anime page
def fetch_download_links(anime_id):
    response = requests.get(f'https://aiofilm.com/?p={anime_id}')
    download_links = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all download items in the page
        dlitems = soup.find_all('li', class_='dlitems')

        for item in dlitems:
            # Check if the quality and link exist
            quality_span = item.find('span', class_='font-bold')
            link_a = item.find('a', href=True)

            if quality_span and link_a:
                quality = quality_span.text.strip()
                url = link_a['href']

                download_links.append({
                    'Quality': quality,
                    'URL': url
                })
    else:
        print(f"Failed to retrieve download links for anime ID {anime_id}. Status code: {response.status_code}")

    return download_links


# Function to save the collected data to a JSON file
def save_data_to_json(data):
    with open('download_links.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Data has been saved to download_links.json")


# Main script execution
if __name__ == "__main__":
    anime_data = fetch_anime_data()  # Fetch anime data from API
    save_data_to_json(anime_data)  # Save data to JSON file
