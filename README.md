# GuessWhat
"Houston we have a problem!"

Please find more details on https://devpost.com/software/guess-what

https://docs.google.com/presentation/d/1iOpLoi-afa1dKs8IT6wSYiSTflpyqeznw9r6D5TQxNg/edit?usp=sharing

# Inspiration
Nowadays, companies use Facebook page to communicate with their customers and some how it ends up with customer feedbacks, problems and complaints and here the problems

Too many posts on Facebook Page
Page Admin has no time to take care of everything
A real big problem will go “viral” if we not solve it in time especially corporate related
What should we focus first?
Is it better to know what is the most important case to handle? Let GuessWhat Assistant to manage priority of your tasks

# What it does
Classification API
Classify intentions from user message/conversation
Classify sentiment from user message/conversation
Prioritized jobs/tasks based on business rules
# How we built it
## Backend
RESTful API using Flask (Python Flask)
Training/testing dataset from Facebook (via API)
MongoDB for a data storage
Redis and Socket io for notification
fastText
Wokers servers hosted on AWS
## Web Frontend
HTML
Vue.js
# Challenges we ran into
Post data on Facebook is unstructured, plenty of noise and we've to carefully process and clean it
We have to build a reliable system to repeat #1 process many times to get better models
Vue.js and fastText are quite new for us
# Accomplishments that we're proud of
We can built a reliable system in just 20 hours
We use Vue.js and fastText for the 1st time with this project!
# What we learned
Machine learning process like data gathering, data cleaning, model training/testing, model tuning and deployment
We cannot get a good model from a single ML process. We have to repeat it many times also each one takes time to get a result. So we have to had a system to support this. The system that can allow us to do the ML process many times as we want and it can give us a fast feedback.
Work under pressure, build a workable product in a short time frame
# What's next for GuessWhat
Some of messages like a simple question/FAQ will be escalated to an integrated Chatbot
Some specific questions escalated to Support Specialist
Custom business rules
