# MeowFinder Enhancing Petshop Experience through Automated  Cat Breeds Classification Cloud Computing

### How to run this File

To install the backend application, follow these steps:
1. Duplicate/Clone the repository code. or downloading it as a zip file.
2. Connect to your database and execute the migration file.
3. Execute the command below to install the necessary dependencies: npm install
4. Initiate the server by using the command: npm run start

## API Endpoints
To access the API documentation, visit (https://documenter.getpostman.com/view/30339066/2s9YkrZeFd).
Machine Learning MODEL : (https://drive.google.com/drive/folders/1ZBJE0UKQdce-ov3hpGNcDvRRPu-Q3Mff?usp=sharing)

# Creating a RESTful API with Flask and Cloud Run
1. Configure a predictive model in the "h.5" format, storing files in the "ML-Backend" directory.
2. Develop the "main.py" script based on the machine learning test model and save the files in the "ML-Backend" folder.
3. Generate a "requirements.txt" file that lists the necessary libraries for code execution.
4. Construct a "Dockerfile" for running the system within a container.
5. Establish a ".dockerignore" file to guide the system in ignoring specific files.
6. Create a "static/uploads" folder for storing photos used in the prediction process.
7. Initialize a new project on the Google Cloud Platform.
8. Enable both the Cloud Run API and Cloud Build API.
9. Install and initialize the Google Cloud SDK through the provided link: [Google Cloud SDK Installation](https://cloud.google.com/sdk/docs/install).
10. Employ Cloud Build to import the code into cloud services (execute: `gcloud builds submit --tag gcr.io/<project_id>/<function_name>`).
11. Deploy the API using Cloud Run (execute: `gcloud run deploy --image gcr.io/<project_id>/<function_name> --platform managed`).
