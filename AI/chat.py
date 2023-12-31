import json
from difflib import get_close_matches
import sys

# Function to load knowledge base from a JSON file
def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

# Function to save knowledge base to a JSON file
def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Function to find the best match for a user question
def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

# Function to get the answer for a specific question from the knowledge base
def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

# Class definition for CampingChatbot
class CampingChatbot:
    def stop_program(self):
        print("Isgoed. Doei doei!")
        sys.exit()

    def __init__(self):
        self.name = ""
        self.toilet = ""
        self.speeltuin = ""

    def get_user_info(self):
        # Collect user information for camping preferences
        print("Hi! Ik ben jouw camping chatbot. Ik kan jouw helpen met het kiezen van de juiste plek en eventuele andere vragen.")
        self.name = input("Hoe kan ik je noemen? ")
        print(f"\nLeuk je te ontmoeten, {self.name}! Ik zal je nu aan paar vragen stellen om de beste plek voor jouw uit te kiezen.")
        self.toilet = input("Moet ik een kampeerplek regelen die niet te ver van 't toilet is? (Ja/Nee) ")
        self.speeltuin = input("Wil je een plekje dichtbij de speeltuin? (Ja/Nee) ")

    def suggest_camping_location(self):
        # Suggest a camping location based on user preferences
        print(f"\nHoi, {self.name}! Gebaseerd op jouw keuzes, raad ik deze plek aan:")

        if "ja" in self.toilet.lower() and "ja" in self.speeltuin.lower():
            print(" A is de juiste plek voor jou!")
        elif "ja" in self.toilet.lower() and "nee" in self.speeltuin.lower():
            print(" B is de juiste plek voor jou!")
        elif "nee" in self.toilet.lower() and "ja" in self.speeltuin.lower():
            print(" C is de juiste plek voor jou!")
        elif "nee" in self.toilet.lower() and "nee" in self.speeltuin.lower():
            print(" D is de juiste plek voor jou!")
        elif "" in self.toilet.lower() and "" in self.speeltuin.lower(): 
            continue_chat = input('Het was voor mij niet duidelijk. Wil je de test opnieuw doen? (ja/nee): ')
            if continue_chat.lower() == 'nee':
                print("oke?")

    def stop_program(self):
        # Stop the program and exit
        print("Isgoed. Doei doei!")
        sys.exit()

    def main(self):
        # Main function to run the camping chatbot
        self.get_user_info()
        self.suggest_camping_location()

        continue_chat = input('Wil je blijven chatten? (ja/nee): ')
        if continue_chat.lower() == 'nee':
            self.stop_program()
        else:
            print("Wat zijn je andere eventuele vragen?")

    def chat_bot(self):
        # Function to interact with the chatbot, handle user queries, and update the knowledge base
        knowledge_base: dict = load_knowledge_base('knowledge_base.json')

        while True:
            user_input: str = input('You: ')

            if user_input.lower() == 'quit':
                break

            best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

            if best_match:
                answer: str | None = get_answer_for_question(best_match, knowledge_base)
                if answer:
                    print(f'Bot: {answer}')
                    continue  
                else:
                    print(f'Bot: Ik weet het antwoord niet voor "{best_match}". kun je het me leren?')
                    new_answer: str = input('Type the answer or "skip" to skip: ')

                    if new_answer.lower() != 'skip':
                        knowledge_base['questions'].append({"question": best_match, "answer": new_answer})
                        save_knowledge_base('knowledge_base.json', knowledge_base)
                        print(f'Bot: bedankt! Ik heb een nieuw antwoord geleerd voor "{best_match}"!')
            else:
                print('Bot: Ik weet het antwoord niet, kun je het mij leren?')
                new_answer: str = input('Typ de vraag of skip om te skippen: ')

                if new_answer.lower() != 'skip':
                    new_answer_response: str = input('Type het antwoord: ')
                    knowledge_base['questions'].append({"question": new_answer, "answer": new_answer_response})
                    save_knowledge_base('knowledge_base.json', knowledge_base)
                    print(f'Bot: Bedankt! Ik heb een nieuw antwoord geleerd voor "{new_answer}"!')

            continue_chat = input('Wil je blijven chatten? (ja/nee): ')
            if continue_chat.lower() == 'nee':
                self.stop_program()
            else:
                print("Wat zijn je andere eventuele vragen?")

# Run the camping chatbot if this script is executed directly
if __name__ == '__main__':
    camping_bot = CampingChatbot() 
    camping_bot.main()
    camping_bot.chat_bot()
