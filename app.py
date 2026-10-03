from flask import Flask, render_template, request, jsonify
import json
from pathlib import Path

app = Flask(__name__)

# Database of study materials
STUDY_DATA = {
    "history": {
        "name": "History",
        "chapters": [
            {
                "id": 1,
                "title": "The Rise of Nationalism in Europe",
                "description": "Understanding the emergence of nation-states and nationalism in Europe"
            },
            {
                "id": 2,
                "title": "Nationalism in India",
                "description": "The Indian independence movement and freedom struggle"
            },
            {
                "id": 3,
                "title": "The Making of a Global World",
                "description": "Colonialism, trade, and global connections"
            }
        ]
    },
    "geography": {
        "name": "Geography",
        "chapters": [
            {
                "id": 1,
                "title": "Resources and Development",
                "description": "Natural and human resources in India"
            },
            {
                "id": 2,
                "title": "Forest and Wildlife Resources",
                "description": "Biodiversity and conservation in India"
            },
            {
                "id": 3,
                "title": "Water Resources",
                "description": "Rivers, dams, and water management"
            }
        ]
    },
    "civics": {
        "name": "Civics",
        "chapters": [
            {
                "id": 1,
                "title": "Power Sharing Arrangements",
                "description": "Constitution, democracy, and federalism"
            },
            {
                "id": 2,
                "title": "Federalism",
                "description": "Union and state governments"
            },
            {
                "id": 3,
                "title": "Democratic Rights",
                "description": "Fundamental rights and duties"
            }
        ]
    },
    "economics": {
        "name": "Economics",
        "chapters": [
            {
                "id": 1,
                "title": "Development",
                "description": "Meaning and indicators of development"
            },
            {
                "id": 2,
                "title": "Sectors of the Indian Economy",
                "description": "Primary, secondary, and tertiary sectors"
            },
            {
                "id": 3,
                "title": "Money and Credit",
                "description": "Banking system and financial services"
            }
        ]
    }
}

# MCQ Database
MCQ_DATA = {
    "history": [
        {
            "id": 1,
            "question": "Which country is considered the birthplace of modern nationalism?",
            "options": ["France", "Germany", "Italy", "Spain"],
            "answer": 0,
            "explanation": "France is considered the birthplace of modern nationalism, especially after the French Revolution."
        },
        {
            "id": 2,
            "question": "In which year did India gain independence?",
            "options": ["1945", "1947", "1950", "1952"],
            "answer": 1,
            "explanation": "India gained independence on August 15, 1947."
        },
        {
            "id": 3,
            "question": "Who was the first Prime Minister of Independent India?",
            "options": ["Dr. Rajendra Prasad", "Jawaharlal Nehru", "Sardar Vallabhbhai Patel", "B.R. Ambedkar"],
            "answer": 1,
            "explanation": "Jawaharlal Nehru was the first Prime Minister of Independent India."
        }
    ],
    "geography": [
        {
            "id": 1,
            "question": "Which is the longest river in India?",
            "options": ["Brahmaputra", "Ganges", "Godavari", "Yamuna"],
            "answer": 1,
            "explanation": "The Ganges (Ganga) is the longest river in India."
        },
        {
            "id": 2,
            "question": "Which state has the highest forest cover in India?",
            "options": ["Assam", "Madhya Pradesh", "Maharashtra", "Odisha"],
            "answer": 1,
            "explanation": "Madhya Pradesh has the highest forest cover in India."
        }
    ],
    "civics": [
        {
            "id": 1,
            "question": "How many parts does the Indian Constitution have?",
            "options": ["20", "22", "24", "26"],
            "answer": 2,
            "explanation": "The Indian Constitution has 24 parts (originally had 8, but amendments added more)."
        },
        {
            "id": 2,
            "question": "Who is the head of state in India?",
            "options": ["Prime Minister", "President", "Governor", "Chief Minister"],
            "answer": 1,
            "explanation": "The President of India is the head of state."
        }
    ],
    "economics": [
        {
            "id": 1,
            "question": "What does GDP stand for?",
            "options": ["Gross Domestic Policy", "Gross Domestic Product", "General Development Plan", "Global Development Program"],
            "answer": 1,
            "explanation": "GDP stands for Gross Domestic Product."
        },
        {
            "id": 2,
            "question": "Which is the largest sector in the Indian economy?",
            "options": ["Primary", "Secondary", "Tertiary", "Quaternary"],
            "answer": 2,
            "explanation": "The tertiary sector (services) is the largest sector in the Indian economy."
        }
    ]
}

@app.route('/')
def index():
    return render_template('index.html', subjects=STUDY_DATA)

@app.route('/subject/<subject>')
def subject(subject):
    if subject not in STUDY_DATA:
        return "Subject not found", 404
    subject_data = STUDY_DATA[subject]
    return render_template('subject.html', subject=subject, subject_data=subject_data)

@app.route('/chapter/<subject>/<int:chapter_id>')
def chapter(subject, chapter_id):
    if subject not in STUDY_DATA:
        return "Subject not found", 404
    
    chapters = STUDY_DATA[subject]['chapters']
    chapter_data = next((ch for ch in chapters if ch['id'] == chapter_id), None)
    
    if not chapter_data:
        return "Chapter not found", 404
    
    return render_template('chapter.html', subject=subject, chapter=chapter_data)

@app.route('/quiz/<subject>')
def quiz(subject):
    if subject not in MCQ_DATA:
        return "Subject quiz not found", 404
    
    return render_template('quiz.html', subject=subject, questions=MCQ_DATA[subject])

@app.route('/api/subjects')
def api_subjects():
    return jsonify(STUDY_DATA)

@app.route('/api/quiz/<subject>')
def api_quiz(subject):
    if subject not in MCQ_DATA:
        return jsonify({"error": "Subject not found"}), 404
    return jsonify(MCQ_DATA[subject])

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()
    results = []
    
    for subject_key, subject_data in STUDY_DATA.items():
        for chapter in subject_data['chapters']:
            if query in chapter['title'].lower() or query in chapter['description'].lower():
                results.append({
                    "subject": subject_key,
                    "subject_name": subject_data['name'],
                    "chapter": chapter
                })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
