<div align="center">
	<h1>Fiore</h1>
	<p>
		<i>framing instances on rectangles everyday</i>
	</p>
</div>

Fiore combines the ideas of journaling with minimalism, giving you an experience that reflects on your life via a visual calendar.

<div align="center">
	<img src="static/fiore_full_zoomed_out.jpg" alt="drawing" width="70%"/>
	
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
<br>
<br>
Fiore supports the most common image formats and has a very minimal UI, reducing the friction between you and your next journal entry.

### Pick a date
For each month, you have a blank canvas in the form of a calendar. Each day can store one image. 
<div align="center">
	<img src="static/date.jpg" alt="drawing" width="70%"/>
</div>

### Upload an image
Chose from a variety of image file formats (even gifs).
<div align="center">
	<img src="static/date.jpg" alt="drawing" width="70%"/>
</div>

### Maybe add a description?
Feel free to add one, like a journal text.

<div align="center">
	<img src="static/description.jpg" alt="drawing" width="70%"/>
</div>

### Done
Fiore! Watch the memory get framed in your calendar!

<div align="center">
	<img src="static/done.jpg" alt="drawing" width="70%"/>
</div>






