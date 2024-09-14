import json


class KeyframesManager:
    def __init__(self):
        self.data = {'frame': {}}
        self.load_keyframes()

    def load_keyframes(self):
        try:
            with open('keyframes.json', 'r') as json_file:
                data = json.load(json_file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {'frame': {}}
            self.save_keyframes(data)  # Créer un fichier avec des données par défaut
        return data

    def save_keyframes(self, data):
        with open('keyframes.json', 'w') as json_file:
            json.dump(data, json_file, indent=3)

    def add_key(self, list_to_add, key_number):
        self.data['frame'][str(key_number)] = list_to_add
        self.save_keyframes(self.data['frame'][str(key_number)])

    def remove_key(self, key_number):
        if str(key_number) in self.data['frame']:
            del self.data['frame'][str(key_number)]
            self.save_keyframes()
        else:
            print(f"Keyframe {key_number} does not exist.")

    def update_keyframe(self, key_number, list_to_update):
        if str(key_number) in self.data['frame']:
            self.data['frame'][str(key_number)] = list_to_update
            self.save_keyframes()
        else:
            print(f"Keyframe {key_number} does not exist.")


def create_keyframes_json(num_frames):
    keyframes_manager = KeyframesManager()
    keyframes = {}
    for i in range(1, num_frames + 1):
        keyframes[str(i)] = {
        }
    keyframes_manager.data['frame'] = keyframes
    keyframes_manager.save_keyframes(keyframes_manager.data)


num_frames = 100
create_keyframes_json(num_frames)
