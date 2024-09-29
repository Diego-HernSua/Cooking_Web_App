WEB APPLICATIONS PROJECT - [ COOKINGTOK ]


-----------------------------------------------------------------------------

AUTHORS:

Francisco José Landa Ortega

Teresa Gener López

Diego Hernández Suárez

-----------------------------------------------------------------------------

NO ADDITIONAL PACKAGES, THE ONES USED IN THE LABORATORIES:

python3 -m venv venv
. venv/bin/activate
flask --debug --app=cooking run

pip install -U pip
pip install Flask python-dateutil
pip install flask-sqlalchemy mysqlclient
pip install flask-bcrypt
pip install flask-login

User name: 24_webapp_028
Password: WgdPsWC3
Name of the database: 24_webapp_028c

----------------------------------------------------------------------------

ADDITIONAL FUNCTIONALITIES:

-The bookmark button is an image (icon) that changes depending on whether the recipe is bookmarked or not (located next to the recipe title).

-We have differentiated between complete and incomplete recipes. The completed ones are with ingredients and steps and the incompleted ones do not
have steps and ingredients. In the main page, there are only showed the completed recipes. The incompleted ones can be seen from the create recipe view 
and from the my_profile view. 

-The user profile displays additional features such as the user's recipes, incomplete recipes and bookmarks (in my_profile, if the
user is authenticated), and also images uploaded by that user.

-While completing the steps of a recipe, thanks to JavaScript, the user can change steps by dragging and placing them in the correct order
(e.g., dragging step 7 into step 1 will switch their positions). Also added with JavaScript, the add and remove buttons for ingredients ansd steps.

-The interface becomes interactive on the webpage when a user hovers over a hyperlink or a box. For example, when a user hovers over a recipe
in the main view (and other elements), the recipe will increase in size to indicate that the mouse is over that recipe.

- We have added a comments section to recipes where any user can add a comment. It displays a single box with the user's rating and comments
separately. Each comment also includes the time it was published, and a user can add several comments but can only add one rate.

-We calculate and plot the average rating score from all the ratings given in a certain recipe (located below the recipe title).

-There is a search function in the main view that finds recipes containing the ingredient entered by the user.

-When a user adds an ingredient to a recipe (or in the before mentioned search function), the web application will recommend the existing
ingredients in the database with similar letters. For example, typing "chee" will prompt recommendations like "cheese."

-If a user clicks on the "CookingTok" image in the header bar, it will always redirect the user to the main view to enhance the user experience.

-When starting a recipe, the user has the option to create a new recipe. Additionally, the user can click on incomplete recipes he has already started
and he is redirected to the page of adding steps and ingredients for that recipe.

-The aesthetic of the webpage is focused on maintaining warm colors as the color palette with some grey.

--------------------------------------------------------------------------------------------------------------------------------------------------------------

USER ACCOUNTS ALREADY REGISTERED:

Email: curro@gmail.com
User: Curro123
Password: Hola


Email: diego@gmail.com
User: Dieguito_guay
Password: minecraft


Email: teresa@gmail.com
User: Teresita_03cooker
Password: 1234


Email: maria@gmail.com
User: merylop7
Password: 0000
