import requests,json,os

speech_key = os.environ['Azure_Speech_Key']
service_region = os.environ['Azure_Speech_Region']
profile_db = "profiles_db.json"

# Create a profile and store in a local database
def create_and_store_profile(profile_name):
    # Create Profile
    url = f"https://{service_region}.api.cognitive.microsoft.com/speaker-recognition/verification/text-independent/profiles?api-version=2021-09-05"

    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type" : "application/json"
    }

    body = {
        "locale" : "it-IT"
    }

    r = requests.post(url=url, headers=headers, json=body)

    if r.ok:
        with open(profile_db,'r') as f:
            data = json.load(f)
        data[profile_name] = r.json()['profileId']

        with open(profile_db, 'w') as f:
            json.dump(data,f)

    return r.json()['profileId']

# Enroll the voice profile
def enroll_profile(**kwargs):
    profile_name = kwargs['profile_name']
    with open(profile_db,'r') as f:
        data = json.load(f)   
    profileId = data.get('profile_name', create_and_store_profile(profile_name))


    url = f"https://{service_region}.api.cognitive.microsoft.com/speaker-recognition/verification/text-independent/profiles/{profileId}/enrollments?api-version=2021-09-05"

    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type" : "audio/wav"
    }

    with open(os.path.join("data",f"{os.environ['language']}-{profile_name}Neural_first.wav"), 'rb') as f:
        data = f.read()

    r = requests.post(url=url, headers=headers, data=data)

    if r.ok:
        # Second
        url = f"https://{service_region}.api.cognitive.microsoft.com/speaker-recognition/verification/text-independent/profiles/{profileId}/enrollments?api-version=2021-09-05"

        headers = {
            "Ocp-Apim-Subscription-Key": speech_key,
            "Content-Type" : "audio/wav"
        }

        with open(os.path.join('data',f"{os.environ['language']}-{profile_name}Neural.wav"), 'rb') as f:
            data = f.read()

        r = requests.post(url=url, headers=headers, data=data)
    
    return r.ok

# Verify
def verify_profile(**kwargs):
    file_name = kwargs['file_name']
    profile_name = kwargs['profile_name']
    auth_code = kwargs.get('auth_code', '')
    with open(profile_db,'r') as f:
        data = json.load(f)   
    profileId = data[profile_name]
    
    url = f"https://{service_region}.api.cognitive.microsoft.com/speaker-recognition/verification/text-independent/profiles/{profileId}:verify?api-version=2021-09-05"

    headers = {
        "Ocp-Apim-Subscription-Key": speech_key,
        "Content-Type" : "audio/wav"
    }
   
    with open(os.path.join('.','data',f"{os.environ['language']}-{file_name}Neural_verify{auth_code}.wav"), 'rb') as f:
        data = f.read()

    r = requests.post(url=url, headers=headers, data=data)

    result = r.json()

    url = f"https://{service_region}.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=it-IT"
    r = requests.post(url, headers=headers, data=data)

    result['Text'] = r.json()['DisplayText'].replace('.','').replace(',','')

    return result

    