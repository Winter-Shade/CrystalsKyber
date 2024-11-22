# **Bridging Cryptography: Simulating Post-Quantum and Classical Algorithms**

This project explores and simulates both **post-quantum (Kyber-PKE and NTRU-Encrypt)** and **classical encryption algorithms (AES and DES3)**.
---

## Team Members:

- Srijan Shukla (22bcs124)
- Ojasv Sakhi (22bcs077)
- Prem Prakash (22bcs090)
- Shiva Rathore (22bcs116)
---
## **Project Status**
| Task                            | Status |
|---------------------------------|--------|
| **Implement KyberPKE**          | ✅ Done |
| **Frontend**                    | ✅ Done |
| **Implement NTRU-Encrypt**      | ✅ Done |
| **Implement DES and AES**       | ✅ Done |
---
## About the algorithms: 
### Kyber-PKE  
Kyber-PKE is a post-quantum cryptographic algorithm standardized by NIST in FIPS 203. It is designed to be secure against quantum computers, making it a reliable choice for future-proof encryption. Kyber is based on the hardness of the Decisional Module Learning With Errors (D-MLWE) problem, which is extremely difficult to solve with both classical and quantum methods. Kyber is particularly efficient for key exchange (Kyber-KEM), where it securely establishes symmetric encryption keys for use in other encryption algorithms. 
(Parameters used in our project: q=3329, n=256, k=3, eta1 = 2, eta2= 2)       
(Resources used:      
https://eprint.iacr.org/2017/634.pdf     
https://cryptopedia.dev/posts/kyber/     
https://youtube.com/playlist?list=PLA1qgQLL41SSUOHlq8ADraKKzv47v2yrF&si=Sj9G9GGmQtG0mAfw )

### NTRUEncrypt  
NTRUEncrypt is a lattice-based encryption algorithm offering strong security against quantum and classical adversaries. It relies on the difficulty of solving the Shortest Vector Problem (SVP) and Closest Vector Problem (CVP) in high-dimensional lattices. It relies on the presumed difficulty of factoring certain polynomials in a truncated polynomial ring into a quotient of two polynomials having very small coefficients. Breaking the cryptosystem is strongly related, though not equivalent, to the algorithmic problem of lattice reduction in certain lattices. 
(Parameters used in our project: N = 256, p = 3,  q = 2048,  d = 3 )       
(Resources used:          
https://en.wikipedia.org/wiki/NTRUEncrypt    
https://youtu.be/_nTWHgLDxp0?si=39y1GBtNNAXK03c8)

### AES (Advanced Encryption Standard)  
AES is a symmetric encryption algorithm standardized by NIST and widely adopted for securing data in various applications. It uses substitution-permutation networks and operates on fixed block sizes of 128 bits, with key sizes of 128, 192, or 256 bits. AES is renowned for its efficiency and strong security, as it is resistant to known attacks, including differential and linear cryptanalysis.              
  (Resources used:        
https://www.geeksforgeeks.org/advanced-encryption-standard-aes/        
https://pypi.org/project/aes/ )

### 3DES (Triple Data Encryption Standard) 
Triple Data Encryption Standard (3DES) enhances the security of the original DES algorithm by applying the encryption process three times using two or three different keys. While it improves the cryptographic strength over DES, it retains compatibility with legacy systems. 3DES provides a key size of up to 168 bits, offering moderate security but with relatively lower performance compared to modern encryption algorithms like AES. Despite being gradually phased out, 3DES remains a reliable option in systems requiring compatibility with older standards.       
(Resources used:    
https://en.wikipedia.org/wiki/Triple_DES    
https://pypi.org/project/pyDes/)

 

---

## **Technology Stack**
- **Frontend**: HTML, CSS, JavaScript 
- **Backend**: Flask
- **Programming Language**: Python
- **Deployment**: https://bridgingpqc-production.up.railway.app/ (**Note**: Since we are using a free server on Railway, the deployed site might take several minutes to load and might not work smoothly) 

--- 

## Screenshots:
![Main Page (1)](https://github.com/user-attachments/assets/51ceda4c-215a-495d-a238-ac4d9d0af2c8)



![2](https://github.com/user-attachments/assets/565145a9-ed3c-49fc-853c-45698ceef2b3)




![Kyber main page](https://github.com/user-attachments/assets/102dd455-b441-4387-bfe6-04de7558d103)



![Kyber-keys generated](https://github.com/user-attachments/assets/20a7f5e3-c729-48fe-9b76-0ebcd2bf28b7)

![Kyber](https://github.com/user-attachments/assets/33febe90-d5ef-49c9-b84c-2cfe0c9ffd64)



![message-encryption by bob](https://github.com/user-attachments/assets/392109a4-a815-43ad-98da-02eb2be189f8)


![7](https://github.com/user-attachments/assets/65d3b6cc-1fc6-4e32-979b-d3a13b1c93e7)


![Kyber Step3](https://github.com/user-attachments/assets/bf674cab-ce8d-4fbb-9a46-6c01632f19fe)

![NTRU MAIN](https://github.com/user-attachments/assets/58292f0a-5dc4-4a95-870b-53add6bc0067)




![ntru1](https://github.com/user-attachments/assets/2aac29a2-302e-41d0-96f1-31a4bc7a1a57)
![11](https://github.com/user-attachments/assets/cb020b60-4583-4853-b223-5b3278c0fa0e)






![ntru3](https://github.com/user-attachments/assets/5c11defb-26ab-4706-952d-157cf657638b)


![aes](https://github.com/user-attachments/assets/6e39ee42-9c6a-44fe-848c-07e371fa86e9)


![aes -2](https://github.com/user-attachments/assets/a3af2daf-12ce-4b3b-b94a-dd2f3b089e8f)


![des3](https://github.com/user-attachments/assets/12ad255c-582e-416b-b69d-510d1342b3f2)




![des3-2](https://github.com/user-attachments/assets/e265c3a5-f559-4fca-8793-b560a4f10cdf)


![17](https://github.com/user-attachments/assets/fa992337-b9c7-429c-95ce-b22aa854a770)
























