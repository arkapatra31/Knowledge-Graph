import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load the JSON file
with open("data/products.json", "r") as f:
    products = json.load(f)

# Initialize a text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Size per chunk
    chunk_overlap=50  # Overlap for context
)

# Prepare chunks for each product
def create_product_chunks(product):
    text = f"""
    Name: {product['name']}
    Brand: {product['brand']}
    Category: {product['category']}
    Price: {product['price']}
    Description: {product['description']}
    """
    return text_splitter.split_text(text)

# Create chunks for all products
json_chunks = []
for product in products:
    json_chunks.append({
        "id": product["id"],
        "chunks": create_product_chunks(product)
    })

__all__ = [json_chunks]
