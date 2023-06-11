from pydub import AudioSegment
import io

def wav_to_mp3(wav_data: bytes, path_to_mp3: str):
    s = io.BytesIO(wav_data)
    AudioSegment.from_wav(s).export(path_to_mp3, format="mp3")


if __name__ == '__main__':
    with open("wav/file_example_WAV_1MG.wav", "rb") as binary_file:
        wav_to_mp3(binary_file.read(), "mp3/my_file.mp3")