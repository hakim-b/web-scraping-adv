import requests
from bs4 import BeautifulSoup


def get_store(listing: BeautifulSoup) -> str:
    """
    Extracts the store name from the given listing.

    Parameters:
    - listing (BeautifulSoup): The BeautifulSoup object representing a deal listing.

    Returns:
    - str: The extracted store name.
    """
    store_element_retailer = listing.select_one(".topictitle_retailer")
    store_element = listing.select_one(".topictitle")

    if store_element_retailer:
        return store_element_retailer.text.strip()
    elif store_element:
        # Extract store from the square brackets, if available
        store_text = store_element.text.strip()
        return store_text.split("]")[0][1:].strip() if "]" in store_text else store_text
    else:
        return "N/A"


def display_latest_deals():
    """
    Displays deal information from the RedFlagDeals forum, sorted by the latest timestamp.
    """
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Example: Extracting information from HTML elements
    # Base URL
    base_url = "https://forums.redflagdeals.com/"

    deals = soup.find_all("li", class_="row topic")

    print("Total deals found: ", len(deals), "\n")

    for listing in deals:
        store = get_store(listing)

        item_element = listing.select_one(".topic_title_link")
        item = item_element.text.strip() if item_element else "N/A"

        votes_element = listing.select_one(".total_count_selector")
        votes = votes_element.text.strip() if votes_element else "N/A"

        username_element = listing.select_one(".thread_meta_author")
        username = username_element.text.strip() if username_element else "N/A"

        timestamp_element = listing.select_one(".first-post-time")
        timestamp = timestamp_element.text.strip() if timestamp_element else "N/A"

        category_element = listing.select_one(".thread_category a")
        category = category_element.text.strip() if category_element else "N/A"

        replies_element = listing.select_one(".posts")
        replies = replies_element.text.strip() if replies_element else "N/A"

        views_element = listing.select_one(".views")
        views = views_element.text.strip() if views_element else "N/A"

        # Extract the URL and prepend the base URL
        url_element = item_element["href"] if item_element else "N/A"
        url = base_url + url_element

        print(f"Store: {store}")
        print(f"Item: {item}")
        print(f"Votes: {votes}")
        print(f"Username: {username}")
        print(f"Timestamp: {timestamp}")
        print(f"Category: {category}")
        print(f"Replies: {replies}")
        print(f"Views: {views}")
        print(f"Url: {url}")
        print("-------------------------")


def count_by_category():
    """
    Displays the number of deals for each category
    """
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    category_count = {}

    for listing in soup.find_all("li", class_="row topic"):
        category_element = listing.select_one(".thread_category a")
        category = category_element.text.strip() if category_element else "N/A"

        if category in category_count:
            category_count[category] += 1
        else:
            category_count[category] = 1

    sorted_categories = sorted(category_count.items(), key=lambda x: x[1], reverse=True)

    for category, count in sorted_categories:
        print(f"{category}: {count} deal(s)")


def find_top_stores():
    """
    Finds the top stores based on the number of deals they have posted.
    """
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    deals = soup.find_all("li", class_="row topic")
    deal_count = len(deals)

    while True:
        top_input = get_number_input("Enter the number of top stores to display: ")
        if top_input < 1 or top_input > deal_count:
            print("Out of bounds.\n")
        else:
            store_count = {}

            for listing in deals[: int(top_input)]:
                store = get_store(listing)

                if store in store_count:
                    store_count[store] += 1
                else:
                    store_count[store] = 1

            for store, count in sorted(store_count.items(), key=lambda x: x[1], reverse=True):
                print(f"{store}: {count} deal(s)")

            break


def log_deal_info():
    """
    Logs deal information from the RedFlagDeals forum to a text file.
    """
    response = requests.get("https://forums.redflagdeals.com/hot-deals-f9/")
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    categories = set()

    for listing in soup.find_all("li", class_="row topic"):
        category_element = listing.select_one(".thread_category a")
        category = category_element.text.strip() if category_element else "N/A"
        categories.add(category)

    categories_list = list(categories)

    print("\nList of Categories:\n")
    for i, category in enumerate(categories_list):
        print(f"{i + 1}. {category}")

    while True:
        category_number = get_number_input(
            "Enter the number corresponding to the category: "
        )
        if category_number < 1 or category_number > len(categories_list):
            print("Out of bounds.\n")
        else:
            corresp_category = categories_list[int(category_number) - 1]
            deals = soup.find_all("li", class_="row topic")
            base_url = "https://forums.redflagdeals.com/"

            for listing in deals:
                item_element = listing.select_one(".topic_title_link")

                category_element = listing.select_one(".thread_category a")
                category = category_element.text.strip() if category_element else "N/A"

                url_element = item_element["href"] if item_element else "N/A"
                url = base_url + url_element

                if category == corresp_category:
                    with open("./log.txt", "a") as file:
                        file.write(f"URL: {url}\n")
                        file.write("-------------------------\n")

            print("All the links have been logged successfully\n")
            break


def print_menu():
    """
    Prints the main menu
    """
    print("***** Web Scraping Adventure *****")
    print("1. Display Latest Deals")
    print("2. Analyze Deals by Category")
    print("3. Find Top Stores")
    print("4. Log Deal Information")
    print("5. Exit")


def get_number_input(prompt: str) -> float:
    """
    Prompts the user to enter a number and returns it as a float.

    Parameters:
    prompt (str): The prompt to display to the user.

    Raises:
    ValueError: If the user enters an invalid number.
    """
    while True:
        try:
            user_input = float(input(prompt))
            return user_input
        except ValueError:
            print("Please enter a number.")


def main():
    """
    The main function
    """
    while True:
        print_menu()
        choice = get_number_input("Enter your choice (1-5): ")
        if choice < 1 or choice > 5:
            print("Invalid choice. Please try again.\n")
        elif choice == 1:
            print()
            display_latest_deals()
            print(".")
            print(".")
            print(".")
        elif choice == 2:
            print()
            count_by_category()
            print("--------------------------------\n")
        elif choice == 3:
            find_top_stores()
            print("--------------------------------\n")
        elif choice == 4:
            log_deal_info()
        elif choice == 5:
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
