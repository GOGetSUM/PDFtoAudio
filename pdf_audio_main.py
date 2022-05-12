from tkinter import *
import pytesseract
from pdf2image import convert_from_path
from boto3 import Session, client
from botocore.exceptions import BotoCoreError, ClientError
import pygame
import time


# _____________PDF to Text__using pdf2image_pytesseract _____this process does not rely on PDF for text structure__converts to image then text extract_________________________________________
def create_text():
    # initialize pytesseract and pdf2image
    # environment variables if you like
    poppler_path = r'C:\Program Files\poppler-0.68.0\bin'
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # conver PDF to image
    text_ = textbox.get(1.0, END)
    print(text_)
    images =  convert_from_path(f'{text_[:-4]}pdf',poppler_path=poppler_path)
    # extract text using pytesseract
    text = pytesseract.image_to_string(images[0])
    text_file = open(f'{text_[:-4]}_Script.txt','w')
    text_ =text
    text_= text_file.write(text_)
    text_file.close()
    print(text) #success
    create_speech(text=text)

def create_speech(text):
    polly = client('polly')
    spoken_text = polly.synthesize_speech(Text=text,
                                                    OutputFormat='mp3',
                                                    VoiceId='Russell')
    with open('output.mp3', 'wb') as f:
        f.write(spoken_text['AudioStream'].read())
    pygame.mixer.init()
    pygame.init()
    sound = pygame.mixer.Sound('output.mp3')
    sound_length = sound.get_length()
    sound.play()
    time.sleep(sound_length)


# ________________________GUI SET UP_____________________________________________
window = Tk()
window.title('Speed Test')
window.config(padx=100,pady=50, bg='grey')

tittle_label=  Label(padx=10,pady=10, bg='green', text="Please insert the PDF file path and hit CONVERT!")
tittle_label.grid(column=0,columnspan=3,row=1)

textbox = Text(height=1, width=100)
textbox.focus()
textbox.grid(column=0,columnspan=3,row=3)

submit_ = Button(pady=5,padx=5,text='CONVERT', command=create_text)
submit_.grid(column=0,columnspan=3,row=4)

quit_button = Button(text="Quit", command=window.destroy).grid(column=1, row=6)


window.mainloop()