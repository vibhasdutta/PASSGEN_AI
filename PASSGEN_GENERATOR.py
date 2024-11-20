import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json



def read_questions_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    categories = {}
    current_category = None

    for line in lines:
        line = line.strip()
        if line.startswith('/c'):
            current_category = line[2:].strip()
            categories[current_category] = []
        elif line.startswith('/q') and current_category:
            question = line[2:].strip()
            categories[current_category].append(question)

    return categories

def collect_answers(categories):
    answers = []

    for category, questions in categories.items():
        print(f"Category: {category}")
        for question in questions:
            print(question)
            answer = input("Your answer: ")
            answers.append(answer)

    return answers

def Gather_info():
    #* Load the JSON data from a file -->
    with open('config.json', 'r') as file:
        config = json.load(file)

    #* Accessing the API Key -->
    genai.configure(api_key=config['API']['API_KEY'])

    #* Accessing the Generation Config -->
    generation_config = config['generation_config']

    #* Set Gemini Model Safety Settings -->
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }

    #* Gemini Model Settings -->
    model = genai.GenerativeModel('gemini-1.5-flash',system_instruction="You are a Paswword Analyist. And your name is PASSGEN",generation_config=generation_config,safety_settings=safety_settings)

    #* Chat history -->
    chat_history = model.start_chat(history=[])


    print("In which category do you want to ask the question?")
    categories = input("Seperate the categories with a comma: ")
    categories = categories.split(",")
    prompt = """Generate meaningfull Questions for the following categories whoes answers should be one word long.:
    categories: {}
    and each category should have 5 questions.
    format:
    /c catergory name
    /q questions
    """.format(categories)
    response = chat_history.send_message(prompt, stream=True)
    output_file_name = f"Question.txt"
    with open(output_file_name, "w") as file:
        for chunk in response:
            file.write(chunk.text)
    categories = read_questions_from_file(output_file_name)
    answers = collect_answers(categories)
    return answers
