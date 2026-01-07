Instruction to setup
Clone the Repository
```
git clone https://github.com/alok9973/smart-pay.git
```

```
cd smart-pay
```

1. Create Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```

2. install dependencies
```
pip install -r requirements.txt
```

3. Start FastAPI Server
```
uvicorn main:app --reload
```
Verify locally:
http://127.0.0.1:8000/docs

4. Expose API using ngrok
Start ngrok Tunnel
```
ngrok http 8000
```


You will receive a public URL like:

https://xxxx.ngrok-free.app