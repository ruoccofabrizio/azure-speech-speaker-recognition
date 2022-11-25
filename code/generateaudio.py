from ntpath import join
import azure.cognitiveservices.speech as speechsdk
from random import randint
from os import path

def synt_text (text, scope, voice_name): 
    # Creates an instance of a speech config with specified subscription key and service region.
    speech_key = os.environ['Azure_Speech_Key']
    service_region = os.environ['Azure_Speech_Region']

    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_synthesis_voice_name = voice_name

    audio_config = speechsdk.audio.AudioOutputConfig(filename= path.join('.','data',f'{voice_name}{scope}.wav'))
    # use the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_text_async(text).get()
    # Check result
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

def generate_audio_files(**kwargs):
    name = kwargs.get('name', 'Cataldo')
    person_name = kwargs.get('name', 'Pierina Bianchi')
    generate_audio= kwargs.get('generate_audio', ["Enroll","Verify"])
    auth_code= kwargs.get('auth_code', randint(0,99999))
    print(auth_code)
    voice_name = f"it-IT-{name}Neural"

    text_first = "Parlo qualche secondo per farti sentire la mia voce, così in futuro mi riconoscerai."
    text = f"Ciao, mi chiamo {person_name} e voglio attivare il servizio di conferma vocale per le mie operazioni Sono nata il 1 Gennaio 1990 a Roma e sono attualmente residente a Milano, in via Genova 123. Ho scelto di facilitare il mio accesso, utilizzando semplicemente solo la mia voce! Continuo a parlare per raggiungere almeno 20 secondi di registrazione per creare il mio profilo vocale!"
    text_verify = f"Sono {person_name} ed il mio codice di conferma per l'operazione è {auth_code:05}"

    if "Enroll" in generate_audio:
        synt_text(text_first, "_first", voice_name)
        synt_text(text, "", voice_name)
    if "Verify" in generate_audio:
        synt_text(text_verify, "_verify", voice_name)