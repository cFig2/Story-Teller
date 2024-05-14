from flask import Flask, request, render_template, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages


@app.route('/', methods=['GET', 'POST'])
def home():
    story = None
    error = None
    if request.method == 'POST':
        print("POST request received")
        print("Form Data:", request.form)
        try:
            genre = request.form['genre']
            reader_age = request.form['reader_age']
            num_characters = int(request.form['num_characters'])
            character_names = [request.form[f'character_name_{i}'] for i in range(1, num_characters + 1)]

            prompt = construct_prompt(genre, reader_age, character_names)
            print("Constructed Prompt:", prompt)
            story = generate_story(prompt)
            print("Generated Story:", story)

            if not story:
                raise ValueError("Failed to generate story. Please try again later.")
        except Exception as e:
            error = str(e)
            flash(f"An error occurred: {error}", 'error')
            print(f"An error occurred: {error}")

    return render_template('home.html', story=story, error=error)


def construct_prompt(genre, reader_age, character_names):
    character_descriptions = ''
    for i, name in enumerate(character_names, start=1):
        character_descriptions += f"The story should include a character named {name}. "
    prompt = (
        f"Create a short one paragraph story with a conflict or moral in the {genre} genre for a reader aged {reader_age}. \n\n"
        f"{character_descriptions}"
        f"Story:"
    )
    print("Prompt:", prompt)  # Debugging print statement
    return prompt


def generate_story(prompt):
    # Mock response for testing without an API key
    print(f"Mock Prompt: {prompt}")
    return ("Once upon a time, in a land far away, there was a brave knight named John who embarked on a thrilling "
            "adventure.")
    """
    api_key = os.getenv('OPENAI_API_KEY')
    print(f"API Key: {api_key}")  # Debugging print statement
    if not api_key:
        raise EnvironmentError("No API Key found. Please set the OPENAI_API_KEY environment variable.")

    # Set up the headers with your API key
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    # Set up the data payload for the POST request
    data = {
        'model': 'gpt-3.5-turbo-instruct',
        'prompt': prompt,
        'max_tokens': 500,
        'temperature': 0.7,
        'frequency_penalty': 0.5,
        'presence_penalty': 0.5,
    }

    # Make the POST request to the OpenAI API
    response = requests.post('https://api.openai.com/v1/completions', json=data, headers=headers)
    print("Response Status Code:", response.status_code)  # Debugging print statement
    print("Response Text:", response.text)  # Debugging print statement

    if response.status_code == 200:
        result = response.json()
        print("Result:", result)  # Debugging print statement
        return result['choices'][0]['text'].strip()
    else:
        print("Error requesting response")
        return None
    """


# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
