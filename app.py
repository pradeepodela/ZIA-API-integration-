import streamlit as st
from langchain.agents import Tool, initialize_agent
from langchain_groq import ChatGroq
from langchain.tools import DuckDuckGoSearchRun
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from twilio.rest import Client
import os
import requests
from langchain.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI




# Replace these with your actual details

@tool
def fetch_emails(search_key:str):
    
    """
    Fetch emails based on search parameters from Zoho Mail API.

    :param search_key: Search criteria string.
    :param received_time: Unix timestamp in milliseconds to filter emails.
    :param start: Starting sequence number of emails.
    :param limit: Number of emails to retrieve.
    :param include_to: Boolean to include 'To' details.
    :return: Response from the API as a JSON object.
    """
    print('-------------------------')
    print(search_key)
    if 'subject:' in search_key:search_key = search_key.replace('subject:','')
    print('-------------------------')
    
    received_time=None
    start=1
    limit=10
    include_to=False
    auth_token = ""  # Replace with your OAuth token
    account_id = ""   # Replace with your account ID

    url = f"https://mail.zoho.com/api/accounts/{account_id}/messages/search"
    
    # Query parameters
    params = {
        "searchKey": f"entire:{search_key}",
        "start": start,
        "limit": limit,
        "includeto": str(include_to).lower()  # Convert boolean to lowercase string
    }
    
    # Add receivedTime if provided
    if received_time:
        params["receivedTime"] = received_time
    
    # Headers
    headers = {
        "Authorization": f"Zoho-oauthtoken {auth_token}"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        emails =  response.json()
        consi = []
        for i in emails['data']:
            #print(i['summary'])
            consi.append(i)
        return emails
    except requests.exceptions.RequestException as e:
        print(f"Error fetching emails: {e}")
        return None

# Example usage


email_search = Tool(
    name="search email",
    func=fetch_emails,
    description="Useful for when you need to retrieve or search emails just retrieve and read it . Input should be qurey to search"
)



def fetch_email_data(f):
    """
    Fetch email data from Zoho API.

    Returns:
        dict or None: The response data as a dictionary if the request is successful, otherwise None.
    """
    # Fetch account_id and auth_token from environment variables
    account_id = ""
    auth_token = ""
    
    if not account_id or not auth_token:
        print("Missing Zoho API credentials.")
        return None

    # Define the API endpoint
    url = f"https://mail.zoho.com/api/accounts/{account_id}/messages/view"

    # Set up the headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {auth_token}"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check the response status
        if response.status_code == 200:
            try:
                return response.json()  # Return JSON response
            except ValueError:
                print("Response did not return JSON.")
                return None
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print("Error Details:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return None

# Ensure Tool is properly imported or defined
# from some_tool_library import Tool

email_inbox = Tool(
    name="email inbox",
    func=fetch_email_data,
    description="Useful for when you need to retrieve my inbox emails."
)


def fetch_acc_details(f):
    """
    Fetch email data from Zoho API.

    Returns:
        dict or None: The response data as a dictionary if the request is successful, otherwise None.
    """
    # Fetch account_id and auth_token from environment variables
    account_id = ""
    auth_token = ""
    
    if not account_id or not auth_token:
        print("Missing Zoho API credentials.")
        return None

    # Define the API endpoint
    url = f"https://people.zoho.com/people/api/forms/employee/getRecords?sIndex=1&limit=100"

    # Set up the headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {auth_token}"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check the response status
        if response.status_code == 200:
            try:
                return response.json()  # Return JSON response
            except ValueError:
                print("Response did not return JSON.")
                return None
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print("Error Details:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return None

# Ensure Tool is properly imported or defined
# from some_tool_library import Tool

acc_details = Tool(
    name="my account details",
    func=fetch_acc_details,
    description="Useful for when you need to retrieve my zoho account details."
)

def extract_blog_details(response):
    blogs = response.get("recentBlogs", {}).get("blogs", [])
    parsed_blogs = []

    for blog in blogs:
        user_name = blog.get("userDetails", {}).get("name", "Unknown")
        title = blog.get("title", "No Title")
        url = blog.get("linkurl", "No URL")
        likes = blog.get("likeCount", "0")
        views = blog.get("viewCount", "0")

        parsed_blogs.append({
            "User": user_name,
            "Title": title,
            "URL": url,
            "Likes": likes,
            "Views": views
        })

    return parsed_blogs
import os
import requests

def fetch_documents(f):
    """
    Fetch email data from Zoho API.

    Returns:
        dict or None: The response data as a dictionary if the request is successful, otherwise None.
    """
    # Fetch account_id and auth_token from environment variables
    account_id = ""
    auth_token = ''
    
    if not account_id or not auth_token:
        print("Missing Zoho API credentials.")
        return None

    # Define the API endpoint
    url = f"https://www.zohoapis.com/writer/api/v1/documents"

    # Set up the headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {auth_token}"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check the response status
        if response.status_code == 200:
            try:
                return response.json()  # Return JSON response
            except ValueError:
                print("Response did not return JSON.")
                return None
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print("Error Details:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return None

# Ensure Tool is properly imported or defined
# from some_tool_library import Tool

doc_details = Tool(
    name="my documents",
    func=fetch_documents,
    description="Useful for when you need to retrieve my documents in writer."
)

def extract_blog_details(response):
    blogs = response.get("recentBlogs", {}).get("blogs", [])
    parsed_blogs = []

    for blog in blogs:
        user_name = blog.get("userDetails", {}).get("name", "Unknown")
        title = blog.get("title", "No Title")
        url = blog.get("linkurl", "No URL")
        likes = blog.get("likeCount", "0")
        views = blog.get("viewCount", "0")

        parsed_blogs.append({
            "User": user_name,
            "Title": title,
            "URL": url,
            "Likes": likes,
            "Views": views
        })

    return parsed_blogs


def fetch_forum(f):
    """
    Fetch email data from Zoho API.

    Returns:
        dict or None: The response data as a dictionary if the request is successful, otherwise None.
    """
    # Fetch account_id and auth_token from environment variables
    account_id = ""
    auth_token =''
    
    if not account_id or not auth_token:
        print("Missing Zoho API credentials.")
        return None

    # Define the API endpoint
    url = f"https://connect.zoho.com/pulse/api/recentBlogs?scopeID=105000017039001&pageIndex=1&limit=10"

    # Set up the headers
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Zoho-oauthtoken {auth_token}"
    }

    try:
        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check the response status
        if response.status_code == 200:
            try:
                return str(extract_blog_details(response.json()))  # Return JSON response
            except ValueError:
                print("Response did not return JSON.")
                return None
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print("Error Details:", response.text)
            return None
    except requests.exceptions.RequestException as e:
        print("An error occurred while making the request:", e)
        return None

# Ensure Tool is properly imported or defined
# from some_tool_library import Tool

forum = Tool(
    name="my forum posts",
    func=fetch_forum,
    description="Useful for when you need to retrieve recent forum posts in connect pl."
)





# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize LLM and conversational memory
# llm = ChatGroq(
#     groq_api_key='',
#     model_name="llama3-70b-8192"
# )

os.environ["GOOGLE_API_KEY"] = '' #Enter your Api key 
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro",temperature=0,max_tokens=None,timeout=None,max_retries=2)

conversational_memory = ConversationBufferWindowMemory(
    memory_key='chat_history',
    k=5,
    return_messages=True
)


# Initialize agent
agent = initialize_agent(
    tools = [email_search,email_inbox,acc_details,doc_details,forum],
    llm=llm,
    agent='chat-conversational-react-description',
    verbose=True,  
    max_iterations=3,
    early_stopping_method='generate',
    memory=conversational_memory,
    handle_parsing_errors=True
)

# Streamlit UI
st.title("ZIA - Zoho Intelligent Assistant")

# Display chat messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    else:
        st.chat_message("assistant").markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Type your message here..."):
    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Process agent response
    with st.spinner("Processing..."):
        try:
            response = agent.run(user_input)
        except Exception as e:
            response = f"Error: {e}"
    
    # Add agent response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)




