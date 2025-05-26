from commitizen.cz.base import BaseCommitizen
import openai
import subprocess

# Authenticate with OpenAI API
openai.api_key = "YOUR_API_KEY_HERE"

class Cz_aiCz(BaseCommitizen):
    def questions(self) -> list:
        return [
            {
                "type": "input",
                "name": "openai_api_key",
                "message": "Please enter your OpenAI API Key:",
                "default": "",
            },
        ]

    def message(self, answers: dict) -> str:
        print("Generating commit message using OpenAI's GPT-3...")
        print(f"answers: {answers}")
        git_diff = subprocess.check_output(["git", "diff"])

        # Check if diff length is too large
        if len(git_diff) > 8000:
            print("The diff is too large to write a commit message.")
            exit()

        # Prepare prompt for OpenAI in Conventional Commits style
        prompt = f"Please generate a commit message in Conventional Commits style for the following changes:\n\n{git_diff.decode('utf-8')}\n\nType 'feat' for a new feature, 'fix' for a bug fix, 'docs' for documentation updates, 'style' for code style changes, 'refactor' for code refactoring, 'test' for test updates, 'chore' for build and tooling updates, or 'other' for any other changes:"

        # Generate text with OpenAI's GPT-3
        response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=64,
        n=1,
        stop=None,
        temperature=0.7,
        )

        # Extract the generated text from the OpenAI response
        commit_type = response.choices[0].text.strip()

        # Format the commit message using the commit type and the diff
        commit_message = f"{commit_type}: {git_diff.decode('utf-8').splitlines()[0]}"

        print(f"Generated commit message: {commit_message}")

        raise NotImplementedError("Not Implemented yet")
