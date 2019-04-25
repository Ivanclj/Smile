# Get-H1B

<!-- toc -->

- [Project Charter](#project-charter)
- [Project Planning](#project-planning)
-  [Backlog](#backlog)
- [IceBox](#IceBox)

<!-- tocstop -->

## Project Charter 

**Vision**:  
To build an app that could predict the probability of a user passing the H1B application, given his/her status and info. Would also provide a detailed report page to help users understand what are the factors that impact the outcomes of an application

**Mission**:  
Enable users to use the app to predict the probability of passing the H1B application and understand what are the variables that are driving the success of an application. 

**Success criteria**:  
	1. Machine Learning metric: The model would be evaluated on misclassification rate of whether predicted the correct outcome out of 5 possible outcomes. A misclassification rate of 10% or lower denotes success
	2. Business metric: A Click through rate of 70% to see the detailed report from the user end and a MAU of 1,000 would denote success
 ## Project Planning
 
 - ***Theme***: The theme of this project is to develop a web app that enables users to predict their chances of getting accepted by a H1B visa application. Besides, the app would help them to learn what are important factors affecting the application thus improvements could be done accordingly
 - ***Epics***:
	 - Data Preparation and Exploration:   
	 At this stage, Data preparation and exploration would be done.
		 - story 1: Data Preparation 
			 - Download H1B application datasets from Kaggle
			 - Merge different CSV files together
			 - Clean datasets by removing/imputing NA values, treating outliers and influential points and removing duplicate records
			 - Treat unbalanced outcome class problem
		 - story 2: Data Exploration 
			 - Explore data by calculating descriptive statistics (mean,min,max etc.) and plotting them for important covariates  
			 - Check skewness of covariates and fix them if exist
			 - Engineer features such as breaking address into city and states to create more aggregated and meaningful features
			 - Perform feature selection for model building later
			 
	 - Model Construction:  
	 At this stage, The full model would be constructed and generate desired output to pass all success metrics.
		 - story 1: Model Initialization 
			 - Random split datasets into 80% training and 20% testing
			 - Try various classification model such as Logistic Regression, Random Forest, XGBoost, Neural Nets and Support Vector Machine to predict H1B application outcome
			 - Model will be implemented using Scikit-Learn and Keras
			 
		 - story 2: Model Tunning
			 - Perform Grid/Random Search or utilize Scikit-optimizer library to find best hyperparameter for each model
			 - Compare different models using 10-fold cross validation to select the best model with the lowest misclassification rate
		
	 - Model  Deployment:  
	 At this stage, the full model would be deployed onto AWS and also the web app should be developed to wrap up the project.
		 - story 1: Transition from Local to AWS 
			 - Write unit tests and model reproducible tests and pass them locally 
			 - Export dependencies for the model 
			 - Move datasets and model related files onto AWS environment 
			 - Run through pipeline to make sure no bugs occurred and write necessary logging files 
		 - story 2: App Development 
			 - Write necessary backend structure using flask and link the database where user information would be saved 
			 - Design frontend user interface to have users input their company, salary, location, education and so on to collect information necessary to make the prediction
			 - Design a detailed information page where user could learn what are important factors in H1B application process
		 - story 3: App Improvement
			 - Add more functionalities to allow user to see visualizations of current H1B application distribution and other fun statistics
			 - Add potential visual components if time permits
		 
 ## Backlog
 1. Theme.epic1.story1: Data Preparation (4 point) -Planned
 2. Theme.epic1.story2: Data Exploration (4 point)  -Planned
 3. Theme.epic2.story1: Model Initialization (4 point) -Planned
 4. Theme.epic2.story2: Model Tunning (8 points)
 5. Theme.epic3.story1: Transition from Local to AWS (4 points)
 6. Theme.epic3.story2: App Development (8 points)

## IceBox
1. Theme.epic3.story3: App Improvement (8 points)
<!--stackedit_data:
eyJoaXN0b3J5IjpbMTc3NzE2MzM3MV19
-->