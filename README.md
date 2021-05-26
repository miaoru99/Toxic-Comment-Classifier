# Toxic Comment Classifier
In this project, a web application was built to allow user to upload a csv file with comments or directly type in a comment to obtain the percentage for each toxic categories which are toxic, severe toxic, obscene, threat, insult and identity hate.

## Six models are used to build toxic comment classifier
1. Convolutional Neural Network (CNN)
2. Recurrent Neural Network (RNN) 
3. Hybrid-NN (RNN + CNN)
4. Support Vector Classifier
5. Multinomial Naive Bayes
6. Logistic Regression 

## Model evaluation
The result of model evaluation is shown below (for detail information please refer to Toxic Comment Classification.ipynb):
![Capture](https://user-images.githubusercontent.com/84840289/119681243-79919580-be74-11eb-997f-10e247b396e2.JPG)

# Toxic-Comment-Classifier web application
## Youtube Web Crawler
A youtube web crawler was built to extract toxic comments (for detail information please refer to Youtube WebCrawler.ipynb):
![Capture](https://user-images.githubusercontent.com/84840289/119682061-2a983000-be75-11eb-9440-039d05c6554e.JPG)

## User Interface
A web application was built with Flask which allow user to insert their comment or upload a csv file with multiple comments such as the output file generated from Youtube web crawler. The best model Hybrid-NN was implemented in this web application (for detail information please refer to flaskapp.py) to classify toxic comments. The user interface of the web application is shown below:
![Capture](https://user-images.githubusercontent.com/84840289/119682657-a4301e00-be75-11eb-9fd1-b3f02c3e539b.JPG)

# Data Visualization
Tableau was used to visualize the top 10 toxic comments for each toxic categories (for detail information please refer to BlackLifeMatterYoutubeToxicCommentsSentimentAnalysis.twb).
![Capture](https://user-images.githubusercontent.com/84840289/119684174-dbeb9580-be76-11eb-9b23-90f280a6a7af.JPG)



