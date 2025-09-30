from scrapling.fetchers import Fetcher
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# MongoDB setup using environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

my_mongo_client = MongoClient(MONGO_URI)
my_db = my_mongo_client[DB_NAME]
my_collection = my_db[COLLECTION_NAME]

def scrape_ebay_page(query='', sort_by='high_price', page=1, items_per_page=60):
    """
    Scrapes the eBay search results page and returns a list of product data dictionaries.
    
    Parameters:
    ----------
    query : str
        The search query to be used on eBay (e.g., 'montblanc+149').
    sort_by : str
        Sorting parameter for results ('high_price', 'low_price', etc.).
    page : int
        The page number of search results to scrape.
    items_per_page : int
        Number of items to retrieve per page (60, 120, or 240).
    
    Returns:
    -------
    list
        A list of dictionaries containing product data (title, link, price, image).
    """
    url = 'https://www.ebay.com/sch/i.html'
    sortId = {
        'ending_soonest': 1,
        'nearest_first': 7,
        'newly_listed': 10,
        'best_match': 12,
        'low_price': 15,
        'high_price': 16
    }
    
    sort_param = sortId.get(sort_by, 16)  # Default to high_price if invalid sort
    page = Fetcher.get(f'{url}?_nkw={query}&_sop={sort_param}&_ipg={items_per_page}&_pgn={page}')
    
    productList = page.css_first('.srp-river-results .srp-results.srp-list')
    
    if not productList:
        print("No products found on the page.")
        return []
    
    productCards = productList.css('li.s-card')
    product_data_list = []
    
    for card in productCards:
        title_el = card.css_first('.su-card-container__content .s-card__title span')
        link_el = card.css_first('.su-card-container__content a.su-link')
        price_el = card.css_first('.su-card-container__content .s-card__price')
        img_el = card.css_first('.su-media img.s-card__image')
        
        title = title_el.text if title_el else ""
        link = link_el.attrib['href'] if link_el else ""
        price = price_el.text if price_el else ""
        imgUrl = img_el.attrib.get('src', '') if img_el else ""
        
        product_data = {
            "title": title,
            "link": link,
            "price": price,
            "image": imgUrl,
            "from": "ebay",
            "like": False  # Default like value
        }
        
        product_data_list.append(product_data)
    
    return product_data_list


def push_to_mongo(products):
    """
    Pushes the scraped product data to MongoDB.
    
    Parameters:
    ----------
    products : list
        A list of dictionaries containing product data.
    
    Returns:
    -------
    None
    """
    for product_data in products:
        # Insert into MongoDB, update if the product already exists (based on 'link')
        my_collection.update_one({"link": product_data["link"]}, {"$set": product_data}, upsert=True)
        print(f'Inserted/Updated: {product_data["title"]}')

def clear_mongo_collection(collection):
    """
    Clears all documents from the MongoDB collection.
    
    This function deletes all the entries in the 'products' collection,
    effectively clearing the entire collection.
    
    Returns:
    -------
    None
    """
    collection.delete_many({})  # This will delete all documents in the collection
    print(f"All documents cleared from {DB_NAME}.{COLLECTION_NAME} collection.")


# Example usage
query = "montblanc+149"
products = scrape_ebay_page(query)
if products:
    push_to_mongo(products)
