# Reddit Flair Detector 
 **Working**

This repository is a reddit flair detction web application using flask and python.The user enters the url of the required post. The app takes the url, extracts various features from it (comments, authors, body .etc.) and tries to predict the flair using them by applying the finalized model.

Web application link : https://reddflair.herokuapp.com/


**Steps required to create this web application**

1.**requirements.txt** : contains the required modules to run this application.

2.**Folder** : **Getting_Started_Jupyter_notebook** 
  
	  It contains the beginning steps :
		
		PART_1: Reddit Data Collection
		PART_2:Exploratory Data Analysis (EDA)
		Part_2_cont: It contains pre process and data cleaning required to perform PART_3
		PART_3: Building a Flair Detector
		
 3.**Folder** : **Web_app**
 
    It contains the work done in Step 2 using Flask.Application has an input field which expects a link 
    to a reddit post from ​r/india​ . On submission it predict the flair of the post.
                
    Web applications also has an endpoint called ' /automated_testing' . This endpoint will be used for 
    testing performance of the classifier.    
            
    '/stats': gives the statistics of the number of comments and upvotes of different flairs.
    
   
**Running on localhost**

    clone into repository bash https://github.com/gtrived/flask_app

    Create a virtual environment .

    Go inside the cloned directory and enter command pip install -r requirements.txt.

    Go inside the Web directory and enter command  python app.py to start the server. 
    
