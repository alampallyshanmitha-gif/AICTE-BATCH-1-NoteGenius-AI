# utils/pdf_export.py
import io
import json
from fpdf import FPDF

def export_workspace_to_pdf(transcript, quiz, flashcards, keywords):
    # ==========================================
    # 1. DATA CLEANING & SAFE FALLBACKS
    # ==========================================
    safe_transcript = str(transcript).strip() if transcript else "No transcript content available for this session."
    
    # Clean and process keywords array safely
    if isinstance(keywords, list):
        safe_keywords = ", ".join([str(k) for k in keywords]) if keywords else "No keywords generated."
    else:
        safe_keywords = str(keywords).strip() if keywords else "No keywords generated."

    # Custom inherited FPDF class to build persistent structure templates
    class SafePDF(FPDF):
        def header(self):
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(79, 70, 229)  # NoteGenius Signature Indigo Accent Color
            self.cell(0, 10, "NoteGenius AI - Workspace Export Summary", ln=True, align="L")
            self.ln(4)
            # Render subtle divider layout line beneath page summary titles
            self.set_draw_color(226, 232, 240)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(6)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 9)
            self.set_text_color(148, 163, 184)
            self.cell(0, 10, f"Page {self.page_no()}", align="C")

        def clean_txt(self, text_content):
            """Prevents Latin-1 encoding mismatch faults during PDF writes"""
            if not text_content:
                return ""
            return str(text_content).encode('latin-1', 'replace').decode('latin-1')

    # Initialize Document Layout Frame
    pdf = SafePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # ------------------------------------------
    # SECTION A: HIGHLIGHT TARGET KEYWORDS
    # ------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "Core Document Keywords:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(71, 85, 105)
    pdf.multi_cell(0, 6, pdf.clean_txt(safe_keywords))
    pdf.ln(6)

    # ------------------------------------------
    # SECTION B: SOURCE LECTURE TRANSCRIPT
    # ------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "Lecture Session Transcript Content:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    pdf.multi_cell(0, 6, pdf.clean_txt(safe_transcript))
    pdf.ln(8)

    # ------------------------------------------
    # SECTION C: PRACTICE EVALUATION QUIZZES
    # ------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "Generated AI Assessment Quiz:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    
    try:
        # Resolve data structure regardless if input is a raw string or an array collection
        quiz_dataset = json.loads(quiz) if isinstance(quiz, str) else quiz
        
        if isinstance(quiz_dataset, list) and len(quiz_dataset) > 0:
            for position, question_node in enumerate(quiz_dataset, 1):
                pdf.set_font("Helvetica", "B", 10)
                q_text = question_node.get('question', 'Question text field missing.')
                pdf.multi_cell(0, 6, pdf.clean_txt(f"\nQ{position}: {q_text}"))
                
                pdf.set_font("Helvetica", "", 10)
                if 'options' in question_node and isinstance(question_node['options'], list):
                    for option_variant in question_node['options']:
                        pdf.multi_cell(0, 5, pdf.clean_txt(f"  [ ] {option_variant}"))
                
                if 'answer' in question_node:
                    pdf.set_text_color(5, 150, 105)  # Muted Emerald Green Highlight
                    pdf.multi_cell(0, 5, pdf.clean_txt(f"  Expected Answer: {question_node['answer']}"))
                    pdf.set_text_color(51, 65, 85)   # Return to Neutral text tint
        else:
            pdf.cell(0, 6, "No quiz evaluation sets compiled in current workspace session.", ln=True)
    except Exception:
        pdf.cell(0, 6, "No quiz evaluation sets compiled in current workspace session.", ln=True)
        
    pdf.ln(6)

    # ------------------------------------------
    # SECTION D: DYNAMIC STUDY FLASHCARDS
    # ------------------------------------------
    pdf.set_font("Helvetica", "B", 12)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(0, 8, "Active Revision Flashcard Pairs:", ln=True)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(51, 65, 85)
    
    try:
        flashcard_dataset = json.loads(flashcards) if isinstance(flashcards, str) else flashcards
        
        if isinstance(flashcard_dataset, list) and len(flashcard_dataset) > 0:
            for card_position, card_node in enumerate(flashcard_dataset, 1):
                front_prompt = card_node.get('front', card_node.get('question', 'Front prompt descriptor empty.'))
                back_response = card_node.get('back', card_node.get('answer', 'Back response verification empty.'))
                
                pdf.set_font("Helvetica", "B", 10)
                pdf.multi_cell(0, 6, pdf.clean_txt(f"\nCard #{card_position} [Front Face]: {front_prompt}"))
                pdf.set_font("Helvetica", "I", 10)
                pdf.multi_cell(0, 6, pdf.clean_txt(f"Card #{card_position} [Back Response]: {back_response}"))
        else:
            pdf.cell(0, 6, "No study flashcards constructed in current workspace session.", ln=True)
    except Exception:
        pdf.cell(0, 6, "No study flashcards constructed in current workspace session.", ln=True)

    # Compile the internal PDF stream layout safely back to standalone binary output
    return bytes(pdf.output(dest="S"))