import streamlit as st
import time
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from scraper import analyze_product


def main():
    st.title("📊 Amazon Product Sentiment Analyzer")

    # Welcome message and choice selection
    st.write("🔍 **Welcome to Amazon Product Sentiment Analyzer!**")
    st.write("1️⃣ **Analyze a single product**")
    st.write("2️⃣ **Compare multiple products based on reviews**")

    choice = st.radio("Select an option:", ["Single Product Analysis", "Compare Multiple Products"])

    if choice == "Single Product Analysis":
        st.subheader("🔍 Analyze a Single Amazon Product")
        url = st.text_input("Enter Amazon product URL:")
        
        if st.button("Analyze Product"):
            if url.strip():
                st.write("⏳ Fetching reviews and analyzing sentiment... Please wait.")
                result = analyze_product(url)
                time.sleep(2)

                if result:
                    st.subheader("✅ Product Sentiment Analysis")
                    st.write(f"### {url}")
                    st.write(f"✅ **Positive Reviews:** {result['positive']:.2f}%")
                    st.write(f"⚠️ **Negative Reviews:** {result['negative']:.2f}%")
                    st.write(f"⭐ **Estimated Rating:** {result['average_rating']} / 5")
                    st.write(f"🛒 **Recommendation:** {result['recommendation']}")
                else:
                    st.error("❌ Could not analyze the product. Try again later.")
            else:
                st.warning("⚠️ Please enter a valid Amazon product URL.")

    elif choice == "Compare Multiple Products":
        st.subheader("🔄 Compare Multiple Products")

        # Allowing up to 5 product inputs
        url1 = st.text_input("Enter Amazon product URL 1")
        url2 = st.text_input("Enter Amazon product URL 2")
        url3 = st.text_input("Enter Amazon product URL 3")
        url4 = st.text_input("Enter Amazon product URL 4")
        url5 = st.text_input("Enter Amazon product URL 5")

        product_urls = [url1, url2, url3, url4, url5]
        product_urls = [url for url in product_urls if url.strip()]  # Remove empty inputs

        if st.button("Compare Products"):
            if not product_urls:
                st.warning("⚠️ Please enter at least one Amazon product URL.")
            else:
                st.write("⏳ Fetching reviews and analyzing sentiment... Please wait.")

                product_results = []
                for url in product_urls:
                    result = analyze_product(url)
                    if result:
                        product_results.append(result)
                    time.sleep(2)  # Prevent Amazon request blocking

                if not product_results:
                    st.error("❌ No products could be analyzed. Try again later.")
                else:
                    st.subheader("🔹 **Product Comparison Results**")
                    for product in product_results:
                        st.write(f"### {product['url']}")
                        st.write(f"✅ **Positive Reviews:** {product['positive']:.2f}%")
                        st.write(f"⚠️ **Negative Reviews:** {product['negative']:.2f}%")
                        st.write(f"⭐ **Estimated Rating:** {product['average_rating']} / 5")
                        st.write(f"🛒 **Recommendation:** {product['recommendation']}")
                        st.write("---")

                    # Find best product
                    best_product = max(product_results, key=lambda x: (x["positive"], x["average_rating"]))

                    st.subheader("🏆 **Best Recommended Product**")
                    st.write(f"### {best_product['url']}")
                    st.write(f"✅ **Positive Reviews:** {best_product['positive']:.2f}%")
                    st.write(f"⭐ **Estimated Rating:** {best_product['average_rating']} / 5")
                    st.write(f"🛒 **Recommendation:** {best_product['recommendation']}")

if __name__ == "__main__":
    main()
