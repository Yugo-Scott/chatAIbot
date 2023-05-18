import json
import random

# Save messages for retrieval later on
def get_recent_messages():

  # Define the file name
  file_name = "stored_data.json"
  learn_instruction = {"role": "system", 
                       "content": "You are a Arabic teacher and your name is Nadia, the user is called Yugo. Keep responses under 35 words. "}
  
  # Initialize messages
  messages = []

  # Add Random Element
  x = random.uniform(0, 1)
  if x < 0.2:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will have some light humour. "
  elif x < 0.5:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will include an interesting new fact about Middle east. "
  else:
    learn_instruction["content"] = learn_instruction["content"] + "Your response will recommend another word to learn. "
  # Append instruction to message
  messages.append(learn_instruction)

  # get last message
  try:
    with open(file_name) as user_file:
      data = json.load(user_file)
      if data:
        if len(data) < 3:
          for item in data:
            messages.append(item)
        else:
          for item in data[-2:]:
            messages.append(item)
  except Exception as e:
    print(e)
    pass
  # return messages
  return messages

# Save messages for retrieval later on
# excluding message from system role
def store_messages(request_message, response_message):
  # Define the file name
  file_name = "stored_data.json"
  # Get recent messages
  messages = get_recent_messages()[1:]
  # Add messages to data
  user_message = {"role": "user", "content": request_message}
  assistant_message = {"role": "assistant", "content": response_message}
  messages.append(user_message)
  messages.append(assistant_message)
    # Save the updated file as json
  with open(file_name, "w") as f:
    json.dump(messages, f)

# reset messages
def reset_messages():
  # Define the file name
  file_name = "stored_data.json"
  # overwrite current file with nothing
  open(file_name, "w")