# charles_grey_Z_prefix_submission
Submission for Z-Prefix RAP January 2025 for Charles Grey


I did all my development in VSCode and used powershell as my terminal of choice.
I had node v22.13, npm v10.9.2, and Python 3.13.1

Once you have the most up to date version of node, npm, and python you'll need two terminals. One to host the front end and one for the back end. I used powershell for both.

The only dependency for the front end is axios which can be installed by "npm axios"
Once you have node and axios installed you can spin up the front end via "npm run dev" from inside the React/inventoryFrontEnd folder
The front end can be accessed at http://localhost:5173

For the back end make sure you have an updated version of python and navigate to the FastAPI folder. The dependencies are listed in a requirement.txt file in that folder. They are:
bcrypt
cryptography
fastapi
python-jose
python-multipart
SQLAlchemy
uvicorn
passlib

Activate your virtual env if you choose to use one via ./env/scripts/activate

Once those are all installed, the back end can be spun up via: uvicorn main:app --reload

If you have any issues testing the app please reach out to me at chas4739@gmail.com or 2603885788

I was unable to get the login functionality working. I do have a sqlite database that can post and get successfully and display new entries to the front end.

