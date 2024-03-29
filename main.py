import pyaudio
import wave
import time
import sys
import struct

if len(sys.argv) < 2:
    print("Plays a wave file.\n\nUsage: %s filename.wav" % sys.argv[0])
    sys.exit(-1)


wf = wave.open(sys.argv[1], 'rb')
index = wf.getnframes() - 1024
wf.setpos(index)
p = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    global index
    data = wf.readframes(frame_count)
    data = data[::-1]
    index -= 1024
    if index < 0:
        return data, pyaudio.paAbort
    else:
        wf.setpos(max(index, 0))
        return data, pyaudio.paContinue

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()
