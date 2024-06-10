# Task-Rabbit
A online courier service where a customer can request from a service from a rabbit (courier) with authentication and payment processing for the services offered by the rabbit. 

## Preview
![image](https://user-images.githubusercontent.com/88239970/227616780-f2cf2179-477f-4d34-9623-2333a9d1acf9.png)

## How to run
- Local Deployment
1. On your local machine, make sure you have Python and SQLite3 installed
2. Clone this repository using the command: `git clone https://github.com/Daniel-Brai/Task-Rabbit.git` ,or download and extract the zipped master file of this project
3. On the terminal of your choice, using pip to install pipenv using the command `python -m pip install pipenv`
4. Create a virtual environment with the command `python -m pipenv shell`
5. In your virtual environment, run the command `python -m pip install pipenv`
6. Download the dependencies of the project using the command `pipenv install`
7. Create a admin user using the command `pipenv run python manage.py createsuperuser` and follow the prompts
8. Export the environment variables or create a `.env` file to read them from: 
- `CLOUD_NAME`
- `CLOUD_API_KEY`
- `CLOUD_API_SECRET`
- `FIREBASE_ACCOUNT_TYPE`
- `FIREBASE_PROJECT_ID`
- `FIREBASE_PRIVATE_KEY_ID`
- `FIREBASE_PRIVATE_KEY`
- `FIREBASE_CLIENT_EMAIL`
- `FIREBASE_CLIENT_ID`
- `FIREBASE_AUTH_URI`
- `FIREBASE_TOKEN_URI`
- `FIREBASE_AUTH_PROVIDER_CERT_URL`
- `FIREBASE_CLIENT_CERT_URL`
- `STRIPE_PUBLIC_KEY`
- `STRIPE_SECRET_KEY`
- `MAPS_API_KEY`
- `DISTANCE_MATRIX_API_KEY`
- `PAYPAL_MODE`
- `PAYPAL_SANDBOX_ACCOUNT`
- `PAYPAL_CLIENT_ID`
- `PAYPAL_APP_SECRET_KEY`
9. Run the local server to view the project using the command `pipenv run python manage.py migrate && pipenv run python manage.py runserver`

