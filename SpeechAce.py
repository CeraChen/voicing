import json
import requests

class SpeechAce:
    def __init__(self, api_key) -> None:  
        self.api_key = api_key
        self.api_endpoint = "https://api2.speechace.com" 
        self.dialect = "en-us"
        self.user_id = "qef_test"
        
        self.premium_url =  self.api_endpoint + "/api/scoring/speech/v9/json" + \
                    '?' + 'key=' + self.api_key + \
                    '&dialect=' + self.dialect + \
                    '&user_id=' + self.user_id
                    
    
    def _get_premium_task_url(self, task_type):
        #"https://api.speechace.co/api/scoring/task/v9/json" + \
        self.premium_task_url = "https://api2.speechace.com/api/scoring/task/v9/json" + \
                    '?' + 'key=' + self.api_key + \
                    '&task_type=' + task_type + \
                    '&dialect=' + self.dialect + \
                    '&user_id=' + self.user_id
        # print(self.premium_task_url)
                    
                    
    def print_result(self, result):
        try:
            print("IELTS overall:\t", result["speech_score"]["ielts_score"]["overall"])
            print("Pronunciation:\t", result["speech_score"]["ielts_score"]["pronunciation"])
            print("Fluency:\t", result["speech_score"]["ielts_score"]["fluency"])
            print("Coherence:\t", result["speech_score"]["ielts_score"]["coherence"])
            print("Grammar:\t", result["speech_score"]["ielts_score"]["grammar"])
            print("Vocabulary:\t", result["speech_score"]["ielts_score"]["vocab"])
            print("Transcript:\n", result["speech_score"]["transcript"])
        except:
            print("Fail to get speech_score")
            
    
    def print_task_result(self, result, context_file):
        try:
            print("Score based on context {}:\t".format(context_file), result["task_score"]["score"])
            return result["task_score"]["score"]
        except:
            return None
        
        
        
        
    def send_premium_request(self, audio_path):
        payload ={
            'include_fluency': '1', 
            'include_intonation': '1',
            'include_speech_score': '1',
            'include_ielts_subscore': '1',
            'include_ielts_feedback': '1',
        }
        audio = open(audio_path, 'rb')
        files = {'user_audio_file': audio}
        response = requests.post(self.premium_url, data=payload, files=files)
        json_result = json.loads(str(response.text))
        result = json.dumps(json_result, indent=4)
        
        splits = audio_path.split("/")
        file_path = "./src/text/response_sample1.json"
        with open(file_path, 'w') as f:
            f.write(result)
        print("Saved result to {}".format(file_path))        
        self.print_result(json_result)
        
        return result
    
    
    def send_premium_task_request(self, audio_path, task_type, task_context, context_file="", id=None):
        payload ={
            'include_fluency': '1', 
            'include_intonation': '1',
            'include_speech_score': '1',
            'include_ielts_subscore': '1',
            'include_ielts_feedback': '1',
            'task_context': task_context,
        }
        audio = open(audio_path, 'rb')
        files = {
            'user_audio_file': audio,
            }
        self._get_premium_task_url(task_type)
        response = requests.post(self.premium_task_url, data=payload, files=files)
        json_result = json.loads(str(response.text))
        result = json.dumps(json_result, indent=4)
        
        splits = audio_path.split("/")
        if id is not None:
            file_path = "./results/" + splits[-1][:-4] + "_" + str(id+1) + ".json"
        else:
            file_path = "./results/" + splits[-1][:-3] + "json"
            
        with open(file_path, 'w') as f:
            f.write(result)
        if id == 0:
            print("Saved result to {}".format(file_path))
            self.print_result(json_result)       
        score = self.print_task_result(json_result, context_file)
        
        return score
    