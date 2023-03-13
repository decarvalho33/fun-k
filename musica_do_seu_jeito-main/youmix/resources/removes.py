from os import remove

def remove_speeded():
    try:
        remove('speeded.wav')
    except Exception:
        pass
    
def remove_source():
    try:
        remove('source.wav')
    except Exception:
        pass
    
def remove_source_temp():
    try:
        remove('source.temp.wav')
    except Exception:
        pass

def remove_source_wav_part():
    try:
        remove('source.wav.part')
    except Exception:
        pass

def remove_all():
    remove_speeded()
    remove_source()
    remove_source_temp()
    remove_source_wav_part()