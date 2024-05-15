# BitPropTask
I still have issues with running the code as my laptop isn't really made for coding so I tried my best to use Visual studio, this code throws an exception in line 2 in flask_sqlalchemy although I have installed both on my Python environment.
This code is best run in Flask,and Python in visual studio.
I have commented out my thoughts and explanations within the code because I prefer coding then explaining at the same time.
even though I integrated sqlalchemy into my whole project/solution I am not really sure if the database is able to run in the code.
I coded very simple interface with CSS and HTML.
I will put some further information on what I was/have intended to do:
Models:
Defines database models for Property, Agent, and InterestedTenant, specifying their attributes and relationships.

sample Data:
Adds sample data to the database if it's empty.

Email Function:**
   - `send_interest_email`: Sends an email to the agent when a tenant expresses interest in a property.

Routes:**
   - `/`: Displays the home page, showing available properties.
   - `/property/<property_id>`: Shows details of a specific property.
   - `/register_interest/<property_id>`: Handles tenant registration of interest (sends an email to the agent).
   - `/agent_login`: Handles agent login.
   - `/agent_dashboard`: Shows the agent's dashboard with interested tenants for their properties.
   - `/tenant_login`:  (Placeholder for tenant login; not implemented).
   - `/logout`: Logs out the agent.

logout`_ Logs out the agent_Run the App:**
   - Starts the Flask app in debug mode
