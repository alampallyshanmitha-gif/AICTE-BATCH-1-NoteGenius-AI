import random

def generate_quiz(text):
    """
    Parses sentences to extract realistic fill-in-the-blank questions 
    with 4 multiple-choice options.
    """
    sentences = text.replace("\n", ". ").split(".")
    quiz = []
    count = 1

    for sentence in sentences:
        sentence = sentence.strip()
        words = sentence.split()
        
        # Look for sentences that are descriptive enough to create a blank
        if len(words) > 6:
            # Pick a dynamic structural keyword from the sentence to hide (avoiding tiny filler words)
            eligible_words = [w.strip(".,;:?!\"'") for w in words if len(w) > 4]
            if not eligible_words:
                continue
                
            correct_answer = random.choice(eligible_words)
            
            # Create the question string by replacing the target word with blanks
            question_text = sentence.replace(correct_answer, "_______")
            
            # Generate 3 dummy alternative choices for distraction
            fillers = ["Concept", "System", "Analysis", "Overview", "Function", "Variable", "Structure"]
            wrong_options = [f for f in fillers if f.lower() != correct_answer.lower()]
            selected_wrongs = random.sample(wrong_options, 3)
            
            # Compile options grid and shuffle them randomly
            options = [correct_answer] + selected_wrongs
            random.shuffle(options)
            
            quiz.append({
                "id": count,
                "question": f"Question {count}: Complete the statement:\n\n\"{question_text}\"",
                "options": options,
                "answer": correct_answer
            })
            count += 1

        if count > 5:
            break

    return quiz