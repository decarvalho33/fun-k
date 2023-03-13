class Music:
    def __init__(self, link, name, bpm=None, intro_second=None):
        self.link = link
        self.name = name
        self.file_name = f'{name}.wav'
        self.bpm = bpm
        self.errors = []
        self.intro_second = intro_second
        #self.intro_time_automatically = intro_time_automatically
        #self.changes = []
        #self.cuts = []
        self.bpm_librosa = -1
    
    def get_link(self):
        return self.link

    def get_name(self):
        return self.name
    
    def get_file_name(self):
        return self.file_name

    def get_bpm(self):
        return self.bpm
    
    def get_bpm_librosa(self):
        return self.bpm_librosa
    
    def set_bpm_librosa(self, bpm_librosa):
        self.bpm_librosa = bpm_librosa

    def get_intro_second(self):
        return self.intro_second

def compare_bpms(musics):
    musics_with_bad_bpm_librosa = []
    
    for music in musics:
        name, bpm, bpm_librosa = music.get_name(), music.get_bpm(), music.get_bpm_librosa()
        if abs(bpm-bpm_librosa) > 5:
            musics_with_bad_bpm_librosa.append([name, bpm, bpm_librosa])
    print(f'\n\tThere are {len(musics_with_bad_bpm_librosa)} bpms above 5+- error range in all {len(musics)}\n')
    for music in musics_with_bad_bpm_librosa:
        print(f'\n\tMusic: {music[0]}\n\tBPM by Google: {music[1]}\n\tBPM by Librosa: {music[2]}\n')