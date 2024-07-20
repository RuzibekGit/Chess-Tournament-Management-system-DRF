

<p style="font-size: 20px; color: rgb(131, 130, 128);"> * This project has not been completed yet...</p>


<br>

# DRF Chess Tournament Management system



This project is a Chess Tournament Management System built using Django REST Framework (DRF). It allows users to create and manage chess tournaments, register participants, and track match results.

## Features

- Create and manage chess tournaments
- Register participants
- Track match results
- Leaderboard for tournaments
- Admin-only access for certain operations

## Requirements

- Python 3.8+
- Django 3.2+
- Django REST Framework
- PostgreSQL (or any other preferred database)

## Setup and Installation

### Clone the Repository

```bash
git clone https://github.com/RuzibekGit/Chess-Tournament-Management-system-DRF.git
cd Chess-Tournament-Management-system-DRF # Change directory
python -m venv env
source env/bin/activate  # On Unix or MacOS
env\Scripts\activate  # On Windows

pip install -r requirements.txt # Install Dependencies

```


## Add and Configure the .env file

 - Create an .env file using example.env  and enter the necessary keys


## API Documentation 

#### your-domain/swagger/
<img src="assets/images/Screenshot 2024-07-20 215759.png" alt="" style="height: ; width: ;">

#### Also you can use my postman collection
 - Postman API documentation ```https://documenter.getpostman.com/view/36448688/2sA3kUGhfJ```

 - Postman Collection API Link```https://api.postman.com/collections/36448688-0f441b28-08e8-4129-83da-23d016354512?access_key=PMAT-01J38NKD864K5WT21MGHXD8SE9```


### Important!!!! 
 - Before using this collection  add new variable, im using ```{ my_urls }``` instead of ```http://127.0.0.1:8000``` 


## Using Collection API Link in Postman

You can easily import a collection into Postman using a collection API link. Follow these steps to use a collection API link in Postman:

### Steps to Import a Collection Using an API Link

1. **Open Postman**:
   - Launch Postman on your computer.

2. **Import Collection**:
   - Click on the **Import** button located in the top left corner of the Postman interface.


3. **Select Link**:
   - In the Import dialog, select the **Link** tab.

4. **Paste the Collection API Link**:
   - Copy the collection API link provided to you.
   - Paste the link into the input field in the Import dialog.

5. **Import the Collection**:
   - Click the **Continue** button.
   - Postman will fetch the collection from the provided link.
   - Click **Import** to add the collection to your workspace.

### Example

If you have a collection API link like `https://www.getpostman.com/collections/your-collection-id`, follow the steps above to import it into Postman.

### Using the Imported Collection

1. **Access the Collection**:
   - Once imported, you will see the collection listed in the left sidebar under the **Collections** tab.

2. **Explore Requests**:
   - Click on the collection name to expand it and view all the requests it contains.

3. **Send Requests**:
   - Select any request from the collection.
   - Click the **Send** button to execute the request and view the response.


### Additional Resources

For more detailed instructions and advanced features, you can refer to the [Postman Learning Center](https://learning.postman.com/docs/collections/using-collections/)[^1^][5].

