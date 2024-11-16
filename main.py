import requests
import json
import streamlit

def invoke_lambda(api_gateway_url, payload):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url=api_gateway_url, json=payload, headers=headers)
        print(f"Raw response: {response.text}")
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error invoking Lambda function: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None

# API GatewayエンドポイントURL
api_gateway_url = "https://11l79ngo06.execute-api.ap-northeast-1.amazonaws.com/dev/"

# Using Streamlit for a better user interface 
streamlit.title("Lambda Function Invoker")
user_input = streamlit.text_input("キーワードを入力してください。")

# Only proceed if user input is provided (for both Streamlit and standard input)
if user_input: # Check if user_input is not empty
    # リクエストペイロード (必要に応じて)
    payload = {
        "key1": user_input,
        "key2": "value2",
    }
    # Lambda関数呼び出し
    result = invoke_lambda(api_gateway_url, payload)
    print("")

    if result:
        try:
            name_1 = result["name1"]
            name_2 = result["name2"]
            name_3 = result["name3"]
            print(f"Lambda function response: {name_1}, {name_2}, {name_3}")
            streamlit.write(f"以下の物件が見つかりました！") #For Streamlit
            streamlit.write(f"{name_1}") #For Streamlit
            streamlit.write(f"{name_2}") #For Streamlit
            streamlit.write(f"{name_3}") #For Streamlit
        except KeyError as e:
            print(f"Error: Key not found in Lambda response: {e}")
            streamlit.error(f"Error: Key not found in Lambda response: {e}") #For Streamlit
    else:
        print("Lambda function invocation failed.")
        streamlit.error("Lambda function invocation failed.") #For Streamlit
else:
    print("Please enter a keyword.")
    streamlit.warning("Please enter a keyword.") #For Streamlit