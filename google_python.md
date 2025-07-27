Transcribe a local file with auto punctuation

bookmark_border
Transcribe a local audio file, including auto punctuation.

Explore further
For detailed documentation that includes this code sample, see the following:

Get automatic punctuation
Code sample
Go
Java
Node.js
PHP
Python
Ruby
To learn how to install and use the client library for Speech-to-Text, see Speech-to-Text client libraries. For more information, see the Speech-to-Text Python API reference documentation.

To authenticate to Speech-to-Text, set up Application Default Credentials. For more information, see Set up authentication for a local development environment.





from google.cloud import speech


def transcribe_file_with_auto_punctuation(audio_file: str) -> speech.RecognizeResponse:
    """Transcribe the given audio file with auto punctuation enabled.
    Args:
        audio_file (str): Path to the local audio file to be transcribed.
    Returns:
        speech.RecognizeResponse: The response containing the transcription results.
    """
    client = speech.SpeechClient()

    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=8000,
        language_code="en-US",
        # Enable automatic punctuation
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    for i, result in enumerate(response.results):
        alternative = result.alternatives[0]
        print("-" * 20)
        print(f"First alternative of result {i}")
        print(f"Transcript: {alternative.transcript}")

    return response