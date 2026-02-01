# # agent_system.py

# import requests
# import json
# import re

# OLLAMA_URL = "http://localhost:11434/api/generate"
# MODEL_NAME = "gemma"

# SYSTEM_PROMPT = """
# You are an autonomous payment operations AI agent.

# CRITICAL:
# - Output ONLY raw JSON.
# - Do NOT use markdown.
# - Do NOT use ``` fences.
# - Do NOT include comments.
# - Do NOT include explanations outside JSON.

# If you output anything other than valid JSON, the system will crash.

# Allowed actions ONLY:
# DO_NOTHING
# REROUTE_<BANK>
# REDUCE_RETRIES_<BANK>
# ALERT_HUMAN
# REQUEST_HUMAN_APPROVAL_<BANK>

# Banks:
# HDFC, ICICI, SBI, AXIS, BOI, INDUSIND
# """

# class AgentSystem:
#     def __init__(self):
#         pass

#     def reason(self, state):
#         payload = {
#             "model": MODEL_NAME,
#             "prompt": self._build_prompt(state),
#             "stream": False
#         }

#         try:
#             r = requests.post(OLLAMA_URL, json=payload, timeout=60)
#             data = r.json()
#         except Exception as e:
#             print("Ollama request failed:", e)
#             return self._fallback()

#         # Extract text
#         if "response" in data:
#             raw_text = data["response"]
#         elif "message" in data and "content" in data["message"]:
#             raw_text = data["message"]["content"]
#         else:
#             print("Unknown Ollama format:", data)
#             return self._fallback()

#         # Strip markdown
#         raw_text = raw_text.strip()
#         raw_text = raw_text.replace("```json", "").replace("```", "").strip()

#         # Extract first JSON object
#         match = re.search(r"\{.*\}", raw_text, re.DOTALL)
#         if not match:
#             print("No JSON object found in LLM output")
#             print(raw_text)
#             return self._fallback()

#         json_text = match.group(0)

#         try:
#             reasoning = json.loads(json_text)
#         except Exception as e:
#             print("Still invalid JSON:")
#             print(json_text)
#             return self._fallback()

#         return reasoning

#     def _build_prompt(self, state):
#         user_input = {
#             "system_state": state
#         }

#         return f"""
# {SYSTEM_PROMPT}

# Input:
# {json.dumps(user_input, indent=2)}

# Return JSON in this exact format:
# {{
#   "anomalies": [],
#   "hypotheses": [
#     {{
#       "issuer": "",
#       "cause": "",
#       "confidence": 0.0
#     }}
#   ],
#   "recommended_actions": [
#     {{
#       "action": "",
#       "reason": ""
#     }}
#   ],
#   "explanation": ""
# }}
# """

#     def _fallback(self):
#         return {
#             "anomalies": [],
#             "hypotheses": [],
#             "recommended_actions": [
#                 {
#                     "action": "DO_NOTHING",
#                     "reason": "LLM failure"
#                 }
#             ],
#             "explanation": "Fallback triggered"
#         }


# agent_system.py

from google import genai
import json
import re
import os

# Use environment variable for safety
# setx GEMINI_API_KEY "YOUR_KEY"  (on Windows)
client = genai.Client(api_key="AIzaSyAxP8tXlyv5OtYJugbwiDR9U69iGcY-xo0")

SYSTEM_PROMPT = """
You are an autonomous payment operations AI agent.

CRITICAL:
- Output ONLY raw JSON.
- No markdown.
- No ``` fences.
- No comments.
- No explanations outside JSON.

Allowed actions ONLY:
DO_NOTHING
REROUTE_<BANK>
REDUCE_RETRIES_<BANK>
ALERT_HUMAN
REQUEST_HUMAN_APPROVAL_<BANK>

Banks:
HDFC, ICICI, SBI, AXIS, BOI, INDUSIND
"""

class AgentSystem:
    def __init__(self):
        pass

    def reason(self, state):
        prompt = self._build_prompt(state)

        try:
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
            raw_text = response.text.strip()
        except Exception as e:
            print("Gemini request failed:", e)
            return self._fallback()

        raw_text = raw_text.replace("```json", "").replace("```", "").strip()

        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if not match:
            print("No JSON object found in Gemini output")
            print(raw_text)
            return self._fallback()

        json_text = match.group(0)

        try:
            reasoning = json.loads(json_text)
        except Exception as e:
            print("Invalid JSON from Gemini:")
            print(json_text)
            return self._fallback()

        return reasoning

    def _build_prompt(self, state):
        user_input = {
            "system_state": state
        }

        return f"""
{SYSTEM_PROMPT}

Input:
{json.dumps(user_input, indent=2)}

Return JSON in this exact format:
{{
  "anomalies": [],
  "hypotheses": [
    {{
      "issuer": "",
      "cause": "",
      "confidence": 0.0
    }}
  ],
  "recommended_actions": [
    {{
      "action": "",
      "reason": ""
    }}
  ],
  "explanation": ""
}}
"""

    def _fallback(self):
        return {
            "anomalies": [],
            "hypotheses": [],
            "recommended_actions": [
                {
                    "action": "DO_NOTHING",
                    "reason": "LLM failure"
                }
            ],
            "explanation": "Fallback triggered"
        }
