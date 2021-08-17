# P9_Develop-a-Web-app-using-Django

***
## Table of contents
1. [Program surroundings](#program-surroundings)
2. [Preliminary remark](#preliminary-remark)
3. [Setup the computer before launching the website in a local environment](#setup-the-computer-before-launching-the-website-in-a-local-environment)
4. [Launch the WebSite locally  using command lines](#launch-the-WebSite-locally-using-command-lines)
5. [Stop the local server](#stop-the-local-server)
6. [Steps to generate a flake8-html file](#steps-to-generate-a-flake8-html-file)
***


## Program surroundings

###### This program is the number nine on thirteen projects to be validated in order to get a degree as a developer in Python applications.  

For more info on that subject please visit the following website:  
https://openclassrooms.com/fr/paths/322-developpeur-dapplication-python
  

###### The aim of this project is to realize a POC of a website following requirement specifications and wireframes

## Preliminary remark
**This program has been tested with Python version 3.8.5(default, Jan 27 2021, 15:41:15)**     


## Set up the computer before launching the website in a local environment

### A. Get the GitHub repository on your computer
There are two ways to get this repository:
#### 1. copy the zipped repository and unzip it where you want on your computer. The following image show you the button to click to copy the zipped repository on your computer  
![how to download the repository](https://github.com/oliviersamin/P9_Developpez-une-application-Web-en-utilisant-Django/blob/main/GitHub-get-repository.png)
#### 2. Clone the repository in command lines
* Go to your working directory and initialize the directory using the following command   
###### git init
* type the following command line     
###### git remote add <short_name_of_local_deposit> https://github.com/oliviersamin/P9_Developpez-une-application-Web-en-utilisant-Django.git    
where <short_name_of_local_deposit> is a name you choose to call later this repository
* git branch -M main
* git pull OC main
the repository is now cloned in your computer

### B. Create and activate a local environment
To create the virtual environment venv follow the next steps in command line:   
#### 1. be inside the root working directory named "P9_Developpez-une-application-Web-en-utilisant-Django"   
#### 2. execute the following command lines in this order :      
###### **python3 -m venv env**  
###### **source env/bin/activate**

***(env)*** should appear at the beginning of the command line   

### C. Install all the necessary packages using requirements.txt  
#### 1. Go in the subdirectory LITReview
#### 2. Execute the following command line: 
###### **pip install -r requirements.txt**


## Launch the WebSite locally  using command lines
When the setup has been done the first time, it is not needed to repeat all the previous steps.   
#### A. Go inside the root working directory named "P9_Developpez-une-application-Web-en-utilisant-Django"
#### B. Launch your virtual environment with the following command line:
###### **source env/bin/activate**   
#### C. Go in the subdirectory LITReview (where the manage.py file is)
#### D. Execute the command:
###### **./manage.py runserver**    
#### E. Using the web browser go to the url **http://127.0.0.1:8000**    
#### F. You are connected to the local website    

## Stop the local server
When you have finished using the WebSite you may do the following:
#### 1. In your Web Browser: close your tab or window corresponding to the website
#### 2. In your terminal stop the server by using the CONTROL-C keys
   
## Steps to generate a flake8-html file    
If you want to check for the PEP8 validity of the code tou may use the following steps:    
#### 1. Launch your virtual environment  
#### 2. Go to the LITReview sub-folder, launch the following command line:   
###### flake8 --config=config_flake8.ini base_app/filter_viewable_posts.py base_app/forms.py base_app/models.py base_app/views.py base_app/templatetags/display_create_critic_button.py
This will check the validity of the 5 following files:
#### views.py
#### models.py
#### filter_viewable_posts
#### forms
#### display_create_critic_button
