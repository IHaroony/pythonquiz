from flask import Flask
from flask_socketio import SocketIO
import sys
import io

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Quiz questions
questions = [
("What is the capital of France?",["A.Berlin","B.Madrid","C.Paris","D.Rome"], "C"),
("Where is the Statue of Liberty?",["                                      A.Los Angeles","B.Washington DC.","C.New York",], "C"),
("The main character Luffy is in which show?", ["                          A. Naruto", "B. One Piece", "C. Hunter x Hunter", "D. Bleach"], "B"),
("Which NBA team has a green jersey and is in Boston?", ["                 A. Chicago Bulls", "B. Miami Heat", "C. Boston Celtics", "D. Los Angeles Lakers"], "C"),
("Which team did Cristiano Ronaldo play for?", ["                          A. Barcelona", "B. Manchester United", "C. Liverpool", "D. Chelsea"], "B"),
("What is the name of the main character in The Sopranos?", ["             A. Tony Soprano", "B. Michael Corleone", "C. Walter White", "D. Ghost"], "A"),
("Who wrote the novel '1984'?", ["                                         A. George Orwell", "B. Aldous Huxley", "C. J.K. Rowling", "D. Ernest Hemingway"], "A")
]

# Initialize quiz state
quiz_state = {
    'current_question': 0,  # Track current question index
    'score': 0,             # Track score
    'total_questions': len(questions)
}

# Helper function to format the question for display
def format_question(question_data):
    question_text = question_data[0]
    choices = "\n".join([f"  {choice}" for choice in question_data[1]])  # Add newlines between choices and indent
    return f"\n{question_text}\n\n{choices}\n"  # Add newlines for spacing

# Handle quiz flow based on user input
@socketio.on('input')
def handle_input(data):
    data = data.strip().upper()

    if quiz_state['current_question'] < quiz_state['total_questions']:
        question_data = questions[quiz_state['current_question']]
        correct_answer = question_data[2]

        # Check if the answer is correct
        if data == correct_answer:
            quiz_state['score'] += 1
            output = "\nCorrect! Well done.\n"
        else:
            output = f"\nWrong! The correct answer was {correct_answer}.\n"

        quiz_state['current_question'] += 1  # Move to the next question

        # If there are more questions, ask the next one
        if quiz_state['current_question'] < quiz_state['total_questions']:
            next_question = questions[quiz_state['current_question']]
            output += "\nNext question:\n" + format_question(next_question)
        else:
            # End the quiz and show final score
            output += "\n::::::::::::::::::: That was the last question! :::::::::::::::::::::"
            output += f"                \nYour final score is {quiz_state['score']} out of {quiz_state['total_questions']}."

            percentage = (quiz_state['score'] / quiz_state['total_questions']) * 100
            if percentage >= 90:
                rating = "Excellent"
            elif percentage >= 70:
                rating = "Good"
            elif percentage >= 50:
                rating = "Average"
            else:
                rating = "Needs Improvement"

            output += f"                       \n\nYour performance: {rating}                             \nThanks for playing the quiz!"

        socketio.emit('output', output)

# Start the quiz by showing the first question
@socketio.on('start_code_execution')
def handle_start_execution():
    quiz_state['current_question'] = 0  # Reset the quiz
    quiz_state['score'] = 0  # Reset the score

    first_question = format_question(questions[0])
    output = "Welcome to the Quiz!\n" + first_question
    socketio.emit('output', output)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
