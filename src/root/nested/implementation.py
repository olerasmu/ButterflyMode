'''
Created on 18. mars 2014

@author: olerasmu
'''

import math
import os
from Crypto.Cipher import AES


#===============================================================================
# This now works with files which have a number of blocks n that is a power of 2
#===============================================================================
class Butterfly(object):
    
    def __init__(self, filepath=None):
        self.filepath = filepath
        #self.f = open(filepath, 'rb')
        print (filepath)
        
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
                # print byte
                byte = newfile.read(16)
            #print ("File has been divided into blocks")
    
    fileTabTest = []
    def blockifyFileTwo(self, filepath):
        with open(filepath, 'rb') as newfile:
            byte = newfile.read(16)
            while byte:
                self.fileTabTest.append(byte)
                print byte
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
    
    count = 0
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
                    self.count += 1
                    self.w(self.fileTab[indexOne], self.fileTab[indexTwo], indexOne, indexTwo)
                    
                    #print indexOne, " ", indexTwo
            else:        
                for i in range(1, int(math.pow(2, j-1))+1):
                    indexOne = int(i+k*math.pow(2, j))-1
                    indexTwo = int(i+k*math.pow(2, j)+math.pow(2, j-1))-1
                    self.count += 1
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
    
    #Some cryptographic operation
    def w(self, blockOne, blockTwo, indexOne, indexTwo):
        #print ("this is a crypto operation ")

        cipher_machine = AES.new(b'This is a key123', AES.MODE_ECB)
        
        #print (len(blockOne))
        
        #=======================================================================
        # #Uncomment this to deactivate interleaving and encryption 
        # print ("one ", indexOne, " two: ", indexTwo) 
        # print ("Before: ", self.butterflyTab[indexOne], " ", self.butterflyTab[indexTwo]) 
        # self.butterflyTab[indexOne] = blockTwo
        # self.butterflyTab[indexTwo] = blockOne
        #=======================================================================
         
         
        #print ("After: ", self.butterflyTab[indexOne], " ", self.butterflyTab[indexTwo])
        
        #Comment this to deactivate interleaving and encryption
        interleaved  = "".join(str(i) for j in zip(blockOne,blockTwo) for i in j)
        print (interleaved)
        new_block_one, new_block_two = interleaved[:int(len(interleaved)/2)], interleaved[int(len(interleaved)/2):]
           
        
        #=======================================================================
        # pad = lambda s: s + (16 - len(s) % 16) * '{'
        # EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        # DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip('{')
        # 
        # enc_new_block_one = EncodeAES(cipher_machine, new_block_one)
        # enc_new_block_two = EncodeAES(cipher_machine, new_block_two)
        #=======================================================================
       
        #print "original: ", new_block_one
       
        print "This is original block one: ", blockOne
        
        new_block_one = cipher_machine.encrypt(new_block_one)
        new_block_two = cipher_machine.encrypt(new_block_two)
        
        print "This is block one encrypted: ", new_block_one
        
        #print "encrypted: ", new_block_one            
       
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
           
        temp = cipher_machine.decrypt(new_block_one)
        print "This is block one decrypted: ", temp
        
        
        
    #===========================================================================
    # def testOpen(self):
    #     for i in range(0, 1000):
    #         f = open("opentest.txt", 'a')
    #         f.write("Dette er en tekst")
    #         os.fsync(f)
    #         f.close()
    #===========================================================================
            
    

bf = Butterfly(filepath="butterflyfile.txt")
print os.path.getsize(bf.filepath)
#bf.testOpen()

bf.blockifyFile()
n = int(bf.fileSize()/16)
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



print (bf.fileTab)
print bf.butterflyTab
print len(bf.butterflyTab)
print (bf.count)

#print bf.blockifyFileTwo('bf_hourglass.txt')

#===============================================================================
# for byte in bf.butterflyTab:
#     print byte, " byte"
#===============================================================================

