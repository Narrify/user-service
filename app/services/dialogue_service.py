import requests

class Dialogue:
    def __init__(self, story, settings, characters):
        self.story = story
        self.settings = settings
        self.characters = characters
        self.response = None

    def generate_dialogue(self):
        data = {
            "story": self.story,
            "settings": self.settings,
            "characters": self.characters
        }
        
        response = requests.post("http://127.0.0.1:8000/generate/dialog", json=data)
        
        if response.status_code == 200:
            self.response = response.json()
        else:
            self.response = {
                "error": "Failed to generate dialogue",
                "status_code": response.status_code,
                "details": response.text
            }

        return self.response
