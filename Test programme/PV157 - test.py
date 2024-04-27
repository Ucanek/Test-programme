import random


def load_questions(filename):
    questions = []
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        current_question = None
        for line in lines:
            line = line.strip()
            if line.startswith('===='):
                if current_question is not None:
                    questions.append(current_question)
                current_question = {'question': '', 'options': [], 'correct_answers': set()}
                answer_number = 0
            elif current_question is not None:
                if line.startswith('*-'):
                    current_question['options'].append(line[1:])
                    current_question['correct_answers'].add(answer_number)
                    answer_number += 1
                else:
                    if not current_question['question']:
                        current_question['question'] = line
                    else:
                        current_question['options'].append(line)
                    answer_number += 1
        if current_question is not None:
            questions.append(current_question)
    return questions


def ask_question(question):
    print(question['question'])
    for i, option in enumerate(question['options'], start=1):
        print(f'  {i}. {option}')
    user_input = input("Zadejte číslo (nebo více čísel oddělených mezerou) správné odpovědi: ")
    user_answers = {int(i) for i in user_input.split()}
    correct_answers = question['correct_answers']
    
    correct_user_answers = user_answers.intersection(correct_answers)
    incorrect_user_answers = user_answers.difference(correct_answers)
    question_score = len(correct_user_answers) * 2 - len(incorrect_user_answers) * 2
    return question_score, correct_answers


def main():
    num_questions = int(input("Zadejte počet otázek: "))
    questions = load_questions('data-PV157-exam.txt')
    random.shuffle(questions)
    max_possible_score = sum(len(question['correct_answers']) for question in questions[:num_questions]) * 2
    score = 0

    for i, question in enumerate(questions[:num_questions], start=1):
        print(f"Otázka {i}:")
        result, correct_answers = ask_question(question)
        score += result
        if result == len(correct_answers) * 2:
            print(f"Správně! Získáno {result} bod(ů).\n")
        else:
            print(f"Nesprávně. Správné odpovědi byly: {', '.join(map(str, correct_answers))}. Zisk {(result)} bod(ů).\n")

    total_questions = len(questions)
    print(f"Skóre: {score}/{max_possible_score}")
    
    while True:
        user_input = input("Stiskněte Enter pro ukončení programu.")
        if user_input == "":
            break


if __name__ == "__main__":
    main()