# scraper-with-chatgpt
It is a powerful data scraping tool that helps you extract information from various online sources. Easily collect data from Google SERP, Maps, Shopify, Zillow, and more. With a user-friendly interface, you can scrape and save data in JSON or Excel formats. Unlock insights from the web effortlessly.

## Table of Contents

- [Installation](#installation)
- [Account Setup](#account-setup)
- [Usage](#usage)
  - [Settings](#settings)
  - [SERP](#serp)
  - [Maps](#maps)
  - [Chat GPT with Scraper](#chat-gpt-with-scraper)
  - [Shopify](#shopify)
  - [Zillow](#zillow)
  - [ANY](#any)

## Installation

To get started, follow these simple steps:

1. Download the application files from the "ready-exe" folder.
2. Run the "main.exe" file to launch the application.

Alternatively, you can also run the Python script:

1. Navigate to the "Python script" folder.
2. Locate the "main.py" file.
3. Open a terminal or command prompt.
4. Navigate to the "Python script" folder using the `cd` command.
5. Run the following command to start the application:
   ```
   python main.py
   ```

That's it! You're ready to start using app to efficiently gather data from various online sources.

*Note: Make sure you have Python3 installed on your system if you choose to run the Python script.*

## Account Setup

Before you begin using app, you'll need to set up your account and provide the necessary API keys. Here's why these API keys are important and how to obtain them:

### Scrape-It.Cloud API Key
The Scrape-It.Cloud API key allows app to connect with the Scrape-It.Cloud service, which enables efficient web scraping. This key is essential for retrieving data from various online sources, such as search engines, maps, and websites.

**Obtaining Scrape-It.Cloud API Key:**

To get your Scrape-It.Cloud API key:
1. Visit the Scrape-It.Cloud website at [scrape-it.cloud](https://scrape-it.cloud).
2. Sign up for an account or log in if you already have one.
3. Navigate to the Dashboard section in your account.
![API key](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/1.jpg)
4. Copy the API key and paste it into the "Scrape-It.Cloud API" field in the Settings of app.

### ChatGPT API Key:
The ChatGPT API key enables app to interact with the ChatGPT service, which adds natural language processing capabilities to the application. This key is necessary for generating human-like responses and engaging conversations.

**Obtaining ChatGPT API Key:**

To acquire your ChatGPT API key:
1. Visit the OpenAI website at [openai.com](https://www.openai.com/).
2. Sign up for an account or log in if you're already registered.
3. Access the [API section](https://platform.openai.com/account/api-keys) in your account dashboard.
![API key](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/2.jpg)
4. Create a new API key.
5. Copy the API key and paste it into the "ChatGPT API" field in the Settings of app.

With both API keys in place, app is ready to provide you with seamless data scraping and natural language interaction. Ensure your keys are kept secure and do not share them with unauthorized individuals.

*Note: API key acquisition and setup steps may vary over time, so be sure to refer to the respective websites for the most up-to-date instructions.*

## Usage

### Settings

The "Settings" tab in app allows you to configure essential preferences and manage your API keys for seamless integration with external services. Here's a breakdown of what you'll find on this tab and how the buttons work:

![Settings Tab](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/3.jpg)

**Scrape-It.Cloud API Key:**
- In the "Scrape-It.Cloud API" field, enter your Scrape-It.Cloud API key that you obtained during the Account Setup process.
- This key is required for data scraping from various sources, ensuring accurate and efficient information retrieval.

**ChatGPT API Key:**
- In the "ChatGPT API" field, enter your ChatGPT API key that you acquired from OpenAI during the Account Setup.
- This key enables app to engage in natural language conversations and generate human-like responses.

**Upload:**
- Click the "Upload" button to import previously saved API keys from database.
- This feature is useful if you don't want to enter data manually.

**Save:**
- After entering or importing API keys, click the "Save" button to store the keys.

**Delete:**
- If needed, you can remove current API keys by clicking the "Delete" button.
- Use this option when you want to update or change the API keys.

Configuring your API keys correctly on the "Settings" tab is crucial for the smooth functioning of app. Once you've entered and saved the keys, you're ready to explore the various data scraping and interaction features the application offers.

### SERP

**Usage: SERP**

The "SERP" tab in App empowers you to gather valuable data from Google's Search Engine Results Pages. This tab provides you with options to customize your search and collect information from different sources. Here's an overview of the features and buttons on the "SERP" tab:

![SERP Tab](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/4.jpg)

**Keyword:**
- Enter the keyword you want to search for on Google SERP.
- This keyword will be used as the basis for data scraping.

**Google Domain:**
- Choose the Google domain you wish to perform the search on (e.g., google.com, google.co.uk).
- This selection determines the localized search results.

**Language:**
- Select the language in which you want to receive search results.
- Choosing the appropriate language ensures relevant data extraction.

**Country:**
- Specify the country you are interested in for location-specific search results.
- This option is useful when collecting region-specific data.

**Data Sources:**
- Check the checkboxes next to data sources (Images, News, Locals, Shopping, Videos) you want to include in your search.
- Selecting these sources tailors your search to your specific data needs.

**Scrape:**
- Click the "Scrape" button to initiate the scraping process.
- App will retrieve and compile data based on your specified criteria.

**Run:**
- After data scraping is complete, choose to save the collected information in JSON or Excel format.
- Select the appropriate format based on your data analysis requirements and Run the app.

The "SERP" tab provides a comprehensive solution for extracting data from Google SERP across various sources. Customize your search parameters, initiate the scraping process, and save the results for further analysis or reference.

*Note: When scrape Google Images, you will get them in folder.*

### Maps

The "Maps" tab in App empowers you to gather data from Google Maps based on specific keywords and location preferences. Here's how to navigate this tab and utilize its features:

![Maps Tab](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/5.jpg)

**Keyword Entry:**
- In the "Keyword" field, input the keyword or topic related to the location you wish to scrape data for.
- This keyword helps narrow down the search and ensures relevant results.

**Country Selection:**
- Choose the desired country from the available options to focus the data scraping on that particular region.
- This feature ensures that you gather location-specific information from Google Maps.

**Data Output Format:**
- You can choose to save the collected data in either JSON or Excel format.

**Run:**
- Click the "Run" button to initiate the data scraping process based on the provided keyword and country.
- App will fetch and organize relevant data from Google Maps.

**Example Use Case:**
Suppose you're interested in gathering information about local businesses related to "restaurants" in the country "United States." By entering the keyword "restaurants" and selecting the country, you can click the "Scrape" button to obtain a comprehensive dataset of restaurant-related data from Google Maps.

### Chat GPT with Scraper

The "Chat GPT with Scraper" tab within App seamlessly integrates data scraping with natural language processing through ChatGPT. Here's a breakdown of how to harness this powerful feature:

![Chat GPT with Scraper Tab](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/6.jpg)

**Website Link:**
1. Paste the URL of the website from which you want to gather textual information.
2. This website will serve as the source for data extraction.

**Prompt to ChatGPT:**
1. Create a prompt that clearly conveys the information you're seeking from the scraped data.
2. The prompt guides ChatGPT's response to ensure meaningful insights.

**Run Generation:**
1. Click the "Send" button to transmit the prompt along with the scraped content to ChatGPT. The response from ChatGPT will be displayed in the text field below
2. ChatGPT will process the input and generate a response based on the prompt and the extracted data.

**Return All Text From Site:**
1. Will return all text information collected on the page without processing it in ChatGPT.

**Example Use Case:**
Imagine you have a service that you want to offer, and a list of companies that might be interested in your service. You can use this tool to gather information about the company and create a ChatGPT prompt. Based on the collected information and details about your service, ChatGPT can help you write a personalized email proposing your services.
Or imagine you've scraped a news article from a website, and you're interested in a concise summary of the article. By pasting the article's link, composing a prompt like "Please provide a brief summary of the article," and sending it to ChatGPT, you'll receive a summarized response that captures the essence of the article.

### Shopify

Explore the capabilities of the "Shopify" tab in App to effortlessly scrape product and collection data from Shopify websites. 
![Shopify Tab](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/7.jpg)

**Link:**
- Enter the URL of the Shopify page containing the products or collections you wish to scrape.
- Ensure the URL directly points to the specific products or collections page.

**Limit (From 1 to 250):**
- Specify the maximum number of items you want to scrape (from 1 to 250).
- This allows you to control the amount of data collected.

**Page:**
- If the data is spread across multiple pages, enter the page number to start scraping from.
- Leave this field blank if you want to start from the first page.

**Collection:**
- If you're targeting a specific collection within the Shopify page, provide the collection name.
- This helps narrow down the scraping process to relevant data.

**Options:**

- **JSON:**
  - Check the JSON checkbox if you want to save the results in JSON format.

- **Excel:**
  - Check the Excel checkbox if you prefer to save the results in Excel format.

**Get Collection Button:**
- Click the "Get Collection" button to initiate the scraping process for collections based on your input.
- App will retrieve collection data according to the specified parameters.

**Get Products Button:**
- Click the "Get Products" button to begin scraping product data using the provided details.
- App will gather product information as per the specified parameters.

The "Shopify" tab simplifies the process of data collection from Shopify websites. Whether you're conducting market research, monitoring trends, or analyzing product details, App streamlines the data scraping process for informed decision-making.

### Zillow

The "Zillow" tab in App provides powerful tools to extract property and listing data from Zillow. This tab is split into two sections: Zillow Property and Zillow Listing. Let's explore how each section works:

![Zillow Tab](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/8.jpg)

**Zillow Property:**

**Link to Property:**
- In the "Link to Property" field, enter the URL of the Zillow property you want to scrape data from.
- This URL should lead to the property page on Zillow.

**Get Button:**
- After entering the property URL, click the "Get" button to initiate the scraping process.
- App will extract relevant data from the provided Zillow property page.

**Zillow Listing:**

**Keyword:**
- Enter a keyword related to the listings you're interested in.
- This keyword helps refine the search for specific types of listings.

**Type and HomeTypes:**
- Choose the "Type" of listings you want to scrape (e.g., "For Sale," "For Rent," "Sold").
- Select one or more "HomeTypes" that match the types of properties you're looking for (e.g., "SingleFamily," "Condo," etc.).

**Excel and JSON Checkboxes:**
- Check the desired format(s) (Excel and/or JSON) to save the scraped listing data.
- Choose one or both options based on your data storage preferences.

**Get Listing Data Button:**
- Click the "Get Listing Data" button to start scraping Zillow listings with the specified criteria.
- App will gather and organize listing data according to your chosen format(s).

Utilizing the Zillow section, you can efficiently gather property information and listing details for your analysis. Make sure to select the appropriate options and enter accurate details to retrieve the data you need.

### ANY

The "ANY" tab in App empowers you to scrape content from any website using a flexible and customizable approach. Here's a detailed breakdown of what you'll find on this tab and how each feature works:

![ANY Tab](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/9.jpg)

**Link to Scrape:**
- Enter the URL of the website you want to scrape in the "Link to Scrape" field.
- App will access and extract data from the provided URL.

**Proxy Configuration:**
- "Proxy" label indicates the proxy settings section.
- Choose the proxy type and select a country for the proxy from the dropdown options.
- Activate proxy usage by checking the checkbox if necessary.
- Utilizing proxies can help ensure anonymity and efficient data scraping.

**Extraction Rules:**
- In the "Extraction Rules" section, you can specify custom labels and CSS selectors for data extraction.
- Enter a descriptive label for the data you want to extract, followed by the CSS selector that targets that specific content.
- Click the "+" button to add additional fields for more extraction rules.
  ![ANY Tab](https://github.com/valka465/scraper-with-chatgpt/blob/main/images/10.jpg)

**Output Format:**
- Choose the desired output format for the scraped data by checking the "Excel" and/or "JSON" checkboxes.
- Excel format is suitable for structured data, while JSON format is ideal for more flexible data representation.

**Run Button:**
- Once you've configured the extraction rules and chosen the output format, click the "Run" button to initiate the scraping process.
- App will access the specified website, extract the defined content, and save it in the selected format.

The "ANY" tab offers a versatile and dynamic way to scrape data from various websites, with options to configure proxies, extraction rules, and output formats. Customize your scraping process to suit your specific data needs, and let App do the rest.
