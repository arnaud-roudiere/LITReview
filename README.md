# LITReview
A book/movies/articles reviews and critics app
<br><br>

## How does it work?
The app allows you to do the following:
- register as user
- create a ticket to request a review
- review a movie/book/etc.
- follow other users
- login and logout
<br><br>

## How is composed the app?
The app is composed by following pages:
- Login : allows to sign up or register
- Flux/Home : this main page shows the tickets and reviews create by us and also the ones created by the user(s) we follow, allow to create a ticket or a review with and without any previous request from a followed user
- Post : allows to edit or delete our tickets and reviews
- Follow : allows to follow users or unfollow them, shows us the user following us as well
<br><br>

## How to install the app?
1. Clone the repository
Enter the following in your Terminal to clone the Github repository: <code class="language-bash" data-lang="bash">git clone [https://github.com/arnaud-roudiere/LITReview.git](https://github.com/arnaud-roudiere/LITReview.git)</code>
2. Create a virtual environnement
Create the virtual environnement: <code class="language-bash" data-lang="bash">python -m venv env</code><br>
3. Activate the virtual environnment 
You need to activate the "active.bat" file in Windows : <code class="language-bash" data-lang="bash">env\Scripts\activate.bat</code><br> (for Mac it's <code class="language-bash" data-lang="bash">source env/bin/activate</code> )
4. Install the requirements
Install the packages with: <code class="language-bash" data-lang="bash">pip install -r requirements.txt</code><br>
5. Migrate the tables to the database
Type the following code : <code class="language-bash" data-lang="bash">python manage.py migrate</code><br>
6. Launch the app
Type the next code : <code class="language-bash" data-lang="bash">python manage.py runserver</code><br>
By default it opens the port 8000.
