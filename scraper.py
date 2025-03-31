import requests
import time
import nltk
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
from flair.models import TextClassifier
from flair.data import Sentence

# Initialize sentiment analyzers
nltk.download("vader_lexicon")
sia = SentimentIntensityAnalyzer()
flair_classifier = TextClassifier.load("en-sentiment")


# User-Agent header to avoid Amazon blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

# Function to scrape reviews for a single product
def scrape_reviews(amazon_url):
    print(f"\n🔍 Fetching reviews from: {amazon_url}")
    try:
        response = requests.get(amazon_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            print(f"⚠️ Failed to fetch page. Status code: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "lxml")
        review_elements = soup.find_all("span", {"data-hook": "review-body"})

        reviews = [review.text.strip() for review in review_elements]
        
        if not reviews:
            print("⚠️ No reviews found. Amazon might be blocking the request.")
        return reviews

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error fetching reviews: {e}")
        return []

# Sentiment Analysis Functions
def analyze_vader(text):
    return sia.polarity_scores(text)["compound"]

def analyze_flair(text):
    sentence = Sentence(text)
    flair_classifier.predict(sentence)
    label = sentence.labels[0]
    return label.score if "POSITIVE" in str(label) else -label.score

# Combined sentiment function
def ensemble_sentiment(text):
    vader_score = analyze_vader(text)
    flair_score = analyze_flair(text)
    final_score = (vader_score + flair_score) / 2

    if final_score > 0.05:
        return "Positive"
    elif final_score < -0.05:
        return "Negative"
    else:
        return "Neutral"

# Function to analyze a single product
def analyze_product(url):
    reviews = scrape_reviews(url)
    if not reviews:
        print("❌ No reviews found for this product. Skipping analysis.")
        return None

    sentiments = {"positive": 0, "negative": 0, "neutral": 0}
    
    for review in reviews:
        sentiment = ensemble_sentiment(review)
        sentiments[sentiment.lower()] += 1

    total_reviews = sum(sentiments.values())
    if total_reviews == 0:
        print("❌ No valid reviews for sentiment analysis. Skipping.")
        return None

    # Calculate sentiment percentages
    positive_ratio = (sentiments["positive"] / total_reviews) * 100
    negative_ratio = (sentiments["negative"] / total_reviews) * 100

    # Corrected rating calculation (scales between 1 and 5)
    avg_rating = round(1 + (positive_ratio / 100) * 4, 1)

    # Recommendation based on positive vs. negative sentiment
    if positive_ratio > 70:
        recommendation = "✅ **Highly Recommended! Buy it!**"
    elif positive_ratio > 50:
        recommendation = "👍 **Good product. Consider buying!**"
    elif positive_ratio > 30:
        recommendation = "⚠️ **Mixed reviews. Buy with caution!**"
    else:
        recommendation = "❌ **Not recommended. Avoid this product!**"

    print(f"\n📊 **Sentiment Analysis for {url}:**")
    print(f"✅ Positive: {positive_ratio:.2f}%")
    print(f"⚠️ Negative: {negative_ratio:.2f}%")
    print(f"⭐ Estimated Rating: {avg_rating}/5")
    print(f"🛒 **Recommendation:** {recommendation}")

    return {
        "url": url,
        "positive": positive_ratio,
        "negative": negative_ratio,
        "average_rating": avg_rating,
        "recommendation": recommendation
    }

# Function to compare multiple products
def compare_products():
    print("\n🔹 **Amazon Product Comparator**")
    
    # Taking 5 fixed product URLs as input
    url1 = input("Enter Amazon product URL 1: ").strip()
    url2 = input("Enter Amazon product URL 2: ").strip()
    url3 = input("Enter Amazon product URL 3: ").strip()
    url4 = input("Enter Amazon product URL 4: ").strip()
    url5 = input("Enter Amazon product URL 5: ").strip()

    product_urls = [url1, url2, url3, url4, url5]

    product_results = []
    
    for url in product_urls:
        if url:  # Ensure URL is not empty
            result = analyze_product(url)
            if result:
                product_results.append(result)
            time.sleep(2)  # Prevent request blocking

    if not product_results:
        print("❌ No products could be analyzed. Please try again.")
        return

    # Find best product
    best_product = max(product_results, key=lambda x: (x["positive"], x["average_rating"]))

    print("\n🔹 **Product Comparison Summary:**")
    for product in product_results:
        print(f"{product['url']} - Positive: {product['positive']:.2f}%, Negative: {product['negative']:.2f}%, Rating: {product['average_rating']}⭐")
        print(f"🛒 Recommendation: {product['recommendation']}\n")

    print(f"\n✅ **Best Recommended Product:** {best_product['url']} (Rating: {best_product['average_rating']}⭐)")

def main():
    print("\n🔍 **Welcome to Amazon Product Sentiment Analyzer!**")
    print("1️⃣ Get sentiment analysis for a single product")
    print("2️⃣ Compare multiple products based on reviews")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        url = input("Enter Amazon product URL: ").strip()
        if url:
            analyze_product(url)
        else:
            print("❌ Invalid input. Please enter a valid Amazon product URL.")

    elif choice == "2":
       compare_products()

    else:
        print("❌ Invalid choice. Please enter 1 or 2.")

# Run the main function
if __name__ == "__main__":
    main()
