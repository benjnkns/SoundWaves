#!/usr/bin/env python
# -*- coding: utf-8 -*-
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.



import sys
import wave
import struct
import math

def main():
	if len(sys.argv)!=3:
		print "Usage: InputFile.wav OutputFile.wav"

	else:
		
		buffer = []
		bufferlength = 0
		
		try:
			
			drySignal = wave.open(sys.argv[1], 'r')
		except EOFError:
			print "Error: Input file is not a wave file"
			return 0
		except IOError:
			print "Error: File does not exist"
			return 0
			
		inputParams = drySignal.getparams()
		
		if inputParams[0:3] != (2, 2, 44100) or inputParams[4:6] != ('NONE', 'not compressed'):
			print "Error: Not a compatible input file"
			print "Input file must be a 2 channel, 16 bit, 44100HZ, uncompressed wave file"
			drySignal.close()
			return 0

		inputLength = drySignal.getnframes()
		
		completedFrames = 0
		
		wetSignal = wave.open(sys.argv[2], 'w')
		
		wetSignal.setparams((2, 2, 44100, 0, 'NONE', 'not compressed'))
		
		sample = drySignal.readframes(1)
		print "Distorting...Please Wait"
		while(sample):
			
			
			numCH1 = struct.unpack("<hxx", sample)[0]
			numCH2 = struct.unpack("<xxh", sample)[0]
	
			# convert to float for division
			floatCH1 = float(numCH1)
			floatCH2 = float(numCH2)
	
			# normalize
			normCH1 = floatCH1 / 100
			normCH2 = floatCH2 / 100
			
			# compute arctan for distortion
			
			distCH1 = math.atan(normCH1)
			distCH2 = math.atan(normCH2)
			#distCH1 = normCH1
			#distCH2 = normCH2
			# convert back to INT and amplify
			
			intDistCH1 = int(distCH1 * 100)
			intDistCH2 = int(distCH2 * 100)
			
			# pack into WAVE format
			
			packCH1 = struct.pack('h' , intDistCH1)
			packCH2 = struct.pack('h', intDistCH2)
			
			# output
			
			
			buffer.append(packCH1)
			buffer.append(packCH2)
			bufferlength = bufferlength + 1
			# If buffer contains 44100 samples dump buffer to output and display percent complete
			if bufferlength == 44100:
				completedFrames = completedFrames + 44100
				bufferlength = 0
				buffer_str = ''.join(buffer)
				# clear buffer
				del buffer[:]
				wetSignal.writeframes(buffer_str)
				
				print str((float(completedFrames) / float(inputLength))*100) + "% completed"
			
			
			sample = drySignal.readframes(1)
	
		
		# dump anything that is still in the buffer before closing
		buffer_str = ''.join(buffer)
		del buffer[:]
		wetSignal.writeframes(buffer_str)
		
		drySignal.close()
		wetSignal.close()
		print "Done"
	
	return 0

if __name__ == '__main__':
	main()