import os
import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "llama3.2"

JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")
# JENKINS_USER = "admin"
# JENKINS_TOKEN = "11d115ec652f2857ba7a425c154418976d"


if not JENKINS_USER or not JENKINS_TOKEN:
    raise ValueError("Jenkins credentials are not set")

def read_config(filename):
    config = {}
    prompt_lines = []
    reading_prompt = False

    with open(filename, "r", encoding="utf-8") as file:
        for line in file:

            line = line.rstrip()

            if line.startswith("prompt:"):
                reading_prompt = True
                continue

            if not reading_prompt and ":" in line:
                key, value = line.split(":", 1)
                config[key.strip()] = value.strip()

            elif reading_prompt:
                prompt_lines.append(line)

    config["prompt"] = "\n".join(prompt_lines).strip()

    return config


# Read configuration
config = read_config("prompt.txt")

jenkins_url = config["jenkins_url"]
job_name = config["job_name"]
build_number = config["build_number"]
application_name = job_name
prompt = config["prompt"]


# Get Jenkins Console Output
console_url = (
    f"{jenkins_url}/job/{job_name}/{build_number}/consoleText"
)

response = requests.get(
    console_url,
    auth=(JENKINS_USER, JENKINS_TOKEN)
)

response.raise_for_status()

console_output = response.text


# Send console output to Ollama
final_prompt = f"""
{prompt}

Application Name:
{application_name}

Jenkins Console Output:
-----------------------
{console_output}
-----------------------
"""

print("Sending console output to Ollama...")

response = requests.post(
    OLLAMA_URL,
    json={
        "model": MODEL,
        "prompt": final_prompt,
        "stream": False
    }
)

response.raise_for_status()

analysis = response.json()["response"]


# Create output directory
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)


# Save AI analysis
output_file = os.path.join(
    output_dir,
    f"{application_name}-build-{build_number}-analysis.txt"
)

with open(output_file, "w", encoding="utf-8") as file:
    file.write(analysis)


print(f"\nAI analysis saved to: {output_file}")
