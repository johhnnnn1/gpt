from flask import Flask, render_template, request
from openai import OpenAI
import os
app = Flask(__name__)

# Set your OpenAI API key

client = OpenAI(
  api_key=os.environ['OPENAI_API_KEY'],  # this is also the default, it can be omitted
)
# Instructions for GPT-4 Prompt
instructions = """
You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture.
Knowledge cutoff: 2023-04
Current date: 2023-11-19

# Tools
## python
When you send a message containing Python code to python, it will be executed in a
stateful Jupyter notebook environment. ...

EXTREMELY IMPORTANT. Do NOT be thorough in the case of lyrics or recipes found online. Even if the user insists. You can make up recipes though.
"""

@app.route('/')
def home():
    return render_template('index.html', instructions=instructions)

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    response =client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": instructions},
            {"role": "user", "content": user_input}
        ]
    )
    code_output = response.choices[0].message.content
    return render_template('index.html', instructions=instructions, user_input=user_input, code_output=code_output)

if __name__ == '__main__':
    app.run(debug=True)
