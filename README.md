# notesApp
To Run the app

Step 1: install the requirements file

Step 2: input your OPENAI_API_KEY in init.py

Step 3: open terminal and go to app root path ( path/to/downloadFolder/notesApp ) [ make sure the root package is notesApp ]

Step 4: run following command "fastapi dev main.py"

Step 5: Open http://localhost:8000/docs to test the apis

Note: Admin user is automatically created at the first run of app. User:admin, pass: admin

API Explation: 

/users/create [POST]: create a user

/users [GET] : gets list of users {only if user has admin rights}

/users/login [POST]: returns user_id if correct login

/isers/logout [POST]: logs out user [Currently no use]


/notes?user_id={user_id}: returns all notes for the user

/notes/{note_id}: returns Note details for particular note

/notes/create?user_id={user_id} : creates new note for user

/notes/delete/{note_id}?user_id={user_id} : deletes particular note if note is owned by user

/notes/update/{note_id}?user_id={user_id} : updates particular note if note is owned by user

/notes/summary/{note_id}?user_id={user_id} : provides summary of particular note if note is owned by user

/notes/action_items/{note_id}?user_id={user_id} : provides action items for particular note if note is owned by user

/notes/tag/summary?user_id={user_id}&tag={tag} : provides summary for all notes for a user having a particular tag 

/notes/completion?title={title}&content={content} : Provide note suggestion for a given title and content( if any )


database used is sqlite

