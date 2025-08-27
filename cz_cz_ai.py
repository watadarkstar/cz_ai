from commitizen.cz.base import BaseCommitizen
import openai
import subprocess
import json
from pathlib import Path
from prompt_toolkit import prompt
import requests
import re

MAX_DIFF_LENGTH = 8000
MAX_TOKENS = 200

class Cz_aiCz(BaseCommitizen):
    def get_ollama_models(self) -> list:
        try:
            response = requests.get("http://localhost:11434/api/tags")
            response.raise_for_status()
            models_data = response.json().get("models", [])
            return [model["name"] for model in models_data]
        except requests.exceptions.ConnectionError:
            print("\nWarning: Could not connect to Ollama to fetch model list.")
            return []
        except Exception as e:
            print(f"\nWarning: An error occurred while fetching Ollama models: {e}")
            return []

    def questions(self) -> list:
        api_key = self.get_open_ai_key()
        
        questions = [
            {
                "type": "list",
                "name": "ai_provider",
                "message": "Which AI provider would you like to use?",
                "choices": ["openai", "ollama"],
                "default": "openai",
            },
            {
                "type": "input",
                "name": "openai_api_key",
                "message": "Please enter your OpenAI API Key:",
                "default": api_key if api_key else "",
                "when": lambda answers: answers.get("ai_provider") == "openai",
            }
        ]

        ollama_models = self.get_ollama_models()
        
        if ollama_models:
            model_question = {
                "type": "list",
                "name": "model",
                "message": "Which Ollama model would you like to use:",
                "choices": ollama_models,
                "when": lambda answers: answers.get("ai_provider") == "ollama",
            }
        else:
            model_question = {
                "type": "input",
                "name": "model",
                "message": "Which model would you like to use (Ollama connection failed):",
                "default": "llama3",
                "when": lambda answers: answers.get("ai_provider") == "ollama",
            }
        
        questions.append(model_question)

        questions.append({
            "type": "input",
            "name": "model",
            "message": "Which OpenAI model would you like to use:",
            "default": "gpt-4o-mini",
            "when": lambda answers: answers.get("ai_provider") == "openai",
        })

        return questions

    def message(self, answers: dict) -> str:
        provider = answers.get("ai_provider")
        model = answers.get("model")
        
        print(f"Generating commit message using {provider} with model {model}...")

        git_diff = subprocess.check_output(["git", "diff", "--staged"])
        decoded_diff = git_diff.decode('utf-8')

        if len(git_diff) > MAX_DIFF_LENGTH:
            print("The diff is too large to write a commit message.")
            exit()

        if provider == "openai":
            api_key = answers.get("openai_api_key")
            self.handle_openai_cache(api_key)
            openai.api_key = api_key
            commit_message = self.get_openai_commit_message(model, decoded_diff)
        elif provider == "ollama":
            commit_message = self.get_ollama_commit_message(model, decoded_diff)
        else:
            print("Invalid AI provider selected.")
            exit()

        print(f"\nSelected commit message:\n\n{commit_message}\n\n")
        
        response = input("Is this auto-generated commit message OK? (Y/n): ").lower()
        
        if response == 'n':
            modified_message = prompt("Please enter your modified commit message: ", default=commit_message)
            return modified_message.strip()
            
        return commit_message.strip()

    def get_openai_commit_message(self, model, diff_text):
        system_prompt = "You are an expert at writing Conventional Commits. Your response must be only the raw text of the commit message. You never include explanations or markdown formatting."
        user_prompt = f"Generate a Conventional Commit message for the following git diff:\n\n{diff_text}"
        
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=MAX_TOKENS,
            temperature=0.7,
            n=3
        )

        print("Available commit messages:")
        for i, choice in enumerate(response.choices):
            print(f"\n{i + 1}. {choice.message.content}")
        
        while True:
            try:
                selection = int(input("\nPlease select a commit message (enter number) [1]: ") or "1")
                if 1 <= selection <= len(response.choices):
                    return response.choices[selection - 1].message.content
                else:
                    print(f"Please enter a number between 1 and {len(response.choices)}")
            except ValueError:
                print("Please enter a valid number")

    def clean_ollama_response(self, raw_text: str) -> str:
        """
        Finds the start of the conventional commit and discards any preceding text.
        """
        commit_types = [
            "feat", "fix", "docs", "style", "refactor", "test", "chore",
            "build", "ci", "perf", "revert"
        ]
        # Create a regex pattern to find a line starting with a commit type.
        types_pattern = "|".join(commit_types)
        regex = re.compile(rf"^\s*({types_pattern})(\(.*\))?:", re.MULTILINE)

        match = regex.search(raw_text)

        if match:
            return raw_text[match.start():].strip()
        
        return raw_text.strip()

    def get_ollama_commit_message(self, model, diff_text):
        system_prompt = (
            "You are an expert at writing Conventional Commits. Your task is to create a commit message that has a subject line and a detailed body. "
            "The format must be: `<type>(<scope>): <subject>\n\n<detailed body explaining the why and how>`. "
            "Your entire response must be ONLY the raw text of this commit message. Do not include any other explanations."
        )
        user_prompt = f"Generate a Conventional Commit message with a subject and a detailed body for the following git diff:\n\n{diff_text}"

        try:
            response = requests.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "stream": False,
                    "options": {
                        "temperature": 0.7
                    }
                },
                timeout=60
            )
            response.raise_for_status()
            
            response_data = response.json()
            raw_response = response_data.get("message", {}).get("content", "").strip()
            
            return self.clean_ollama_response(raw_response)

        except requests.exceptions.ConnectionError:
            print("\nError: Could not connect to Ollama.")
            print("Please ensure Ollama is running on your local machine at http://localhost:11434")
            exit()
        except requests.exceptions.RequestException as e:
            print(f"\nAn error occurred with Ollama: {e}")
            exit()
    
    def get_open_ai_key(self):
        cache_dir = Path.cwd() / ".commitizen"
        cache_file = cache_dir / "openai_cache.json"
        
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                try:
                    cache = json.load(f)
                    return cache.get('openai_api_key')
                except json.JSONDecodeError:
                    return None
        return None

    def handle_openai_cache(self, new_api_key):
        cache_dir = Path.cwd() / ".commitizen"
        cache_file = cache_dir / "openai_cache.json"
        cached_key = self.get_open_ai_key()

        if cached_key != new_api_key and new_api_key:
            with open(cache_file, 'w') as f:
                json.dump({'openai_api_key': new_api_key}, f)
