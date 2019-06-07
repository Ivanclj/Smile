# Smile
## Developer: Lingjun Chen
#### QA: Si(Angela) Chen
# Outline

-   [Project Charter](https://github.com/Ivanclj/Smile/blob/d35348804c4b6943c13673f204d25871ecf6d078/README.md#project-charter)
-   [Project Planning](https://github.com/Ivanclj/Smile/blob/d35348804c4b6943c13673f204d25871ecf6d078/README.md#project-planning)
-   [Backlog](https://github.com/Ivanclj/Smile/blob/d35348804c4b6943c13673f204d25871ecf6d078/README.md#backlog)
-   [IceBox](https://github.com/Ivanclj/Smile/blob/d35348804c4b6943c13673f204d25871ecf6d078/README.md#IceBox)

## [](https://github.com/Ivanclj/Smile/blob/d35348804c4b6943c13673f204d25871ecf6d078/README.md#project-charter)Project Charter

**Vision**:  
This app would allows employees at Tech companies to find out whether they need to seek treatment for potential mental health issues. It also helps Tech companies to track the mental health of their employees and provide them with necessary assistance if needed

**Mission**:  
Help users to find out whether they need treatment for mental health problems by taking their input on a series of survey question and predict outcome for the user. It would also provides a report on what are the factors impact the user's result

**Success criteria**:  
1. Machine Learning metric: The model would be evaluated on misclassification rate of whether predicted the correct outcome. A misclassification rate of 10% or lower denotes success  
2. Business metric: A Click through rate of 70% to see the detailed report from the user end and a MAU of 1,000 would denote success

## [](https://github.com/Ivanclj/Smile/blob/d35348804c4b6943c13673f204d25871ecf6d078/README.md#project-planning)Project Planning

-   _**Theme**_: The theme of this project is to develop a web app that enables users to find out whether they need to receive treatment for potential mental issues. Besides, the app would help them to learn what are important factors affecting the result
-   _**Epics**_:
    -   Data Preparation and Exploration:  
        At this stage, Data preparation and exploration would be done.
        
        -   story 1: Data Preparation
            -   Download mental survey datasets from Kaggle
            -   Clean datasets by removing/imputing NA values, treating outliers and influential points and removing duplicate records
            -   Treat potential unbalanced outcome class problem
        -   story 2: Data Exploration
            -   Explore data by calculating descriptive statistics (mean,min,max etc.) and plotting them for important covariates
            -   Check skewness of covariates and fix them if exist
            -   Engineer features such as breaking address into city and states to create more aggregated and meaningful features
            -   Perform feature selection for model building later
    -   Model Construction:  
        At this stage, The full model would be constructed and generate desired output to pass all success metrics.
        
        -   story 1: Model Initialization
            
            -   Random split datasets into 80% training and 20% testing
            -   Try various classification model such as Logistic Regression, Random Forest, XGBoost, Neural Nets and Support Vector Machine
            -   Model will be implemented using Scikit-Learn and Keras
        -   story 2: Model Tunning
            
            -   Perform Grid/Random Search or utilize Scikit-optimizer library to find best hyperparameter for each model
            -   Compare different models using 10-fold cross validation to select the best model with the lowest misclassification rate
    -   Model Deployment:  
        At this stage, the full model would be deployed onto AWS and also the web app should be developed to wrap up the project.
        
        -   story 1: Transition from Local to AWS
            -   Write unit tests and model reproducible tests and pass them locally
            -   Export dependencies for the model
            -   Move datasets and model related files onto AWS environment
            -   Run through pipeline to make sure no bugs occurred and write necessary logging files
        -   story 2: App Development
            -   Write necessary backend structure using flask and link the database where user information would be saved
            -   Design frontend user interface to have users input their company, salary, location, education and so on to collect information necessary to make the prediction
            -   Design a detailed information page where user could learn what are important factors that affects results
        -   story 3: App Improvement
            -   Add more functionalities to allow user to see visualizations of their answers among all users
            -   Add potential visual components if time permits

## [](https://github.com/Ivanclj/Smile/blob/d35348804c4b6943c13673f204d25871ecf6d078/README.md#backlog)Backlog

1.  Theme.epic1.story1: Data Preparation (4 point) -Planned
2.  Theme.epic1.story2: Data Exploration (4 point) -Planned
3.  Theme.epic2.story1: Model Initialization (4 point) -Planned
4.  Theme.epic2.story2: Model Tuning (8 points)
5.  Theme.epic3.story1: Transition from Local to AWS (4 points)
6.  Theme.epic3.story2: App Development (8 points)

## [](https://github.com/Ivanclj/Smile/blob/d35348804c4b6943c13673f204d25871ecf6d078/README.md#icebox)IceBox

1.  Theme.epic3.story3: App Improvement (8 points)
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE3MTQzNDE1ODIsODcwMzM4NTc1XX0=
-->