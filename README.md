# Local AI Coding Assistant

A lightweight, developer-focused web user interface built with Streamlit that hooks directly into your locally running LLMs via LM Studio. 

## Features
- **Interactive Chat:** Converse with a local LLM fine-tuned for code tasks.
- **Code Explanation:** Breakdown code syntax and paradigms automatically.
- **Bug Finder:** Locate security flaws, logic mistakes, or performance bottlenecks.
- **Optimization Suggestions:** Refactor your scripts for better execution speed and clarity.
- **File Uploader:** Directly read and feed existing source scripts into the chat workflow.

## Prerequisites

1. **Download & Install LM Studio:** [https://lmstudio.ai/](https://lmstudio.ai/)
2. **Download the Model:** Open LM Studio, search for `Qwen3-8B` (or `Qwen2.5-Coder-7B`), and download it.
3. **Start the Local Server:**
   - Go to the **Local Server** tab (developer icon on the left panel).
   - Select your downloaded model from the top dropdown menu.
   - Click **Start Server**. Verify that the server endpoint shows `http://localhost:1234`.

## Installation & Setup

1. **Clone or navigate to the project directory:**
   ```bash
   cd /path/to/your/project-folder
