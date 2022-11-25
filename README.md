# Azure Speech - Speaker Recognition Demo
Sample application to test Azure Speech - Speaker Recognition


## What is speaker recognition?

Speaker recognition can help determine who is speaking in an audio clip. The service can verify and identify speakers by their unique voice characteristics, by using voice biometry. 

You provide audio training data for a single speaker, which creates an enrollment profile based on the unique characteristics of the speaker's voice. You can then cross-check audio voice samples against this profile to verify that the speaker is the same person (speaker verification). You can also cross-check audio voice samples against a *group* of enrolled speaker profiles to see if it matches any profile in the group (speaker identification).


## Speaker verification

Speaker verification streamlines the process of verifying an enrolled speaker identity with either passphrases or free-form voice input. For example, you can use it for customer identity verification in call centers or contactless facility access.

## How does speaker verification work?

The following flowchart provides a visual of how this works:

![image](https://github.com/MicrosoftDocs/azure-docs/raw/main/articles/cognitive-services/Speech-Service/media/speaker-recognition/speaker-rec.png)

Speaker verification can be either text-dependent or text-independent. *Text-dependent* verification means that speakers need to choose the same passphrase to use during both enrollment and verification phases. *Text-independent* verification means that speakers can speak in everyday language in the enrollment and verification phrases.

For text-dependent verification, the speaker's voice is enrolled by saying a passphrase from a set of predefined phrases. Voice features are extracted from the audio recording to form a unique voice signature, and the chosen passphrase is also recognized. Together, the voice signature and the passphrase are used to verify the speaker. 

Text-independent verification has no restrictions on what the speaker says during enrollment, besides the initial activation phrase to activate the enrollment. It doesn't have any restrictions on the audio sample to be verified, because it only extracts voice features to score similarity. 

The APIs aren't intended to determine whether the audio is from a live person, or from an imitation or recording of an enrolled speaker. 

## How to run the application with Docker
1. Build docker image
```
    docker build . -t YOUR_DOCKER_IMAGE_NAME
```
2. Modify the .env file with your application settings
```
    speech_key=Azure_Speech_Key
    service_region=Azure_Speech_Region
```
3. Run the image
```
    docker run --env-file .env -p 80:80 -t YOUR_DOCKER_IMAGE_NAME
```