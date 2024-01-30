import numpy as np


class QuestionTransformer:
    points = {
        "hard": 10,
        "medium": 5,
        "easy": 1
    }

    def run(self, api_data):
        custom_response = []
        for q in api_data:
            answers = [
                {"answer": q['correct_answer'], "points": self.points[q['difficulty']]}
            ]
            for a in q['incorrect_answers']:
                answers.append({"answer": a, "points": 0})
            np.random.shuffle(answers)
            custom_response.append({
                'question': q['question'],
                'answers': answers
            })

        return custom_response
