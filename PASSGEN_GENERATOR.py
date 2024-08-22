from termcolor import colored

def gather_user_info():
    user_info = {}
    
     # Interests
    print("We'd love to know more about your interests to personalize your experience:")
    
    # Favorite Foods
    foods = input("List your favorite foods (separated by commas): ")
    user_info['favorite_foods'] = [food.strip() for food in foods.split(',')]
    
    # Favorite Movies
    movies = input("List your favorite movies (separated by commas): ")
    user_info['favorite_movies'] = [movie.strip() for movie in movies.split(',')]
    
    # Hobbies
    hobbies = input("List your hobbies or activities you enjoy (separated by commas): ")
    user_info['hobbies'] = [hobby.strip() for hobby in hobbies.split(',')]
    
    # Favorite Sports
    sports = input("List your favorite sports (separated by commas): ")
    user_info['favorite_sports'] = [sport.strip() for sport in sports.split(',')]
    
    # Favorite Travel Destinations
    destinations = input("List your favorite travel destinations (separated by commas): ")
    user_info['favorite_destinations'] = [destination.strip() for destination in destinations.split(',')]
    
    # Profession Identification
    print("\nTo better understand your background, please provide some details about your professional life.")
    
    # Asking for profession and roles
    profession = input("What is your primary profession or field of study? (e.g., Software Developer, Doctor, Student): ")
    user_info['profession'] = profession
    
    # Specific roles within the profession
    if profession.lower() in ['technology', 'healthcare', 'education', 'business', 'arts', 'gaming']:
        role = input(f"What is your specific role or focus within {profession}? (e.g., Front-end Developer, Nurse, Teacher, Marketing Manager): ")
        user_info['specific_role'] = role
    elif profession.lower() == 'gaming':
        platforms = input("Which gaming platforms do you use? (e.g., PC, Xbox, PlayStation): ")
        games = input("List your favorite games (separated by commas): ")
        genres = input("What are your favorite gaming genres? (e.g., RPG, FPS, Strategy): ")
        user_info['gaming_info'] = {'platforms': platforms, 'favorite_games': [game.strip() for game in games.split(',')], 'genres': genres}
    else:
        other_field = input("Please describe your field or profession: ")
        user_info['other_field'] = other_field


    return user_info

def PasswordGen(userinfo: dict):
    specific_fields = ""
    for key, value in userinfo.get('specific_fields', {}).items():
        specific_fields += f"- {key.replace('_', ' ').title()}: {value}\n"
    
    Website = input("Enter the name of the website for which you are Generating Password: ")

    prompt = f"""
    You are a password generation assistant. Based on the following information provided, generate a secure and memorable password:

    **User Information Data Set:**
    - Data Set A: {', '.join(userinfo.get('favorite_foods', []))}
    - Data Set B: {', '.join(userinfo.get('favorite_movies', []))}
    - Data Set C: {', '.join(userinfo.get('hobbies', []))}
    - Data Set D: {', '.join(userinfo.get('favorite_sports', []))}
    - Data Set E: {', '.join(userinfo.get('favorite_destinations', []))}
    - Professions: {', '.join(userinfo.get('professions', []))}
    - Additional Data:
    {specific_fields}

    **Website Type:** The website is a {Website}. Based on this, select the most relevant data sets to create a password.

    Generate 10 passwords adhering to the following advanced criteria:
    - Length: Each password must be at least 12 characters long, providing robust security while balancing user memorability.

    - Special Characters: Integrate 2 to 4 special characters, strategically placed throughout the password, with at least one positioned in the middle (e.g., !, @, #, $, %, ^, &, *). Ensure these characters disrupt common patterns and enhance unpredictability.

    - Numbers: Include 2 to 4 numbers, distributed unevenly within the password to avoid obvious sequences, further complicating brute-force attempts.

    - Complexity: Implement a sophisticated mix of uppercase and lowercase letters, avoiding simple capitalization rules (e.g., not just the first letter) and ensuring a random distribution to thwart pattern recognition.

    - Relevance: Analyze the website type and intelligently select the most relevant user data sets. For instance, for a streaming service like Netflix, prioritize integrating elements related to movies, travel, and the user's profession to create passwords that are both meaningful and secure.

    - Entropy Maximization: Design each password to maximize entropy, ensuring no two passwords share more than three consecutive characters or follow similar structural patterns.

    - Unpredictability: Each password should be unique and resilient against common attack vectors, such as dictionary attacks, by avoiding easily guessable phrases, repetitions, or common keyboard paths.

    - No Explanation: Provide only the passwords without any context or reasoning behind their construction, ensuring that the focus remains solely on the output.
    """

    return prompt, Website

