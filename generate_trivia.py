import json
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import random

# Load T5 model and tokenizer
tokenizer = T5Tokenizer.from_pretrained("valhalla/t5-base-qg-hl")
model = T5ForConditionalGeneration.from_pretrained("valhalla/t5-base-qg-hl")

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

def generate_question(prompt, options, correct_answer):
    """Generate a question using T5."""
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=100)
    question = tokenizer.decode(outputs[0], skip_special_tokens=True).capitalize()
    if not question.endswith("?"):
        question = question.rstrip(".") + "?"
    return {
        "questionText": question,
        "options": options,
        "correctAnswer": correct_answer
    }

def generate_trivia(avatar, username):
    """Generate 20 trivia questions from avatar."""
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
        # Mindset (Big 5 traits, values)
        {
            "category": "Mindset",
            "prompt": f"question: What personality trait is {username} known for based on: {avatar['description']} [HL] Openness [HL]",
            "options": ["Openness", "Conscientiousness", "Extraversion", "Agreeableness"],
            "correctAnswer": 0
        },
        {
            "category": "Mindset",
            "prompt": f"question: What value does {username} prioritize based on: {avatar['values']} [HL] Transparency [HL]",
            "options": ["Transparency", "Competition", "Tradition", "Security"],
            "correctAnswer": 0
        },
        # Career (interests)
        {
            "category": "Career",
            "prompt": f"question: What is {username}'s top interest based on: {avatar['interests']} [HL] Artificial Intelligence [HL]",
            "options": ["Artificial Intelligence", "Finance", "Sports", "Art"],
            "correctAnswer": 0
        },
        {
            "category": "Career",
            "prompt": f"question: What technology does {username} engage with based on: {avatar['interests']} [HL] Blockchain [HL]",
            "options": ["Blockchain", "Virtual Reality", "Quantum Computing", "Robotics"],
            "correctAnswer": 0
        },
        # Life Goals
        {
            "category": "Life Goals",
            "prompt": f"question: What is {username}'s main goal based on: {avatar['goals']} [HL] Build decentralized solutions [HL]",
            "options": ["Build decentralized solutions", "Start a traditional business", "Become a teacher", "Travel the world"],
            "correctAnswer": 0
        },
        # Vibe (communication style)
        {
            "category": "Vibe",
            "prompt": f"question: How does {username} communicate based on: {avatar['communication_style']} [HL] Enthusiastic and technical [HL]",
            "options": ["Enthusiastic and technical", "Formal and reserved", "Casual and humorous", "Direct and blunt"],
            "correctAnswer": 0
        },
        # Online Habits
        {
            "category": "Online Habits",
            "prompt": f"question: When does {username} typically post about tech based on their active hours?",
            "options": ["Morning", "Afternoon", "Evening", "Late Night"],
            "correctAnswer": 2  # Mocked based on tweet timestamps
        }
    ]

    # Generate 20 questions (3-4 per category)
    for _ in range(20):
        template = random.choice(templates)
        category = template["category"]
        question = generate_question(template["prompt"], template["options"], template["correctAnswer"])
        question.update({
            "category": category,
            "stake_amount": 0.01,  # ETH to stake
            "reward": 0.02,  # ETH for correct answer
            "questionId": len(questions) + 1
        })
        categories[category].append(question)
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