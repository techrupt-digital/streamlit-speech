import streamlit as st
import azure.cognitiveservices.speech as speechsdk

def text_to_speech_ssml(ssml_text, key, region):
    speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_synthesizer.speak_ssml_async(ssml_text).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        st.success("Speech synthesized successfully!")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        st.error(f"Speech synthesis canceled: {cancellation_details.reason}")
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            st.error(f"Error details: {cancellation_details.error_details}")

# Sidebar for Azure Speech key and region
st.sidebar.title("Azure Speech Service Settings")

# Credentials Input
speech_key = st.sidebar.text_input("Azure Speech Service API Key", type="password")
speech_region = st.sidebar.text_input("Azure Speech Service Region", placeholder="e.g., eastus")

# Main page with tabs for Text-to-Speech and Speech-to-Text
st.title("Azure Speech Service")

# Create tabs
tab1, tab2 = st.tabs(["Text-to-Speech", "Speech-to-Text"])

# Text-to-Speech tab
with tab1:
    st.header("Text-to-Speech")
    
    # SSML Controls
    use_ssml = st.checkbox("Use SSML")
    voice_options = ["en-US-JennyNeural", "en-GB-RyanNeural", "es-ES-ElviraNeural"]
    selected_voice = st.selectbox("Choose a voice", voice_options)

    if use_ssml:
        rate = st.slider("Rate", -50, 50, 0, help="Adjust the rate of speech. Negative values slow it down, positive values speed it up.")
        pitch = st.slider("Pitch", -50, 50, 0, help="Adjust the pitch of the speech. Negative values lower the pitch, positive values raise it.")
        ssml_text = st.text_area("SSML Input", value="Hello, welcome to the Azure AI Speech Services lab!")
        ssml_input = f"""
            <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
                <voice name='{selected_voice}'>
                    <prosody rate='{rate}%' pitch='{pitch}Hz'>{ssml_text}</prosody>
                </voice>
            </speak>
        """
        if st.button("Synthesize Speech with SSML"):
            if speech_key and speech_region:
                text_to_speech_ssml(ssml_input, speech_key, speech_region)
            else:
                st.error("Please provide both subscription key and region.")
    else:
        text_input = st.text_area("Enter text to synthesize", "Hello, welcome to the Azure AI Speech Services lab!")

        if st.button("Synthesize Speech"):
            if speech_key and speech_region:
                try:
                    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
                    speech_config.speech_synthesis_voice_name = selected_voice
                    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
                    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

                    # Synthesize the speech directly
                    result = speech_synthesizer.speak_text_async(text_input).get()

                    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                        st.success("Speech synthesized successfully!")
                    elif result.reason == speechsdk.ResultReason.Canceled:
                        st.error(f"Speech synthesis canceled: {result.cancellation_details.reason}")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
            else:
                st.error("Please provide both subscription key and region.")

# Speech-to-Text tab
with tab2:
    st.header("Speech-to-Text")

    def recognize_from_microphone():
        try:
            speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
            audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

            st.info("Listening... Please start speaking.")
            result = speech_recognizer.recognize_once()

            if result.reason == speechsdk.ResultReason.RecognizedSpeech:
                st.success("Speech recognized successfully!")
                st.write(f"Transcribed Text: {result.text}")
            elif result.reason == speechsdk.ResultReason.NoMatch:
                st.error("No speech could be recognized.")
            elif result.reason == speechsdk.ResultReason.Canceled:
                st.error(f"Speech recognition canceled: {result.cancellation_details.reason}")
                st.error(f"Error details: {result.cancellation_details.error_details}")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    if st.button("Start Speaking"):
        if not speech_key or not speech_region:
            st.error("Please provide your Azure Speech Service API key and region.")
        else:
            recognize_from_microphone()