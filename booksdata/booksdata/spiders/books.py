import scrapy
from pathlib import Path
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import datetime

# Load environment variables from .env file
load_dotenv()

# Get the MongoDB connection string from the .env file
mongo_uri = os.getenv("MONGO_URI")

# Connect to MongoDB
client = MongoClient(mongo_uri)

db = client.scrapy

def insertToDb(page, title, rating, image, price, inStock):
    collection = db[page]
    doc = {
        "title": title,
        "rating": rating,
        "image": image,
        "price": price,
        "inStock": inStock,
        "date": datetime.datetime.utcnow()
    }

    inserted = collection.insert_one(doc)
    return inserted.inserted_id


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["toscrape.com"]
    start_urls = ["https://toscrape.com"]

    def start_requests(self):
        urls = [
            "https://books.toscrape.com/catalogue/category/books/history_32/index.html",
            "https://books.toscrape.com/catalogue/category/books/poetry_23/index.html",
            "https://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"books-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")

        cards = response.css(".product_pod")
        for card in cards:
            title = card.css("h3>a::text").get()

            rating = card.css(".star-rating").attrib["class"].split(" ")[1]

            image = card.css(".image_container img")
            image = image.attrib["src"]

            price = card.css(".price_color::text").get()

            availability = card.css(".availability")
            inStock = len(availability.css(".icon-ok")) > 0

            insertToDb(page, title, rating, image, price, inStock)
