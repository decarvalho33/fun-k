from resources.functions import restrict_musics_number, download_process, beat_and_tempo_by_librosa, calc_tempo_by_alvraw, funk_by_bpm, export_wav, playback_by_audio_segment, load_librosa, load_audio_segment, slice_silence, bpm_sync, apply
from resources.errors import print_errors_all
from resources.removes import remove_all
from musics.musics_list import musics
import warnings
import os

warnings.filterwarnings('ignore') # I put it to stop: warnings of PySoundFile

youmix_musics_directory, musics_directory = os.getcwd()+'/musics/youmix musics', os.getcwd()+'/musics/musics'
os.chdir(musics_directory)

#NUMBER OF MUSICS YOU WANT - choose the number of musics in the parameter 'musics_number'
musics, musics_number = restrict_musics_number(musics, musics_number=40)

#MUSICS DOWNLOAD
ydl_opts = download_process(musics_number, musics, musics_directory)

while musics_number > 0:
    musics_number -= 1
    name, file_name, bpm = musics[musics_number].get_name(), musics[musics_number].get_file_name(), musics[musics_number].get_bpm()
    if(file_name in os.listdir(musics_directory)):
        try:
            #LOADING ORIGINAL AUDIO; TAKING BPMS AND BEATS BY
            original = load_audio_segment(file_name, name)
            original_audio_time_series, original_sampling_rate_of_audio_times_series = load_librosa(file_name, name)

            #TEMPO AND BEATS BY LIBROSA
            tempo, beats = beat_and_tempo_by_librosa(original_audio_time_series, original_sampling_rate_of_audio_times_series, name)

            #INTRO DETECTION

            #TEMPO CALCS from Alvraw
            tempo, playback_bpm = calc_tempo_by_alvraw(tempo)

            #LOAD FUNK BY BPM
            funk_file_name = funk_by_bpm(int(tempo))
            y_version, sr_version = load_librosa(funk_file_name, name)
            playback = playback_by_audio_segment(funk_file_name, name)

            #START PROCESS  - SLICE  
            sliced = slice_silence(original_audio_time_series, original_sampling_rate_of_audio_times_series, original, name)
            
            #BPM SYNC
            version_synced = bpm_sync(tempo, playback_bpm, playback, name)

            #APPLY VERSION
            sliced_baixo, version_synced_alta= sliced - 10, version_synced + 5
            final = apply(sliced_baixo, version_synced_alta, name)

            #END PROCESS - EXPORT RESULT
            export_wav(final, youmix_musics_directory, musics_directory, name, music_name=f'{name} - YouMix v.wav')
        except Exception:
            print(f'\nError in music {name}')
            raise Exception #Comment it to pass the exception 
    remove_all()
print_errors_all()