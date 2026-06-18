import random

def generate_flashcards(text):
    """
    Transforms lecture data into specific, contextual questions (Front)
    and detailed study answers (Back).
    """
    sentences = text.replace("\n", ". ").split(".")
    flashcards = []
    count = 1

    for sentence in sentences:
        sentence = sentence.strip()
        words = sentence.split()
        
        # Focus on substantial, informative sentences
        if len(sentence) > 30 and len(words) > 6:
            sentence_lower = sentence.lower()
            
            # Scenario A: Definition sentences ("is a", "refers to")
            if " is a " in sentence_lower or " refers to " in sentence_lower:
                indicator = " is a " if " is a " in sentence_lower else " refers to "
                parts = sentence.split(indicator, 1)
                subject = parts[0].strip()
                
                # Make it clean
                if subject:
                    subject = subject[0].upper() + subject[1:]
                
                question = f"What exactly is **{subject}** and how is it defined?"
                answer = sentence

            # Scenario B: Cause and Effect / Processes ("causes", "leads to", "creates")
            elif " cause " in sentence_lower or " leads to " in sentence_lower or " results in " in sentence_lower:
                # Use the first few words as context to derive a question
                words_chunk = " ".join(words[:4]).strip(".,;:!")
                question = f"What are the direct outcomes or consequences related to **{words_chunk}**?"
                answer = sentence

            # Scenario C: Function or Mechanism ("uses", "works by", "helps to", "functions")
            elif " use " in sentence_lower or " work " in sentence_lower or " function " in sentence_lower:
                subject_hint = words[0] if len(words[0]) > 3 else " ".join(words[:2])
                question = f"How does **{subject_hint}** function or operate within this context?"
                answer = sentence

            # Fallback Scenario: Standard structural question variety
            else:
                # Pull out a meaningful middle noun/verb phrase for a core target question
                mid_index = len(words) // 2
                target_phrase = " ".join(words[max(0, mid_index-1):min(len(words), mid_index+2)]).strip(".,;:!")
                
                question_styles = [
                    f"Can you explain the significance of the concept involving **{target_phrase}**?",
                    f"What key takeaway should you remember regarding **{target_phrase}**?",
                    f"Break down the core idea behind: **{target_phrase}**."
                ]
                question = random.choice(question_styles)
                answer = sentence

            # Append structured payload back
            flashcards.append({
                "id": count,
                "question": question,
                "answer": answer
            })
            count += 1

        if count > 5:
            break

    return flashcards