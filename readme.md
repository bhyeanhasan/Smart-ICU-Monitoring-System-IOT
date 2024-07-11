# Setup Manual (Backend Server + Raspberry PI)

## Procedure:

1. **Retrieve IP Addresses:**
   - Run `Network.py` to obtain the IP addresses of the Server and Raspberry PI.

2. **Connect to Raspberry PI:**
   - Use Remote Desktop to connect to the Raspberry PI.

3. **Configure Server IP in PI Script:**
   - Ensure the SERVER-IP-ADDRESS is correctly set in the PI Script (`'ws://192.168.35.62:8000/ws/temperature/'`).

4. **Start the Server:**
   - Start the Django server:
     ```bash
     python manage.py runserver 0.0.0.0:8000
     ```

5. **Run the PI Script:**
   - Execute the Raspberry PI script.

## Server Side:

### Install package
```
pip install django
python -m pip install -U channels["daphne"]
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

