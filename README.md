# MDT monitoring server

A simple & lightweight flask based API server that recieves updates from ongoing MDT deployments without the need for the full deployment services to be installed.

## Quick Start
1. Install the requirements. 
   
   `pip install -r requirements.txt`

2. Add/Edit the line below to the CustomSettings.ini file (usually located in $DepolymentShare/Control/ ) to point to the new monitoring server.
   
   `EventService=http://<Server_address>:9805`
3. Create an environment variable DATABASE_URL that points to a database server. If not created, the application creates an sqlite database called
   app.db in the project root.
4. Configure FLASK_APP environment variable to point to mdt_interface.py for your platform.
   
   `export FLASK_APP=mdt_interface.py` (Unix Bash (Linux, Mac, etc.))

   `set FLASK_APP=mdt_interface.py` (Windows CMD)

5. Start app with flask run and begin deployments, you should see monitoring logs appear on the console and the database will be populated.