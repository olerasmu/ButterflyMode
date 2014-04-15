'''
Created on 18. mars 2014

@author: olerasmu
'''

import math
import os
import timeit
import sys
from Crypto.Cipher import AES


#===============================================================================
# This now works with files which have a number of blocks n that is a power of 2
#===============================================================================
class Butterfly(object):
    
    def __init__(self, filepath=None):
        self.filepath = filepath
        #self.f = open(filepath, 'rb')
        #print (filepath)
        
    fileTab = []
    butterflyTab = []
    
    #Return the size of file in bytes
    def fileSize(self):
        tempFile = open(self.filepath, 'rb')
        tempFile.seek(0,2)
        size = tempFile.tell()
        tempFile.seek(0,0)
        tempFile.close()
        return size
    
    #Slit the file into blocks of 128 bit (16*8 bytes)    
    def blockifyFile(self):
        with open(self.filepath, 'rb') as newfile:
            byte = newfile.read(16)
            while byte:
                self.fileTab.append(byte)
                #print (byte)
                byte = newfile.read(16)
            #print ("File has been divided into blocks")
        
        #print (self.fileTab)
        
        
    fileTabTest = []
    def blockifyFileTwo(self, filepath):
        with open(filepath, 'rb') as newfile:
            byte = newfile.read(16)
            while byte:
                self.fileTabTest.append(byte)

                #print byte
                byte = newfile.read(16)
            #print ("File has been divided into blocks")
        return self.fileTabTest
    
    
    def fileifyBlocks(self, filepath, butterflyTab):
        with open(filepath, 'ab') as hourglass_file:
            for byte in butterflyTab:
                hourglass_file.write(byte)
    
    #Initialize the butterfly function. Variable j is controlled from here
    def initiateButterfly(self, d, n):
        self.butterflyTab = [None]*n
        #print ("initiate")
        for j in range(1, d+1):
            #print "this is j: ", j
            self.executeButterfly(j, n)
    
    #count = 0
    #Execute the butterfly algorithm
    def executeButterfly(self, j, n):
        #print ("execute")
        #print ("this is j: ", j)    
        for k in range(0, int((n/math.pow(2, j))-1)+1):
            #print ("this is k: ", k)
            if j == 1:
                for i in range(1, int(math.pow(2, j-1))+1):
                    indexOne = int(i+k*math.pow(2, j))-1
                    indexTwo = int(i+k*math.pow(2, j)+math.pow(2, j-1))-1
                    #self.count += 1
                    self.w(self.fileTab[indexOne], self.fileTab[indexTwo], indexOne, indexTwo)
                    
                    #print indexOne, " ", indexTwo
            else:        
                for i in range(1, int(math.pow(2, j-1))+1):
                    indexOne = int(i+k*math.pow(2, j))-1
                    indexTwo = int(i+k*math.pow(2, j)+math.pow(2, j-1))-1
                    #self.count += 1
                    self.w(self.butterflyTab[indexOne], self.butterflyTab[indexTwo], indexOne, indexTwo)
                    
                    #print indexOne, " ", indexTwo
                #print ("this is i: ", i)
                #print ("this is index one: ", indexOne, " and this is index two: ", indexTwo)
                #===============================================================
                # temp = [int(i+k*math.pow(2, j))-1, int(i+k*math.pow(2, j)+math.pow(2, j-1))-1]
                # print temp
                #===============================================================
        #print ("count: ", self.count)
        #print (self.butterflyTab)
    

    cipher_machine = AES.new(b'This is a key123', AES.MODE_ECB)
    #Some cryptographic operation
    def w(self, block_one, block_two, indexOne, indexTwo):
        #print ("this is a crypto operation ")

        
        print (self.count2)
        #print (len(blockOne))
        
        #=======================================================================
        # #Uncomment this to deactivate interleaving and encryption 
        # print ("one ", indexOne, " two: ", indexTwo) 
        # print ("Before: ", self.butterflyTab[indexOne], " ", self.butterflyTab[indexTwo]) 
        #=======================================================================
        
        #=======================================================================
        # self.butterflyTab[indexOne] = block_two
        # self.butterflyTab[indexTwo] = block_one
        #=======================================================================
         
         
        #print ("After: ", self.butterflyTab[indexOne], " ", self.butterflyTab[indexTwo])
        
        #=======================================================================
        # #Comment this to deactivate interleaving and encryption
        # interleaved  = "".join(str(i) for j in zip(block_one, block_two) for i in j)
        # new_block_one, new_block_two = interleaved[:int(len(interleaved)/2)], interleaved[int(len(interleaved)/2):]
        #=======================================================================
       
        interleaved = ''
        for i in range(0, len(block_one)):
            interleaved = interleaved + block_one[i] + block_two[i]
         
         
        new_block_one = interleaved[:int(len(interleaved)/2)]
        new_block_two = interleaved[int(len(interleaved)/2):]
        
        #print (interleaved)
        
        
       
        #print "original: ", new_block_one
       
        #print "This is original block one: ", blockOne
        
        #Comment out this to deactivate encryption
        new_block_one = self.cipher_machine.encrypt(new_block_one)
        new_block_two = self.cipher_machine.encrypt(new_block_two)
        
        #print "This is block one encrypted: ", new_block_one
                  
       
        #=======================================================================
        # dec_new_block_one = DecodeAES(cipher_machine, enc_new_block_one)
        #=======================================================================
          
          
        #=======================================================================
        # print "original: ", new_block_one
        # print "encrypted: ", enc_new_block_one
        # print "decrypted: ", dec_new_block_one
        #=======================================================================
          
        self.butterflyTab[indexOne] = new_block_two
        self.butterflyTab[indexTwo] = new_block_one
           
        #temp = cipher_machine.decrypt(new_block_one)
        #print "This is block one decrypted: ", temp
        
        
        
    #===========================================================================
    # def testOpen(self):
    #     for i in range(0, 1000):
    #         f = open("opentest.txt", 'a')
    #         f.write("Dette er en tekst")
    #         os.fsync(f)
    #         f.close()
    #===========================================================================
            
    




    def start(self, input_filepath):
        bf = Butterfly(filepath=input_filepath)
        #print os.path.getsize(bf.filepath)
        #bf.testOpen()
        
        start = timeit.default_timer()
        bf.blockifyFile()
        n = len(bf.fileTab)
        #n = int(bf.fileSize()/16)
        #print (int(math.pow(2, 1-1)))
        #print (n) 
        d = int(math.log(n, 2))
        bf.initiateButterfly(d, n)
        #print ("This is d: ", d)
         
        #===============================================================================
        # print (len(bf.butterflyTab))
        # print (len(bf.fileTab))
        #===============================================================================
        
        #Try to xor the blocks together 
        #temp = bf.w('a', 'b')
        #bf.w(temp, 'b')
        
        #Uncomment this to write the bf table to file.
        bf.fileifyBlocks('bf_hourglass.txt', bf.butterflyTab)
        
        stop = timeit.default_timer()
        
        print "Start: ", start, "\nStop: ", stop, "\nTime: ", stop - start

    def input(self, input_filepath):
        try_again = ''
        if os.path.isfile(input_filepath):
            bf.filepath = input_filepath
            bf.start(input_filepath)
        elif not os.path.isfile(input_filepath):
            try_again = raw_input("Provided filepath did not exist, try again or write quit to exit...")
            if try_again == 'quit':
                sys.exit('You choose to quit')
            else:
                self.input(try_again)
        
bf = Butterfly()

input_filepath = raw_input("Provide filepath...")

bf.input(input_filepath)



#print (bf.fileTab)
#print bf.butterflyTab
#print len(bf.butterflyTab)
#print (bf.count)

#print bf.blockifyFileTwo('bf_hourglass.txt')

#===============================================================================
# for byte in bf.butterflyTab:
#     print byte, " byte"
#===============================================================================
