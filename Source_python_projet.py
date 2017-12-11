#!/usr/bin/python2.7
#coding: utf-8
import sys
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from itertools import chain, product
from collections import defaultdict
from pprint import pprint
import string

def unpadtest(padded_data, block_size, style='pkcs7'):
	pdata_len = len(padded_data)
	if pdata_len % block_size:
		raise ValueError("Input data is not padded")
	if style in ('pkcs7', 'x923'):
		padding_len = ord(padded_data[-1])
		if padding_len<1 or padding_len>min(block_size, pdata_len):
			raise ValueError("Padding is incorrect.")
		if style == 'pkcs7':
			if padded_data[-padding_len:]!=chr(padding_len)*padding_len:
				raise ValueError("PKCS#7 padding is incorrect.")
		else:
			if padded_data[-padding_len:-1]!=chr(0)*(padding_len-1):
				raise ValueError("ANSI X.923 padding is incorrect.")
	elif style == 'iso7816':
		padding_len = pdata_len - padded_data.rfind(chr(128))
		if padding_len<1 or padding_len>min(block_size, pdata_len):
			raise ValueError("Padding is incorrect.")
		if padding_len>1 and padded_data[1-padding_len:]!=chr(0)*(padding_len-1):
			raise ValueError("ISO 7816-4 padding is incorrect.")
	else:
		raise ValueError("Unknown padding style")
	
	return padded_data[:-padding_len]

def dicts(t): return {k: dicts(t[k]) for k in t}
def tree(): return defaultdict(tree)
node = tree()

def dec_hacky(ciphertext,style='pkcs7',prev=''):
	plaintext = ""
	dico = list(bruteforce(string.digits+string.letters,2))

	#bruteforce 
	for s in dico:
		tmpblocks=ciphertext
		try:
			tmpk = hashlib.sha256(s).digest()
			c = AESCipher(tmpk)
			tmpblocks=c.decrypt(tmpblocks)
			#if verify_func(tmpblocks):
			#tmpblocks = AESCipher._unpad(tmpblocks)
			tmpblocks = unpadtest(tmpblocks,32,style)
			print "[*] Valid padding found with key: " + s
			node[prev][s]
			#print tmpblocks
			dec_hacky(tmpblocks,style,prev+s)
		except:
			continue

def verify_pkcs7(ciphertext):
	if len(ciphertext) <= 0:
		return False

	pad = ord(ciphertext[-1])
	all_padding = ciphertext[-pad:]
	ret = True
	for byte in all_padding:
		if ord(byte) != pad:
			ret = False
	return ret

def bruteforce(charset, maxlength):
	return (''.join(candidate)
		for candidate in chain.from_iterable(product(charset, repeat=i)
		for i in range(maxlength, maxlength + 1)))

class AESCipher(object):
	def __init__(self, key):
		self.bs = 32			
		self.key = key

	@staticmethod
	def str_to_bytes(data):
		u_type = type(b''.decode('utf8'))
		if isinstance(data, u_type):
			return data.encode('utf8')
		return data
		
	@staticmethod
	def _pad(self, s): 
		return s + (self.bs - len(s) % self.bs) * AESCipher.str_to_bytes(chr(self.bs - len(s) % self.bs)) 
	@staticmethod
	def _unpad(s):
		return s[:-ord(s[len(s)-1:])]

	def encrypt(self, raw):
		raw = self._pad(self, AESCipher.str_to_bytes(raw)) 
		iv = Random.new().read(AES.block_size) 
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return iv + cipher.encrypt(raw)

	def decrypt(self, enc):
		iv = enc[:AES.block_size]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return cipher.decrypt(enc[AES.block_size:])

class SecureEncryption(object):
	def __init__(self, keys):
		lenkey=len(keys)
		self.keys = keys 
		self.ciphers = [] 
		for i in range(lenkey):
			self.ciphers.append(AESCipher(keys[i])) 

	def enc(self, plaintext,lenkey): 
		tmpblocks=plaintext 
		for i in range(lenkey/2):
			tmpblocks=self.ciphers[i].encrypt(tmpblocks) 
		ciphertext=tmpblocks 
		return ciphertext

	def dec(self, ciphertext,lenkey):
		tmpblocks=ciphertext
		for i in range(lenkey/2):
			tmpblocks=AESCipher._unpad(self.ciphers[lenkey/2-i-1].decrypt(tmpblocks))
		plaintext=tmpblocks
		return plaintext

if __name__ == "__main__":

	filename = sys.argv[1]
	plaintext = open(filename, "rb").read()

	user_input = sys.argv[2].encode('utf-8')
	keys=[]
	for i in range(len(user_input)/2): 
		keys.append(hashlib.sha256(user_input[i*2:(i*2)+2]).digest()) 
	s = SecureEncryption(keys) 

	#ciphertext = s.enc(plaintext,len(user_input)) 
	plaintext_ = s.dec(plaintext,len(user_input))
	#plaintext_ = dec_hacky(plaintext,'pkcs7')
	#print pprint(dicts(node))
	#assert plaintext == plaintext_

	print plaintext_

	#open(filename+".encrypted", "wb").write(ciphertext)
