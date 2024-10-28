# 💰 One Piece Card Price Watcher API 🏴‍☠️

![One Piece Image](https://github.com/GomuGomuu/card-price-watcher/assets/42194516/14b8554f-40a2-45b1-8738-023625a7b199)

Ahoy there, fellow pirates! Ever wanted to keep track of those elusive One Piece card prices without breaking a sweat? Look no further! This API is here to help you conquer the Grand Line of card collecting!

## Features:

- **Automated Price Tracking:**  Effortlessly retrieves card prices from [Liga One Piece](https://www.ligaonepiece.com.br/). 
- **Fast and Efficient:**  Utilizes Selenium for website navigation and OCR (Optical Character Recognition) for accurate price extraction.
- **Caching Magic:**  Leverages Redis for caching, ensuring snappy response times and reducing unnecessary requests.
- **Dockerized for Your Convenience:**  Sail smoothly with the power of Docker for easy setup and deployment.
- **Friendly API:**  Simple and intuitive API design for seamless integration into your projects.

## Getting Started:

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/card-price-watcher.git
   ```

2. **Set Sail with Docker:**

   ```bash
   docker-compose up -d
   ```

3. **Make a Request:**

   Send a POST request to `http://localhost:5000/get_price` with a JSON payload like this:

   ```json
   {
       "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Roronoa+Zoro+%28OP01-001-PAR%29&ed=OP-01&num=OP01-001-PAR",
       "card_name": "Roronoa Zoro (OP01-001-PAR)"
   }
   ```

   And you'll receive a JSON response with the current price!

## Example Usage:

```python
import requests

url = "http://localhost:5000/get_price"
payload = {
    "url": "https://www.ligaonepiece.com.br/?view=cards/card&card=Roronoa+Zoro+%28OP01-001-PAR%29&ed=OP-01&num=OP01-001-PAR",
    "card_name": "Roronoa Zoro (OP01-001-PAR)"
}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    data = response.json()
    print("Price:", data['price'])
    print("Card Name:", data['card_name'])
else:
    print("Error:", response.text)
```

## Configuration:

Customize your treasure map! Fine-tune the settings in the `.env` file:

- `REDIS_PORT_HOST`, `REDIS_PORT`, `REDIS_DB`: Configure Redis connection.
- `DEBUG`: Set to `true` for debugging.
- `SELENIUM_HOST`:  Keep it as `selenium` when using Docker.
- `OCR_PATH`: Path to Tesseract OCR executable. Example for Linux: `/usr/bin/tesseract`. For Windows: `C:\Program Files\Tesseract-OCR\tesseract` (requires Tesseract installation).

## Dependencies:

All the necessary tools for this adventure are listed in `requirements.txt`. Install them using:

```bash
pip install -r requirements.txt
```

## Future Enhancements:

- **Multilingual Support:**  Adding the ability to extract prices in different currencies and languages.
- **Webhooks:**  Implement webhooks to notify you of price changes in real-time. 

## Contributions:

Want to join the crew? We welcome contributions! Feel free to submit pull requests for new features, bug fixes, or improvements. 

Set sail on your One Piece card collecting journey with ease! Happy Hunting! 
