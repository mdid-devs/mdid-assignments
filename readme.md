## MDID Assignments

###Status 

Alpha, do not install on a production machine (there will likely be additional schema changes).

###Summary 

* Create courses inside of MDID
    * Enroll users as instructors or students
    * Assign and collect presentations from students
    * Flexible but optional semester definition
    
* Log in to MDID3 via LTI (optional), features of LTI tool provider include:
    * Create/Link to course from LTI Consumer (e.g. Blackboard)
    * Create/link to assignment from LTI Consumer
    * User first/last name & email sync (optional)

#### Planned additional features
* Addition of a Personal Work record (for creation of e-portfolios)
* Addition of an e-portfolio record

### Dependencies
* ims-lti-py
* lxml
* oauth2
* nose
