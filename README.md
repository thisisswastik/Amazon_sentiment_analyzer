📊 Amazon Product Sentiment Analyzer
🚀 Analyze Amazon product reviews and get recommendations based on sentiment analysis!

🔹 Features
✅ Single Product Analysis – Fetches reviews and provides sentiment insights for one product.
✅ Multi-Product Comparison – Compare up to 5 Amazon products based on sentiment and estimated ratings.
✅ Fake Review Detection – (Planned Feature) Identifies potential fake or biased reviews.
✅ Price Tracking (Coming Soon) – Analyzes sentiment trends with price changes.


📂 Project Structure
📦 Amazon-Product-Sentiment-Analyzer  
 ├── 📜 scraper.py           # Scrapes Amazon reviews and performs sentiment analysis  
 ├── 📜 app.py               # Streamlit frontend for the tool  
 ├── 📜 requirements.txt     # All necessary dependencies  
 ├── 📜 README.md            # Project documentation  
 ├── 📜 .gitignore           # Ignore unnecessary files  


🚀 Setup Instructions
🔹 1. Clone the Repository
```bash
git clone https://github.com/yourusername/Amazon-Product-Sentiment-Analyzer.git
cd Amazon-Product-Sentiment-Analyzer
```
🔹 2. Install Dependencies
```bash
pip install -r requirements.txt
```
🔹 3. Run the Streamlit App
```bash
streamlit run app.py
```
🛠 How It Works?
1️⃣ Enter an Amazon product URL or up to 5 product URLs.
2️⃣ The scraper fetches reviews, cleans data, and analyzes sentiment.
3️⃣ Displays sentiment scores, estimated ratings, and a recommendation.
4️⃣ Recommends the best product based on positive reviews and rating.

📌 Example Output
🔍 Product: XYZ Phone  
✅ Positive Reviews: 87.3%  
⚠️ Negative Reviews: 12.7%  
⭐ Estimated Rating: 4.5/5  
🛒 Recommendation: Strongly Recommended!  
