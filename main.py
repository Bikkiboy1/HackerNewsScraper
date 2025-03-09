import json
from scraper import fetch_html, extract_headlines, save_to_json

URL = "https://news.ycombinator.com/"

def main_menu():
    """
    Displays the menu and handles user interactions.
    """
    headlines = []  # Store fetched headlines

    while True:
        print("\n🔹 Hacker News Scraper 🔹")
        print("1. Scrape new headlines")
        print("2. View stored headlines")
        print("3. Save headlines to JSON")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == "1":
            try:
                pages = int(input("Enter the number of pages to scrape: ").strip())
            except ValueError:
                print("\n⚠ Invalid input. Please enter a valid number.")
                continue

            print(f"\nFetching latest headlines from {pages} pages...")
            html_pages = fetch_html(URL, pages)  # ✅ Fetch multiple pages
            headlines = extract_headlines(html_pages)  # ✅ Process multiple pages properly

            if headlines:
                print("\n✅ Latest Hacker News Headlines:\n")
                for i, item in enumerate(headlines[:100], start=1):
                    print(f"{i}. {item['title']} ({item['link']})")
            else:
                print("\n⚠ No headlines found. Check if the website structure has changed.")

        elif choice == "2":
            try:
                with open("headlines.json", "r", encoding="utf-8") as file:
                    stored_headlines = json.load(file)

                if not stored_headlines:
                    print("\n⚠ No stored headlines found. Try scraping first!")
                else:
                    print("\n📂 Stored Headlines:\n")
                    for i, item in enumerate(stored_headlines[:100], start=1):  # ✅ Show 100 headlines
                        print(f"{i}. {item['title']} ({item['link']})")

            except FileNotFoundError:
                print("\n⚠ No stored headlines found. Try scraping first!")
            except json.JSONDecodeError:
                print("\n⚠ Error reading headlines. File might be corrupt.")

        elif choice == "3":
            if not headlines:
                print("\n⚠ No headlines available to save. Try scraping first!")
            else:
                save_to_json(headlines)

        elif choice == "4":
            print("Exiting... Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number from the menu.")

main_menu()
