import requests

class Story:
    def __init__(self, title, settings, characters, plots=1, endings=1):
        self.title = title
        self.settings = settings
        self.characters = characters
        self.plots = plots
        self.endings = endings
        self.response = None

    def generate_story(self):
        data = {
            "title": self.title,
            "settings": self.settings,
            "characters": self.characters,
            "plots": self.plots,
            "endings": self.endings
        }
        
        response = requests.post("http://127.0.0.1:8000/generate/story", json=data)
        
        if response.status_code == 200:
            self.response = response.json()
        else:
            self.response = {
                "error": "Failed to generate story",
                "status_code": response.status_code,
                "details": response.text
            }

        return self.response
