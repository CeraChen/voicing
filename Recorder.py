 
import datetime
import wave
import pyaudio
import keyboard
from SpeechAce import SpeechAce


CHUNK = 1024
FORMAT = pyaudio.paInt16  # 16bit encoding wav
CHANNELS = 1  # single
RATE = 16000  # sample rate
MAX_RECORD_SECONDS = 2 * 58 # no longer than 2 minute 
MAX_LOOP_NUM = int(RATE / CHUNK * MAX_RECORD_SECONDS)

START = 0
END = 1

    

class Recorder:
    def __init__(self, api_key, to_assess=True) -> None:
       self.speechace = SpeechAce(api_key) 
       self.isRecording = False
       self.frames = []
       self.audio = None
       self.stream = None 
       
       self.task_assigned = False
       self.to_assess = to_assess
       
    def assign_task(self, task_type, task_context):
        self.task_assigned = True
        self.task_type = task_type
        self.task_context = task_context       
       
    def start_recording(self):
        self.isRecording = True
        self.audio = pyaudio.PyAudio()        
        self.stream = self.audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
        print("Recording starts. Please speak:\n")    
        i = 0
        while True:
            data = self.stream.read(CHUNK)
            self.frames.append(data)        
            i += 1
            if(keyboard.is_pressed("space") or i == MAX_LOOP_NUM):
                if(i == MAX_LOOP_NUM):
                    print("Exceed two minute. Recording ends.")
                else:
                    self.beep(END)
                    print("-- Space is pressed --")      
                return self.stop_recording()
    
    
    def stop_recording(self):  
        self.isRecording = False
        audio_name = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S.wav")
        audio_path = "./speech/" + audio_name
        
        try:
            self.stream.stop_stream()
            self.stream.close()
            self.audio.terminate() 
            print("Recording ends. Please wait...\n")     
            
            wf = wave.open(audio_path, 'wb')
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(self.audio.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            print(f"Saved speech to {audio_path}")
            
            if self.to_assess:
                if self.task_assigned:
                    self.speechace.send_premium_task_request(audio_path, self.task_type, self.task_context)
                else:
                    self.speechace.send_premium_request(audio_path)
            
        except Exception as e:
            print(e)     
               
        self.frames = [] 
        return audio_path
        
        
    def beep(self, state):
        file_name = './audio/{}.wav'.format("start" if state == START else "end")    
        file = wave.open(file_name, 'rb')
        sample_rate = file.getframerate()
        num_channels = file.getnchannels()
        sample_width = file.getsampwidth()
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(sample_width),
                        channels=num_channels,
                        rate=sample_rate,
                        output=True)
        data = file.readframes(CHUNK)
        while data:
            stream.write(data)
            data = file.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        p.terminate()
        file.close()  
            