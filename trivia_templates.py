QUESTION_TEMPLATES = [
    {
        "questionText": "What's {username}'s secret Twitter superpower?",
        "options": ["{superpower}", "Going viral with one word", "Predicting trends", "Endless retweets"],
        "correctAnswer": 0,
        "category": "Personality"
    },
    {
        "questionText": "When is {username} most likely to tweet?",
        "options": ["Morning", "Afternoon", "Evening", "3am"],
        "correctAnswer": lambda report: 3 if "Night owl" in report["posting_style"] else 0,
        "category": "Posting Habits"
    },
    {
        "questionText": "What's {username}'s biggest vibe?",
        "options": ["Chill Vibes CEO", "Meme King/Queen", "Deep Thinker", "Chaos Agent"],
        "correctAnswer": lambda report: 1 if "Meme" in report["posting_style"] else 2,
        "category": "Vibe"
    },
    {
        "questionText": "If {username} were a movie character, what genre would they be in?",
        "options": ["Sci-Fi", "Comedy", "Drama", "Action"],
        "correctAnswer": None,
        "category": "Personality"
    },
    {
        "questionText": "What's {username}'s favorite topic to tweet about?",
        "options": ["{topic}", "Politics", "Food", "Travel"],
        "correctAnswer": 0,
        "category": "Topics"
    },
    {
        "questionText": "What's another topic {username} loves to tweet about?",
        "options": ["{secondary_topic}", "Fashion", "Sports", "Music"],
        "correctAnswer": 0,
        "category": "Topics"
    },
    {
        "questionText": "What's {username}'s hidden quirk?",
        "options": ["{quirk}", "Sings to plants", "Collects rare coins", "Talks to their code"],
        "correctAnswer": 0,
        "category": "Personality"
    },
    {
        "questionText": "What's {username}'s Twitter motto?",
        "options": ["{motto}", "Keep it real", "YOLO", "Stay curious"],
        "correctAnswer": 0,
        "category": "Personality"
    },
    {
        "questionText": "What's {username}'s posting style?",
        "options": ["{posting_style}", "One-word wonders", "Essay threads", "GIF spam"],
        "correctAnswer": 0,
        "category": "Posting Habits"
    },
    {
        "questionText": "What drives {username}'s tweets?",
        "options": ["Innovation", "Humor", "Drama", "Chill vibes"],
        "correctAnswer": lambda report: 0 if report["big5_traits"]["Openness"] >= 70 else 1,
        "category": "Personality"
    },
    {
        "questionText": "What's {username}'s Twitter nickname vibe?",
        "options": ["{nickname}", "The Silent Sage", "The Meme Machine", "The Dream Weaver"],
        "correctAnswer": 0,
        "category": "Personality"
    },
    {
        "questionText": "If {username} went viral, what would it be for?",
        "options": ["Epic thread", "Hilarious meme", "Hot take", "Tech breakthrough"],
        "correctAnswer": None,
        "category": "Vibe"
    },
    {
        "questionText": "What's {username}'s social media energy?",
        "options": ["Tech guru", "Meme maestro", "Philosopher", "Party starter"],
        "correctAnswer": None,
        "category": "Vibe"
    },
    {
        "questionText": "What's {username}'s tweet frequency vibe?",
        "options": ["Daily poster", "Ghost then flood", "Once a week", "Random bursts"],
        "correctAnswer": lambda report: 1 if "Night owl" in report["posting_style"] else 0,
        "category": "Posting Habits"
    },
    {
        "questionText": "What's {username}'s Twitter personality trait?",
        "options": ["Creative", "Organized", "Social", "Spicy"],
        "correctAnswer": lambda report: 0 if report["big5_traits"]["Openness"] >= 70 else 2,
        "category": "Personality"
    },
    {
        "questionText": "What's {username}'s ideal Twitter moment?",
        "options": ["Viral meme", "Deep thread", "Tech debate", "Chill Q&A"],
        "correctAnswer": None,
        "category": "Vibe"
    }
]