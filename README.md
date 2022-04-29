# Capstone-Project

# Installation Instructions
git clone https://github.com/johnzwiss/Capstone-Project.git <br />
cd Capstone-Project <br />
pipenv shell <br />
cd Capstone-Project/capstone-project <br />
python3 manage.py runserver <br />

## Route Table
| Routes      | Description |
| ----------- | ----------- |
| /      | index       |
| /login   | Login        |
| /logout   | Logout        |
| /signup   | Sign up        |
| /teacher/classroom   | Teacher's Classrooms        |
| /teacher/classroom/<classroom_id>   | Specific Teacher's Classroom        |
| /teacher/classroom/<classroom_id>/<student_id>   | Specific Student in Teacher's Classroom        |
|/student/welcome/<student_id>      | Initial Student view       |
|/student/game      | Student Game       |
|/student/results   | Student's scores       |


# User Story 

The user will be presented with a login page and two options. They can sign in as a teacher or as a student. As a teacher, they will be able to create a classroom, add students to the classroom, and track students progress in memorizing their multiplication facts. The teacher will be able to click on individual students and see a more detailed breakdown of the student. The student, when logging in, will be presented with a welcome page and an option to start the current lesson they are assigned. When a student completes a lesson in sufficient time, with enough accuracy, they will be automatically moved on to the next set of questions. When either user is done with their session, they will be able to log out. 

# MVP
Full CRUD on Classroom Model <br />
Teacher can edit students <br />
Flashcard game for students times tables 1-12 <br />
Flippable flashcards <br />
Timed game/ graded game<br />
Display student progress in classroom <br />
Multiple classrooms for teachers<br /> 

# Stretch 
Addition, subtraction, and division games<br /> 
Sound effects<br /> 
Parent profiles<br /> 
Review lessons<br /> 

# Tech Stack 
Django<br />
Python<br />
PosgreSQL<br />
Materialize<br /> 

# Wireframes


![Sign up](https://i.imgur.com/YkJ9jJ0.png)
![Teacher Login](https://i.imgur.com/dPsaRLQ.png)
![Student login](https://i.imgur.com/9Zo5YG0.png)
Student Welcome Page
![Student Welcome Page](https://i.imgur.com/XW0129v.png)
Flash Card Page
![Flash Card Page](https://i.imgur.com/vCq4q6T.png)
Classroom View
![Classroom View](https://i.imgur.com/GR6xUfZ.png)
Student Detail Page
![Student View](https://i.imgur.com/4CGdaSD.png)

# ERD
![ERD](https://i.imgur.com/Yd9CzDK.png)

