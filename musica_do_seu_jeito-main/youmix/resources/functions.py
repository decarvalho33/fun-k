from pydub import AudioSegment, effects
from .errors import append_error
import youtube_dl
import librosa
import os

def restrict_musics_number(musics, musics_number):
    musics_number = musics_number if(musics_number <= len(musics)) else len(musics)
    musics = musics[:musics_number] if(musics_number <= len(musics)) else musics
    return musics, musics_number 

def download_by_youtube_dl(name, link):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{name}.wav',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        return  ydl_opts        
    except Exception:
        append_error('youtube_download', name)

def download_process(musics_number, musics, musics_directory):
    if len(os.listdir(musics_directory)) < musics_number:
        ydl_opts = []
        i = -1
        while(len(os.listdir(musics_directory)) < musics_number):
            i+=1
            name, link = musics[i].get_name(), musics[i].get_link()
            if f'{name}.wav' not in os.listdir(musics_directory):
                try:
                    ydl_opts.append(download_by_youtube_dl(name, link))
                except Exception:
                    append_error('Download', name)

def load_audio_segment(file_name, name):
    try:
        return AudioSegment.from_file(file_name)
    except Exception:
        append_error(f'load_audio_segment there is not {file_name} in the {os.getcwd()} directory')
        raise Exception

def load_librosa(file_name, name):
    try:
        original_audio_time_series, original_sampling_rate_of_audio_times_series = librosa.load(file_name)
        return original_audio_time_series, original_sampling_rate_of_audio_times_series
    except Exception:
        append_error('load_librosa', name)
        raise Exception

def beat_and_tempo_by_librosa(original_audio_time_series, original_sr, name):
    try:
        return librosa.beat.beat_track(y=original_audio_time_series, sr=original_sr)
    except Exception:
        append_error('tempo, beats = librosa.beat.beat_track()', name)
        raise Exception

def calc_tempo_by_alvraw(tempo):
    tempo = tempo * 2 if (tempo < 100) else tempo
    alhpa_tempo = tempo % 5,
    playback_bpm_semint = tempo-alhpa_tempo
    playback_bpm = int(playback_bpm_semint)
    return tempo, playback_bpm

def funk_by_bpm(bpm):
    if bpm<=160 and bpm>=100:
        return f'../funks/funk{bpm-bpm%5}.wav'
    elif bpm >160:
        return f'../funks/funk{160}.wav'
    else:
        return f'../funks/funk{100}.wav'

def playback_by_audio_segment(file_name, name):
    try:
        return AudioSegment.from_file(file_name)
    except Exception:
        append_error('playback_by_audio_segment', name)
        raise Exception

def slice_silence(original_audio_time_series, original_sampling_rate_of_audio_times_series, original, name):
    try:
        oenv = librosa.onset.onset_detect(y=original_audio_time_series, sr=original_sampling_rate_of_audio_times_series, units='time')
        duration_in_milliseconds = len(original)
        duration_sliced = duration_in_milliseconds - (oenv[0]*1000)
        sliced = original[-duration_sliced:]
        return sliced
    except Exception:
        append_error('slice_silence', name)
        raise Exception

def bpm_sync(sync_bpm_1, sync_bpm_2, sync_input, name):
    try:
        alfa_sync = (sync_bpm_1 / sync_bpm_2)
        playback_speeded = effects.speedup(sync_input, alfa_sync)
        playback_speeded.export('speeded.wav', format='wav')
        playback_speeded = AudioSegment.from_file('speeded.wav')
        return playback_speeded
    except:
        append_error('bpm_sync', name)
        raise Exception

def apply(original, versao, name):
    try:
        final = original.overlay(versao, loop=True)
        return final
    except:
        append_error('apply', name)
        raise Exception

def export_wav(music, youmix_musics_directory, current_directory, name, music_name):
    try:
        os.chdir(youmix_musics_directory)
        music.export(music_name, format='wav')
        os.chdir(current_directory)
        print(f'\nMusic {name} successfully converted!')
    except Exception:
        append_error('export_wav', name)
        raise Exception