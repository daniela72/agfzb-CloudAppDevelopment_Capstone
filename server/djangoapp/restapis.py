import requests
import json
import urllib
import datetime
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


def get_request(url, **kwargs):
    # print(f"get_request section {kwargs}")
    # print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        if 'api_key' in kwargs:
            params = dict()
            params["text"] = kwargs["text"]
            params["version"] = kwargs["version"]
            params["features"] = kwargs["features"]
            params["return_analyzed_text"] = kwargs["return_analyzed_text"]
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs, 
            auth=HTTPBasicAuth('apikey', kwargs['api_key']))
        else:
            response = requests.get(url, headers={'Content-Type': 'application/json'}, params=kwargs)
    except:
        print("Network exception occured")
    # print(f"Status Code is: {response.status_code}")
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    json_result = get_request(url)
    if json_result:
        dealers = json_result["fields"]
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


# def get_dealer_by_id(url, **kwargs):
def get_dealer_by_id(url, dealer_id):
    results = []
    json_result = get_request(url, id=dealer_id)
    if json_result:
        dealers = json_result["body"]
        for dealer in dealers:
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   id=dealer["id"], lat=dealer["lat"], long=dealer["long"],
                                   short_name=dealer["short_name"], st=dealer["st"], zip=dealer["zip"])
            results.append(dealer_obj)
    return results


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# get from cf. Linked to views
#  we need to define dealer_id argument
def get_dealer_reviews_from_cf(url, dealerId):
    # print(f"GET the {dealerId}")
    results = []
    # dealer_id is from action and dealerId from the url
    json_result = get_request(url, dealer_id=dealerId)
    if json_result:
        reviews = json_result["reviews"]
        for review in reviews:
                review_obj = DealerReview(make=review["car_make"], model=review["car_model"], 
                                    year=review["car_year"], dealer_id=review["dealership"], 
                                    id=review["id"], name=review["name"], purchase=review["purchase"], 
                                    purchase_date=review["purchase_date"], review=review["review"])                                   
                review_obj.sentiment = analyze_review_sentiments(review_obj.review)
                results.append(review_obj)

    return results


# `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(dealerreview):
    result = []
    try:
        json_result = get_request(
                        url="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/62586fea-a45d-420e-a129-7dcba8bdeee9/v1/analyze", 
                        api_key="9XJvPs5xSt_DDQjL7fklWit_4FN2LZ45APWMMcxWzzRy", 
                        version="2021-08-01",
                        features="sentiment",
                        language='en',
                        return_analyzed_text=True,
                        text=dealerreview)
        result = json_result["sentiment"]["document"]["label"]
    finally:
        return result


def post_request(url, json_payload, **kwargs):
    url = url + '/post'
    print('Payload: ', json_payload, '. Params: ', kwargs)
    print(f'POST {url}')
    try:
        # response = requests.post(url, headers={'Content-type': 'application/json'}, json=json_payload, params=kwargs)
        response = requests.post(url, json=json_payload)
    except:
        # If any error occurs
        print('Network exception occurred')
    status_code = response.status_code
    print('With status {} '.format(status_code))
    json_data = json.loads(response.text)
    return json_data

