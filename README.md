<div align="center">
	<h1>Fiore</h1>
	<p>
		<i>framing instances on rectangles everyday</i>
	</p>
</div>

Fiore combines the ideas of journaling with minimalism, giving you an experience that reflects on your life via a visual calendar.

<div align="center">
	<img src="static/fiore_full_zoomed_out.jpg" alt="drawing" width="60%"/>
	
</div>



## Installation
Fiore is built on Flask, which is a Python web framework. If you don't already have Python, you can install it <a href="https://www.python.org/">here</a>.

Once Python is installed, download and open this repository and run the following command in your terminal to install all the dependencies:
``` bash
pip install -r requirements.txt
```

Run the script via this command to create the database:
``` bash
sqlite3 schema.sql
```
Note: Running the Python script will set up the database for you, so you don't need to download SQLite separately.

### Usage

Once finished with the installation, head over onceagain to your project directory and run it via
``` bash
flask run
```

## Getting started with Fiore

Fiore works by framing instances on rectangles everyday and creating a calendar that is uniquely yours. It's like flipping a page on your calendar, but on each day you see a glimpse of what your day was like. 

Fiore supports the most common image formats and has a very minimal UI, reducing the friction between you and your next journal entry. Here's how to get started!

### Pick a date
For each month, you have a blank canvas in the form of a calendar. Each day can store one image. 
<div align="center">
	<img src="static/date.jpg" alt="drawing" width="55%"/>
</div>

### Upload an image
Chose from a variety of image file formats (even gifs). The support for a variety of file formats ensures that no matter what your media source is, Fiore just works.
<div align="center">
	<img src="static/date.jpg" alt="drawing" width="55%"/>
</div>

### Maybe add a description?
Either adding a bit of context to the image, or just using it as a written journal, you have the option and space to write it.

<div align="center">
	<img src="static/description.jpg" alt="drawing" width="55%"/>
</div>

### Done
Fiore! Watch the memory get framed in your calendar!

<div align="center">
	<img src="static/done.jpg" alt="drawing" width="55%"/>
</div>


## Features

Fiore is inspired by a touch of Italy. The islands, the landscapes and the beaches, they reflect the calmness that comes with intentional living and the calmness that Fiore brings to your journaling experience.

### Viewing, scrolling and deleting entries

Each day can be expanded to it's own page. It will feature the uploaded image in a much bigger size (and a description if you added that).

On the same page, you will find left and right arrow buttons. The left arrow takes you to the previous journal entry, and the right arrow takes you to the next journal entry. The entry can also be deleted from this page.

<div align="center">
	<img src="static/journal_entry.jpg" alt="drawing" width="55%"/>
</div>

### Profile stats

On the profile page, you can see all your account details, with list of all your entries you have created.
This page also allows you to delete your account.
<div align="center">
	<img src="static/profile.jpg" alt="drawing" width="55%"/>
</div>

### Handling errors

Errors, be it from the user or the server, can occcur, and the apology page handles them with a Harry Potter reference while giving you a random place in Italy to explore! 
<div align="center">
	<img src="static/apology.jpg" alt="drawing" width="55%"/>
</div>




