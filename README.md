stellar-bulk-upload
===================

Python interface to MIT's course management software "Stellar"


How I use it
------------
1. Run it in IPython. (I had trouble running it within the Canopy IDE because of getpass password prompt)
2. Authenticate by issuing `auth()`. It will prompt for the Kerberos username and password
3. `upload_comment` will upload a file and/or comment for a specific class member to assignment1. To change the assignment, you need to change the URL inside `upload_comment`. The class member is specified with the full stellar username, e.g. 'benbit@mit.edu'.

  
