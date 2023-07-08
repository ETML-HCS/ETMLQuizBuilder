#########################################################################################
#                               ETMLQuizBuilder                                         #
#########################################################################################
# Auteur      : Helder Costa Lopes                                                      #
# Date        : juillet 2023                                                            #
# Description :                                                                         #
# Ce code Python utilise Flask pour créer un module de quiz interactif.                 #
# Il permet de charger un quiz depuis un fichier CSV, de générer le formulaire HTML,    #
# de gérer les réponses en temps réel et d'afficher les résultats.                      #
# Il offre une solution complète, simplifiant également l'ajout des fichiers            #
# CSS et JavaScript nécessaires pour le fonctionnement du module.                       #
##########################################################################################

# Importation des modules nécessaires
import os  # Module pour interagir avec le système d'exploitation
import csv  # Module pour la lecture et l'écriture de fichiers CSV

# Définition des fonctions
def create_css_file(module_dir, file_name, css_content):
    # Définition des répertoires
    static_dir = os.path.join(module_dir, "static")
    css_dir = os.path.join(static_dir, "css")
    
    # Vérification et création du répertoire css s'il n'existe pas
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
    
    # Chemin complet du fichier css
    file_path = os.path.join(css_dir, file_name)
    
    # Ouverture du fichier en mode écriture et encodage utf-8
    with open(file_path, "w", encoding="utf-8") as file:
        # Écriture du contenu CSS dans le fichier
        file.write(css_content)
    
    # Retourne le chemin complet du fichier créé
    return file_path

def create_js_file(module_dir, file_name, js_content):
    # Définition des répertoires
    static_dir = os.path.join(module_dir, "static")
    js_dir = os.path.join(static_dir, "js")
    
    # Vérification et création du répertoire js s'il n'existe pas
    if not os.path.exists(js_dir):
        os.makedirs(js_dir)
    
    # Chemin complet du fichier JavaScript
    file_path = os.path.join(js_dir, file_name)
    
    # Ouverture du fichier en mode écriture et encodage utf-8
    with open(file_path, "w", encoding="utf-8") as file:
        # Écriture du contenu JavaScript dans le fichier
        file.write(js_content)
    
    # Retourne le chemin complet du fichier créé
    return file_path

def load_quiz(file_name):
    quiz = []  # Liste qui stockera les questions, choix et réponses correctes du quiz

    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()  # Lecture de toutes les lignes du fichier
        title = lines[0].strip()  # La première ligne contient le titre du quiz
        question = ''  # Variable pour stocker la question en cours de lecture
        choices = []  # Liste pour stocker les choix possibles de réponse pour la question
        correct_choice = ''  # Variable pour stocker la réponse correcte pour la question
        question_number = 0  # Numéro de la question en cours de lecture

        for line in lines[2:]:
            line = line.strip()  # Supprimer les espaces vides en début et fin de ligne

            if line:
                if line.startswith(str(question_number+1) + '.'):
                    # Si la ligne commence par le numéro de la question suivi d'un point,
                    # cela signifie qu'une nouvelle question commence
                    question = line
                    question_number += 1

                elif line.startswith('a)') or line.startswith('b)') or line.startswith('c)'):
                    # Si la ligne commence par 'a)', 'b)' ou 'c)', cela signifie que c'est un choix de réponse
                    choices.append(line)
                    if line.endswith('$true$'):
                        # Si la ligne se termine par '$true$', cela indique que c'est la réponse correcte
                        correct_choice = line

            else:
                # Si la ligne est vide, cela signifie que la question actuelle est terminée
                # et on peut ajouter la question, les choix et la réponse correcte à la liste du quiz
                quiz.append((question, choices, correct_choice))
                choices = []  # Réinitialiser les choix pour la prochaine question
                correct_choice = ''  # Réinitialiser la réponse correcte pour la prochaine question
                question = ''  # Réinitialiser la question pour la prochaine question

    return title, quiz  # Retourner le titre du quiz et la liste des questions, choix et réponses correctes

# Génère le code HTML pour le questionnaire
def generate_questionnaire_html(title, quiz):
    form_html = f'''
<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <link rel="stylesheet" type="text/css" href="/static/css/styles.css">
    <script src="/static/js/student_form_script.js" defer></script>
</head>
<body>
    <header>
        <div id="logo"> </div>
    </header>

    <form method="POST" action="/submit">
     <h3 id="error"></h3>
        <div class="oneQuest show" id="0">
            <p>Entrez votre pseudo :</p>
            <input type="text" id="pseudo" name="pseudo">
        </div>
       
'''
    for i, (question, choices, correct_choice) in enumerate(quiz):
        form_html += f'<div class="oneQuest" id="{i+1}">\n'
        form_html += f'<p>{question}</p>\n'
        for choice in choices:
            value = choice[0]
            text = choice[3:].replace("$true$", "")
            if choice == correct_choice:
                form_html += f'<label>\n'
                form_html += f'<input type="radio" name="question_{i}" value="{value}" data-correct="true" /> {text}\n'
                form_html += f'</label>\n'
            else:
                form_html += f'<label>\n'
                form_html += f'<input type="radio" name="question_{i}" value="{value}" /> {text}\n'
                form_html += f'</label>\n'
        form_html += '</div>\n'

    form_html += '''
    <input  id="submitButton" type="submit" value="Submit" style="display:none;" />
    </form>
    <div onClick="goToPreviousQuestion();" id="previousButton" style="display: inline;height: 20px;width:50px;text-align:center;margin-right: 10px;" > << </div>
    <div onClick="goToNextQuestion();" id="nextButton" style="display: inline;height: 20px;width:50px;text-align:center;margin-right: 10px;" > >> </div>
    <footer>ETML / CFPV | Quiz serveur | Section informatique</footer>
</body>

</html>
'''
    return form_html

# Génère le script JavaScript pour afficher les réponses des étudiants
def generate_student_response_script(quiz):

    script = '''const socket = io();
    socket.on('connect', () => {
        console.log('Connected to server');
    });

    socket.on('student_count', (count) => {
        document.getElementById('student-count').textContent = `Nombre d'étudiants ayant répondu : ${count}`;
    });

    socket.on('student_response', (data) => {
        const { pseudo, responses } = data;
        const tableRow = document.createElement('tr');

        const pseudoCell = document.createElement('td');
        pseudoCell.textContent = pseudo;
        tableRow.appendChild(pseudoCell);

        // Récupérer les clés de réponse depuis le quiz
        const responseKeys = {};
        '''
    for i, (question, _, correct_choice) in enumerate(quiz):
        script += f"responseKeys[{i}] = {repr(correct_choice)};\n"

    script += '''
        // Parcourir les clés de réponse pour afficher les réponses
        Object.values(responseKeys).forEach((responseKey, index) => {
            const response = responses[`Question ${index + 1}`];

            const responseCell = document.createElement('td');
            responseCell.textContent = response;
            responseCell.classList.add(response === responseKeys[index][0] ? 'correct' : 'incorrect');
            tableRow.appendChild(responseCell);
        });

        // Ajouter la ligne au tableau
        document.getElementById('student-responses').appendChild(tableRow);
    });

    socket.on('all_students_submitted', () => {
        // Tous les étudiants ont répondu, effectuer les actions nécessaires (par exemple, afficher un message)
        console.log('Tous les étudiants ont répondu');
    });

    const showSolutionsButton = document.getElementById('show-solutions-btn');
    const solutionsDiv = document.getElementById('solutions');

    showSolutionsButton.addEventListener('click', () => {
        solutionsDiv.style.display = 'block';
    });
    '''
    return script

# Génère le code HTML pour les résultats du quiz
def generate_results_html(num_questions):
    html_content = f'''<!DOCTYPE html>
<html>
<head>
    <title>Résultats du quiz</title>
    <link rel="stylesheet" type="text/css" href="/static/css/styles.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.3.1/socket.io.js"></script>
    <script src="/static/js/student_response_script.js" defer></script>
</head>
<body>
    <h1>Résultats du quiz</h1>
    <div id="student-count">Nombre d'étudiants ayant répondu : 0</div>
    <table id="student-responses">
        <tr>
            <th>Pseudo</th>
'''
    for i in range(num_questions):
        html_content += f'            <th>Question {i+1}</th>\n'

    html_content += '''        </tr>
    </table>
    <button id="show-solutions-btn">Afficher les solutions</button>
    <div id="solutions" style="display: none;"></div>
    <footer>ETML / CFPV | Quiz serveur | Section informatique</footer>
</body>
</html>
'''
    return html_content

# Enregistre le contenu HTML dans un fichier
def save_html(html_content, file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(html_content)

# Enregistre le contenu statique dans un fichier
def save_static_file(content, file_name, folder):
    with open(os.path.join(folder, file_name), 'w', encoding='utf-8') as file:
        file.write(content)

def create_quiz_module(file_name):
    # Crée un module de quiz à partir d'un fichier
    module_name = os.path.splitext(file_name)[0]
    module_dir = f"quiz_module_{module_name}"
    template_dir = os.path.join(module_dir, "templates")
    static_dir = os.path.join(module_dir, "static")
    images_dir= os.path.join(static_dir, "images")
    
    # Crée les répertoires nécessaires pour le module de quiz
    os.makedirs(template_dir, exist_ok=True)
    os.makedirs(static_dir, exist_ok=True)
    os.makedirs(images_dir, exist_ok=True)

    # Charge le quiz à partir du fichier
    title, quiz = load_quiz(file_name)
    
    # Génère le code HTML pour le questionnaire, les résultats et le script de réponse des étudiants
    question_html = generate_questionnaire_html(title, quiz)
    results_html = generate_results_html(len(quiz))
    student_response_script = generate_student_response_script(quiz)
    
    css_content = """
#region Styles pour le corps de la page
body {
    position: static;
    width: 85%;
    margin: 0 auto;
    padding: 10px;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
    font-size: larger;
}
#endregion

#region Styles pour le pied de page
footer {
    position: fixed;
    bottom: 0;
    height: 25px;
    width: 100%;
    text-align: center;
    color: #ffffff;
    background-color: #007bff;
    margin-left: auto;
    margin-right: auto;
    left: 0;
    right: 0;
}
#endregion

#region Styles pour le logo
#logo {
    background-image: url("/static/images/ETML.png");
    background-size: contain;
    background-repeat: no-repeat;
    min-height: 30px;
    padding-bottom: 4px;
    border-bottom: 2px solid rgb(116, 116, 4);
}
#endregion

#region Styles pour les titres de niveau 2
h2 {
    font-size: 18px;
    font-weight: bold;
    margin-bottom: 10px;
}
#endregion

#region Styles pour les paragraphes de question
p.question {
    margin-bottom: 10px;
}
#endregion

#region Styles pour les étiquettes de question
p.question-label {
    font-weight: bold;
}
#endregion

#region Styles pour les champs de texte
input[type="text"],
textarea {
    width: 100%;
    padding: 5px;
    margin-bottom: 10px;
}
#endregion

#region Styles pour les boutons radio et les cases à cocher
input[type="radio"],
input[type="checkbox"] {
    margin-block: 20px;
    margin-inline: 12px;
}
#endregion

#region Styles pour les boutons
#bt_login,
#previousButton,
#nextButton,
input[type="submit"] {
    background-color: darkblue;
    color: white;
    font-weight: bold;
    padding: 10px 20px;
    border: none;
    cursor: pointer;
}
#endregion

#region Styles pour les boutons au survol
#bt_login:hover,
#previousButton:hover,
#nextButton:hover,
input[type="submit"]:hover {
    background-color: darkcyan;
}
#endregion

#region Styles pour les messages d'erreur
#error {
    color: red;
    margin-top: 5px;
}
#endregion

#region Styles pour les sections de question
.oneQuest {
    height: 60vh;
    display: none;
    flex-direction: column;
}
.show {
    display: flex;
}
#endregion

#region Styles pour le nombre d'étudiants ayant répondu
#student-count {
    font-weight: bold;
    margin-bottom: 10px;
}
#endregion

#region Styles pour les réponses des étudiants
#student-responses {
    margin-top: 20px;
}
#endregion

#region Styles pour le tableau des réponses des étudiants
#student-responses table {
    width: 100%;
    border-collapse: collapse;
}
#student-responses th,
#student-responses td {
    padding: 8px;
    text-align: left;
    border-bottom: 1px solid #ddd;
}
#endregion

#region Styles pour les réponses incorrectes
.incorrect {
    background-color: #ff9999; /* Couleur de fond pour les réponses incorrectes */
    color: #ff0000; /* Couleur du texte pour les réponses incorrectes */
}
#endregion

#region Styles pour les réponses correctes
.correct {
    background-color: #99ff99; /* Couleur de fond pour les réponses correctes */
    color: #009900; /* Couleur du texte pour les réponses correctes */
}
#endregion


"""
    js_content = """const submitButton = document.getElementById('submitButton');
const previousButton = document.getElementById('previousButton');
const nextButton = document.getElementById('nextButton');
const errorElement = document.getElementById('error');
let hasError = null;

// Fonction pour récupérer l'ID de la dernière question
function getLastQuestionId() {
    const questions = document.querySelectorAll('.oneQuest');
    return questions.length-1;
}

const nQuestions = getLastQuestionId();

// Fonction pour vérifier si toutes les radios sont valides
function validateRadios() {

    const currentQuestion = document.querySelector('.oneQuest.show');

    if (currentQuestion) {
        const radioButtons = currentQuestion.querySelectorAll('input[type="radio"]');

        for (let i = 0; i < radioButtons.length; i++) {

            const radioButton = radioButtons[i];
            const radioButtonName = radioButton.getAttribute('name');
            const radioGroup = document.getElementsByName(radioButtonName);

            let checked = false;

            for (let j = 0; j < radioGroup.length; j++) {
                if (radioGroup[j].checked) {
                    checked = true;
                    break;
                }
            }
            if (!checked) {
                if (errorElement) {
                    errorElement.textContent = 'Veuillez sélectionner une réponse.';
                }
                return false;
            }
        }
    }
    return true;
}

function goToNextQuestion() {
    if (hasError != null) {
        errorElement.textContent = "";
    }

    hasError = validateRadios();

    // Vérifier si toutes les radios sont valides
    if (!hasError) {
        return; // Arrêter l'exécution si les radios ne sont pas valides
    }

    // Récupération de l'ID de la question actuelle
    const currentQuestionId = parseInt(document.querySelector('.oneQuest.show').id);

    // Vérification si la question actuelle est la dernière question
    if (currentQuestionId === nQuestions) {
        nextButton.style.display = 'none';
        previousButton.style.display = 'none';

        // Affichage du bouton "Submit" lorsque la dernière question est atteinte
        submitButton.style.display = 'block';
    } else {
        // Recherche de la question actuellement affichée
        const currentQuestion = document.querySelector('.oneQuest.show');

        // Récupération de la prochaine question
        const nextQuestion = currentQuestion.nextElementSibling;

        // Masquage de la question actuelle
        currentQuestion.classList.remove('show');

        // Affichage de la prochaine question
        nextQuestion.classList.add('show');

        // Affichage du bouton "Précédent"
        previousButton.style.display = 'inline';
    }
}

// Fonction pour passer à la question précédente
function goToPreviousQuestion() {
    // Recherche de la question actuellement affichée
    const currentQuestion = document.querySelector('.oneQuest.show');

    // Vérification si une question est actuellement affichée
    if (currentQuestion) {
        // Récupération de la question précédente
        const previousQuestion = currentQuestion.previousElementSibling;

        // Vérification si la question précédente existe
        if (previousQuestion) {
            // Masquage de la question actuelle
            currentQuestion.classList.remove('show');

            // Affichage de la question précédente
            previousQuestion.classList.add('show');

            // Affichage du bouton "Suivant"
            nextButton.style.display = 'inline';

            // Masquage du bouton "Submit" si la question actuelle n'est pas la dernière question
            if (currentQuestion.id !== getLastQuestionId()) {
                submitButton.style.display = 'none';
            }
        }

        // Masquage du bouton "Précédent" si la question actuelle est la première question
        if (!previousQuestion) {
            previousButton.style.display = 'none';
        }
    }
};"""

    css_file_path = create_css_file(module_dir, "styles.css", css_content)
    js_questions_path = create_js_file(module_dir, "student_form_script.js", js_content)    
    js_responses_path = create_js_file(module_dir, "student_response_script.js", student_response_script)

    save_html(question_html, os.path.join(template_dir, "Quest.html"))
    save_html(results_html, os.path.join(template_dir, "Results.html"))

    # Generate serverquiz.py
    server_quiz_content = f'''from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import csv
import os

def save_responses_to_csv(responses):
    with open('responses.csv', 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(responses.values())

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO(app)

@app.route('/results')
def results():
    return render_template('Results.html')

@app.route('/')
def index():
    return render_template('Quest.html')

@app.route('/submit', methods=['POST'])
def submit():
    pseudo = request.form['pseudo']
    responses = {{'pseudo': pseudo}}

    for i, (question, _, _) in enumerate({quiz}): # question_0, ...
        question_key = f'question_{{i}}'
        response_key = f'Question {{i+1}}'
        response = request.form[question_key]
        responses[response_key] = response

    # Obtenez l'adresse IP de l'élève
    ip_address = request.remote_addr

    # Exemple d'affichage des réponses soumises
    print(f"Pseudo: {{pseudo}}")
    for i, (question, _, _) in enumerate({quiz}):
        response_key = f'Question {{i+1}}'
        response = responses[response_key]
        print(f"{{response_key}}: {{response}}")

    # Enregistrez les réponses dans un fichier CSV avec l'adresse IP
    responses['IP'] = ip_address
    save_responses_to_csv(responses)

    # Émettre l'événement 'student_response' avec les réponses à tous les clients connectés
    emit('student_response', {{'pseudo': pseudo, 'responses': responses}}, namespace='/', broadcast=True)

    # Réponse de confirmation
    return 'Réponses soumises avec succès.'

if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)'''

    save_static_file(server_quiz_content, 'serverQuiz.py', module_dir)

    print(f"Le dossier '{module_dir}' et les fichiers HTML ont été créés avec succès.")

def read_file_content(file_name):
    # Lit le contenu d'un fichier et le retourne
    with open(file_name, 'r', encoding='utf-8') as file:
        content = file.read()  # Lecture du contenu du fichier
    return content  # Retourne le contenu du fichier

def main():
    # Fonction principale pour exécuter le programme
    file_name = input("Entrez le nom du fichier .quiz : ")  # Demande à l'utilisateur d'entrer le nom du fichier .quiz
    create_quiz_module(file_name)  # Crée un module de quiz à partir du fichier spécifié

# Début du programme principal
if __name__ == '__main__':
    # Exécute le code suivant uniquement lorsque ce module est exécuté directement en tant que programme principal
    main()
