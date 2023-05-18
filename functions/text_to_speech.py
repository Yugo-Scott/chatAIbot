import requests
from decouple import config

ELEVEN_LABS_API_KEY=config("ELEVEN_LABS_API_KEY")

# Eleven Labs
# Convert text to speech
def convert_text_to_speech(message):
  # define data
  body = {
    "text": message, "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0,
        "similarity_boost": 0
    }
  }
# define voice
  voice_domi = "AZnzlk1XvdvUeBnXmlld"

  # Construct request headers and url
  headers = { "xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type": "application/json", "accept": "audio/mpeg" }
  endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_domi}"

# Make request
  try:
    response = requests.post(endpoint, json=body, headers=headers)
    print(response)
  except Exception as e:
     return
  if response.status_code == 200:
    return response.content
  else:
    return