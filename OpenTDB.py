from .QuestionTransformer import QuestionTransformer
import requests


class OpenTDB():
    base_url = "https://opentdb.com/api.php?amount={amount}&category={category}&difficulty={difficulty}&encode=url3986"

    def __init__(self):
        self.transformer = QuestionTransformer()

    def create_url(self, amount, category, difficulty):
        final_url = self.base_url.replace("{amount}", amount)
        final_url = final_url.replace("{category}", category)
        final_url = final_url.replace("{difficulty}", difficulty)
        return final_url

    def get(self, amount, category, difficulty):
        url = self.create_url(amount, category, difficulty)
        response = requests.get(url)
        json = response.json()
        return self.transformer.run(json['results'])
