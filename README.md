# stuywritingcenter
Stuy Writing Center official website.

### Database structures:

#### Editors database:
 - email [text]: prefix of the stuy.edu in your email
 - password [text]: hashed version of ur password
 - fname [text]: first name
 - lname [text]: last name
 - grade [integer]: grade
 - hours [real]: hours worked
 - selected [text]: a comma-separated string indicating the request ids that the user has selected
 - months [text]: stringified dictionary representing the amount you've worked each month
 - pronouns [text]: the user's pronouns
 - verified [integer]: a 0 or 1 indicating whether the user's account has been verified

#### Mentees database:
 - email [text]: prefix of the stuy.edu in your email
 - password [text]: hashed version of ur password
 - fname [text]: first name
 - lname [text]: last name
 - grade [integer]: grade
 - requests [text]: a comma-separated string representing the ids of every request id the user has made
 - pronouns [text]: the user's pronouns
 - verified [integer]: a 0 or 1 indicating whether the user's account has been verified

#### Requests database:
 - requester_fname [text]: the requester's first name
 - requester_lname [text]: the requester's last name
 - requester_grade [integer]: the requester's grade
 - requester_email [text]: the requester's email
 - requester_pronouns [text]: the requester's pronouns
 - teacher [text]: the name of the teacher
 - course [text]: the name of the course
 - period [integer]: the period of the class
 - help [text]: the things they need help with
 - assignment_link [text]: a link to the assignment
 - essay_link [text]: a link to their essay draft
 - time_created [integer]: an integer timestamp of the request creation date
 - time_due [integer]: an integer timestamp of the due date
 - editor_matched [integer]: an integer equal to 0 or 1 indicating whether an editor has been matched
 - edit_completed [integer]: an integer equal to 0 or 1 indicating whether an editor has marked the edit as "completed"
 - approved_by_mentee [integer]: an integer equal to 0 or 1 indicating whether the edit has been finished
 - editor_email [text]: the email prefix of the editor
 - editor_name [text]: the full name of the editor
 - hours [real]: the number of hours spent on the edit
 - tags [text]: the tags of the edit
 - helped [text]: what the editor helped with
 - in_person [integer]: a 0 or 1 representing whether the mentee would prefer to meet in-person
