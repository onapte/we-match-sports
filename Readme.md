# WeMatchSports

## About the Project

- For “WeMatchSports”, we have built a web application that helps people quickly find sports buddies nearby. Many people enjoy sports but often struggle to find others to play with due to busy schedules or last-minute changes. WeMatchSports solves this by connecting users with others who share similar sports interests.
- The application allows users to:
   - View sport specific Public Rooms so that people can access the latest news about that sport.
   - Get matched with similar skilled players to find people with similar skill sets by just a click of a button
   - Chat with Connected Partners securely to coordinate the game details and what not.
- We have aimed to make it easy, secure, and fast for people to connect with other fellow players who want to play the same sports. The app also keeps user data private with encryption.
- We have made it easier to discover sports by creating a responsive, safe, and user-friendly platform that facilitates communication. This allows for more impromptu, enjoyable sporting activities without requiring a predetermined group of buddies to be accessible, saving users time while meeting new people at the same time.


## Steps to run the code on docker container
For Backend:
- docker build .
- docker run -p 8000:8000 <image_id>

For Kafka:
- docker compose up

## Steps to run the code without docker container
- python manage.py runserver
- bin/zookeeper-server-start.sh config/zookeeper.properties (Assuming that Kafka is added to the path)
- bin/kafka-server-start.sh config/server.properties (Assuming that Kafka is added to the path)

## Microservices with snapshots
### Authentication
- Manages the authentication and authorization processes of the project.
- Consists of sections like sign-up, login and logout.
- Manages and stores temporary data in the form of user sessions.
- Prevents unauthorized access to the service by redirecting users to the login section.
- Leverages Django's inbuilt Cross-Site Resource Forgery (CSRF) protection mechansim by passing unique tokens with each API POST call.

#### Login

![image](https://github.com/user-attachments/assets/b29361c2-c7e0-4b28-b38a-f972e0876e0d)   

#### Sign-Up

![image](https://github.com/user-attachments/assets/2932f2e4-5343-4509-adfa-bbdcd610feaa)   

### General
- Renders a customized dashboard for every user.
- Handles general services like notification management and users connection management.
- Allows users to make changes to their profiles.
- Contains public rooms dedicated to various sport that users can view based on their interests.
- Provides seamless interface for users to browse through a list of similar profiles.

#### Dashboard

![image](https://github.com/user-attachments/assets/2398f8fc-7095-41b3-91f7-3a2d0ce5e7d2)   

#### User Profile

![image](https://github.com/user-attachments/assets/91a57ae5-296f-44df-ae69-29aa8e1f145a)   

#### Public Rooms

![image](https://github.com/user-attachments/assets/4afbdf1c-d284-4654-aac6-a5021b78de3b)   

#### Public Rooms - Tennis

![image](https://github.com/user-attachments/assets/c4aa5035-3404-44ac-a800-959f1b765b18)   

### Matchmaking
- Allows users to view a list of players with similar skills by clicking a button.
- Utilizes a cosine similarity algorithm in the backend to identify players with matching skill sets.
- Displays the list of similar skilled players with an option to send a connect request via a dedicated button.

#### Find Matched Players
![image](https://github.com/user-attachments/assets/d95470c9-899c-4a0e-aefe-90b62a554abe)


### Messaging
- Displays a messaging user interface for the user with its connections.
- Stores the messages in an encrypted in the database.
- Messages are saved in the chat history.

#### All chats per connection
![image](https://github.com/user-attachments/assets/ca667701-bd1e-4d29-b99d-b7f7ff8700af)
