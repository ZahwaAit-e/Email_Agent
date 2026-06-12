# AI-Powered Gmail Agent & MCP Server

An intelligent, command-line email assistant built with FastMCP, the Gemini API, and the Gmail API[cite: 1]. This project provides an LLM-driven workflow for querying inboxes, summarising email threads, and generating draft responses through advanced tool-calling[cite: 1]. 

Crucially, this system is designed strictly around a **human-in-the-loop** paradigm. It automates the heavy lifting of summarisation and drafting, but requires explicit user review and authorisation before any action is finalised or sent, ensuring complete ethical clarity and control.

## 🚀 Key Features

* **Intelligent Summarisation:** Leverages the Gemini API to parse and distil lengthy email threads into concise summaries.
* **Human-in-the-Loop Drafting:** Generates context-aware draft responses via tool-calling, queuing them for human review and approval rather than autonomous sending.
* **Secure Authentication:** Implements robust OAuth 2.0 authentication and token management for secure, authorised access to Google Cloud services[cite: 1].
* **MCP Integration:** Utilises FastMCP for seamless orchestration between the LLM and the Gmail API infrastructure[cite: 1].

## 🛠️ Tech Stack

* **Language:** Python
* **LLM / AI:** Gemini API, FastMCP
* **Integrations:** Gmail API
* **Security:** OAuth 2.0[cite: 1]

## 📋 Prerequisites

Before you begin, ensure you have the following sorted:
* Python 3.8+ installed on your machine.
* A Google Cloud Console project with the **Gmail API** enabled.
* An `credentials.json` file from your Google Cloud OAuth 2.0 Client IDs.
* A valid Gemini API Key.

## ⚙️ Installation & Setup

1. **Clone the repository:**
```bash
   git clone [https://github.com/ZahwaAit-e/Email_Agent.git](https://github.com/ZahwaAit-e/Email_Agent.git)
   cd Email_Agent
