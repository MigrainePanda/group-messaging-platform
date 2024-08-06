# Group Messaging Platform

A real-time messaging platform that uses JWT (JSON Web Tokens) for secure user authentication and SocketIO for online conversation.

![chatroom-demo-optimize.gif](https://i.postimg.cc/m2hb4GHp/chatroom-demo-optimize.gif)

## Features
**Secure Authentication**: Utilizes JWT to securely authenticate users and control access to chat rooms.

![b.png](https://i.postimg.cc/X7HH83tf/b.png)

**Real-Time Messaging**: Uses SocketIO for real time messaging with other users.

![c.png](https://i.postimg.cc/jqvZxtxp/c.png)

**Custom Chat Rooms**: Create and join personalized chat rooms to talk with people of similar interests, topics, or just hang out with friends.
    
![chatrooms.png](https://i.postimg.cc/C1tfhKdJ/chatrooms.png)

**Message History**: Stores user message histories in an SQLite database for later viewing on their profile page.
    
![a.png](https://i.postimg.cc/2yCcH5zw/a.png)

## Tech Stack
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Socket.io](https://img.shields.io/badge/Socket.io-black?style=for-the-badge&logo=socket.io&badgeColor=010101)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

## Run Locally

Clone the project

```bash
  git clone https://github.com/MigrainePanda/group-messaging-platform
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python -m application
```

Navigate to <http://127.0.0.1:5000> to start chatting!

## Authors

- Nicholas Tanaka ([@MigrainePanda](https://www.github.com/MigrainePanda))
- Brandon Xu ([@bxrr](https://www.github.com/bxrr))
