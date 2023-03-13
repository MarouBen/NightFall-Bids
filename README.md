# Nightfall Bids
#### Video Demo:  <[URL HERE](https://www.youtube.com/watch?v=-_5_357Y1co)>
Nightfall Bids is a Django-based auction site where users can create listings for items they want to auction off, and other users can bid on those items. The site also allows users to add items to their watchlist, view all active listings, and filter listings by category.

## Installation
To run Nightfall Bids on your local machine, follow these steps:

Clone the repository to your local machine using `git clone https://github.com/<your-username>/nightfall-bids.git`
Install the required packages by running `pip install -r requirements.txt`
Run the database migrations by running `python manage.py migrate`
Create a superuser account for the Django admin interface by running `python manage.py createsuperuser`
Start the development server by `running python manage.py runserver`

### Usage
Once the development server is running, navigate to `http://localhost:8000` in your web browser to access the site.

### Create Listing
To create a new listing, click on the "List" link in the navigation bar or the Home page. Fill out the form with the required information, including the title, description, starting bid,images and category.

### Featured Listings
The default route of the site displays six latest listing that are open. Each listing displays the title, description, current price, and photo.

### Search page
Users should be able to visit a search page where they view all listed items and can search for listings by state (open or closed) or by category.

### Listing Page
Clicking on a listing takes you to a page specific to that listing, where you can view all details about the listing, including the current price for the listing. If you are signed in, you can add the item to your watchlist or bid on the item. If you are the one who created the listing, you can also close the auction from this page.

### Watchlist
Users who are signed in can add items to their watchlist by clicking the "Add to Watchlist" button on a listing page. They can view all of their watched items on the Watchlist page, which displays all of the listings that the user has added to their watchlist and can remove items from thier watch list by clicking a designated heart icon.


### Django Admin Interface
Site administrators can view, add, edit, and delete any listings, comments, and bids made on the site by accessing the Django admin interface at `http://localhost:8000/admin`.


### Fork the repository
Create a new branch for your changes
Make your changes and commit them to your branch
Create a pull request to merge your changes into the main branch

### Credits
Nightfall Bids was created by MarouBen.