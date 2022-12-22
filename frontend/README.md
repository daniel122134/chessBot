# Daniels HW website

## this is a frontend only app served by an http server for CORS support
###best way to view the site will be:
running this in the root folder:
####python3
    * python3 -m http.server
####python2
    * python -m simpleHTTPServer

and simply navigate to http://localhost:8000 on chrome

###if a Oneliner is required this can be used:

###Mac Onliner
####python3
     * python3 -m http.server & ; open -a "Google Chrome" http://localhost:8000
####python2
     * python -m simpleHTTPServer & ; open -a "Google Chrome" http://localhost:8000

notice the "&" i used for detaching the proccess in order to keep this command a oneliner
this will require you to close the proccess manually when viewing the site is done.

###Windows Onliner
####python3
     * python3 -m http.server & ; Chrome http://localhost:8000
####python2
     * python -m simpleHTTPServer & ; Chrome http://localhost:8000

this was **`not`** tested on Windows but should work as long as chrome and python are in your PATH environment variable



---
####the site includes 2 means of contact: 
* a link to my linkedin page
* a contact form that opens the user's email software and embeds his details into the email.
  * validations on input
    * first name - must be present
    * last name - must be present
    * phone number -  must be an israeli mobile phone number


---
### js notes

####used a framework written by my friend david. 
* similar to react
* easy to read
* all in native js (no jsx)
* stying is specified inside component's js file

####imported some components and styling we wrote in our previous projects (text-input, x-switch, themes styles etc...)
* some detail about previous projects is available in the "Vote for projects" page

####js in this project is used for:
* navigation
* input validation
* formatting and changing themes
* opening mail app