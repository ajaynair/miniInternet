Based on https://realpython.com/python-https/#creating-an-example-application

The aim of this project is to get hands-on experience on most common yet confusing concepts in the working of the internet.
ssl, https, tls, CA, root ca, proxy, vpn, reverse proxy, cert signing, crt crs pem files etc. can get very confusing. This project helps
me get good hands-on experience on a few of these concepts.

Currently, this repo has a mini https server and a mini Certificate Authority that signs the mini server. 
So, we can make our browser recognize the CA and let users access any server that has cert signed by our CA 
without warning. 

So currently, this repo consists of 2 main parts:
1. A mini Certificate Authority that can provide signed public key to a server
2. A mini server that uses HTTPS and is signed by the mini certificate

How to run:
1. Generate ca private and public key
cd certificateAuthorities
python3 ca_keys_gen.py # should generate private and public pem files in ca_keys

2. Generate server csr and private key 
   1. cd ../servers 
   2. python3 generate_csr.py # Should generate a csr and the private key

3. Sign server public key by CA 
   1. cd ../certificateAuthorities 
   2. python3 ca_sign_csr.py ../server/csr_dir/<csrFile> # should create a public key that is signed by CA

4. Add CA public key to firefox certificates authority 
   1. Firefox -> preferences -> search 'certificates' -> authorities -> import 
   2. Choose certificateAuthorities/ca_keys/<public_key> # This tells firefox to trust this CA

5. Access the server page 
   1. cd ../server 
   2. uwsgi --master --https localhost:5683,key_dir/server-public-key.pem,key_dir/server-private-key.pem --mount /=https_server:app 
   3. firefox:https://localhost:5683