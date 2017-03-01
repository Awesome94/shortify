
![Alt text](/static/images/back.jpg?raw=true "Shortify")

# Shortify.

App can be accessed from https://shortifyapp.herokuapp.com.<br/>
Demo video can be found at https://www.youtube.com/watch?v=YQn-Yq5kJXk

Shortify is a URL shortening service. The application accepts long URLs and turns them into short URLs for easy use and Sharing. Registered users can provide customized short URL’s . Additionally, the user can update or delete the shortened URL at will.

#Application Features.
# For normal Users
1. Shortens a long URL to a much shorter URL that is easier to remember 
2. Provides a list for most active Users based on their number of shortened URLs
3. Provides a list of  popular shortened URLs by how many times they have been clicked.
4. Provides a list of shortened URLs by how recent they were created.

# Registered Users.
1. User is able to edit the customized URL.
2. User can activate and deactivate shortened URL at will
3. User can delete shortened URL at will

# Dependencies.
1. Python3.6
2. PostgreSQL
3. Flask

# Running the Application.
1. Clone the application to your local machine:<br/>
``` $ git clone https://github.com/Awesome94/shortify.git.```

2. Navigate to the shotify directory.<br/>
```$ cd shotify.```

3. Create a Virtual enviroment and Install the dependencies.<br/>
```$ mkvirtualenv shortify.```<br/>
```$ pip install -r requirements.txt.```
    
4.  Setup database and seed data.<br/>
set_up postgres  on your local using the following steps  http://bit.ly/1v7Cu0l<br/>
``` $ python manage.py db init ```</br>
``` $ python manage.py db upgrade ```

5.   Start the server.<br/>
``` $ python app.py ```<br/>
Visit http://localhost:5000 to view the application on your preferred web browser.

# Testing
Run the following command from the terminal in the root folder of the app to get all tests running<br/>
``` $ python -m unittest discover ```

End.
