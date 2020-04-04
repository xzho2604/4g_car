import requests


payload = {'name':"erik"}

# send the post request to the expeted route
r = requests.post("http://127.0.0.1:5000/",json=payload)
print(r.text)
