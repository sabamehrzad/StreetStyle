## I. INTRODUCTION AND STYLE
This project employed Python, HTML, CSS, Flask, and Javascript. We aimed for a crisp and clean aesthetic. We designed our own color scheme, focusing on a set of light blues, and designed our own logo and favicon. Users can navigate through different pages via the navigation bar. Additionally, we designed a footer that allows the users to simply click “Contact us!” on any page to easily send us an email.

## II. HELPERS
We have two functions within helpers.py that app.py uses. login_required(f) will decorate routes to require user login. We also have dateString(dashDate), which converts dates to a more visually pleasing format. Since dates in our SQL table are all in the format of YYYY-MM-DD, this function will return a string instead in the form of “Month Day, Year”, also stripping any superfluous 0s (so 0998-03-07 would become March 7, 998).

## III. LOGGING IN

### Register

#### App.py
Using the post method, the register route accepts user information from the request.form.get syntax. This route checks for multiple potential errors, including the user not inputting information in the username, password, and confirmation form inputs and if the password doesn’t match the confirmation input. Additionally, register requires the password to be at least 8 characters by returning the register page if the length of the password string is less than 8. Finally, the register route checks if the password submitted includes a lowercase letter, uppercase letter, number, and a symbol. First, we set lower, capital, symbol, and number to false. Then, we created a for-loop that loops through every letter in the password input. Inside the for-loop, we coded if statements, checking if the password included uppercase letters, numbers, and a symbol with the .is(upper, lower, alnum, digit) syntax and setting these variable names to true. If any one of these variables was set to false, the password that the user inputted would be deemed too weak.

Finally, we used the try and except syntax to test a SQL insert statement into the users table in order to store information regarding each user’s username and password (hashed for personal security). This was set to an ID variable since this line would output the row number of what was just inputted into SQL, which is how our ID system works. However, if there is a value error, that would mean that a user with that username already exists, flashing an error message and returning the page route. Finally, we set the id value to our session user id since the id output is equivalent to the row number.

#### HTML/Jinja
We, first, extended our layout.html document. Then, we created a form that directs to our register route in app.py. Next, we wrote inputs, including a username, password, and confirmation input. Finally, we created a submit button, ended the form, and ended the layout.

### Log In

#### App.py
The @login_required decorator before most of the routes means that users must be logged in to access pages including the journal or shopping log

The login route, sourced from our past problem sets, accepts user login through the POST method and the request.form.get syntax. Additionally, it checks that the user inputted each of the required fields with an if statement that verifies the username and password inputs exist with the not syntax. Next, we query our SQL database of users to retrieve all of the information in the table and name it as our “rows” variable. Next, we check whether the username and password inputted matches our SQL records. We created an if statement stating that if the length of our rows variable is not equal to 1 or if our hashed password (when hash is removed) does not equal to the inputted password, flash an error message that an invalid username or password was submitted.

#### HTML
We, first, extended our layout.html document. Then, we created a form that directs to our login route in app.py. Next, we created inputs for our form, including username and password, and a submit button.

### Profile

#### Setting up image inputs
Our first step is creating a file path where the user-uploaded image will be saved; we store this file path in “app.config[“IMAGE_UPLOADS”]”. We also create a variable called “imagefilepath” that is a more condensed version of the file path stored in “app.config[“IMAGE_UPLOADS”].”  We also declare the file types that the user is allowed to upload – the user is restricted to uploading only png, jpeg, jpg, and gif file types.

### App.py
Using the post method, the register route accepts user information from the request.form.get syntax. In this route, we request text inputs and an image file input, which will eventually be fed into our input route. Then, we check if the user inputted the requested information with a series of if statements that check if there is an input with the “not” syntax.

In order to “select” the picture that the user uploads; instead of selecting this image through “request.form.get”, we use “request.files[name_of_image]”. The [name_of_image] is the value of the “name” attribute in the “input” tag with type “file” in our profile.html file.

Next, we have a series of conditionals to make sure that the image is of an allowed file type and that the name of the image contains no spaces. If these conditions are violated, we flash an error message to the user. But assuming these conditions are satisfied, we save the image using the “save(os.path.join(…” command, which allows us to save the image to the file path we stored earlier in “app.config[“IMAGE_UPLOADS”].”

Finally, we store the file path and the name of the image into our profile SQL table, inside the “filepath” and “picture” columns, respectively. Of course, along with storing these two pieces of data inside our table, we also store the other text based data that the user submitted through the form (the name, birthday, hometown, and favorite brand of the user – we get these pieces of data using the standard “request.form.get” syntax). We use the UPDATE syntax because our profile table initially stored NULL values for these fields in order to keep our id system consistent with row numbers in the users and profile tables.

Once all this data is stored in our table, we then redirect the user to the index.html page, which displays the user’s profile information.

#### HTML
We, first, extended our layout.html document. Then, we created a form that directs to our profile route in app.py. Next, we created inputs for our form—including name, birthday, hometown, favorite brand, and profile picture—and a submit button.

### Index

#### App.py
First, we create a variable called “profile” that selects all of the information present in the table regarding the logged in individual. Next, we set our birthString variable (which references our helper function) equal to the date that is inputted in our profile table.

Next, we check if the user inputted an image when prompted by creating an if statement that displays our no image file.

#### HTML/Jinja
Index is our homepage. Due to the fact that we used the login_required decorator in our app.py, this information can only be viewed by a logged in user. We first created an introduction banner with a brief description of the website. Then, we displayed the user’s inputted information with the Jinja delimiter {{ }} referencing our name, hometown, and birthString variables in app.py. Finally, we displayed the user’s profile picture by referencing the user’s filepath from app.py in the profile SQL table.

## IV. LOGGING CLOTHING

### Log Clothes

Allowing the user to submit the date, article type, brand name, and URL link is straightforward. These data items will be stored as TEXT types in our SQL table. The complexity of this functionality is finding a way to allow the user to upload an image of the article of clothing. We need to find a way to successfully “save” the image in our SQL table, and our team decided that there were 2 ways to approach this: 1) convert the image into a BLOB data and store that BLOB data in our SQL table or 2) save the image inside a certain folder within our Codespace, and store the file path that leads to the image inside our SQL table as a TEXT type. Our team chose to go with Option 2.

We accepted image inputs by using the same method described in the profile section.


### Shopping Log

In order to display a table that contains all of the user’s past entries to the “Log Clothes” webpage, we use a mix of HTML and Jinja. The primary HTML feature is a table tag, and inside the table tag we use Jinja to loop through a list of dictionaries that was passed into the “shopping_log_history” html file. We iterate through each dictionary and select the values from each dictionary using the keys “Date”, “Clothing Type”, “Brand”, and “Link” – the key names are exactly the values that we extract from each dictionary. We also display the image of the article of clothing through the source attribute of an “img” tag, which is equal to the file path where the image is saved (using Jinja syntax).

## V. JOURNAL
In order for users to be able to write new entries to the journal, “journal_post.html” has a form with inputs for the date, title, subject, and entry.” Hence, when users hit the submit button on this page, register(), under the “POST” method will get the date, title, subject, and entry the user inputted. register() will make sure the user filled out all of these fields, flashing the appropriate message if they haven’t. After running these checks, these four inputs will all be inserted (along with the corresponding user’s id) into the SQL table “journal,” and the user will be redirected to the journal itself.

For the journal page, we simply execute a “SELECT” statement from the “journal” table to get a row’s date, title, subject, and entry if the row id matches the user. journal() also uses the dateString() function to make the dates more aesthetically pleasing. This list is passed into journal.html, which with Jinja in journal.html will iterate through every single dictionary within this list and display each corresponding title, date, subject, and entry text.


## VI. RANDOMIZE

We start with the “randomizer” function in app.py. The app.route decorator only has the “GET” method (and not the “POST” method) because the user isn’t submitting any data to the server – the outfits will be randomly generated, not selected by the user.

The first block of db.execute statements run SQL commands to get the file paths and brand names of each article of clothing for each article type that the user has uploaded in the past to the shopping_log SQL table. For example in the first db.execute statement, the user will get back a
list of dictionaries for all accessories that the user has uploaded in the past, where each dictionary represents a unique accessory. Each dictionary (representing an accessory) within this list has 2 keys: filepath (which is the file path where that specific accessory’s image is saved) and brand (which is a TEXT type that is the brand name of that specific accessory).

Once we have these 5 lists of dictionaries, we have to somehow find a way to “pass” these into the html file so that we can manipulate them using Javascript. In order to pass these into the html file, we have to convert these lists to strings using the json.dumps syntax. Finally, we pass
these strings into the randomizer.html file.

Once we have passed these 5 strings into the randomizer.html file, we then have to find a way to “convert” them back into 5 lists of dictionaries that we can manipulate using Javascript. To do this, we have to use a combination of {{ article_type | tojson | safe }} and JSON.parse syntax. Using a combination of these two will allow us to re-convert the passed-in strings to 5 arrays of dictionaries.

Afterwards, we have Javascript code that listens for a button click (this button is the “Randomize” button that the user can select each time the user wants to randomly generate an outfit). Every time the button is clicked, it will "try to randomize" each article type via a for loop. For each of the five article types, an index will be randomly generated. This index will be used to randomly select a dictionary from this array of dictionaries for that article type (if there’s only one dictionary, then that sole dictionary will be selected; if there are no dictionaries, then an empty dictionary will be selected). This randomly selected dictionary for each article type represents the random selection of an article of clothing, for each article type. After selecting this dictionary, we then use the “filepath” and “brand” keys of the dictionary to select the file path where the image of that article is saved and the brand name of the article, respectively.

Once we do this for each article type, we then display a pre-created table. This table is what is shown to the user; the first row of the table is a row of article type headers. The second row is a row of html “img” tags whereby each img tag’s source attribute is set to the file path where the image of the article is saved. If a user has not uploaded a particular article type in the past and there is no image to select, then the “img” tag has a default “src” value that leads to a default picture that displays “No Image Available”. Finally, the third row of the table displays the brand name for each article of clothing that’s displayed in the above row.

Each time the user hits the “Randomize” button, new combinations of randomly generated articles of clothing will be displayed, allowing the user to witness the full gamut of randomly generated outfits.

## VII. STATISTICS
Our analytics route first has two “SELECT” statements to the articles and brands and dates from the user. Analytics has three dictionaries, one to keep track of data on articles, another for brands, and another for dates. articleDict has five keys, each an article (i.e. accessory, hat, top, bottom, or shoe). A for loop will iterate through each article from the “shopping_log” table and update the appropriate value for the key. Likewise, we do so for brands, either updating values if the key already exists, or adding the brand to the dictionary if it is not yet there. Additionally, it gets only the top five most worn brands from the dictionary. Finally, it converts all of the months from numbers (e.g. “12”) to the names of months (e.g. “December”), and updates the count of each month. These all get passed into analytics.html. Within analytics.html, we are able to create 3 graphs representing data on articles, brands, and dates. We are able to make lists that act as each graphs' dataset based on whatever the numbers are within accessoryDict, dateCount, and sortedBrands. These graphs are able to access the information from these lists to label the graphs and determine the correct values.