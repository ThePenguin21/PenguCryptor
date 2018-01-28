from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import hashlib
import os
backend = default_backend()


while True:
	while True:
		root = input("Root> ").upper()
		if root == 'C':
			print("Are you sure? (Y)es/(N)o")
			sure = input('> ').lower()
			if sure == "yes" or sure == 'y':
				break
		else:
			break
	print("(E)ncrypt/(D)ecrypt")
	mode = input("Mode> ").lower()
	i = 0
	perms = 0
	err = 0
	a = {}
	if mode == "encrypt" or mode == 'e' or mode == "en":
		key = hashlib.md5(input("Key> ").encode()).hexdigest()
		for path, subdirs, files in os.walk(root+':/'):
			for name in files:
				if os.path.splitext(name)[1] != '.pngu':
					a[i] = os.path.join(path, name)
					try:
						file = open(a[i], 'rb')
						raw = file.read()
						file.close()
						padder = padding.PKCS7(128).padder()
						pad = padder.update(raw) + padder.finalize()
						IV = os.urandom(16)
						cipher = Cipher(algorithms.AES(key.encode()), modes.CBC(IV), backend=backend)
						encryptor = cipher.encryptor()
						enc = encryptor.update(pad) + encryptor.finalize()
						file = open(a[i], 'wb')
						file.write(IV+enc)
						file.close()
						os.rename(a[i], a[i] + '.pngu')
					except PermissionError:
						perms = perms+1
					except ValueError:
						err = err+1
					except:
						print("Unable to encrypt.")
					i = i+1
		if len(a) > 0:
			print("Successfully encrypted "+str(len(a))+" file(s).")
		else:
			print("No unencrypted files found.")
		if perms > 0:
			print("Skipped "+str(perms)+" files due to insufficient permissions.")
		if err > 0:
			print("Unable to encrypt "+str(err)+" file(s).")
	elif mode == "decrypt" or mode == 'd' or mode == "de":
		key = hashlib.md5(input("Key> ").encode()).hexdigest()
		for path, subdirs, files in os.walk(root+':/'):
			for name in files:
				if os.path.splitext(name)[1] == '.pngu':
					a[i] = os.path.join(path, name)
					try:
						file = open(a[i], 'rb')
						IV = file.read(16)
						raw = file.read()
						file.close()
						cipher = Cipher(algorithms.AES(key.encode()), modes.CBC(IV), backend=backend)
						decryptor = cipher.decryptor()
						dec = decryptor.update(raw) + decryptor.finalize()
						unpadder = padding.PKCS7(128).unpadder()
						unpad = unpadder.update(dec) + unpadder.finalize()
						file = open(a[i], 'wb')
						file.write(unpad)
						file.close()
						os.rename(a[i], os.path.splitext(a[i])[0])
					except PermissionError:
						perms = perms+1
					except ValueError:
						err = err+1
					except:
						print("Unable to decrypt.")
					i = i+1
		if len(a) > 0:
			print("Successfully decrypted "+str(len(a))+" file(s).")
		else:
			print("No encrypted files found.")
		if perms > 0:
			print("Skipped "+str(perms)+" files due to insufficient permissions.")
		if err > 0:
			print("Unable to decrypt "+str(err)+" file(s). Invalid key?")
	else:
		print("Invalid mode.")