import json
import requests
from requests import *

class empire_api_core:

	# constructor method
	def __init__(self):
		
		# initiate API global vars some w/passed values
		self.api_session_token = ""
		self.api_perm_token = ""
		self.api_request_token = ""
		self.api_user = ""
		self.api_pass = ""
		self.api_host = ""
		self.api_port = ""
		self.api_version = ""
		self.api_url_holder = ""
		
		# tracks the authentication status of object/instance
		self.object_authentication_status = False

	
	#### SET GLOBALS FUNCTIONS ######

	# set the API username
	def api_set_username(self,username):
		
		if username != "": 
			self.api_user = username
			return True
		
		else:
			return False
			
	# set the API password
	def api_set_password(self,password):
		
		if password != "":
			self.api_pass = password
			return True
		
		else:
			return False
	
	# set the API host
	def api_set_host(self,host):
		
		if host != "":
			self.api_host = host
			return True
		
		else:
			return False
	
	# set the API port
	def api_set_port(self,port):
		
		if port != "":
			self.api_port = port
			return True
		
		else:
			return False

	
	#### BUILD API REQUEST FUNCTION ######
	
	# Build and send the JSON request
	def api_send_request(self,request_type,request_page,request_data):

		# build the API  request
		url = "https://" +self.api_host + ":" + self.api_port + request_page
		data_json = json.dumps(request_data)
		
		# set the API URL variable
		self.api_url_holder = request_type + " : " + url + " [ " + str(data_json) + " ]" 

		# check the request type - different actions for GET and POST
		if request_type == "GET":

			try:
				response = requests.get(url,verify=False,timeout=3)
				return response.json()
					
			except Exception as e:	
				return "ERROR: Fail on GET Request: " + str(e) 


		elif request_type == "POST":

			try:
				headers = { 'Content-Type' : 'application/json' }
				response = requests.post(url,headers=headers,data=data_json,verify=False,timeout=3)
				return response.json()								
					
			except Exception as e:
				return "ERROR: Fail on POST Request: " + str(e) 

		
		elif request_type == "DELETE":
			
			try:
				response = requests.delete(url,verify=False,timeout=3)
				return response.json()
					
			except Exception as e:
				return "ERROR: Fail on DELETE Request: " + str(e) 
			
		
		else: return False
	
	
	#### ADMIN FUNCTIONS ######
	
	# ADMIN - Get Session Token - Handle response in wrapper code
	def admin_get_session_token(self):
		
		# Handler : POST /api/login
		# Description : Logs into the API and gets the current session token.
		# No parameters
		
		# build the login POST request
		data = { "username" : self.api_user, "password" : self.api_pass }
		response = self.api_send_request("POST","/api/admin/login",data)
	
		# try to grab the session token
		try:			
			# set session and request token values on success
			self.api_session_token = response['token'] 
			self.api_request_token = self.api_session_token
			
			# authentication status to true		
			self.object_authentication_status = True
			
			return True
									
		except Exception as e:
			return str(response)
		
	# ADMIN - Get Permanent Session Token - Handle response in wrapper code
	def admin_get_perm_token(self):
		
		# GET /api/admin/permanenttoken
		# Description : Gets the permanent session token, reusable without login. Doesn't change on API restart.
		# No parameters
		
		response = self.api_send_request("GET","/api/admin/permanenttoken?token=" + self.api_request_token,"")
		
		try:
					
			# set session and request token values on success
			self.api_perm_token = response['token'] 
			self.api_request_token = self.api_perm_token

			# authentication status to true		
			self.object_authentication_status = True
			
			return True
			
		except Exception as e:	
			print str(e)
					
	# ADMIN - Restart Empire RESTful API Server
	def admin_restart_restful_api_server(self):
		
		# Handler : GET /api/admin/restart
		# Description : Restarts the RESTful API server.
		# No parameters

		return self.api_send_request("GET","/api/admin/restart?token=" + self.api_request_token,"")
							
	# ADMIN - Shutdown the Empire RESTful API Server
	def admin_shutdown_restful_api_server(self):
		
		# Handler : GET /api/admin/shutdown
		# Description : Shutdown the RESTful API server.
		# No parameters

		return self.api_send_request("GET","/api/admin/shutdown?token=" + self.api_request_token,"")
		
	
	#### API FUNCTIONS ######	
	
	# get the current Empire Version
	def api_config_get_current_version(self):
		
		# Handler : GET /api/version
		# Description : Returns the current Empire version.
		# No parameters
		
		return self.api_send_request("GET","/api/version?token=" + self.api_request_token,"")
	
		
	# API - Get Empire API Configuration Information
	def api_config_info(self):
		
		# Handler : GET /api/config
		# Description : Returns the current Empire configuration.
		# No parameters
		
		return self.api_send_request("GET","/api/config?token=" + self.api_request_token,"")
					
	
	##### LISTENER FUNCTIONS ######
	
	# LISTENERS - Get Current Listeners
	def listeners_get_current_listeners(self):

		# Handler : GET /api/listeners
		# Description : Returns all current Empire listeners.
		# No parameters

		return self.api_send_request("GET","/api/listeners?token=" + self.api_request_token,"")
						
	# LISTENERS - Get Listener Options by Name
	def listeners_get_listener_by_name(self,listener_name):
		
		# Handler : GET /api/listeners/LISTENER_NAME
		# Description : Returns the listener specifed by the name/id LISTENER_NAME.
		# No parameters
		
		return self.api_send_request("GET","/api/listeners/" + listener_name + "?token=" + self.api_request_token,"")
	
	# LISTENERS - Get Current Listener Options
	def listeners_get_current_listener_options(self,listener_type):

		# Handler : GET /api/listeners/options/listener_type
		# Description : Returns the current listener options for the specified type.
		# No parameters
		
		return self.api_send_request("GET","/api/listeners/options/" + listener_type + "?token=" + self.api_request_token,"")
		
	# LISTENERS - Create a Listener
	def listeners_create_listener(self,listener_data,listener_type):
		
		# Handler : POST /api/listeners/listener_type
		# Description : Creates a listener with the specified parameters.
		# Parameters (none required) :
        # Name : name for the listener
        # All required parameters have default values

		return self.api_send_request("POST","/api/listeners/" + listener_type + "?token=" + self.api_request_token,listener_data)

	# LISTENERS - Kill a Listener
	def listeners_kill_listener(self,listener_name):
		
		# Handler : DELETE /api/listeners/LISTENER_NAME
		# Description : Kills the listener specifed by the name/id LISTENER_NAME.
		# No parameters
		
		return self.api_send_request("DELETE","/api/listeners/" + listener_name + "?token=" + self.api_request_token,"")
	
	# LISTENERS - Kill all Listeners
	def listeners_kill_all_listeners(self):
	
		# Handler : DELETE /api/listeners/all
		# Description : Kills all listeners.
		# No parameters
		
		return self.api_send_request("DELETE","/api/listeners/all?token=" + self.api_request_token,"")


	##### STAGERS FUNCTIONS ######
		
	# STAGERS - Get Current Stagers
	def stagers_get_current_stagers(self):
	
		# Handler : GET /api/stagers
		# Description : Returns all current Empire stagers and options.
		# No parameters
	
		return self.api_send_request("GET","/api/stagers?token=" + self.api_request_token,"")
	
	# STAGERS - Get Stager By Name
	def stagers_get_stager_by_name(self,stager_name):
		
		# Handler : GET /api/stagers/STAGER_NAME
		# Description : Returns the Empire stager specified by STAGER_NAME.
		# No parameters
		
		return self.api_send_request("GET","/api/stagers/" + stager_name + "?token=" + self.api_request_token,"")

	# STAGERS - Generate Stager 
	def stagers_generate_stager(self,stager_data):
		
		# Handler : POST /api/stagers
		# Description : Returns the Empire stager specified by parameters.
		# Parameters :
			# StagerName : the stager name to generate (required)
			# Listener : the listener name to generate the stager for (required)
			# additional : any additional stager values enumerated from stager options
		
		return self.api_send_request("POST","/api/stagers?token=" + self.api_request_token,stager_data)


	##### AGENT FUNCTIONS ######
	
	# AGENTS - Get Current Agents
	def agents_get_current_agents(self):
	
		# Handler : GET /api/agents
		# Description : Returns all current Empire agents.
		# No parameters

		return self.api_send_request("GET","/api/agents?token=" + self.api_request_token,"")
	
	# AGENTS - Get Stale Agents
	def agents_get_stale_agents(self):
		
		
		# Handler : GET /api/agents/stale
		# Description : Returns all 'stale' Empire agents (past checkin window).
		# No parameters
		
		return self.api_send_request("GET","/api/agents/stale?token=" + self.api_request_token,"")
		
	# AGENTS - Remove Stale Agents
	def agents_remove_stale_agents(self):
		
		
		# Handler : DELETE /api/agents/stale
		# Description : Removes all 'stale' Empire agents (past checkin window).
		# No parameters

		return self.api_send_request("DELETE","/api/agents/stale?token=" + self.api_request_token,"")
		
	# AGENTS - Get Agent By Name
	def agents_get_agent_by_name(self,agent_name):
		
		# Handler : GET /api/agents/AGENT_NAME
		# Description : Returns the agent specifed by AGENT_NAME.
		# No parameters
		
		return self.api_send_request("GET","/api/agents/" + agent_name + "?token=" + self.api_request_token,"")
		
	# AGENTS - Remove Agent
	def agents_remove_agent(self,agent_name):
		
		# Handler : DELETE /api/agents/AGENT_NAME
		# Description : Removes the agent specifed by AGENT_NAME (doesn't kill first).
		# No parameters
	
		return self.api_send_request("DELETE","/api/agents/" + agent_name + "?token=" + self.api_request_token,"")

	# AGENTS - Task Agent to Run Shell Command
	def agents_task_agent_run_shell_cmd(self,agent_name,command_data):
		
		# Handler : POST /api/agents/AGENT_NAME/shell
		# Description : Tasks the agent specifed by AGENT_NAME to run the given shell command.
		# Parameters :
		#   command : the shell command to task the agent to run (required)
		
		return self.api_send_request("POST","/api/agents/" + agent_name + "/shell?token=" + self.api_request_token,command_data)
	
	# AGENTS - Task All Agents to Run Shell Command 
	def agents_task_all_agents_run_shell_cmd(self,command_data):
		
		# Handler : POST /api/agents/all/shell
		# Description : Tasks all agents to run the given shell command.
		# Parameters :
        #	command : the shell command to task the agents to run (required)

		return self.api_send_request("POST","/api/agents/all/shell?token=" + self.api_request_token,command_data)
	
	# AGENTS - Get Agent Results
	def agents_get_agent_results(self,agent_name):
		
		# Handler : GET /api/agents/AGENT_NAME/results
		# Description : Retrieves results for the agent specifed by AGENT_NAME.
		# No parameters
		
		return self.api_send_request("GET","/api/agents/" + agent_name + "/results?token=" + self.api_request_token,"")

	# AGENTS - Delete Agent Results
	def agents_delete_agent_results(self,agent_name):
		
		# Handler : DELETE /api/agents/AGENT_NAME/results
		# Description : Deletes the result buffer for the agent specifed by AGENT_NAME.
		# No parameters

		return self.api_send_request("DELETE","/api/agents/" + agent_name + "/results?token=" + self.api_request_token,"")

	# AGENTS - Delete All Agent Results
	def agents_delete_all_agent_results(self):
		
		# Handler : DELETE /api/agents/all/results
		# Description : Deletes all agent result buffers
		# No parameters
	
		return self.api_send_request("DELETE","/api/agents/all/results?token=" + self.api_request_token,"")
	
	# AGENTS - Clear QUEUED AGENT TASKING
	def agents_clear_queued_agent_tasking(self,agent_name):
		
		# Handler : POST/GET /api/agents/AGENT_NAME/clear
		# Description : Clears the queued taskings for the agent specified by AGENT_NAME.
		# No parameters

		return self.api_send_request("POST","/api/agents/" + agent_name + "/clear?token=" + self.api_request_token,"")

	# AGENTS - Rename Agent
	def agents_rename_agent(self,agent_name,newname_data):
		
		# Handler : POST/GET /api/agents/AGENT_NAME/rename
		# Description : Renames the agent specified by AGENT_NAME.
		# Parameters :
		#    newname : the name to rename the specified agent to (required)

		return self.api_send_request("POST","/api/agents/" + agent_name + "/rename?token=" + self.api_request_token,newname_data)

	# AGENTS - Kill Agent
	def agents_kill_agent(self,agent_name):
		
		# Handler : POST/GET /api/agents/AGENT_NAME/kill
		# Description : Tasks the agent specified by AGENT_NAME to exit.
		# No parameters

		return self.api_send_request("GET","/api/agents/" + agent_name + "/kill?token=" + self.api_request_token,"")

	# AGENTS - Kill All Agents
	def agents_kill_all_agents(self):
		
		# Handler : POST/GET /api/agents/all/kill
		# Description : Tasks all agents to exit.
		# No parameters
		
		return self.api_send_request("GET","/api/agents/all/kill?token=" + self.api_request_token,"")
	
	
	###### MODULES FUNCTIONS #######
	
	# MODULES - Get Current Modules
	def modules_get_current_modules(self):
		
		# Handler : GET /api/modules
		# Description : Returns all current Empire modules.
		# No parameters

		return self.api_send_request("GET","/api/modules?token=" + self.api_request_token,"")
	
	# MODULES - Get Module by Name
	def modules_get_module_by_name(self,module_name):
		
		# Handler : GET /api/modules/MODULE_NAME
		# Description : Returns the module specified by MODULE_NAME.
		# No parameters
		
		return self.api_send_request("GET","/api/modules/" + module_name + "?token=" + self.api_request_token,"")

	# MODULES - Search for Module
	def modules_search_for_module(self,keyword_data):
		
		# Handler : POST /api/modules/search
		# Description : Searches all module fields for the given term.
		# Parameters (none required) :
		#    term : the term to search for (required)

		return self.api_send_request("POST","/api/modules/search?token=" + self.api_request_token,keyword_data)
	
	# MODULES - Execute a Module
	def modules_execute_module(self,module_name,module_data):
		
		
		# Handler : POST /api/modules/MODULE_NAME
		# Description : Tasks an
		# Parameters (none required) :
		# 	Agent : the agent to task the module for (or all). Required.
		# 	additional : any additional module values enumerated from module options

		return self.api_send_request("POST","/api/modules/" + module_name + "?token=" + self.api_request_token,module_data)
	
	
	#### CREDENTIALS FUNCTIONS ######
	
	# CREDENTIALS - Get Stored Credentials
	def creds_get_stored_credentials(self):
		
		# Handler : GET /api/creds
		# Description : Returns all credentials currently stored in an Empire server.
		# No parameters
		
		return self.api_send_request("GET","/api/creds?token=" + self.api_request_token,"")
	
	
	###### REPORTING FUNCTIONS ######
	
	# REPORTING - Get All Logged Events 
	def reporting_get_all_logged_events(self):
				
		# Handler : GET /api/reporting
		# Description : Returns all logged events.
		# No parameters

		return self.api_send_request("GET","/api/reporting?token=" + self.api_request_token,"")

	# REPORTING - Get Agent Logged Events
	def reporting_get_agent_logged_events(self,agent_name):
		
		# Handler : GET /api/reporting/agent/AGENT_NAME
		# Description : Returns the events for a specified AGENT_NAME
		# No parameters
		
		return self.api_send_request("GET","/api/reporting/agent/" + agent_name + "?token=" + self.api_request_token,"")

	# REPORTING - Get Logged Events of Specific Type
	def reporting_get_logged_events_of_specific_type(self,type_name):

		# Handler : GET /api/reporting/type/MSG_TYPE
		# Description : Returns the events of a specified MSG_TYPE (checkin, task, result).
		# No parameters
		
		return self.api_send_request("GET","/api/reporting/type/" + type_name + "?token=" + self.api_request_token,"")

	# REPORTING - Get Logged Events with Specific Msg
	def reporting_get_logged_events_with_specific_msg(self,msg_value):
		
		# Handler : GET /api/reporting/msg/MSG
		# Description : Returns the events matching a specific MSG.
		# No parameters
		
		return self.api_send_request("GET","/api/reporting/msg/" + msg_value + "?token=" + self.api_request_token,"")
