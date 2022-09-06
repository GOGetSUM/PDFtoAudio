import pytesseract
from pdf2image import convert_from_path
from boto3 import Session, client

import pygame
import time


class PDF_Manipulation:
    """ PDF Manipulation class creates text from a pdf and also creates audio from a txt script.

    There are two methods in this class, first is create_text() which takes in an PDF file path and fetches
    the text from this PDF file, Out-put is a .txt file.
    Second method is create_speech() where a given script as a .txt file is given and the method creates an
    audio mp3 file.

    Attributes:
        create_text(): Asks for PDF filepath from user and returns script text as printed on console and save (.txt)
        create_speech(text): Uses given argument text and returns audio, auto plays audio and saves .mp3
        file to location.

    Typical usage example:
        create_text()
        create_speech(text)
    """
    def __init__(self):
        self.create_text()
        self.create_speech()

    def create_text(speech=False,playback=False)->str:
        """Fetches text from PDF, outputs str on console and saves .txt file in location of filepath provided.

        On user input for file path to pdf, create_text() fetches text from given pdf file path.

        Args:
            speech:
                Bool input if True method create_speech(text) will be executed using given text,
                If false create_speech(text) will not be executed.

            playback:
                Bool input used in nested method call create_speech() if True create_speech() will playback audio.
                Else create_speech() will only save mp3 file to project folder location MP3.

        Returns:
            A string printed onto the console based on txt found in pdf file. It also saves a .txt file named
            "input pdf"_Script to location Scripts.

        """

        # initialize pytesseract and pdf2image
        poppler_path = r'C:\Program Files\poppler-0.68.0\bin'
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


        filePath = input('Please provide file path to PDF location:') # User input for file path.
        print(f'File Path provide: {filePath}\n')

        images =  convert_from_path(f'{filePath[:-3]}pdf',poppler_path=poppler_path) #converts pdf to image

        text = pytesseract.image_to_string(images[0]) # extract text using pytesseract

        # Creates and opens a text file, writes extracted text and closes file in location.
        # Prints text script to console
        text_file = open(f'{filePath[:-4]}_Script.txt','w')
        text_ = text
        text_ = text_file.write(text_)
        text_file.close()
        print(f'{text}\n')

        if speech:
            if playback:
                PDF_Manipulation.create_speech(text=text,playback=True)
            else:
                PDF_Manipulation.create_speech(text=text)






    def create_speech(text:str, playback =False):
        """Creates Audio mp3 file based on text argument.

        Leveraging the AWS Polly a cloud based service that converts text into spoken audio.
        VoiceID is set to Russell but can be change to any acceptable Voice ID per AWS polly.
        Output Format is set to mp3 but can be change to any acceptable AWS polly output format.

        Args:
            text:
                Any string formated text script.
            playback:
                Bool input if True create_speech() will playback audio.
                Else create_speech() will only save mp3 file to project folder location MP3.

        Returns:
            Playback in audio form of given text input.
            MP3 file save to location, MP3 folder. Please note 'OUTPUT.MP3' will be overwritten each time
            create_speech() is executed.
        """
        # Activate polly - settings for OutputFormat and VoiceID
        polly = client('polly')
        spoken_text = polly.synthesize_speech(Text=text,
                                                        OutputFormat='mp3',
                                                        VoiceId='Russell')

        # Creates mp3 file and writes audiostream to the file
        with open(f'MP3\OUTPUT.mp3', 'wb') as f:
            f.write(spoken_text['AudioStream'].read())

        # Leverages pygame to playback audio if playback argument is True.
        if playback:
            pygame.mixer.init()
            pygame.init()
            sound = pygame.mixer.Sound('MP3\OUTPUT.mp3')
            sound_length = sound.get_length()
            sound.play()
            time.sleep(sound_length)
