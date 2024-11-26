from flask import Flask, request, render_template, session, redirect, url_for
import random
import sqlite3

#intializing our flask app and session secret key
app = Flask(__name__)
app.secret_key = ('Wordle_Game')

"""
1.Connecting to the database
2.creating a cursor object
3.creating a table words if it does not exist
4.Selecting all the words in the db
5.Storing all the words in form of a list words
"""

conn = sqlite3.connect("words.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word TEXT NOT NULL
)""")

cursor.execute("SELECT word FROM Words")
words = []

for row in cursor.fetchall():
    words.append(row[0])

CORRECT_WORD = ""
def get_new_word():
    """Selecting a random word from the words list
    if word is empty, it sets the CORRECT_WORD to flask"""
    global CORRECT_WORD
    if words:
        CORRECT_WORD = random.choice(words)
    else:
        CORRECT_WORD = "flask"


#initializing the main page for flask
@app.route('/', methods=['GET', 'POST'])
def wordle():
    if 'game_state' not in session:
        # Initialize session variables
        session['game_state'] = {
            'attempts': [],
            'keyboard': {chr(c): None for c in range(97, 123)},  # a-z with initial state None
            'game_over': False,
            'message': ""
        }

    game_state = session['game_state']

    if request.method == 'POST' and not game_state['game_over']:
        user_word = request.form['word'].lower()

        if len(user_word) != len(CORRECT_WORD):
            game_state['message'] = f"Word must be {len(CORRECT_WORD)} letters long."
        elif len(game_state['attempts']) >= 5:
            game_state['message'] = f"Game over! The correct word was '{CORRECT_WORD}'."
            game_state['game_over'] = True
        else:
            feedback = []
            for i, char in enumerate(user_word):
                if char == CORRECT_WORD[i]:
                    feedback.append('green')  # Correct position
                    game_state['keyboard'][char] = 'green'
                elif char in CORRECT_WORD:
                    feedback.append('yellow')  # Correct letter, wrong position
                    if game_state['keyboard'][char] != 'green':  # Avoid downgrading green
                        game_state['keyboard'][char] = 'yellow'
                else:
                    feedback.append('gray')  # Incorrect letter
                    game_state['keyboard'][char] = 'gray'

            game_state['attempts'].append({'word': user_word, 'feedback': feedback})

            if user_word == CORRECT_WORD:
                game_state['message'] = "Correct! You guessed the word!"
                game_state['game_over'] = True
            elif len(game_state['attempts']) >= 5:
                game_state['message'] = f"Game over! The correct word was '{CORRECT_WORD}'."
                game_state['game_over'] = True
            else:
                game_state['message'] = f"Wrong! Attempts left: {5 - len(game_state['attempts'])}"

        session.modified = True

    return render_template('wordle.html', game_state=game_state)

"""
1.Getting new word
2.removing the game state from the session 
3.redirecting to the main game page
"""
@app.route('/reset')
def reset():
    get_new_word()
    session.pop('game_state', None)
    return redirect(url_for('wordle'))


if __name__ == '__main__':
#getting a new word at start of the game
    get_new_word()
    app.run(debug=True)
