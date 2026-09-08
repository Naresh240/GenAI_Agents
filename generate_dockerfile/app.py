import os
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2"

# Read application name and prompt from file
with open("prompt.txt", "r", encoding="utf-8") as file:
    content = file.read()

# Split application_name and prompt
application_name = ""
prompt_lines = []
reading_prompt = False

for line in content.splitlines():

    if line.startswith("application_name="):
        application_name = line.split("=", 1)[1].strip()
        continue

    if line.startswith("prompt="):
        reading_prompt = True
        continue

    if reading_prompt:
        prompt_lines.append(line)

prompt = "\n".join(prompt_lines).strip()

if not application_name:
    raise ValueError("application_name is missing in prompt.txt")

if not prompt:
    raise ValueError("prompt is missing in prompt.txt")

# Call Ollama
response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }
)

response.raise_for_status()

dockerfile = response.json()["response"]

# Create application-specific directory
output_dir = os.path.join("generated", application_name)
os.makedirs(output_dir, exist_ok=True)

# Save Dockerfile
dockerfile_path = os.path.join(output_dir, "Dockerfile")

with open(dockerfile_path, "w", encoding="utf-8") as file:
    file.write(dockerfile)

print(f"Dockerfile generated successfully: {dockerfile_path}")
