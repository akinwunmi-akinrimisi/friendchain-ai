import json
import random

def load_avatar(username):
    """Load personality avatar."""
    try:
        with open(f"{username}_avatar.json", "r") as f:
            avatar = json.load(f)
        print(f"Loaded avatar for {username}")
        return avatar
    except Exception as e:
        print(f"Error loading avatar: {e}")
        return {}

def generate_trivia(avatar, username):
    """Generate 20 trivia questions from avatar using templates."""
    questions = []
    categories = {
        "Mindset": [],
        "Career": [],
        "Life Goals": [],
        "Vibe": [],
        "Online Habits": []
    }

    # Question templates
    templates = [
        # Mindset (3 questions)
        {
            "category": "Mindset",
            "questionText": f"What personality trait is {username} most known for?",
            "options": ["Openness", "Conscientiousness", "Extraversion", "Agreeableness"],
            "correctAnswer": 0
        },
        {
            "category": "Mindset",
            "questionText": f"What value does {username} prioritize most?",
            "options": ["Transparency", "Competition", "Tradition", "Security"],
            "correctAnswer": 0
        },
        {
            "category": "Mindset",
            "questionText": f"What drives {username}’s motivation?",
            "options": ["Innovation", "Stability", "Fame", "Comfort"],
            "correctAnswer": 0
        },
        # Career (5 questions)
        {
            "category": "Career",
            "questionText": f"What is {username}’s top interest?",
            "options": ["Artificial Intelligence", "Finance", "Sports", "Art"],
            "correctAnswer": 0
        },
        {
            "category": "Career",
            "questionText": f"What technology does {username} engage with?",
            "options": ["Blockchain", "Virtual Reality", "Quantum Computing", "Robotics"],
            "correctAnswer": 0
        },
        {
            "category": "Career",
            "questionText": f"What skill is {username} passionate about?",
            "options": ["Coding", "Marketing", "Design", "Writing"],
            "correctAnswer": 0
        },
        {
            "category": "Career",
            "questionText": f"Where does {username} thrive professionally?",
            "options": ["San Francisco tech scene", "Wall Street", "Hollywood", "Academic research"],
            "correctAnswer": 0
        },
        {
            "category": "Career",
            "questionText": f"What field excites {username}?",
            "options": ["Tech Events", "Fashion", "Politics", "Culinary Arts"],
            "correctAnswer": 0
        },
        # Life Goals (4 questions)
        {
            "category": "Life Goals",
            "questionText": f"What is {username}’s main goal?",
            "options": ["Build decentralized solutions", "Start a traditional business", "Become a teacher", "Travel the world"],
            "correctAnswer": 0
        },
        {
            "category": "Life Goals",
            "questionText": f"What impact does {username} want to have?",
            "options": ["Advance technology", "Preserve tradition", "Promote art", "Protect environment"],
            "correctAnswer": 0
        },
        {
            "category": "Life Goals",
            "questionText": f"What does {username} aim to build?",
            "options": ["Decentralized platforms", "Corporate empires", "Charity organizations", "Social media apps"],
            "correctAnswer": 0
        },
        {
            "category": "Life Goals",
            "questionText": f"What future does {username} envision?",
            "options": ["Decentralized internet", "Global corporation", "Sustainable cities", "Space exploration"],
            "correctAnswer": 0
        },
        # Vibe (4 questions)
        {
            "category": "Vibe",
            "questionText": f"How does {username} communicate?",
            "options": ["Enthusiastic and technical", "Formal and reserved", "Casual and humorous", "Direct and blunt"],
            "correctAnswer": 0
        },
        {
            "category": "Vibe",
            "questionText": f"What tone does {username} use in posts?",
            "options": ["Excited", "Sarcastic", "Neutral", "Critical"],
            "correctAnswer": 0
        },
        {
            "category": "Vibe",
            "questionText": f"What’s {username}’s social vibe?",
            "options": ["Tech enthusiast", "Corporate professional", "Free spirit", "Activist"],
            "correctAnswer": 0
        },
        {
            "category": "Vibe",
            "questionText": f"How would friends describe {username}’s energy?",
            "options": ["Innovative", "Conservative", "Relaxed", "Intense"],
            "correctAnswer": 0
        },
        # Online Habits (4 questions)
        {
            "category": "Online Habits",
            "questionText": f"When does {username} typically post about tech?",
            "options": ["Morning", "Afternoon", "Evening", "Late Night"],
            "correctAnswer": 2
        },
        {
            "category": "Online Habits",
            "questionText": f"What events does {username} share online?",
            "options": ["Tech Events", "Music Festivals", "Book Clubs", "Sports Games"],
            "correctAnswer": 0
        },
        {
            "category": "Online Habits",
            "questionText": f"What’s {username}’s favorite online topic?",
            "options": ["Web3", "Politics", "Travel", "Food"],
            "correctAnswer": 0
        },
        {
            "category": "Online Habits",
            "questionText": f"How often does {username} post about coding?",
            "options": ["Frequently", "Occasionally", "Rarely", "Never"],
            "correctAnswer": 0
        }
    ]

    # Shuffle and select 20 questions
    random.shuffle(templates)
    for i, template in enumerate(templates[:20], 1):
        question = {
            "questionText": template["questionText"],
            "options": template["options"],
            "correctAnswer": template["correctAnswer"],
            "category": template["category"],
            "stake_amount": 0.01,  # ETH to stake
            "reward": 0.02,  # ETH for correct answer
            "questionId": i
        }
        categories[template["category"]].append(question)
        questions.append(question)

    # Save questions to JSON
    output = {
        "username": username,
        "questions": questions,
        "categories": {k: len(v) for k, v in categories.items()}
    }
    with open(f"{username}_trivia.json", "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved {len(questions)} trivia questions to {username}_trivia.json")
    return output

if __name__ == "__main__":
    # Load avatar
    username = "alex.base"
    avatar = load_avatar(username)
    if avatar:
        # Generate trivia
        trivia = generate_trivia(avatar, username)
        # Print first 5 questions
        print(json.dumps(trivia["questions"][:5], indent=2))