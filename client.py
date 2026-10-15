from websockets.sync.client import connect
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO
import requests
import json
import threading
import dog_api


url = "ws://localhost:8765"
score = 0
question_number = 0
correct_breed = None
answered = False

#------ Tkinter ------#
root=tk.Tk()

root.title("Dog Guesser Pro Deluxe Edition")
root.geometry("1200x900")
start_frame = tk.Frame(root)
start_frame.pack(pady=150)

welcome_label = tk.Label(
    start_frame,
    text="Bienvenue sur Dog Guesser Pro Deluxe Edition!",
    font=("Arial", 24, "bold")
)
welcome_label.pack(pady=20)

username_label = tk.Label(
    start_frame,
    text="Entre ton username :",
    font=("Arial", 14)
)
username_label.pack(pady=10)

username_entry = tk.Entry(
    start_frame,
    font=("Arial", 14),
    width=25
)
username_entry.pack(pady=10)


title_label=tk.Label(root, text="Dog Guesser Pro Deluxe Edition", font=("Arial",24,"bold"))

question_label=tk.Label(root,text="Guess the breed of the dog", font=("Ariel",14))

image_label=tk.Label(root)

buttons_frame=tk.Frame(root)

button1 = tk.Button(buttons_frame, text="0", width=40,bg="#4CAF50", fg="white")
button2 = tk.Button(buttons_frame, text="1", width=40,bg="#FDD835", fg="black")
button3 = tk.Button(buttons_frame, text="2", width=40,bg="#F44336", fg="white")
button4 = tk.Button(buttons_frame, text="3", width=40,bg="#2196F3", fg="white")

button1.grid(row=0, column=0, padx=10, pady=10, ipadx=20, ipady=15)
button2.grid(row=0, column=1, padx=10, pady=10, ipadx=20, ipady=15)
button3.grid(row=1, column=0, padx=10, pady=10, ipadx=20, ipady=15)
button4.grid(row=1, column=1, padx=10, pady=10, ipadx=20, ipady=15)

button1.config(command=lambda: submit_answer(button1.cget("text")))
button2.config(command=lambda: submit_answer(button2.cget("text")))
button3.config(command=lambda: submit_answer(button3.cget("text")))
button4.config(command=lambda: submit_answer(button4.cget("text")))

buttons = [button1, button2, button3, button4]

score_label = tk.Label(root, text="Score : 0", font=("Arial", 14))
score_label.pack(pady=5)

restart_button = tk.Button(root, text="Recommencer une partie", font=("Arial", 12), command=lambda: restart_game())


#----------#----------#----------#----------#

def start_game():
    global username, ws

    username = username_entry.get().strip()

    if not username:
        username_label.config(text="Entre un username pour commencer !",fg="red")
        return

    try:
        ws = connect(url, legacy=True)
    except Exception as error:
        username_label.config(text="Impossible de joindre le serveur.",fg="red")
        print(f"Erreur de connexion : {error}")
        return

    start_frame.pack_forget()

    # Afficher les éléments du jeu
    title_label.pack(pady=20)
    question_label.pack(pady=10)
    image_label.pack(pady=10)
    buttons_frame.pack(pady=20)
    score_label.pack(pady=5)

    threading.Thread(target=receive_messages,daemon=True).start()
    ask_new_question()

# --- Bouton Start --- #
start_button = tk.Button(start_frame,text="Commencer la partie",font=("Arial", 14, "bold"),command=start_game)
start_button.pack(pady=20)
# -------------------- #


def receive_messages():
    while True:
        try:
            response = json.loads(ws.recv())
            root.after(0, handle_message, response)
        except Exception as error:
            print(f"Erreur de connexion : {error}")
            break

def display_image(image_url):
    response = requests.get(image_url)
    response.raise_for_status()

    image = Image.open(BytesIO(response.content))
    image = image.resize((300, 250))

    photo = ImageTk.PhotoImage(image)
    image_label.config(image=photo)
    image_label.image = photo

def ask_new_question():
    global correct_breed, answered

    try:
        correct_breed, image_url, choices = dog_api.quizz()

        display_image(image_url)

        question_label.config(
            text=f"Question {question_number + 1}/10 : "
                 "Guess the breed of the dog"
        )

        for button, choice in zip(buttons, choices):
            button.config(text=choice, state="normal")

        answered = False

    except Exception as error:
        question_label.config(text="Impossible de charger la question.")
        print(f"Erreur : {error}")

def handle_message(message):
    global score, question_number

    if message["type"] == "score":
        score = message["score"]
        score_label.config(text=f"Score : {score}")

        if question_number >= 10:
            ws.send(json.dumps({"type": "game_over","username": username}))
        else:
            root.after(1500, ask_new_question)

    elif message["type"] == "game_saved":
        score = message["score"]
        question_label.config(text=f"Partie terminée ! Score final : {score}/10")
        restart_button.pack(pady=15)

    elif message["type"] == "score_reset":
        score = 0
        question_number = 0
        score_label.config(text="Score : 0")
        restart_button.pack_forget()
        ask_new_question()

def submit_answer(answer):
    global answered, question_number

    if answered or question_number >= 10:
        return

    answered = True
    question_number += 1

    for button in buttons:
        button.config(state="disabled")

    is_correct = answer == correct_breed

    if is_correct:
        question_label.config(text="Bonne réponse !")
    else:
        question_label.config(
            text=f"Mauvaise réponse ! C'était : {correct_breed}"
        )

    ws.send(json.dumps({
        "type": "answer",
        "correct": is_correct
    }))

def next_question():
    ws.send("new_question")

def restart_game():
    global score, question_number, answered

    # Cacher l'écran de jeu
    title_label.pack_forget()
    question_label.pack_forget()
    image_label.pack_forget()
    buttons_frame.pack_forget()
    score_label.pack_forget()
    restart_button.pack_forget()

    # Réinitialiser les variables coté client et serveur
    score = 0
    question_number = 0
    answered = False
    ws.send(json.dumps({"type": "reset_score"}))

    # Réafficher l'écran d'accueil
    username_entry.delete(0, tk.END)
    username_label.config(text="Entre ton username :", fg="black")
    start_frame.pack(pady=150)



root.mainloop()