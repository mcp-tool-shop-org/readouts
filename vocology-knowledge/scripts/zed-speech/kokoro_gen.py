import sys, warnings
warnings.filterwarnings('ignore')
from kokoro import KPipeline
import soundfile as sf

text_file = sys.argv[1]
voice      = sys.argv[2]
speed      = float(sys.argv[3])
wav_file   = sys.argv[4]

with open(text_file, 'r', encoding='utf-8') as f:
    text = f.read()

pipeline = KPipeline(lang_code='a')
generator = pipeline(text, voice=voice, speed=speed)
for i, (gs, ps, audio) in enumerate(generator):
    sf.write(wav_file, audio, 24000)
    break
