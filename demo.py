import webbrowser
import time
import pyautogui

# List of search queries

queries = [
    "learn guitar chords",
    "best hiking boots",
    "puppy training tips",
    "lose weight fast",
    "grow taller naturally",
    "stop snoring remedies",
    "improve memory power",
    "quit smoking guide",
    "reduce stress quickly",
    "clear skin routine",
    "build muscle mass",
    "fix leaky faucet",
    "paint bedroom ideas",
    "organize small closet"
    "make money online",
    "write better essays",
    "improve public speaking",
    "learn to dance salsa",
    "cook healthy meals",
    "decorate living room",
    "find new hobbies",
    # "improve handwriting",
    # "save money tips",
    # "deal with anxiety",
    # "improve sleep quality",
    # "increase focus power",
    # "build credit score",
    # "learn to code python",
    # "start a blog",
    # "lose belly fat"
]


# queries = [
#     "Best vacation spots",
#     "Latest tech news",
#     "Healthy breakfast recipes",
#     "Popular movies 2024",
#     "Top science podcasts",
#     "Vegan restaurants nearby",
#     "Upcoming sports events",
#     "Classic novel summaries",
#     "DIY home products",
#     "Current stock prices",
#     "Best books to read",
#     "Future technology trends",
#     "Travel tips for Europe",
#     "How to start a blog",
#     "Work from home jobs",
#     "Top fashion trends 2024",
#     "Easy dinner recipes",
#     "Most visited websites",
#     "Top mobile apps",
#     "Fitness tips for beginners",
#     "Best-selling products 2024",
#     "Latest smartphone reviews",Classic
#     "How to meditate",
#     "Yoga for beginners",
#     "Best workout routines",
#     "Mental health tips",
#     "How to invest in stocks",
#     "Cryptocurrency news",
#     "Online learning platforms",
#     "Popular social media platforms"
# ]

# queries = [
#     "Top vacation destinations 2024",
#     "Latest technology trends",
#     "Healthy breakfast ideas",
#     "Upcoming movies 2024",
#     "Popular science podcasts",
#     "Best vegan restaurants",
#     "Sports events near me",
#     "Classic literature summaries",
#     "DIY home improvement projects",
#     "Current stock market trends",
#     "Best books to read",
#     "Future technology trends",
#     "Travel tips for Europe",
#     "How to start a blog",
#     "Work from home jobs",
#     "Top fashion trends 2024",
#     "Easy dinner recipes",
#     "Most visited websites",
#     "Top mobile apps",
#     "Fitness tips for beginners",
    #     "Best-selling products 2024",
    #     "Latest smartphone reviews",
    #     "How to meditate",
    #     "Yoga for beginners",
    #     "Best workout routines",
    #     "Mental health tips",
    #     "How to invest in stocks",
    #     "Cryptocurrency news",
    #     "Online learning platforms",
    #     "Popular social media platforms"
# ]


# Function to search a query
def search_query(query):
    for char in query:
        pyautogui.typewrite(char)
        time.sleep(0.1)
        # Adding a small delay between keystrokes
    pyautogui.press('enter')
    time.sleep(1)  # Wait for the search results to load


# Open the browser with the initial URL
search_url = "https://www.bing.com"
webbrowser.get("windows-default").open(search_url)

# Give the browser time to open
time.sleep(3)

# Perform the searches
for query in queries:
    search_query(query)
    # Open a new tab for the next query if it's not the last one
    if query != queries[-1]:
        # pyautogui.hotkey('ctrl', 't')
        # time.sleep(1)
        webbrowser.get("windows-default").open(search_url)
        time.sleep(2)

# Optional: Keep the browser open for a while to review the results
# time.sleep(5)


# from selenium import webdriver
# import webbrowser
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
# from selenium.webdriver.edge.options import Options
# from webdriver_manager.microsoft import EdgeChromiumDriverManager
# import time
#
# # List of search queries
# queries = [
#     "Best vacation spots",
#     "Latest tech news",
#     # "Healthy breakfast recipes",
#     # "Popular movies 2024",
#     # "Top science podcasts",
#     # "Vegan restaurants nearby",
#     # "Upcoming sports events",
#     # "Classic novel summaries",
#     # "DIY home projects",
#     # "Current stock prices"
# ]
#
# driver = webdriver.Edge()
#
# # Open the browser
# driver.get("https://www.bing.com")
#
#
# # Function to search a query in a new tab
# def search_query(query):
#     search_box = driver.find_element(By.ID, "sb_form_q")
#     for char in query:
#         search_box.send_keys(char)
#         time.sleep(0.1)  # Adding a small delay between keystrokes
#     search_box.send_keys(Keys.RETURN)
#     time.sleep(2)  # Wait for the search results to load
#
#
# # Iterate through the queries and perform the searches
# for query in queries:
#     if query != queries[0]:
#         driver.execute_script("window.open('');")
#         driver.switch_to.window(driver.window_handles[-1])
#         driver.get("https://www.bing.com")
#     search_query(query)
#
# # Close the browser after the operations
# time.sleep(5)  # Optional: Keep the browser open for a while to review the results
# driver.quit()
