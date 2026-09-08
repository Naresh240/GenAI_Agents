# AI Agent – Ollama Setup on Windows

This guide explains how to install **Ollama**, download the **Llama 3.2** model, and run it locally on Windows as the foundation for a AI Agent.

## Prerequisites

* Windows 10/11
* Internet connection
* PowerShell or Command Prompt
* Sufficient disk space for the Llama model

## 1. Download Ollama for Windows

Download Ollama from the official website:

https://ollama.com/download/windows

Download the Windows installer and save it to your machine.

## 2. Install Ollama

Run the downloaded installer and follow the installation steps.

After installation, open **PowerShell** or **Command Prompt** and verify the installation:

```powershell
ollama --version
```

You should see the installed Ollama version.

## 3. Download Llama 3.2

Pull the Llama 3.2 model using:

```powershell
ollama pull llama3.2
```

This downloads the model locally to your machine.

To verify the downloaded models:

```powershell
ollama list
```

Expected output will contain something similar to:

```text
NAME              ID              SIZE
llama3.2          ...             ...
```

## 4. Run Llama 3.2

Start the model with:

```powershell
ollama run llama3.2
```

You can now interact with the model directly.

Example:

```text
>>> What is Kubernetes?
```

To exit:

```text
/bye
```

## 5. Verify Ollama is Running

Ollama normally runs as a local service.

The default API endpoint is:

```text
http://localhost:11434
```

You can verify the API from PowerShell:

```powershell
curl http://localhost:11434/api/tags
```

Or:

```powershell
Invoke-WebRequest http://localhost:11434/api/tags
```

## 6. AI Agent Architecture

Once Ollama and Llama 3.2 are running, the Python application can use Ollama as the local LLM.

```text
                    Windows Machine
                         |
                         v
                      Ollama
                         |
                         v
                    Llama 3.2
                         |
                         v
                  +--------------+
                  |  AI Agent |
                  +--------------+
                    /    |     \
                   /     |      \
                  v      v       v
              GitHub   Jenkins  Kubernetes
                               
                         |
                         v
                         AWS / Cloud
```

## 7. Basic Ollama Commands

### Check Ollama version

```powershell
ollama --version
```

### List available models

```powershell
ollama list
```

### Pull a model

```powershell
ollama pull llama3.2
```

### Run a model

```powershell
ollama run llama3.2
```

### Remove a model

```powershell
ollama rm llama3.2
```

### Show running models

```powershell
ollama ps
```

## 8. Next Step – Build the AI Agent

The next step is to create a Python application that communicates with Ollama.

For example:

```text
User
  |
  v
AI Agent
  |
  +----> Ollama / Llama 3.2
  |
  +----> GitHub
  |
  +----> Jenkins
  |
  +----> Kubernetes
  |
  +----> AWS
```

The agent can then be designed to:

1. Read a GitHub issue
2. Analyze the issue using Llama 3.2
3. Inspect the source code
4. Identify the likely root cause
5. Generate a code fix
6. Create a Git branch
7. Commit the changes
8. Push the branch to GitHub
9. Trigger Jenkins
10. Analyze the build/test results
11. Report the result to the user

## Summary

The basic setup is:

```powershell
# Verify Ollama
ollama --version

# Download Llama 3.2
ollama pull llama3.2

# Run Llama 3.2
ollama run llama3.2

# List installed models
ollama list
```

After this setup, Ollama provides the local LLM runtime that can be integrated into the AI Agent.
