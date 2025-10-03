from scrapling.fetchers import Fetcher, DynamicFetcher, StealthyFetcher
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

def scrape_ebay_page(query='', sort_by='newly_listed', page=1, items_per_page=60):
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
    
    query = query.replace(' ', '+')
    sort_param = sortId.get(sort_by, 16)  # Default to high_price if invalid sort
    page_data = Fetcher.get(f'{url}?_nkw={query}&_sop={sort_param}&_ipg={items_per_page}&_pgn={page}')
    
    product_list = page_data.css_first('.srp-river-results .srp-results.srp-list')
    
    if not product_list:
        print("No products found on the page.")
        return []
    
    product_cards = product_list.css('li.s-card')
    product_data_list = []
    
    for card in product_cards:
        title_el = card.css_first('.su-card-container__content .s-card__title span.primary')
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
# https://www.carousell.sg/search
def scrape_carousell_page(query='', sort_by='newly_listed'):
    """
    Scrapes the Carousell search results page and returns a list of product data dictionaries.
    
    Parameters:
    ----------
    query : str
        The search query to be used on Carousell (e.g., 'montblanc 149').
    sort_by : str
        Sorting parameter for results ('newly_listed', 'low_price', 'high_price', 'best_match', 'nearest_first').
    page : int
        The page number of search results to scrape.
    """
    url = 'https://www.carousell.sg/search'
    sortId = {
        'nearest_first': 6,
        'newly_listed': 3,
        'best_match': 1,
        'low_price': 4,
        'high_price': 5
    }
    
    query = query.replace(' ', '%20')
    sort_param = sortId.get(sort_by, 'newly_listed')  # Default to newly_listed if invalid sort
    page = StealthyFetcher.fetch(f'{url}/{query}?addRecent=true&canChangeKeyword=true&includeSuggestions=true&sort_by={sort_param}&t-search_query_source=direct_search', humanize=True, headless=False, network_idle=True)
    # page = Fetcher.get(f'https://www.carousell.sg/search/montblanc%20149?addRecent=true&canChangeKeyword=true&includeSuggestions=true&t-search_query_source=direct_search')
    product_list = page.css_first('.asm-browse-listings')  # Main container for product listings
    
    if not product_list:
        print("No products found on the page.")
        return []
    
    product_cards = product_list.css('div.D_sF.D_sZ div.D_tk')  # Each product card
    product_data_list = []
    
    for card in product_cards:
        title_el = card.css_first('div.D_tm>a.D_kW:nth-of-type(2)>p.D_le.D_lf.D_lj.D_lm.D_lp.D_lr.D_ln.D_la')
        link_el = card.css_first('div.D_tm>a.D_kW:nth-of-type(2)')
        price_el = card.css_first('div.D_tm>a.D_kW:nth-of-type(2)>.D_aOH>p.D_le.D_lf.D_lj.D_ll.D_lp.D_ls.D_kZ')
        img_el = card.css_first('div.D_tm>a.D_kW:nth-of-type(2) .D_ac_.D_acA img')
        
        title = title_el.text if title_el else ""
        link = f"https://www.carousell.sg{link_el.attrib['href']}" if link_el else ""
        price = price_el.text if price_el else ""
        imgUrl = img_el.attrib.get('src', '') if img_el else ""
        
        product_data = {
            "title": title,
            "link": link,
            "price": price,
            "image": imgUrl,
            "from": "carousell",
            "like": False  # Default like value
        }
        
        product_data_list.append(product_data)
    
    return product_data_list

def scrape_google_page(query='', sort_by='relevance', page=1, items_per_page=60):
    """
    Scrapes the Google Shopping search results page and returns a list of product data dictionaries.
    
    Parameters:
    ----------
    query : str
        The search query to be used on Google Shopping (e.g., 'montblanc 149').
    sort_by : str
        Sorting parameter for results ('relevance', 'price_low_to_high', 'price_high_to_low', etc.).
    page : int
        The page number of search results to scrape.
        """ 
    url = 'https://www.google.com/search'
    sortId = {
        'relevance': 'r',
        'price_low_to_high': 'p',
        'price_high_to_low': 'pd',
        'best_selling': 'b',
        'new_arrivals': 'n'
    }
    
    query = query.replace(' ', '+')
    sort_param = sortId.get(sort_by, 'r')  # Default to relevance if invalid sort
    start = (page - 1) * items_per_page
    page_data = Fetcher.get(f'{url}?q={query}&tbm=shop&start={start}&tbs=vw:l,ss:44,p_ord:{sort_param}')
    
    product_list = page_data.css_first('div.sh-dlr__list-result')
    
    if not product_list:
        print("No products found on the page.")
        return []
    
    product_cards = product_list.css('div.sh-dlr__list-result div.sh-dlr__content')
    product_data_list = []
    
    for card in product_cards:
        title_el = card.css_first('.sh-dlr__content .sh-dlr__title')
        link_el = card.css_first('.sh-dlr__content a.sh-dlr__title-link')
        price_el = card.css_first('.sh-dlr__content .sh-dlr__price')
        img_el = card.css_first('.sh-dlr__content img.sh-dlr__image')
        
        title = title_el.text if title_el else ""
        link = link_el.attrib['href'] if link_el else ""
        price = price_el.text if price_el else ""
        imgUrl = img_el.attrib.get('src', '') if img_el else ""
        
        product_data = {
            "title": title,
            "link": link,
            "price": price,
            "image": imgUrl,
            "from": "google",
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
        my_collection.update_one({"title": product_data["title"]}, {"$set": product_data}, upsert=True)
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
    collection.delete_many({"like": False})  # This will delete all documents in the collection
    print(f"All documents cleared from {DB_NAME}.{COLLECTION_NAME} collection.")


# Example usage
query = "montblanc 149"
clear_mongo_collection(my_collection)
# products = scrape_ebay_page(query)
products = scrape_carousell_page(query)
if products:
    push_to_mongo(products)
