# **WeMatchSports**

## **Overview**
WeMatchSports is a Django-based monolithic web application designed to connect sports enthusiasts by enabling them to find nearby players, match based on skills, and communicate seamlessly. This platform allows users to:
- Discover and join sport-specific public rooms for updates and discussions.
- Match with players of similar skill levels.
- Securely chat with connected partners to coordinate games.

The application is built for scalability, user privacy, and ease of use, with data security measures like encryption for sensitive information.

---

## **Architecture**
WeMatchSports follows a modular, monolithic architecture with distinct Django apps for key functionalities:
- **Authentication**: Handles user sign-up, login, session management, and CSRF protection.
- **General**: Manages the user dashboard, profile settings, notifications, and public rooms.
- **Matchmaking**: Matches users based on skill similarity using algorithms like cosine similarity.
- **Messaging**: Provides an encrypted chat interface for secure communication.

---

## **Setup and Deployment**

### **Run with Docker**
1. Build the Docker image:
   ```bash
   docker build .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 <image_id>
   ```
3. Start Kafka services:
   ```bash
   docker compose up
   ```

### **Run without Docker**
1. Start the Django development server:
   ```bash
   python manage.py runserver
   ```
2. Start Kafka services (ensure Kafka is installed and added to the PATH):
   ```bash
   bin/zookeeper-server-start.sh config/zookeeper.properties
   bin/kafka-server-start.sh config/server.properties
   ```

---

## **Core Features by App**

### **1. Authentication**
- User sign-up, login, and logout functionalities.
- Session management for temporary user data.
- CSRF protection via Django's built-in mechanism.

### **2. General**
- Personalized user dashboard and profile management.
- Notification and connection management.
- Sport-specific public rooms for discussions and updates.

### **3. Matchmaking**
- Suggests players with similar skills using cosine similarity algorithms.
- Easy connect requests for matched players.

### **4. Messaging**
- Secure, encrypted chat functionality.
- Messages stored in the database with chat history retrieval.

---

## **Technology Stack**
- **Backend**: Django, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production-ready configuration)
- **Messaging**: Apache Kafka
- **Containerization**: Docker, Docker Compose

---

## **Contributing**
Contributions are welcome. To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Submit a pull request with detailed changes.