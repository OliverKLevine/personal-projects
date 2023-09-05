import os
import sys
import requests

def main(api_token, questions):
    if os.path.exists(api_token):
        f = open(api_token, "r")
        api_token = f.read().strip()
        f.close()
    survey_id = "SV_0Do9oXaedE3CQpE"
    data_center = "ca1"
    base_url = f"https://ugeorgia.{data_center}.qualtrics.com/API/v3/survey-definitions/{survey_id}"
    headers = {
        "x-api-token": api_token,
    }

    response = requests.post(base_url, headers=headers)
    print(response.text)
    

if __name__ == "__main__":
    main(*sys.argv[1:])