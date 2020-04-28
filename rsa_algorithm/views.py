from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from PIL import Image
import numpy as np
import requests
from io import BytesIO
from sympy import *
from decimal import Decimal
import os

# Create your views here.

#Set values for p and q (Two prime numbers)
p = 7
q = 37

#from django.http import HttpResponse


def index(request):
    return render(request, 'index.html')

#GCD function
def gcd(a,b):
    if b==0:
        return a
    else:
        return gcd(b,a%b)

# RSA encrypt function
def rsa_encrypt(no,p,q):
    if isprime(p) and isprime(q):
        n = p * q
        t = (p-1)*(q-1)

        for e in range(2,t):
            if gcd(e,t)== 1:
                break

        for i in range(1,10):
            x = 1 + i*t
            if x % e == 0:
                d = int(x/e)
                break

        ctt = Decimal(0)
        ctt =pow(no,e)
        ct = ctt % n

        return int(ct)

# RSA Decrypt Function
def rsa_decrypt(ct,p,q):
    if isprime(p) and isprime(q):
        n = p * q
        t = (p-1)*(q-1)

        for e in range(2,t):
            if gcd(e,t)== 1:
                break

        for i in range(1,10):
            x = 1 + i*t
            if x % e == 0:
                d = int(x/e)
                break

        dtt = Decimal(0)
        dtt = pow(ct,d)
        dt = dtt % n

        return int(dt)



def encrypt(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['input_image']
        uploaded_file_name = uploaded_file.name
        uploaded_file_size = uploaded_file.size

        fs = FileSystemStorage()
        fs.save(uploaded_file_name,uploaded_file)
        #fs.save("original.jpg",uploaded_file)

        img = Image.open(os.path.join("/home/ImageEncrypt/image_encrypt/media",uploaded_file_name))
        img_array=np.array(img)
        width, height = img.size

        img_array_duplicate = [[[img_array[i][j][k] for k in range(0,3)] for j in range(0,width)] for i in range(0,height)]
        img_array_duplicate=np.array(img_array_duplicate)

        for i in range (0,height):
            for j in range (0,width):
                for k in range (0,3):
                    img_array_duplicate[i][j][k] = rsa_encrypt(int(img_array_duplicate[i][j][k]),p,q)

        encrypted_img = Image.fromarray(img_array_duplicate, 'RGB')
        encrypted_img.save(os.path.join("/home/ImageEncrypt/image_encrypt/media",'encrypted.jpg'))

        np.save(os.path.join("/home/ImageEncrypt/image_encrypt/media",'encrypted'), img_array_duplicate)


        fs.delete(uploaded_file_name)

    return render(request, 'output1.html', {'msg':"Encrypted image is ready"})

def decrypt(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['input_npy']
        uploaded_file_name = uploaded_file.name
        uploaded_file_size = uploaded_file.size

        fs = FileSystemStorage()


        if os.path.isfile('/home/ImageEncrypt/image_encrypt/media/encrypted.npy'):
            fs.delete("encrypted.npy")

        fs.save(uploaded_file_name,uploaded_file)

        img_array_duplicate = np.load(os.path.join("/home/ImageEncrypt/image_encrypt/media",uploaded_file_name))

        height = img_array_duplicate.shape[0]
        width = img_array_duplicate.shape[1]

        for i in range (0,height):
            for j in range (0,width):
                for k in range (0,3):
                    img_array_duplicate[i][j][k] = rsa_decrypt(int(img_array_duplicate[i][j][k]),p,q)

        decrypted_img = Image.fromarray(img_array_duplicate, 'RGB')
        decrypted_img.save(os.path.join("/home/ImageEncrypt/image_encrypt/media",'decrypted.jpg'))

        fs.delete(uploaded_file_name)

    return render(request, 'output2.html', {'msg':"Decrypted image is ready"})