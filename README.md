routely-akshaya-patra
=====================

This is a project for the Code For India Hackathon 2014

How do I use it?

      1. Edit the configuration in the minitwit.py file or
         export an MINITWIT_SETTINGS environment variable
         pointing to a configuration file.

      2. Fire up a shell and run this:

         flask --app=minitwit initdb

      3. Now you can run minitwit:

         flask --app=minitwit run

         the application will greet you on
         http://localhost:5000/
