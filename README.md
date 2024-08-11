# PassGen AI

This tool analyzes passwords to evaluate their strength, identify potential risks, and provide suggestions for improvement. It also generates alternative password suggestions for enhanced security.

## Features :

- **Strengths and Weaknesses Assessment:** Evaluates the provided password for its strengths and weaknesses.
- **Risk Identification:** Highlights any specific risks associated with the password.
- **Suggestions for Improvement:** Provides concise advice on how to make the password more secure.
- **Password Alternatives:** Generates alternative passwords with explanations for better securit

## Installion Guide :

1. Install the necessary packages by running:
   ```
   pip install -r requirements.txt
   ```
   or, if you're using `pip3`:
   ```
   pip3 install -r requirements.txt
   ```

2. **Configure Gemini API**

   - Open the `config.json` file located in the project directory.
   - Add your Gemini API key to the file in the following format:

     ```json
     {
       "API" : {
        "API_KEY" : "Your API KEY"
       }
     }
     ```

   *Ensure you replace `"YOUR_GEMINI_API_KEY_HERE"` with your actual Gemini API key.*

3. **Add Custom Wordlists**

   - To enhance password generation, you can add custom wordlists in the `PassGen_Wordlist` folder.
   - Place your `.txt` files containing wordlists in this directory to improve the variety and security of generated passwords.

4. Run the `PASSGEN_AI.py` script:
   ```
   python PASSGEN_AI.py
   ```
   or, if you're using `python3`:
   ```
   python3 PASSGEN_AI.py
   ```

*Note: Ensure you have Python installed on your system. If not, download it from the [official website](https://www.python.org/downloads/).*
