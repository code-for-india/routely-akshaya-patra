routely-akshaya-patra
=====================

This is a project for Code For India Hackathon 2014

How do I use it?

      1. edit the configuration in the minitwit.py file or
         export an MINITWIT_SETTINGS environment variable
         pointing to a configuration file.

      2. fire up a shell and run this:

         flask --app=minitwit initdb

      3. now you can run minitwit:

         flask --app=minitwit run

         the application will greet you on
         http://localhost:5000/
