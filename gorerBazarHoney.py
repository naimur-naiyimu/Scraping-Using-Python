from bs4 import BeautifulSoup
import requests
import pandas as pd

url = "https://ghorerbazarbd.com/new/product-category/honey-%e0%a6%ae%e0%a6%a7%e0%a7%81/"
response = requests.get(url)

if response.status_code == 200:
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    product_links = soup.find_all('h3', class_='wd-entities-title')
    product_name = []
    product_weight = []
    product_price = []
    product_sold_out = []

    for product in soup.find_all('div', class_='product-grid-item'):
        # Extract product name
        product_name.append(product.find('h3', class_='wd-entities-title').text)

        # Extract product weight
        product_weight.append(product.find('div', class_='wd-product-brands-links').text)

        # Extract product price
        price_text = product.find('span', class_='price').text
        cleaned_price = '৳' + price_text.replace('৳', '').replace(',', '').replace('\xa0', '')
        product_price.append(cleaned_price)

        # Check if the product is sold out
        try:
            is_sold_out = "Sold out" in product.find('div', class_='product-labels').text
        except AttributeError:
            is_sold_out = False

        product_sold_out.append(is_sold_out)

else:
    print("Failed to retrieve the webpage.")

# Create a DataFrame with the extracted data
data = {'Product Name': product_name, 'Product Weight': product_weight, 'Product Price': product_price, 'Sold Out': product_sold_out}
df = pd.DataFrame(data)

# Now df contains the product details, including whether they are sold out or not
print(df)

# Save the DataFrame to a CSV file
df.to_csv('gorerBazarHoney.csv', index=False)
