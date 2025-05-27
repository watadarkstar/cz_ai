from commitizen.cz.base import BaseCommitizen
import openai
import subprocess
import json
from pathlib import Path
from prompt_toolkit import prompt

MAX_DIFF_LENGTH = 8000
MAX_TOKENS = 200
class Cz_aiCz(BaseCommitizen):
    def questions(self) -> list:
        api_key = self.get_open_ai_key()
        return [
            {
                "type": "input",
                "name": "openai_api_key",
                "message": "Please enter your OpenAI API Key:",
                "default": api_key if api_key else "",
            },
            {
                "type": "input",
                "name": "model",
                "message": "Which OpenAI model would you like to use:",
                "default": "gpt-4o-mini",
            },
        ]

    def message(self, answers: dict) -> str:
        print("Generating commit message using OpenAI's GPT-4o...")

        # Try to get API key from cache first
        cache_dir = Path.cwd() / ".commitizen"
        cache_file = cache_dir / "openai_cache.json"
        cache_api_key = self.get_open_ai_key()
        api_key = answers.get("openai_api_key")
        model = answers.get("model", "gpt-4o-mini")
        
        # Update the cache if the API key has changed
        if cache_api_key != api_key and api_key:
            with open(cache_file, 'w') as f:
                json.dump({'openai_api_key': api_key}, f)

        # Authenticate with OpenAI API
        openai.api_key = api_key

        print(f"Using OpenAI API Key: {openai.api_key}\n\n")

        git_diff = subprocess.check_output(["git", "diff", "--staged"])

        print(f"Git diff: {git_diff}\n\n")

        # Check if diff length is too large
        if len(git_diff) > MAX_DIFF_LENGTH:
            print("The diff is too large to write a commit message.")
            exit()

        # Prepare prompt for OpenAI in Conventional Commits style
        ai_prompt = f"Please generate a commit message in Conventional Commits style for the following changes:\n\n{git_diff.decode('utf-8')}\n\nType 'feat' for a new feature, 'fix' for a bug fix, 'docs' for documentation updates, 'style' for code style changes, 'refactor' for code refactoring, 'test' for test updates, 'chore' for build and tooling updates, or 'other' for any other changes:"

        # Generate text with OpenAI's GPT-4o
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates commit messages in Conventional Commits style. Do not include any markdown."},
                {"role": "user", "content": ai_prompt}
            ],
            max_tokens=MAX_TOKENS,
            temperature=0.7,
            n=3  # Generate 5 different responses
        )

        # Display all available choices
        print("Available commit messages:")
        for i, choice in enumerate(response.choices):
            print(f"\n{i + 1}. {choice.message.content}")
        
        # Ask user to select a message
        commit_message = None
        while True:
            try:
                selection = int(input("\nPlease select a commit message (enter number) [1]: ") or "1")
                if 1 <= selection <= len(response.choices):
                    commit_message = response.choices[selection - 1].message.content
                    break
                else:
                    print(f"Please enter a number between 1 and {len(response.choices)}")
            except ValueError:
                print("Please enter a valid number")
        
        print(f"\nSelected commit message:\n\n{commit_message}\n\n")
        
        # Ask user if they want to accept the message
        response = input("Is this auto-generated commit message OK? (Y/n): ").lower()
        
        if response == 'n':
            # Let user modify the message
            modified_message = prompt("Please enter your modified commit message: ", default=commit_message)
            return modified_message.strip()
            
        return commit_message.strip()
    
    def get_open_ai_key(self):
        cache_dir = Path.cwd() / ".commitizen"
        cache_file = cache_dir / "openai_cache.json"
        
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True, exist_ok=True)
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                cache = json.load(f)
                return cache.get('openai_api_key')
        return None
