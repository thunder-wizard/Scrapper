# **FastAPI Backend and Scraper for Collectible Items**

This project consists of a **FastAPI backend** that serves a **RESTful API** for fetching collectible items and a **scraper** that fetches item data from eBay and stores it in a MongoDB database.

## **Project Overview**

1. **Scraper**: A Python script that scrapes collectible pen data from eBay and stores it in MongoDB.
2. **FastAPI Backend**: A FastAPI-based REST API that provides endpoints to interact with the database and retrieve or update collectible items.

---

## **Requirements**

### **Backend:**

* Python >= 3.10
* FastAPI
* Uvicorn (ASGI server)
* Pymongo (for MongoDB integration)
* Python-dotenv (for environment variable management)
* CORS middleware for cross-origin requests

### **Scraper:**

* Python >= 3.10
* Requests, Scrapling (or other scraping libraries)

---

## **Installation & Setup**

### **1. Install Dependencies for Backend**

1. Create a virtual environment:

   ```bash
   python -m venv env
   ```

2. Activate the virtual environment:

   * On Windows:

     ```bash
     .\env\Scripts\activate
     ```

   * On macOS/Linux:

     ```bash
     source env/bin/activate
     ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Install the CORS middleware:

   ```bash
   pip install fastapi[all]
   ```

5. Ensure MongoDB is installed and running locally or use a cloud-based MongoDB service (e.g., MongoDB Atlas).

6. Create a `.env` file in the root directory to store environment variables like MongoDB URI, database, and collection names:

   Example `.env` file:

   ```
   MONGO_URI=mongodb://localhost:27017/
   DB_NAME=products_db
   COLLECTION_NAME=products
   ```

---

### **2. Running the Backend**

1. To start the FastAPI backend, run:

   ```bash
   uvicorn main:app --reload
   ```

2. The backend will be available at `http://127.0.0.1:8000`.

3. To test the API endpoints, you can use [Swagger UI](http://127.0.0.1:8000/docs) or [ReDoc](http://127.0.0.1:8000/redoc) for documentation and testing.

---

### **3. Install Dependencies for Scraper**

1. Install the required libraries for the scraper:

   ```bash
   pip install -r requirements.txt
   ```

2. The scraper will use **Scrapling** to fetch eBay pages and parse HTML data. It will store the scraped data in MongoDB.

---

### **4. Running the Scraper**

To run the scraper, execute the Python script:

```bash
python product-scraper.py
```

The scraper will scrape the data from eBay and insert it into MongoDB.

---

## **API Endpoints**

### **1. `GET /items`**

Fetches a list of collectible items from the MongoDB database.

**Response:**

```json
[
  {
    "id": "1",
    "name": "1925 Parker Duofold Senior Black & Gold",
    "price": "€2,850",
    "image": "pen1.jpg",
    "url": "#",
    "saved": false
  },
  ...
]
```

### **2. `PUT /items/{item_id}`**

Updates the "saved" status of an item.

**Request Body:**

```json
{
  "saved": true
}
```

**Response:**

```json
{
  "id": "1",
  "name": "1925 Parker Duofold Senior Black & Gold",
  "price": "€2,850",
  "image": "pen1.jpg",
  "url": "#",
  "saved": true
}
```

---

## **CORS Configuration**

In order to allow your React frontend (running on a different port) to access the backend, we’ve configured **CORS**.

The FastAPI backend will accept requests from `http://localhost:8080` by default. If you're running your frontend on a different domain or port, update the `allow_origins` in the backend code to allow that origin.

---

## **Development Notes**

1. **Scraper**: The scraper fetches product details from eBay, including `title`, `price`, `image`, and `link`. It stores the data in MongoDB and sets the `saved` field to `false` by default.

2. **Backend**: The FastAPI backend exposes endpoints to get all items and update the saved status. This enables the frontend to interact with MongoDB via API calls.

3. **Frontend**: In your React app, make API calls to the FastAPI backend to display items and update their saved status. Use `fetch` or any preferred HTTP client (like Axios) to interact with the backend.

---

## **Troubleshooting**

### **CORS Error**:

If you encounter CORS issues, ensure that the backend includes the correct origin in the `allow_origins` configuration in the FastAPI CORS middleware.

### **MongoDB Connection Error**:

Make sure MongoDB is running locally or use MongoDB Atlas. If using MongoDB locally, confirm that the `MONGO_URI` in the `.env` file points to the correct MongoDB instance.

### **API Error**:

If any API errors occur, check the backend logs for more information. Make sure the MongoDB collection and database exist.

---

## **Contributing**

Feel free to fork the repository and submit pull requests. Ensure that all code follows the project's coding conventions and includes necessary tests.

---

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

---
