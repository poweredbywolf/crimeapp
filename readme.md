Install Dependencies
----------------------
pip install -r requirements.txt

mysql -u root -p


When app is deployed on the cloud the YAML file will set the Environment variables
In Dev the ENV varaibles will be set by exporting in Terminal
export 

The only Env variable needed to be set in local dev is  "DEPLOYED_STATE"
There after the config file will pull the Database and other environment variables from there
