import os
from tkinter import filedialog
from tinytag import TinyTag
from pathlib import Path
import csv
from stat import *
from datetime import datetime
from tkinter import *

audio_file_extensions = ['.wav', '.ogg', '.aif', '.aiff', '.aifc',
                         '.caf', '.cda', '.raw', '.Pcm', '.oga',
                         '.flac', '.fla', 'm4a', '.CAF', '.shn',
                         '.ape', '.wma', '.mp3', '.vqf', '.vql',
                         '.vqe', '.wma', '.asf', '.wma', '.wmv', '.aac',
                         '.mp4', '.m4a', '.m4b', '.m4r]'
                         ]
field_names = ['Titre','Album', 'Interprète', 'Interprète de l\'album', 'Durée', 'Genre', 'Date de création', 'Date de modification', 'Taille']
window = Tk()
window.source_folder=''
files_to_keep = []


def walktree(top, callback):
    """recursively descend the directory tree rooted at top,
       calling the callback function for each regular file"""

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
            file_name, extension = os.path.splitext(pathname)
            if extension in audio_file_extensions:
                files_to_keep.append(pathname)
        else:
            # Unknown file type, print a message
            print('Skipping %s' % pathname)


def visitfile(file):
    print('visiting', file)


def choose_dir():
    """This function is used to choose the directory where audio files are located"""
    window.source_folder = filedialog.askdirectory(parent=window, initialdir='.', title="Sélectionner le répertoire dans lequel se trouve vos fichiers de musique")


def create_file(file_name,files_to_keep):
    csv_file = open(file_name, 'w')
    with csv_file:
        writer = csv.writer(csv_file, delimiter=';',  quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(field_names)
        for file in files_to_keep:
            tag = TinyTag.get(file)
            title = tag.title
            album = tag.album
            artist = tag.artist
            album_artist = tag.albumartist
            duration = float(tag.duration) / 100
            genre = tag.genre
            creation_date = datetime.fromtimestamp(os.path.getctime(file)).__format__("%d/%m/%Y %H:%M")
            modification_date = datetime.fromtimestamp(os.path.getmtime(file)).__format__("%d/%m/%Y %H:%M")
            filesize = '{} Mo'.format(str(float(tag.filesize) / 1000000))
            writer.writerow([title, album, artist, album_artist, duration, genre, creation_date, modification_date, filesize])
    csv_file.close()


choose_dir()
window.destroy()
window.mainloop()

walktree(window.source_folder, visitfile)
files_to_keep.sort()
home = str(Path.home())
now = datetime.now()
dte_string = now.strftime("%Y%m%d%H%M")
file_name = '{}/musiques_{}.csv'.format(home, dte_string)

create_file(file_name, files_to_keep)


