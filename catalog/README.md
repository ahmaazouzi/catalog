# World Literature application Description
This application is a catalogue for world literature works. The user can browse through different languages and see literary works and classics belonging written these languages. The user will also find information about the books, such as their titles, authors, translators, the years the works have been translated, an amazon link for each work and a short summary.
Authorized users, who are logged in using their google plus credentials, can also add, delete and edit items in the application.


# How to run the app
Running the app requires Virtual box and vagrant virtual machine. To run the application:

1.Using the terminal, change directory to catalog (**cd catalog**), then type **vagrant up** to launch the virtual machine.

2.Once it is up and running, type **vagrant ssh**. This will log your terminal into the virtual machine, and you'll get a Linux shell prompt. When you want to log out, type **exit** at the shell prompt.  To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it. Now that you have Vagrant up and running type **vagrant ssh** to log into your VM.  change to the /vagrant directory by typing **cd /vagrant**. This will take you to the shared folder between your virtual machine and host machine.
Type **ls** to ensure that you are inside the directory that contains proj.py, database.py, lotsofbooks.py and a directory named 'templates’.

3.Now type **python database.py** to initialize the database.

4.Type **python lotsofbooks.py** to populate the database with languages and book items. (Optional)

5.Type **python proj.py** to run the Flask web server. In your browser visit **http://localhost:8000** to view the World Literature app.  You should be able to view languages and books available in the app. To add, edit, and delete books and add new languages. You must first login using your google plus credentials.

6. The application also provides son api endpoints.
