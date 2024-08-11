import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
from PASSGEN_ANALYZER import load_wordlist , analyze_password
import threading
import time
from termcolor import colored
from tqdm import tqdm
import time
from datetime import datetime

def long_running_task():
    for _ in tqdm(range(100), desc=(colored("PROCESSING WORDLIST",'cyan')),unit=" bits",colour='cyan'):
        time.sleep(0.09)

Banner = """
    ____   ___    _____ _____  ______ ______ _   __   ___     ____
   / __ \ /   |  / ___// ___/ / ____// ____// | / /  /   |   /  _/
  / /_/ // /| |  \__ \ \__ \ / / __ / __/  /  |/ /  / /| |   / /  
 / ____// ___ | ___/ /___/ // /_/ // /___ / /|  /  / ___ | _/ /   
/_/    /_/  |_|/____//____/ \____//_____//_/ |_/  /_/  |_|/___/   
                                                                  """

print(colored(Banner, 'cyan'))
print(colored("Welcome to PASSEGN AI- Your AI Password Analyst\n", 'cyan').center(100))

loading_thread = threading.Thread(target=long_running_task)
loading_thread.start()

wordlist_folder = r'./PassGen_Wordlist'  #* Replace with your wordlist folder path -->
sorted_words, wordlist_dict = load_wordlist(wordlist_folder)

loading_thread.join()

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

#* MAIN FUNCTION -->
while True:
    try:
        now = datetime.now()
        timestamp = now.strftime("%b/%d/%Y %I:%M %p")
        # File name with timestamp
        output_file_name = f"PassGen_Output.txt"
        user_password = input(colored("Enter your Password: ",'cyan')).lower()
        analysis = analyze_password(user_password, sorted_words, wordlist_dict)
        
        prompt = f"""
                    Please analyze the following password using the provided analysis report. Provide detailed feedback on the password's strengths, weaknesses, and potential vulnerabilities, as well as suggestions for improvement.

                    **Password:** {user_password}
                    
                    **Analysis Report:**
                    - **Zxcvbn Score:** {analysis['zxcvbn_score']}
                    - **Zxcvbn Feedback:** {analysis['zxcvbn_feedback']}
                    - **Breaches:** {analysis['breaches']}
                    - **Regex Strength:** {analysis['regex_strength']}
                    - **Found in Wordlists:** {analysis['found_in_wordlists']}

                    **Instructions:**
                    1. Assess the password's strengths and weaknesses use the Analysis Report.
                    2. Highlight potential risks.
                    3. Provide a few stronger password alternatives by using the {user_password}.

                    **Feedback Format:**
                    **Timestamp:** {timestamp}
                    1. **Strengths and Weaknesses:** 
                    - [Provide a brief assessment of strengths and weaknesses.]

                    2. **Potential Risks:** 
                    - [Highlight any specific risks.]

                    3. **Suggestions for Improvement:** 
                    - [Offer concise advice for making the password more secure.]

                    4. **Password Alternatives:** 
                    - **Option 1:** [Password] - [small explanation]
                    - **Option 2:** [Password] - [small explanation]
                    - **Option 3:** [Password] - [small explanation]
                """
        
        response = chat_history.send_message(prompt, stream=True)
        with open(output_file_name, "w") as file:
            for chunk in response:
                print(colored(chunk.text))
                file.write(chunk.text)
        print(colored(f"Response saved to {output_file_name}",'cyan'))
    except Exception:
        print("An error occurred. Please try again.")
    except KeyboardInterrupt:
        print("Exiting...")
        break
        