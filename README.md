# Radar Data Viewer

### Introduction

The Radar Data Viewer Project is be a web-based software designed to visualize high-frequency (HF) and X-Band radar data. Initially, it focuses on displaying radar data files in a B-Scan format, with plans to expand to multiple files and animations in the future. The web application also shows key details such as when and where the radar data was collected, the transmission frequency, bandwidth, and the maximum range. Although the first version of the software have limited functionality, it will be accessible from different operating systems like Windows, Ubuntu, etc. In addition to that, we plan to integrate advanced data analysis features, including spectrum and parameter extraction algorithms, in future versions of the software.

### How to run the project

#### \* Frontend

To run the frontend server, you need to navigate to "frontend" folder and run the following command :

```
npm run dev
```

#### \* Frontend

To run the backend server, you need to navigate to "radarDataViewer" folder and run the following command under the virtual environment :

```
python manage.py runserver 8000
```

### System Architecture

-    Backend: Django (Python)
-    Database: SQLite (Django’s default database)
-    Frontend: React.js, TailwindCSS (for building an interactive UI)
-    API: RESTful APIs for seamless frontend-backend communication

The ReactJS front-end enables users to upload radar files, view visualizations, and access metadata. The Django back-end processes radar data, converts SORT files into matrix format and interacts with SQLite database to store metadata and processed results. NumPy and SciPy handle matrix conversion and data processing. The modular system allows for future enhancements like advanced visualizations and wave spectrum analysis.

### Functional Features

#### \* File Upload Process

1. Registration
     - A super admin will be created by default in the system.
     - The registration page will only be accessible by the super admin, who should be able to create users with credentials such as username and password.
2. Landing page
     - The system's landing page is a login page where users can log in using their credentials.
     - The user uses their credentials and the system verifies the data from the server to give authentication access.
     - As mentioned above, if the user is a super admin, the user will be able to see an option to view the Registration page to create new user with credentials.
3. Loaded files history and file upload

     - The system routes to the history files page where all the previously uploaded SORT files are shown on a page for the logged-in user. The user can select any of those previously uploaded files and can view all the generated images from the SORT file.
     - The user will also have the option to upload any new SORT file as per the choice of the user

4. File selection
     - When the user clicks the Upload File button, the system displays a file picker window to select files from the user's local machine.
     - Every file is uploaded based on users. i.e. the uploaded file will be tagged with the username so that every time the user logs in, the system can show all the previously uploaded files.
5. File validation
     - If a non-SORT file is uploaded, the system throws an error: “The provided file is not allowed. Please upload a valid SORT file.”
     - If a valid SORT file is selected, the file is processed further.

#### \* Data transfer to Backend

1. Frontend Action
     - The credentials with username and password are sent in JSON format to the server for processing and authorization.
     - The selected SORT file is sent to the backend server with the username and other data in JSON format via RESTful API.

#### \* Backend Processing

1. Data Processing:
     - The backend uses libraries like NumPy, SciPy, and Pillow to process the SORT file, converting its data into a matrix format.
2. Metadata Storage
     - Metadata and processed results are stored in the SQLite database.
     - User-specific data was stored in localStorage to maintain the user priority such as showing all the previously uploaded files. LocalStorage contains data such as user token, username, firstName, lastName, and isLoggedIn value
3. Image Generation
     - Generated images are encoded in base64 format for transmission.
4. Response to Frontend
     - The server provides an authentication response in JSON format whether the the user was authenticated successfully or not.
     - The backend sends the processed data, including encoded images and metadata, back to the frontend.
     - The backend server provides response of various API in JSON format such as previously uploaded files of a particular user, all users, multiple images from SORT files and others.

#### \* Slideshow Feature

1. Frontend Actions
     - The front end decodes the base64 images provided by the backend.
     - All the decoded images and metadata are displayed in a slideshow format.
2. User Controls
     - Play/Pause: Users can start or stop the slideshow at any point.
     - Forward/Backward
          1. A Forward button lets users skip to the next image.
          2. A Backward button allows navigation to previous images.

### Additional Features

1. The CI/CD pipeline has been implemented with build error safety and test case integration.
2. More than 22 unit test cases have been written in Django to check the functional features such as the User module and File upload module separately.
3. The CI/CD build phase checks the project build errors such as compilation errors and run time environment errors. If the build is completed successfully, it goes to the next phase ‘test phase’.
4. In the test phase, the CI/CD pipeline runs all the test cases from the tests.py file and can only forward to the deployment phase if all the test cases are passed.

### Test case coverage

1. Model Testing:
     - Validation of file path generation using timestamps.
     - Verification of the RadarFile model's file storage and retrieval behavior.
     - Testing of string representation for the RadarFile model.
2. Utility Function Testing
     - Transformation of DMS (Degrees, Minutes, Seconds) coordinates into decimal format.
     - Generation of base64-encoded images from numerical data arrays.
     - Handling of edge cases and invalid inputs in utility functions.
3. User Authentication Testing
     - Validation of login functionality with various combinations of usernames and passwords.
     - Ensuring robust handling of edge cases like empty or invalid input fields.
