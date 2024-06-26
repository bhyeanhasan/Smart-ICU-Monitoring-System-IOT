# Setup Manual (Backend Server + Raspberry PI)

### Follow this procedure
```
1. Please run Network.py to get the IP addresses of the Server and PI
2. Connect to PI using Remote Desktop 
3. Make sure the SERVER-IP-ADDRESS is correct in PI Script ('ws://192.168.35.62:8000/ws/temperature/')
4. Start the Server (python manage.py runserver 0.0.0.0:8000
5. Run the PI Script 
```

## Server Side:

### Install package
```
pip install django
python -m pip install -U channels["daphne"]
python manage.py runserver 0.0.0.0:8000
```
### Super User
* username : pstu
* password: 1234

 



## Raspberry PI:
### Install package

```
pyfirmata
```

### Remote Connection
* username : pi
* password: cse

