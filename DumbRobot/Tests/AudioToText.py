from openai import OpenAI
client = OpenAI(api_key="sk-svcacct-dO8EKFhbR50o0EwRjz3r80imib9nqTaaeUPcZAr9BwmW08iHhTuQpq9f8xDxGT3BlbkFJ3Ee55z90UJH73WocK3DrPwMCgiIL7hk3l4vWo6wmNTlpYdRL9TLv9Dk8oyxoAA")

audio_file= open("dog.wav", "rb")
transcription = client.audio.transcriptions.create(
model="whisper-1", 
file=audio_file
)
print(transcription.text)