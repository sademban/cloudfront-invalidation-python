## setup 
windows
```
1. clone the repository
2. cd into the cloned directory
3. create .env file and set the necessary variables
    AWS_ACCESS_KEY_ID=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
    AWS_SECRET_ACCESS_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
    AWS_DEFAULT_REGION=us-east-1
    DISTRIBUTION_ID_1=xxxxxxxxxxxxx
    DISTRIBUTION_ID_2=xxxxxxxxxxxxx
4. create venv  with  'python -m venv venv'
5. activate venv wiht 'source venv/Scripts/activate
6. pip install -r requirements.txt
7. run the scrip  with ' python script.py'
8. enter your choice when promted and invalidate your cf distribution
```