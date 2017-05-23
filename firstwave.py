import wave
import array
import math
f = wave.open("solo.wav", 'r')
channels = f.getnchannels()  
samplewidth = f.getsampwidth() # -- returns sample width in bytes      
framerate = f.getframerate()  #-- returns sampling frequency
numframes = f.getnframes()    #-- returns number of audio frames
comptype = f.getcomptype()   #-- returns compression type ('NONE' for linear samples)
compname = f.getcompname()  # -- returns human-readable version of
params = f.getparams()     #-- returns a namedtuple consisting of all of the
frames = f.readframes(numframes)   #returns at most n frames of audio
f.close()

print samplewidth
print framerate
print numframes
print comptype
print compname
print params
list1 = []
for i in range(len(frames)):
	#print frames [i]
	list1.append(int(ord(frames [i])/2))
	#print list1 [i]
	#list1[i] = ord(list1 [i]) *2
	#print list1
	#print (" ")
	#frames[i] = 0
	#print frames [i]
	#print "\n"
#print ord(list1 [0])
#print list1 [1]
f = wave.open("solodist1.wav", 'w')
f.setnchannels(channels) #-- set the number of channels
f.setsampwidth(samplewidth) #-- set the sample width
f.setframerate(framerate) #-- set the frame rate
f.setnframes(numframes)   #-- set the number of frames
f.setcomptype(comptype, compname)  #-- set the compression type and the human-readable compression type
f.setparams(params)# -- set all parameters at once
#f.tell()          #-- return current position in output file
#f.writeframesraw()
                  #    -- write audio frames without pathing up the file header
#for i in range (len(frames)):  
thingy = str(bytearray(list1))       
f.writeframes(thingy)
	#print list1[i]
                  #   -- write audio frames and patch up the file header
f.close()         #-- patch up the file header and close the output file