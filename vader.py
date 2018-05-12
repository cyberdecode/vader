# Vader.py - Tkinter Frontend for Empire Project
# v1.0.3.2018
# @badhackjob

import Tkinter
from Tkinter import *
import ttk
import tkFont
from ScrolledText import ScrolledText
from empire_api_core import empire_api_core
from Queue import Queue
from threading import Thread
import tkMessageBox
import time
import ast
from ast import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# task all shell command class POPUP
class api_task_all_agents_run_shell_popup:
	
	def __init__(self,parent):
	
		top = self.top = Tkinter.Toplevel(parent)
		
		self.task_all_agents_shell_popup_label = Tkinter.Label(self.top, text = "Shell Command: ")
		self.task_all_agents_shell_popup_label.grid(row=0,column=0,sticky=W,padx=10,pady=10)
		
		self.task_all_agents_shell_entry = Tkinter.Entry(self.top,width=40)
		self.task_all_agents_shell_entry.grid(row=0,column=1,sticky=NW,padx=5,pady=5,columnspan=15)
		
		self.task_all_agents_shell_action_button = Tkinter.Button(self.top,text = "Send Command",command=self.send)
		self.task_all_agents_shell_action_button.grid(row=1,column=1,sticky=NW,padx=10,pady=10)
		
		self.task_all_agents_shell_cancel_button = Tkinter.Button(self.top,text = "Cancel", command = self.top.destroy)
		self.task_all_agents_shell_cancel_button.grid(row=1,column=2,sticky=NW,padx=10,pady=10)
	
	def send(self):
		
		self.command = self.task_all_agents_shell_entry.get()
		self.top.destroy()
		
# rename agent class POPUP
class api_rename_agent_popup:
	
	def __init__(self,parent):
	
		top = self.top = Tkinter.Toplevel(parent)
		
		self.rename_agent_label = Tkinter.Label(self.top, text = "New Agent Name: ")
		self.rename_agent_label.grid(row=0,column=0,sticky=W,padx=10,pady=10)
		
		self.rename_agent_entry = Tkinter.Entry(self.top,width=40)
		self.rename_agent_entry.grid(row=0,column=1,sticky=NW,padx=5,pady=5,columnspan=15)
		
		self.rename_agent_action_button = Tkinter.Button(self.top,text = "Rename Agent",command=self.send)
		self.rename_agent_action_button.grid(row=1,column=1,sticky=NW,padx=10,pady=10)
		
		self.rename_agent_cancel_button = Tkinter.Button(self.top,text = "Cancel", command = self.top.destroy)
		self.rename_agent_cancel_button.grid(row=1,column=2,sticky=NW,padx=10,pady=10)
	
	def send(self):
		
		self.new_name = self.rename_agent_entry.get()
		self.top.destroy()

# stagers results window
class stagers_results_window:
	
	def __init__(self,parent,response,launcher,outfile):
		
		# define the window
		top = self.top = Tkinter.Toplevel(parent)
		top.grid_columnconfigure(0,weight=1)
		top.grid_rowconfigure(1,weight=1)
		
		title = Tkinter.Label(self.top,text=launcher + " Output: ")
		title.grid(row=0,column=0,sticky=W)		
		
		# track row position in table
		row_count = 2 
		
		# for key,value in response:
		# we have to do some digging here	
		for key,value in response[launcher].iteritems():
			
			# check if Output, display accordingly
			if key == "Output":
				
				if outfile != "":
				
					try:
						f = open(outfile,"w")
						f.write(str(value))
						f.close()

						scrolltext = ScrolledText(self.top,height=12,width=100)
						scrolltext.config(state="normal")
						scrolltext.grid(row=1,column=0,sticky='NEWS',columnspan=3)
						scrolltext.insert(Tkinter.END,"[*] Stager Output File created at " + outfile)
					
					except Exception as e:
						
						scrolltext = ScrolledText(self.top,height=12,width=100)
						scrolltext.config(state="normal")
						scrolltext.grid(row=1,column=0,sticky='NEWS',columnspan=3)
						scrolltext.insert(Tkinter.END,"[!!] Exception on Outfile create: " + str(e))

				else:
				
					scrolltext = ScrolledText(self.top,height=12,width=100)
					scrolltext.config(state="normal")
					scrolltext.grid(row=1,column=0,sticky='NEWS',columnspan=3)
					scrolltext.insert(Tkinter.END,str(value))
			
				# increment row count
				row_count += 1

	# option to save results to file
	def savefile(self):
		
		file_name = tkFileDialog.asksaveasfile(mode='w',defaultextension=".txt")
		agent_results = self.results
		try:
			file_name.write(agent_results)
			file_name.close()
		except: pass;

# reporting event details window
class reporting_event_details_window:
	
	def __init__(self,parent,data):
	
		# define the window
		top = self.top = Tkinter.Toplevel(parent)
		top.grid_columnconfigure(0,weight=1)
		top.grid_rowconfigure(1,weight=1)
		top.wm_title("Reporting Event Details")
		
		scrolltext = ScrolledText(self.top,height=10,width=60)
		scrolltext.config(state="normal")
		scrolltext.grid(row=0,column=0,sticky='NEWS')
		
		keys = [ "EventType","TimeStamp","TaskID","AgentName","Message","ID" ]
		
		for i in range(0,len(keys)):
			scrolltext.insert(Tkinter.END,keys[i] + ": " + str(data[i]) + "\n")
		
		scrolltext.config(state="disabled")
	
# credentials event details window
class credentials_event_details_window:
	
	def __init__(self,parent,data):
	
		# define the window
		top = self.top = Tkinter.Toplevel(parent)
		top.grid_columnconfigure(0,weight=1)
		top.grid_rowconfigure(1,weight=1)
		top.wm_title("Credential Details")
		
		scrolltext = ScrolledText(self.top,height=10,width=60)
		scrolltext.config(state="normal")
		scrolltext.grid(row=0,column=0,sticky='NEWS')
				
		keys = [ "ID", "UserName", "Domain", "CredType", "Notes", "Host", "SID", "Password", "OS" ]
		
		for i in range(0,len(keys)):
			scrolltext.insert(Tkinter.END,keys[i] + ": " + str(data[i]) + "\n")
		
		scrolltext.config(state="disabled")

# main application classs
class vader:
	
	###### CONSTRUCTOR #####
	def __init__(self):
		
		# empire api core object
		self.eac_object = empire_api_core()
		
		# stager outfile path
		self.stager_outfile_path = ""
		
		# module outfile path
		self.module_outfile_path = ""
		
		# empire version string
		self.empire_version = ""
		
		# reporting by agent name choice dict
		self.reporting_agent_choices = []
		self.reporting_agent_choices.append("")
		
		# selected agent name for option execution
		self.selected_agent_name = ""
		
		# selected module name for option execution
		self.selected_module_name = ""
		
		# define the API Logging Queue
		self.api_log_queue = Queue(maxsize=0)
		
		# define the main form - super parent
		self.form = Tkinter.Tk()
		self.form.wm_title(' Vader.py - v1.0.3.2018 ')
		self.form.resizable(0,0)
		
		###### ACTION TABS FRAME #######
		
		# application tabs notebook, child to the form, parent to the tabs
		self.nb = ttk.Notebook(self.form,height=600,width=1300)
		self.nb.pack(fill=BOTH, expand=True)
		self.nb.pressed_index = None
		
		# define the API frames 
		self.admin_api = Tkinter.Frame(self.nb)
		self.listeners_api = Tkinter.Frame(self.nb)
		self.agents_api = Tkinter.Frame(self.nb)
		self.modules_api = Tkinter.Frame(self.nb)
		self.stagers_api = Tkinter.Frame(self.nb)
		self.creds_api = Tkinter.Frame(self.nb)
		self.report_api = Tkinter.Frame(self.nb)
		
		# pack frames into notebook
		self.admin_api.pack(fill=BOTH, expand=True)
		self.listeners_api.pack(fill=BOTH, expand=True)
		self.agents_api.pack(fill=BOTH, expand=True)
		self.modules_api.pack(fill=BOTH, expand=True)
		self.stagers_api.pack(fill=BOTH, expand=True)
		self.creds_api.pack(fill=BOTH, expand=True)
		self.report_api.pack(fill=BOTH, expand=True)
		
		# add application frames to notebook
		# defines the tab ordering
		self.nb.add(self.admin_api,text='      Admin / API     ')
		self.nb.add(self.listeners_api,text='     Listeners     ',state="disabled")
		self.nb.add(self.stagers_api,text='     Stagers     ',state="disabled")
		self.nb.add(self.agents_api,text='     Agents     ',state="disabled")
		self.nb.add(self.modules_api,text='     Modules     ',state="disabled")
		self.nb.add(self.creds_api,text='     Credentials     ',state="disabled")
		self.nb.add(self.report_api,text='     Reporting     ',state="disabled")
				
		######### API LOG FRAME #################
		self.api_log_textbox = ScrolledText(self.form,height=12)
		self.api_log_textbox.config(bg='black',fg='white',state="disabled")
		self.api_log_textbox.pack(fill=BOTH,expand=YES,padx=5)
							
		######### BUILD APPLICATION ###########
		self.build_api_admin_tab()
		self.build_listeners_tab()	
		self.build_stagers_tab()
		self.build_agents_tab()
		self.build_modules_tab()
		self.build_reporting_tab()
		self.build_credentials_tab()
		
		# start the application
		self.start_application()
		
	# API / ADMIN Tab 
	def build_api_admin_tab(self):
	
		# notebook tab - admin/api
	
		##### AUTHENTICATION INFO FRAME ##############
		# authentication input fields
		self.api_connection_lframe = Tkinter.LabelFrame(self.admin_api)
		self.api_connection_lframe.grid(row=0,column=0,padx=10,pady=5,sticky=NW)
		
		# ------- Username Entry Field ------------ #
		# Define the Username label text
		self.api_username_label = Tkinter.StringVar()	
		self.api_username_label.set("Username: ") 
		
		# Display the Username label - reference label text var
		self.api_username_dlabel = Tkinter.Label(self.api_connection_lframe,textvariable=self.api_username_label)
		self.api_username_dlabel.grid(row=0,column=0,sticky=E)
		
		# Define the Username text entry field
		self.api_username_str = Tkinter.StringVar()
		self.api_username_str.set("empire")
		self.api_username_field = Tkinter.Entry(self.api_connection_lframe,textvariable=self.api_username_str,width=30)
		self.api_username_field.grid(row=0,column=1,sticky=W,padx=5,pady=5,columnspan=2) 
		# ------- Username Entry Field ------------ #
		
		# ------- Password Entry Field ------------ #
		# Define the Password label text
		self.api_password_label = Tkinter.StringVar()	
		self.api_password_label.set("Password: ") 
		
		# Display the Password label - reference label text var
		self.api_password_dlabel = Tkinter.Label(self.api_connection_lframe,textvariable=self.api_password_label)
		self.api_password_dlabel.grid(row=1,column=0,sticky=E)
		
		# Define the Password text entry field
		self.api_password_str = Tkinter.StringVar()
		self.api_password_str.set("empire")
		self.api_password_field = Tkinter.Entry(self.api_connection_lframe,textvariable=self.api_password_str,width=30,show="*")
		self.api_password_field.grid(row=1,column=1,sticky=W,padx=5,pady=5,columnspan=2) 
		# ------- Password Entry Field ------------ #
			
		# ------- Host Entry Field ------------ #
		# Define the Host label text
		self.api_host_label = Tkinter.StringVar()	
		self.api_host_label.set("Host / IP: ") 
		
		# Display the Host label - reference label text var
		self.api_host_dlabel = Tkinter.Label(self.api_connection_lframe,textvariable=self.api_host_label)
		self.api_host_dlabel.grid(row=2,column=0,sticky=E)
		
		# Define the Host text entry field
		self.api_host_str = Tkinter.StringVar()
		self.api_host_str.set("127.0.0.1")
		self.api_host_field = Tkinter.Entry(self.api_connection_lframe,textvariable=self.api_host_str,width=30)
		self.api_host_field.grid(row=2,column=1,sticky=W,padx=5,pady=5,columnspan=2) 
		# ------- Host Entry Field ------------ #
		
		
		# ------- Port Entry Field ------------ #
		# Define the Port label text
		self.api_port_label = Tkinter.StringVar()	
		self.api_port_label.set("Port: ") 
		
		# Display the Port label - reference label text var
		self.api_port_dlabel = Tkinter.Label(self.api_connection_lframe,textvariable=self.api_port_label)
		self.api_port_dlabel.grid(row=3,column=0,sticky=E)
		
		# Define the Port text entry field
		self.api_port_str = Tkinter.StringVar()
		self.api_port_str.set("1337")
		self.api_port_field = Tkinter.Entry(self.api_connection_lframe,textvariable=self.api_port_str,width=10)
		self.api_port_field = Tkinter.Entry(self.api_connection_lframe,textvariable=self.api_port_str,width=10)
		self.api_port_field.grid(row=3,column=1,sticky=W,padx=5,pady=5) 
		# ------- Port Entry Field ------------ #
		
		# Get Session Token
		self.api_action_get_session_button = Tkinter.Button(self.api_connection_lframe,text="Access the Empire",command=self.api_get_session)
		self.api_action_get_session_button.config(fg='white',bg='blue',font=('arial','10','bold'))
		self.api_action_get_session_button.grid(row=3,column=2,sticky=W,padx=5,pady=5)
				
		##### CONNECTION INFO FRAME ##############
		
		##### API BUTTON FRAME ##############
		self.api_action_lframe = Tkinter.LabelFrame(self.admin_api)
		self.api_action_lframe.grid(row=0,column=1,padx=10,pady=5,sticky=NW)
		
		# Get Permanent Session Token
		self.api_action_get_perm_session_button = Tkinter.Button(self.api_action_lframe,text="Get Permanent Token",command=self.api_get_perm_session)
		self.api_action_get_perm_session_button.config(state="disabled",fg='white',bg='slate gray',font=('arial','10','bold'))
		self.api_action_get_perm_session_button.grid(row=1,column=0,sticky=W,padx=5,pady=5)
		
		# Restart RESTful API Server
		self.api_action_restart_api_button = Tkinter.Button(self.api_action_lframe,text="Restart API Server",command=self.api_restart_api_server)
		self.api_action_restart_api_button.config(state="disabled",fg='white',bg='slate gray',font=('arial','10','bold'))
		self.api_action_restart_api_button.grid(row=2,column=0,sticky=W,padx=5,pady=5)
		
		# Shutdown RESTful API Server
		self.api_action_shutdown_api_button = Tkinter.Button(self.api_action_lframe,text="Shutdown API Server",command=self.api_shutdown_api_server)
		self.api_action_shutdown_api_button.config(state="disabled",fg='white',bg='slate gray',font=('arial','10','bold'))
		self.api_action_shutdown_api_button.grid(row=3,column=0,sticky=W,padx=5,pady=5)
		
		##### API ACTION FRAME ##############

		######## API CONFIG INFO FRAME #############
		self.api_config_lframe = Tkinter.LabelFrame(self.admin_api)
		self.api_config_lframe.grid(row=1,column=0,columnspan=2,padx=10,pady=5,sticky=NW)
		
		self.api_config_textbox = ScrolledText(self.api_config_lframe,width=75,height=12)
		self.api_config_textbox.config(bg='ghost white',state="disabled")
		self.api_config_textbox.grid(row=0,column=0,sticky='W',columnspan=2)
		
		# ------- Request Session Tokem ------------ #
		# Define the Request Session Token label text
		self.api_request_session_token_label = Tkinter.StringVar()	
		self.api_request_session_token_label.set("Request Token: ") 
		
		# Display the Request Session Token label - reference label text var
		self.api_request_session_token_dlabel = Tkinter.Label(self.api_config_lframe,textvariable=self.api_request_session_token_label)
		self.api_request_session_token_dlabel.grid(row=1,column=0,sticky=E,pady=5)
		
		# Define the Request Session Token field
		self.api_request_token_str = Tkinter.StringVar()
		self.api_request_token_str.set("")
		self.api_request_token_field = Tkinter.Entry(self.api_config_lframe,textvariable=self.api_request_token_str,width=45)
		self.api_request_token_field.grid(row=1,column=1,sticky=W)
		self.api_request_token_field.config(state="readonly") 
				
	# LISTENERS Tab 
	def build_listeners_tab(self):
		
		# notebook tab - listeners
	
		##### LISTENER TYPE SELECTION FRAME ##############
		
		self.listener_options_lframe = Tkinter.LabelFrame(self.listeners_api)
		self.listener_options_lframe.grid(row=0,column=0,padx=5,pady=5,sticky=NW)
		
		# LISTENER TYPES LISTBOX
		self.listener_type_treeview = ttk.Treeview(self.listener_options_lframe,height=8,selectmode="extended")
		self.listener_type_treeview.column("#0",minwidth="0",width="250")
		self.listener_type_treeview.heading("#0",text="     Listener Types:     ")
		
		# Add Listener Types
		self.listener_type_treeview.insert("","end", text="dbx")
		self.listener_type_treeview.insert("","end", text="http")
		self.listener_type_treeview.insert("","end", text="http_com")
		self.listener_type_treeview.insert("","end", text="http_foreign")
		self.listener_type_treeview.insert("","end", text="http_hop")
		self.listener_type_treeview.insert("","end", text="meterpreter")
		self.listener_type_treeview.insert("","end", text="redirector")
			
		# Bind to Action
		self.listener_type_treeview.bind("<Double-1>", self.api_get_listener_type_options)
		self.listener_type_treeview.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
		
		###### List ALL LISTENERS ############
		self.listener_all_treeview = ttk.Treeview(self.listener_options_lframe,height=7)
		self.listener_all_treeview.heading("#0",text="     Current Listeners:     ")
		self.listener_all_treeview.column("#0",minwidth="0",width="250")
		
		# Bind to Action
		self.listener_all_treeview.bind("<Double-1>", self.api_get_listener_by_name)
		self.listener_all_treeview.grid(row=2,column=0,sticky=NW,padx=5,pady=5)
		
		
		# ---------- Refresh Button----------#
		self.listener_refresh_button = Tkinter.Button(self.listener_options_lframe,text="  Refresh List  ",command=self.api_get_current_listeners)
		self.listener_refresh_button.config(state="normal",fg='white',bg='slate gray',font=('arial','10','bold'))
		self.listener_refresh_button.grid(row=3,column=0,sticky=N,padx=5,pady=5)
		
		###### LISTENER OPTIONS ENTRY FRAME - DYNAMIC ############
		
		self.listener_type_dynamic_lframe = Tkinter.Frame(self.listeners_api)
		self.listener_type_dynamic_lframe.grid(row=0,column=1,sticky=NE,rowspan=3)

		# Build the listeners API Canvas and Scroll
		self.listeners_api_canvas = Canvas(self.listener_type_dynamic_lframe,width=1010, height=600)
		self.listeners_api_scroll = Scrollbar(self.listener_type_dynamic_lframe, command=self.listeners_api_canvas.yview)
		self.listeners_api_canvas.config(yscrollcommand=self.listeners_api_scroll.set, scrollregion=(0,0,100,2000))
		self.listeners_api_canvas.pack(side=LEFT, fill=BOTH, expand=True)
		self.listeners_api_scroll.pack(side=RIGHT, fill=Y)
		
	# STAGERS Tab
	def build_stagers_tab(self):
	
		##### STAGERS TYPE SELECTION FRAME ##############
		
		self.stagers_options_lframe = Tkinter.LabelFrame(self.stagers_api)
		self.stagers_options_lframe.grid(row=0,column=0,padx=5,pady=5,sticky=NW)
	
		###### List ALL STAGERS ############
		self.stagers_all_treeview = ttk.Treeview(self.stagers_options_lframe,height=18)
		self.stagers_all_treeview.heading("#0",text="     Stagers:     ")
		self.stagers_all_treeview.column("#0",minwidth="0",width="250")

		# Bind to Action
		self.stagers_all_treeview.bind("<Double-1>", self.api_get_stager_by_name)
		self.stagers_all_treeview.grid(row=0,column=0,sticky=NW,padx=5,pady=5)

		
		###### STAGERS OPTIONS ENTRY FRAME - DYNAMIC ############
		
		self.stager_type_dynamic_lframe = Tkinter.Frame(self.stagers_api)
		self.stager_type_dynamic_lframe.grid(row=0,column=1,sticky=NE)

		# Build the stagers API Canvas and Scroll
		self.stagers_api_canvas = Canvas(self.stager_type_dynamic_lframe,width=1010, height=600)
		self.stagers_api_scroll = Scrollbar(self.stager_type_dynamic_lframe, command=self.stagers_api_canvas.yview)
		self.stagers_api_canvas.config(yscrollcommand=self.stagers_api_scroll.set, scrollregion=(0,0,100,2000))
		self.stagers_api_canvas.pack(side=LEFT, fill=BOTH, expand=True)
		self.stagers_api_scroll.pack(side=RIGHT, fill=Y)
		
	# AGENTS Tab
	def build_agents_tab(self):
		
		##### agents TYPE SELECTION FRAME ##############
		self.agents_current_options_lframe = Tkinter.LabelFrame(self.agents_api)
		self.agents_current_options_lframe.grid(row=0,column=0,padx=5,pady=5,sticky=NW)
		
		###### List CURRENT AGENTS ############
		self.agents_current_treeview = ttk.Treeview(self.agents_current_options_lframe,height=8)
		self.agents_current_treeview.heading("#0",text="     Current Agents:     ")
		
		# Bind to Action and Grid
		self.agents_current_treeview.bind("<Double-1>", self.api_get_agent_by_name)
		self.agents_current_treeview.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
		
		# ---------- Refresh Current Agents----------#
		self.agents_current_refresh_button = Tkinter.Button(self.agents_current_options_lframe,text="  Refresh List  ",command=self.api_get_current_agents)
		self.agents_current_refresh_button.config(fg='white',bg='slate gray',font=('arial','10','bold'))
		self.agents_current_refresh_button.grid(row=1,column=0,sticky=N,padx=5,pady=5)
		
		###### List STALE AGENTS ############
		self.agents_stale_treeview = ttk.Treeview(self.agents_current_options_lframe,height=5)
		self.agents_stale_treeview.heading("#0",text="     Stale Agents:     ")
		self.agents_stale_treeview.grid(row=3,column=0,sticky=NW,padx=5,pady=5)
		
		# ---------- Remove Stale Agents----------#
		self.agents_stale_remove_button = Tkinter.Button(self.agents_current_options_lframe,text="  Remove Stale Agents  ",command=self.api_get_remove_stale_agents)
		self.agents_stale_remove_button.config(fg='white',bg='slate gray',font=('arial','10','bold'))
		self.agents_stale_remove_button.grid(row=4,column=0,sticky=N,padx=5,pady=5)
		
		###### AGENTS INFO / ACTION FRAME - DYNAMIC ############
		self.agent_info_action_lframe = Tkinter.Frame(self.agents_api)
		self.agent_info_action_lframe.grid(row=0,column=1,padx=15,pady=5,sticky=NW)
	
	# MODULES Tab
	def build_modules_tab(self):
		
		##### modules TYPE SELECTION FRAME ##############
		
		self.modules_options_lframe = Tkinter.LabelFrame(self.modules_api)
		self.modules_options_lframe.grid(row=0,column=0,padx=5,pady=5,sticky=NW,rowspan=2)
	
		###### List ALL modules ############
		self.modules_all_treeview = ttk.Treeview(self.modules_options_lframe,height=20)
		self.modules_all_treeview.heading("#0",text="     Modules:     ")
		self.modules_all_treeview.column("#0",minwidth="0",width="540")

		# Bind to Action
		self.modules_all_treeview.bind("<Double-1>", self.api_get_module_by_name)
		self.modules_all_treeview.grid(row=0,column=0,sticky=NW,padx=5,pady=5,rowspan=2,columnspan=10)
		
		# search entry and search button
		self.modules_search_str = Tkinter.StringVar()
		self.modules_search_field = Tkinter.Entry(self.modules_options_lframe,textvariable=self.modules_search_str,width=25)
		self.modules_search_field.grid(row=2,column=0,sticky=W,padx=5,pady=5) 
		
		self.modules_search_button = Tkinter.Button(self.modules_options_lframe,text="Search Modules",command=self.api_search_for_module)
		self.modules_search_button.config(fg='white',bg='slate gray',font=('arial','10','bold'))
		self.modules_search_button.grid(row=2,column=1,sticky=W,padx=5,pady=5)
		
		# view all modules button
		self.modules_view_all_button = Tkinter.Button(self.modules_options_lframe,text="View All",command=self.api_get_current_modules)
		self.modules_view_all_button.config(fg='white',bg='slate gray',font=('arial','10','bold'))
		self.modules_view_all_button.grid(row=2,column=2,sticky=W,padx=5,pady=5)
		
		###### modules OPTIONS ENTRY FRAME - DYNAMIC ############
		
		# options frame for entry
		self.modules_type_dynamic_frame = Tkinter.Frame(self.modules_api)
		self.modules_type_dynamic_frame.grid(row=0,column=1,sticky=NE)
		
		# Build the modules API Canvas and Scroll
		self.modules_api_canvas = Canvas(self.modules_type_dynamic_frame,width=720, height=600)
		self.modules_api_scroll = Scrollbar(self.modules_type_dynamic_frame, command=self.modules_api_canvas.yview)
		self.modules_api_canvas.config(yscrollcommand=self.modules_api_scroll.set, scrollregion=(0,0,100,2000))
		self.modules_api_canvas.pack(side=LEFT, fill=BOTH, expand=True)
		self.modules_api_scroll.pack(side=RIGHT, fill=Y)
		
	# REPORTING tab
	def build_reporting_tab(self):
			
		# delete all childitems on reload
		# clear the frame
		try:
			for child in self.report_api.winfo_children():
				child.destroy()
		except:
			pass
		
		##### REPORTING OUTPUT ##############
		
		self.reporting_output_lframe = Tkinter.LabelFrame(self.report_api)
		self.reporting_output_lframe.grid(row=0,column=0,padx=5,pady=5,sticky='nw')
		
		# ---------- Request Events----------#
		reporting_request_button = Tkinter.Button(self.reporting_output_lframe,text="  Request Events  ",command=self.reporting_display_output)
		reporting_request_button.config(fg='white',bg='blue',font=('arial','10','bold'))
		reporting_request_button.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
		
		cols = [ "EventType", "TimeStamp", "TaskID", "AgentName", "Message", "ID" ]

		self.reporting_tree = ttk.Treeview(self.reporting_output_lframe, columns=cols, show="headings",height="23")
		self.reporting_tree.bind("<Double-1>", self.misc_reporting_display_event_details)
		
		for c in cols:
			self.reporting_tree.heading(c, text=str(c), command=lambda x=c: self.misc_col_sort(self.reporting_tree, x, 0) )
			self.reporting_tree.column(c, width=tkFont.Font().measure(c.title() + " " * 28))
		
		self.reporting_tree.grid(row=1,column=0,padx=5,pady=5)
	
	# CREDENTIALS tab
	def build_credentials_tab(self):
		
		# creds main frame
		self.creds_output_lframe = Tkinter.LabelFrame(self.creds_api)
		self.creds_output_lframe.grid(row=0,column=0,padx=10,pady=10,sticky=NW)
		
		# refresh button
		self.creds_refresh_button = Button(self.creds_output_lframe,text="Refresh Credentials",command=self.api_get_stored_credentials)
		self.creds_refresh_button.config(fg='white',bg='slate gray',font=('arial','10','bold'))
		self.creds_refresh_button.grid(row=0,column=0,padx=5,pady=5,sticky=NW)
		
		# label info
		self.creds_label_info = Label(self.creds_output_lframe,text="* Double-click Credential row to view details in separate window.")
		self.creds_label_info.grid(row=0,column=1,padx=5,pady=5,sticky=W)
		
		# build creds treeview
		cols = [ "username", "domain", "credtype", "notes", "host", "sid", "password", "os", "id" ]
		
		self.creds_tree = ttk.Treeview(self.creds_output_lframe, columns=cols, show="headings",height="23")
		self.creds_tree.bind("<Double-1>", self.misc_creds_display_event_details)
		
		for c in cols:
			self.creds_tree.heading(c, text=str(c), command=lambda x=c: self.misc_col_sort(self.creds_tree, x, 0))
			self.creds_tree.column(c, width=tkFont.Font().measure(c.title() + " " * 18))
		
		self.creds_tree.grid(row=1,column=0,padx=2,pady=2,columnspan=20)
		
	####### ADMIN FUNCTIONS ###########
	
	# get session token
	def api_get_session(self): 
		
		# validate and set authentication form fields
		if self.error_check_api_auth_fields():
			
			# get session token request successful (True)
			response = self.eac_object.admin_get_session_token()
			
			# authentication successful
			if response == True:
							
				# set the request token field
				self.api_request_token_str.set(self.eac_object.api_request_token)
				
				# get the api server configuration
				try:
					response = self.eac_object.api_config_info()
					self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
					
					# clear the config textarea
					self.api_config_textbox.config(state="normal")
					self.api_config_textbox.delete(1.0,Tkinter.END)
					self.api_config_textbox.config(state="disabled")
				
					# write to the config scrolledtext window root
					for item in response['config']:
						
						for key,value in item.iteritems():
							self.api_config_textbox.config(state="normal")
							
							# mask password value
							if str(key).upper() == "API_PASSWORD":
								self.api_config_textbox.insert(Tkinter.END,str(key).upper() + " : " + "**************" + "\n")
							else:
								self.api_config_textbox.insert(Tkinter.END,str(key).upper() + " : " + str(value) + "\n")
								
							self.api_config_textbox.see(Tkinter.END)
							self.api_config_textbox.config(state="disabled")				
				
				except Exception as e:
					tkMessageBox.showerror("ERROR","API Configuration Request Failed - " + str(e))
				
				# enable additional Admin / API Actions
				# ------------------------------------- #
				self.api_action_get_perm_session_button.config(state="normal")
				self.api_action_restart_api_button.config(state="normal")
				self.api_action_shutdown_api_button.config(state="normal")
				
				# enable additional application tabs
				# ------------------------------------- #
				try:
					self.nb.tab(self.listeners_api,state="normal")
					self.nb.tab(self.agents_api,state="normal")
					self.nb.tab(self.modules_api,state="normal")
					self.nb.tab(self.stagers_api,state="normal")
					self.nb.tab(self.creds_api,state="normal")
					self.nb.tab(self.report_api,state="normal")
					
					# build application selection lists 
					# -----------------------------#
					self.api_get_current_listeners()
					self.api_get_current_stagers()
					self.api_get_current_agents()
					self.api_get_current_modules()
					self.api_get_stored_credentials()
					
				except Exception as e:
					tkMessageBox.showerror("ERROR","Error enabling additional application tabs and function calls: " + str(e))
				
				# start the API Logging Threads
				self.api_log_update_thread = Thread(target=self.api_thread_update_queue,args=(self.api_log_queue,))
				self.api_log_update_thread.setDaemon(True)
				self.api_log_update_thread.start()
				
				self.api_log_display_thread = Thread(target=self.api_thread_display_queue)
				self.api_log_display_thread.setDaemon(True)
				self.api_log_display_thread.start()
				
			else:
				tkMessageBox.showerror("ERROR","Unable to retrieve Session Token with provided authentication info:" + response)
				
	# get permanent token
	def api_get_perm_session(self):
		
		# get the permanent token
		if self.eac_object.admin_get_perm_token():
			
			# set the request token field
			self.api_request_token_str.set(self.eac_object.api_request_token)
		
		# log the request
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
	# restart the api server
	def api_restart_api_server(self):
	
		if tkMessageBox.askyesno("Restart API","Are you sure you want to restart the API?"):
	
			# restart api server call
			response = self.eac_object.admin_restart_restful_api_server()
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")

			# restart success
			if response['success']:	
				pass
			else:
				tkMessageBox.showerror("ERROR","Empire RESTful API Server restart FAILED.")
		
	# shutdown the api server
	def api_shutdown_api_server(self):
		
		if tkMessageBox.askyesno("Shutdown API","Are you sure you want to shutdown the API?"):
		
			# shutdown api server call
			response = self.eac_object.admin_shutdown_restful_api_server()
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")

			try:
				# shutdown success
				if response['success']:	
					
					# disable additional Admin / API Actions
					# ------------------------------------- #
					self.api_action_get_perm_session_button.config(state="disabled")
					self.api_action_restart_api_button.config(state="disabled")
					self.api_action_shutdown_api_button.config(state="disabled")				
					
					# clear the config textarea
					self.api_config_textbox.config(state="normal")
					self.api_config_textbox.delete(1.0,Tkinter.END)
					self.api_config_textbox.config(state="disabled")
					
					
					# disable additional application tabs
					# ------------------------------------- #
					self.nb.tab(self.listeners_api,state="disabled")
					self.nb.tab(self.agents_api,state="disabled")
					self.nb.tab(self.modules_api,state="disabled")
					self.nb.tab(self.stagers_api,state="disabled")
					self.nb.tab(self.creds_api,state="disabled")
					self.nb.tab(self.report_api,state="disabled")
					
					# set the request token field
					self.api_request_token_str.set("")
					return
			
				# shutdown failed		
				else:
					tkMessageBox.showerror("ERROR","Empire RESTful API Server shutdown FAILED.")
					return
			
			except Exception as e:
				tkMessageBox.showerror("ERROR","Error occurred processing shutdown: " + str(e))
	
	
	##### LISTENER FUNCTIONS ########
		
	# get listener by name
	def api_get_listener_by_name(self,event):
		
		# get the selected item
		try:
			self.selected_listener = self.listener_all_treeview.selection()[0]
			listener_name =  str(self.listener_all_treeview.item(self.selected_listener,"text"))
			
		except Exception as e:
			tkMessageBox.showerror("ERROR","An error has occurred defining selected listener - "  + str(e))
			
			return
			
		# call to the api with listener name
		response = self.eac_object.listeners_get_listener_by_name(listener_name)
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
		# parsing was successful
		try:
		
			# clear the canvas
			try:
				for child in self.listeners_api_canvas.winfo_children():
					child.destroy()
			except:
				pass
			
			# build temporary frame
			# define the temp labelframe
			self.temp_labelframe = Tkinter.LabelFrame(self.listeners_api_canvas)
			self.listeners_api_canvas.create_window(0,10,window=self.temp_labelframe,anchor=NW)
					
			# display the kill listener and kill all listeners buttons
			# ---------- Kill Listener Button----------#
			listener_kill_button = Tkinter.Button(self.temp_labelframe,text="Kill Listener",command=self.api_delete_kill_listener)
			listener_kill_button.config(fg='white',bg='slate gray',font=('arial','10','bold'))
			listener_kill_button.grid(row=0,column=1,sticky=NW,padx=2,pady=2)
			
			# ---------- Kill All Listener Button----------#
			listener_kill_all_button = Tkinter.Button(self.temp_labelframe,text="Kill All Listeners",command=self.api_delete_kill_all_listeners)
			listener_kill_all_button.config(fg='white',bg='slate gray',font=('arial','10','bold'))
			listener_kill_all_button.grid(row=0,column=2,sticky=NW,padx=2,pady=2)
		
			# track the row count for placement
			row_count = 1
						
			# create the dynamic form - readonly state
			
			for item in response['listeners']:
				
				for key,value in item.iteritems():   
				
					# regular key value print
					if (key == "listener_type") or \
					   (key == "name") or \
					   (key == "listener_category") or \
					   (key == "module") or \
					   (key == "ID"):
					
						# Option Name
						self.option_name_str = Tkinter.StringVar()
						self.option_name_str.set(key)
						self.option_name_dlabel = Tkinter.Label(self.temp_labelframe,textvariable=self.option_name_str,justify=LEFT)
						self.option_name_dlabel.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
					
						# Option Field Value
						self.option_field_str = Tkinter.StringVar()
						self.option_field_str.set(value)
						self.option_entry_field = Tkinter.Entry(self.temp_labelframe,textvariable=self.option_field_str,width=40)
						self.option_entry_field.config(state="disabled",disabledbackground='ghost white',disabledforeground='black')
						self.option_entry_field.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
						
						# increment the row count
						row_count += 1
					
					# check if options key
					# iterate thru dictionaries in options value
					# style fields based on requirements	
					
					elif (key == "options"):
						
						# we need to do some digging					
						for key2,val2 in value.iteritems():
							
							for key3,val3 in val2.iteritems():
							
								if key3 == "Description":
									description_str = val3
																					
								elif key3 == "Value":
									value_str = val3
			
							# Option Name
							self.option_name_str = Tkinter.StringVar()
							self.option_name_str.set(key2)
							self.option_name_dlabel = Tkinter.Label(self.temp_labelframe,textvariable=self.option_name_str,justify=LEFT)
							self.option_name_dlabel.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
		
							# Option Field
							self.option_field_str = Tkinter.StringVar()
							self.option_field_str.set(str(value_str))
							self.option_entry_field = Tkinter.Entry(self.temp_labelframe,textvariable=self.option_field_str,width=40)
							self.option_entry_field.config(state="disabled",disabledbackground='ghost white',disabledforeground='black')
							self.option_entry_field.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
							
							# Option Description
							self.option_description_str = Tkinter.StringVar()
							self.option_description_str.set(str(description_str))
							self.option_description_dlabel = Tkinter.Label(self.temp_labelframe,textvariable=self.option_description_str,wraplength=500,justify=LEFT)
							self.option_description_dlabel.grid(row=row_count,column=3,sticky=W,padx=2,pady=2)
							
							# increment the row count
							row_count += 1			
		
		# parsing json failed
		except Exception as e:
			tkMessageBox.showerror("ERROR","Error parsing Get Listener by Name - " + str(e))
						
	# get current listeners
	def api_get_current_listeners(self):
		
		# Get All current Listeners
		response = self.eac_object.listeners_get_current_listeners()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
		# temp list of listener names
		holder = []
		
		try:
			
			for item in response['listeners']:
				
				holder.append(item['name'])
				holder.sort()
			
			# clear the treeview
			self.listener_all_treeview.delete(*self.listener_all_treeview.get_children())
			
			# populate treeview
			for l in holder:
				self.listener_all_treeview.insert("","end", text=str(l))
		
		except Exception as e:
			
			tkMessageBox.showerror("ERROR","Unable to parse response from Current Listeners: " + str(e))
			
	# get listener options and display
	def api_get_listener_type_options(self,event):
		
		try:
			# get the selected item
			self.selected_item = self.listener_type_treeview.selection()[0]
		except:
			return
		
		# call to api function with selected listener type, return json
		response = self.eac_object.listeners_get_current_listener_options(str(self.listener_type_treeview.item(self.selected_item,"text")))
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
		# parsing was successful
		try:
			
			# try to destory previous temp_labelframe if it exists
			try:
				for child in self.listeners_api_canvas.winfo_children():
					child.destroy()
			except:
				pass

			
			# define the temp labelframe
			self.temp_labelframe = Tkinter.LabelFrame(self.listeners_api_canvas)
			self.listeners_api_canvas.create_window(0,10,window=self.temp_labelframe,anchor=NW)
						
			# ---------- Create Button----------#
			listener_create_action_button = Tkinter.Button(self.temp_labelframe,text="Create Listener",command=self.api_post_create_listener)
			listener_create_action_button.config(fg='white',bg='blue',font=('arial','10','bold'))
			listener_create_action_button.grid(row=0,column=1,sticky=NW,padx=2,pady=2)
					
			# track the row count for placement (account for button, row =1)
			row_count = 1
			column_count = 0
						
			# create the dynamic form
			
			# track all key name values
			self.temp_keys_list = []
			
			# track all required key name values
			self.temp_reqd_keys_list = []
			
			for key,value in response['listeneroptions'].iteritems():
				
				# append to temp keys list
				self.temp_keys_list.append(key)
				
				# grab dictionary values				
				for key2,value2 in value.iteritems():
					
					if key2 == "Description":
						description_str = value2
					
					elif key2 == "Required":
						required_bool = value2
					
					elif key2 == "Value":
						val = value2
	
				# Option Name
				name_label = Tkinter.Label(self.temp_labelframe,text=str(key),justify=LEFT)
				name_label.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
								
				
	 			# check if field required
	 			# if so, append to reqd keys name list and change entry bgcolor
	 			if required_bool:
					
					# append key name to reqd key name lsit
					self.temp_reqd_keys_list.append(key)
				
					# Option Field
					temp_field_str = Tkinter.StringVar()
					temp_field_str.set(str(val))
					
					option_field = Tkinter.Entry(self.temp_labelframe,textvariable=temp_field_str,width=40)
					option_field.grid(row=row_count,column=1,sticky=W,padx=2,pady=2)
					option_field.config(background="wheat") 
					
				else:
					temp_field_str = Tkinter.StringVar()
					temp_field_str.set(str(val))
					entry_field = Tkinter.Entry(self.temp_labelframe,textvariable=temp_field_str,width=40)
					entry_field.grid(row=row_count,column=1,sticky=W,padx=2,pady=2) 
	 				 			
				# Option Description
				description_label = Tkinter.Label(self.temp_labelframe,text=str(description_str),wraplength=500,justify=LEFT)
				description_label.grid(row=row_count,column=2,sticky=W,padx=2,pady=2)
	
				
				# increment the row count
				row_count += 1
				
			
		# parsing json failed
		except Exception as e:
			
			tkMessageBox.showerror("ERROR","Get Listener Type parse failed - " + str(e))
			
	# create new listener
	def api_post_create_listener(self):
	
		# grab all child item values from listener type frame
		try:
			
			# temp list holding values
			vals = []
			
			# for each child item within the frame (dynamic, depends on options for selected listener type)
			for i in range(0,len(self.temp_labelframe.winfo_children())):
				
				# grab value and append to temp values list
				try:
					vals.append(str(self.temp_labelframe.winfo_children()[i].get()).strip())
				
				# appending values to vals[] failed
				except Exception as e:
					
					# do nothing if you cant get it
					pass
		
		# grabbing child item values failed				
		except Exception as e:
			
			tkMessageBox.showerror("ERROR","Grabbing child items failed on Create Listener - " + str(e))
			return
		
		# check if value list is same size as temp keys list for listener type selected
		if len(vals) == len(self.temp_keys_list):
			
			# temp dictionary for the JSON data
			temp_dict = {}
			
			# build the dictionary with key->value pairs for listener type options
			for i in range(0,len(vals)):
				
				# check if option is required, and if blank
				# if so, error out and stop
				if (self.temp_keys_list[i] in self.temp_reqd_keys_list) and (vals[i] == ""):
					
					# display pop error message
					tkMessageBox.showerror("Required Field Missing","Please enter a value for: " + str(self.temp_keys_list[i]))
					
					return
				
				elif (self.temp_keys_list[i] == "CertPath") and (vals[i] == ""):
					continue
				
				# required fields met, append to dictionary
				else:
					temp_dict[self.temp_keys_list[i]] = str(vals[i]).strip()
			

			# -- Send the Create Listener Command --- #
			self.eac_object.listeners_create_listener(temp_dict,str(self.listener_type_treeview.item(self.selected_item,"text")))
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			# Refresh the current listeners list
			self.api_get_current_listeners()
											
	# kill a listener
	def api_delete_kill_listener(self):
		
		# confirm they want to kill listener
		if tkMessageBox.askyesno("Confirm Kill Listener","Are you sure you want to kill the Listener?"):
		
			# get the listener name
			listener_name = str(self.listener_all_treeview.item(self.selected_listener,"text"))
			
			# call to the api with listener name
			response = self.eac_object.listeners_kill_listener(listener_name)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			try:
			
				if response['success']:
					
					# clear the temporary frame with deleted listener
					# try to destory previous temp_labelframe if it exists
					try:
						for child in self.listeners_api_canvas.winfo_children():
							child.destroy()
					except:
						pass
						
					# Refresh the current listeners list
					self.api_get_current_listeners()
					
					
			except Exception as e:
				tkMessageBox.showerror("ERROR","Kill Listener failed - " + str(e))
	
	# kill all listeners
	def api_delete_kill_all_listeners(self):
		
		# confirm they want to kill all listeners
		if tkMessageBox.askyesno("Confirm Kill All Listeners","Are you sure you want to kill All Listeners?"):
		
			# call to the api 
			response = self.eac_object.listeners_kill_all_listeners()
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			try:
			
				if response['success']:
					
					# clear the temporary frame with deleted listener
					# try to destory previous temp_labelframe if it exists
					try:
						for child in self.listeners_api_canvas.winfo_children():
							child.destroy()
					except:
						pass
						
					# Refresh the current listeners list
					self.api_get_current_listeners()
					
			except Exception as e:
				tkMessageBox.showerror("ERROR","Kill All Listeners failed - " + str(e))
	
		
	###### STAGERS FUNCTIONS ##########
	
	# get current stagers
	def api_get_current_stagers(self):
	
		# call to api function
		response = self.eac_object.stagers_get_current_stagers()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
		try:
			
			# holds name values returned
			holder = []
			
			# grab the name values, append to holder then sort
			for item in response['stagers']:
				holder.append(item['Name'])
			holder.sort()
			
			# clear the treeview
			self.stagers_all_treeview.delete(*self.stagers_all_treeview.get_children())
			
			# for names in holder, add to listobx
			for n in holder:
				self.stagers_all_treeview.insert("","end", text=str(n))

		except Exception as e:
			tkMessageBox.showerror("ERROR","Get Current Stagers failed: " + str(e))
			return
			
	# get stager by name
	def api_get_stager_by_name(self,event):
		
		# Global Lister Option Field Str
		self.option_listener_field_str = Tkinter.StringVar()
		
		# get the selected item
		try:
			self.selected_stager = self.stagers_all_treeview.selection()[0]
			stager_name =  str(self.stagers_all_treeview.item(self.selected_stager,"text"))
			
		except Exception as e:
			tkMessageBox.showerror("ERROR","Exception getting the selected Stager by Name: " + str(e))
			return
				
		# call to the api with stager name
		response = self.eac_object.stagers_get_stager_by_name(stager_name)
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
	
		try:
			
			# clear the frame
			try:
				for child in self.stagers_api_canvas.winfo_children():
					child.destroy()
			except:
				pass
			
			# define the core frame
			# required to hold the multiple dynamic labelframes in the canvas
			self.temp_stagers_dynamic_coreframe = Tkinter.Frame(self.stagers_api_canvas)
			self.stagers_api_canvas.create_window(0,10,window=self.temp_stagers_dynamic_coreframe,anchor=NW)
			
			# build details temporary frame
			self.temp_stagers_details_labelframe = Tkinter.LabelFrame(self.temp_stagers_dynamic_coreframe)
			self.temp_stagers_details_labelframe.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
			
			# build options temporary frame
			self.temp_stagers_options_labelframe = Tkinter.LabelFrame(self.temp_stagers_dynamic_coreframe)
			self.temp_stagers_options_labelframe.grid(row=1,column=0,sticky=NW,padx=2,pady=5)
			
			# ---------- Create Button----------#
			stagers_create_action_button = Tkinter.Button(self.temp_stagers_options_labelframe,text="Generate Stager",command=self.api_generate_stager)
			stagers_create_action_button.config(fg='white',bg='blue',font=('arial','10','bold'))
			stagers_create_action_button.grid(row=0,column=1,sticky=NW,padx=2,pady=2)
			
			# track the row count for placement (account for button, row=1)
			row_count = 1
			
			# track all required key name values
			self.temp_stager_reqd_keys_list = []
			
			# track all key name values
			self.temp_stager_keys_list = []

			for item in response['stagers']:
				
				for key,value in item.iteritems():
					
					# regular key value print
					if (key == "Name"):
						
						# Option Name
						self.option_name_str = Tkinter.StringVar()
						self.option_name_str.set(str(key))
						self.option_name_dlabel = Tkinter.Label(self.temp_stagers_details_labelframe,textvariable=self.option_name_str,justify=LEFT)
						self.option_name_dlabel.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
						
						# Option Field Value
						self.option_field_str = Tkinter.StringVar()
						self.option_field_str.set(str(value))
						self.option_entry_field = Tkinter.Entry(self.temp_stagers_details_labelframe,textvariable=self.option_field_str,width=70)
						self.option_entry_field.config(state="disabled",disabledbackground="ghost white",disabledforeground="black")
						self.option_entry_field.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
						
						# increment the row count
						row_count += 1
						
					elif (key == "Description"):
						
						# Option Name
						self.option_name_str = Tkinter.StringVar()
						self.option_name_str.set(str(key))
						self.option_name_dlabel = Tkinter.Label(self.temp_stagers_details_labelframe,textvariable=self.option_name_str,justify=LEFT)
						self.option_name_dlabel.grid(row=row_count,column=0,sticky=NE,padx=2,pady=2)
						
						# Option Field Value
						self.option_entry_textbox = ScrolledText(self.temp_stagers_details_labelframe,width=80,height=2)
						self.option_entry_textbox.config(bg="ghost white",state="disabled")
						self.option_entry_textbox.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
						
						self.option_entry_textbox.config(state="normal")
						self.option_entry_textbox.insert(Tkinter.END,str(value))
						self.option_entry_textbox.config(state="disabled")
												
						# increment the row count
						row_count += 1
					
					elif (key == "Author"):
							 
						# Option Name
						self.option_name_str = Tkinter.StringVar()
						self.option_name_str.set(str(key))
						self.option_name_dlabel = Tkinter.Label(self.temp_stagers_details_labelframe,textvariable=self.option_name_str,justify=LEFT)
						self.option_name_dlabel.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
						
						 # Option Field Value
						authors = ""
													
						# grab the list values
						for i in value:
							authors += str(i) + " "
							
						# Option Field Value
						self.option_field_str = Tkinter.StringVar()
						self.option_field_str.set(str(authors))
						self.option_entry_field = Tkinter.Entry(self.temp_stagers_details_labelframe,textvariable=self.option_field_str,width=70)
						self.option_entry_field.config(state="disabled",disabledbackground="ghost white",disabledforeground="black")
						self.option_entry_field.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
						
						# increment the row count
						row_count += 1
				
					elif (key == "Comments"):

						# check if Comments blank - if so, skip
						if ( len(value) == 1) and ( str(value[0]) == "" ):
							continue
						
						# Comment not blank, so display
						else:
							
							# Option Name
							self.option_name_str = Tkinter.StringVar()
							self.option_name_str.set(str(key))
							self.option_name_dlabel = Tkinter.Label(self.temp_stagers_details_labelframe,textvariable=self.option_name_str,justify=LEFT)
							self.option_name_dlabel.grid(row=row_count,column=0,sticky=NE,padx=2,pady=2)
													
							# Option Field Value
							comments = ""
							
							# grab the list values
							for i in value:
								comments += str(i) + " "
									
							# grid the field dlablel								
							# Option Field Value
							self.option_entry_textbox = ScrolledText(self.temp_stagers_details_labelframe,width=80,height=2)
							self.option_entry_textbox.config(bg="ghost white",state="disabled")
							self.option_entry_textbox.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
							
							self.option_entry_textbox.config(state="normal")
							self.option_entry_textbox.insert(Tkinter.END,str(comments))
							self.option_entry_textbox.config(state="disabled")
							
							# increment the row count
							row_count += 1
							
					elif (key == "options"):
						
						# we have to do some digging here: value is a dictionary of dictionaries
						for key2,value2 in value.iteritems():
							
							# append to stager temp list of keys
							self.temp_stager_keys_list.append(key2)
							
							for key3,value3 in value2.iteritems():
								
								if key3 == "Description":
									description_str = value3
					
								elif key3 == "Required":
									required_bool = value3
					
								elif key3 == "Value":
									val = value3
									
							# Option Name
							name_label = Tkinter.Label(self.temp_stagers_options_labelframe,text=str(key2) + ": ",justify=LEFT)
							name_label.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
						
							# check if Listener option
							# if so, append to reqd keys name list and change entry bgcolor
							if required_bool:
								
								# append key name to reqd key name list
								self.temp_stager_reqd_keys_list.append(key2)
								
								# add drop down for Listener value
								if key2 == "Listener":
									
									# grid universal Listener drop down
									response = self.eac_object.listeners_get_current_listeners()
									self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
									
									# list holding listener names, dropdown choices
									choices = []
									
									# if no listeners, append blank
									if len(response['listeners']) == 0: choices.append('');
								
									# else, grab name for each listener, append to choices list
									else:
								
										try:					
											for item in response['listeners']:
												choices.append(str(item['name']))
										
										except Exception as e:
											tkMessageBox.showerror("ERROR","Grab name for each Listener failed - " + str(e))
									
									# build the drop down menu
									option_field = Tkinter.OptionMenu(self.temp_stagers_options_labelframe,self.option_listener_field_str,*choices,command=self.misc_set_listener_field_str)
									option_field.grid(row=row_count,column=1,sticky=W,padx=2,pady=2)
									option_field.config(background="wheat",width=20)
								
								# regular required field, use Entry 
								else:
									# change the bgcolor of the entry field
									temp_field_label_str = Tkinter.StringVar()
									temp_field_label_str.set(str(val))
									field_label = Tkinter.Entry(self.temp_stagers_options_labelframe,textvariable=temp_field_label_str)
									field_label.grid(row=row_count,column=1,sticky=W,padx=2,pady=2)
									field_label.config(background="wheat",width=25) 
								
							# not a required field, display white background	
							else:					
								temp_field_label_str = Tkinter.StringVar()
								temp_field_label_str.set(str(val))
								field_label = Tkinter.Entry(self.temp_stagers_options_labelframe,textvariable=temp_field_label_str)
								field_label.config(width=25) 
								field_label.grid(row=row_count,column=1,sticky=W,padx=2,pady=2) 
														
							# Option Description
							description_label = Tkinter.Label(self.temp_stagers_options_labelframe,text=str(description_str),wraplength=450,justify=LEFT)
							description_label.grid(row=row_count,column=2,sticky=W,padx=2,pady=2)
								
							# increment the row count
							row_count += 1

		except Exception as e:
			# log the URL requested
			tkMessageBox.showerror("ERROR","Exception parsing Stager options JSON - " + str(e))

	# generate stager
	def api_generate_stager(self):
		
		# grab all child item values from stager options frame
		try:
			
			# temp list holding values
			vals = []
			
			# for each child item within the frame (dynamic, depends on options for selected listener type)
			for i in range(0,len(self.temp_stagers_options_labelframe.winfo_children())):
				
				# grab value and append to temp values list
				try:
					
					if self.temp_stagers_options_labelframe.winfo_children()[i].winfo_class() == "Menubutton":
						vals.append(self.option_listener_field_str.get())
					
					else:
						vals.append(self.temp_stagers_options_labelframe.winfo_children()[i].get())
					
				# appending values to vals[] failed
				except Exception as e:
					
					# do nothing if you cant get it
					pass
			
			# check if value list is same size as temp keys list for listener type selected
			if len(vals) == len(self.temp_stager_keys_list):
				
				# temp dictionary for the JSON data
				# append the StagerName as first entry
				temp_dict = {}
				temp_dict['StagerName'] = str(self.stagers_all_treeview.item(self.selected_stager,"text"))
				
				# build the dictionary with key->value pairs for listener type options
				for i in range(0,len(vals)):
					
					# check if option is required, and if blank
					# if so, error out and stop
					if (self.temp_stager_keys_list[i] in self.temp_stager_reqd_keys_list) and (vals[i] == ""):
						
						tkMessageBox.showerror("ERROR","Required field missing - " +  str(self.temp_stager_keys_list[i]))
						return
					
					# required fields met, append to dictionary
					# perform check to see if outfile creation required
					else:
				
						temp_dict[self.temp_stager_keys_list[i]] = vals[i]
						
						# if OutFile has a value, we need to create file
						# set global outfile path variable
						if (self.temp_stager_keys_list[i] == "OutFile"):
							
							if (temp_dict[self.temp_stager_keys_list[i]] != ""): 
								self.stager_outfile_path = temp_dict[self.temp_stager_keys_list[i]]
							
			
			# -- Send the Create Stagers Command --- #
			response = self.eac_object.stagers_generate_stager(temp_dict)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")

			# call stagers results window class, params: parent, json response, name of launcher, and stager outfile path
			stager_results = stagers_results_window(self.form,response,str(temp_dict['StagerName']),self.stager_outfile_path)
			self.form.wait_window(stager_results.top)
			
			# reset stager outfile after call
			self.stager_outfile_path = ""
			

		except Exception as e:
			tkMessageBox.showerror("ERROR","Generate Stager failed. " + str(e))
			
	
	####### AGENT FUNCTIONS ##########
	
	# get current agents
	def api_get_current_agents(self):
		
		# call to api function
		response = self.eac_object.agents_get_current_agents()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
		# JSON Parsing - response is a {'agents':[{dict1},{dict2},...]}
		try:
			
			# temp list of agent names
			holder = []
		
			for item in response['agents']:
				
				holder.append(item['name'])
				holder.sort()
			
			# clear the treeview
			self.agents_current_treeview.delete(*self.agents_current_treeview.get_children())
			
			# populate treeview
			for l in holder:
				self.agents_current_treeview.insert("","end", text=str(l))
		
		# JSON Parsing Failed
		except Exception as e:
			tkMessageBox.showerror("ERROR","Get Current Agents failed." + str(e))
		
		### UPDATE - makes the call to api_get_stale_agents too
		self.api_get_stale_agents()
		
	# get current agents for reporting optionmenu
	def api_get_current_agents_reporting(self):
		
		# call to api function
		response = self.eac_object.reporting_get_all_logged_events()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
		# JSON Parsing - response is a {'agents':[{dict1},{dict2},...]}
		try:
			
			# temp list of agent names
			holder = []
		
			# build the list
			for item in response['reporting']:
				
				# skip duplicates
				if item['agentname'] not in holder:
				
					holder.append(item['agentname'])
					holder.sort()
			
			# reload global dict
			self.reporting_agent_choices[:] = []
			self.reporting_agent_choices.append("")
			
			# append to global list
			for a in holder:
				self.reporting_agent_choices.append(a)

		# JSON Parsing Failed
		except Exception as e:
			tkMessageBox.showerror("ERROR","Get Current Agents failed." + str(e))
		
	# get stale agents
	def api_get_stale_agents(self):
		
		# call to api function
		response = self.eac_object.agents_get_stale_agents()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
		# JSON Parsing - response is a {'agents':[{dict1},{dict2},...]}
		try:
			
			# temp list of agent names
			holder = []
		
			for item in response['agents']:
				
				holder.append(item['name'])
				holder.sort()
			
			# clear the treeview
			self.agents_stale_treeview.delete(*self.agents_stale_treeview.get_children())
			
			# populate treeview
			for l in holder:
				self.agents_stale_treeview.insert("","end", text=str(l))
		
		# JSON Parsing Failed
		except Exception as e:
			tkMessageBox.showerror("ERROR","Get Stale Agents failed." + str(e))
		
	# remove stale agents
	def api_get_remove_stale_agents(self):
		
		# call to api function
		self.eac_object.agents_remove_stale_agents()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
		# clear the frame
		try:
			for child in self.agent_info_action_lframe.winfo_children():
				child.destroy()
		except:
			pass

		# refresh the current agents and stale agents views (one call required)
		self.api_get_current_agents()

	# get agent by name
	def api_get_agent_by_name(self,event):
		
		# get the selected item
		try:
			self.selected_agent = self.agents_current_treeview.selection()[0]
			self.selected_agent_name =  str(self.agents_current_treeview.item(self.selected_agent,"text"))
			
		except Exception as e:
			tkMessageBox.showerror("ERROR","Getting selected Agent failed: " + str(e))
			return
		
		# call to the api with listener name
		response = self.eac_object.agents_get_agent_by_name(self.selected_agent_name)
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
		# parsing was successful
		try:
		
			# clear the frame
			try:
				for child in self.agent_info_action_lframe.winfo_children():
					child.destroy()
			except:
				pass
			
			# build temporary details frame
			self.temp_agent_labelframe = Tkinter.LabelFrame(self.agent_info_action_lframe)
			self.temp_agent_labelframe.grid(row=0,column=0,padx=2,pady=2,sticky=NW)
			
			# track the row count and column count for placement
			row_count = 0
			col_count = 0
			
			# hold the os value
			temp_os_name = ""
			
			# hold the agent language
			temp_agent_lang = ""
						
			# create the dynamic form - readonly state
			for item in response['agents']:
				
				for key,value in item.iteritems():
					
					attrs = ["internal_ip","hostname","listener","os_details","ID","name","external_ip","username","checkin_time","session_id","lastseen_time"]
					
					if key in attrs:   
				
						# Option Name
						option_name_str = Tkinter.StringVar()
						option_name_str.set(key)
						option_name_dlabel = Tkinter.Label(self.temp_agent_labelframe,textvariable=option_name_str)
						option_name_dlabel.grid(row=row_count,column=col_count,sticky=E,padx=2,pady=2)
					
						# increment the column count
						col_count += 1
					
						# Option Field Value
						option_field_str = Tkinter.StringVar()
						option_field_str.set(value)
						option_entry_field = Tkinter.Entry(self.temp_agent_labelframe,textvariable=option_field_str,width=30)
						option_entry_field.config(state="disabled",disabledbackground='ghost white',disabledforeground='black')
						option_entry_field.grid(row=row_count,column=col_count,sticky=W,padx=2,pady=2)
						
						# increment the column count
						col_count += 1
						
						# check - if 4th item break into new line
						# set col_count to 0, and increment row_count
						if (col_count == 4): 
							row_count += 1
							col_count = 0;
			
			##### ADD THE MENU BUTTONS ########
			# Agent Actions
			# Harcoded to the 4th column in grid
			self.mb_agent_actions = Menubutton(self.temp_agent_labelframe,text="   Agent Actions    ",relief=RAISED)
			self.mb_agent_actions.grid(row=0,column=4,sticky=NW,padx=2,pady=2)
			
			self.submenu_agent_actions = Menu ( self.mb_agent_actions, tearoff = 0 )
			self.mb_agent_actions.config(menu=self.submenu_agent_actions)
			
			self.submenu_agent_actions.add_command(label="Rename Agent",command=self.api_rename_agent)
			self.submenu_agent_actions.add_command(label="Clear Agent Queued",command=self.api_clear_queued_agent_taskings)
			self.submenu_agent_actions.add_command(label="Delete Agent Results",command= lambda: self.api_delete_agent_results(self.selected_agent_name))
			self.submenu_agent_actions.add_command(label="Remove Agent",command=self.api_remove_agent)
			self.submenu_agent_actions.add_command(label="Kill Agent",command=self.api_kill_agent)
		
			# All Agent Actions
			# Agent Actions
			self.mb_all_agent_actions = Menubutton(self.temp_agent_labelframe,text="   All Agent Actions    ", relief=RAISED)
			self.mb_all_agent_actions.grid(row=1,column=4,sticky=NW,padx=2,pady=2)
			
			self.submenu_all_agent_actions = Menu ( self.mb_all_agent_actions, tearoff = 0 )
			self.mb_all_agent_actions.config(menu=self.submenu_all_agent_actions)
			
			self.submenu_all_agent_actions.add_command(label="Run Shell Command",command=self.api_task_all_agents_run_shell_cmd)
			self.submenu_all_agent_actions.add_command(label="Delete All Agent Results",command=self.api_delete_all_agent_results)
			self.submenu_all_agent_actions.add_command(label="Kill All Agents",command=self.api_kill_all_agents)
			
			
			######## ADD THE AGENT RESULTS AND SHELL COMMAND FIELDS  ###########
			
			self.temp_agent_results_labelframe = Tkinter.Frame(self.agent_info_action_lframe)
			self.temp_agent_results_labelframe.grid(row=1,column=0,padx=2,pady=2,sticky=NW)
			
			self.task_agent_shell_popup_label = ttk.Label(self.temp_agent_results_labelframe, text = "POWERSHELL: ")
			self.task_agent_shell_popup_label.grid(row=0,column=0,sticky=E,padx=5,pady=5)
		
			self.task_agent_shell_entry = Tkinter.Entry(self.temp_agent_results_labelframe,width=40)
			self.task_agent_shell_entry.grid(row=0,column=1,sticky=W,padx=5,pady=5)
			
			self.task_agent_shell_action_button = Tkinter.Button(self.temp_agent_results_labelframe,text = "Execute",command=self.api_task_agent_run_shell_cmd)
			self.task_agent_shell_action_button.config(fg='white',bg='blue',font=('arial','10','bold'))
			self.task_agent_shell_action_button.grid(row=0,column=3,sticky=W,padx=2,pady=2)
			
			self.temp_RefreshButton = Tkinter.Button(self.temp_agent_results_labelframe,text="Refresh Results",command= lambda: self.api_get_agent_results(self.selected_agent_name))
			self.temp_RefreshButton.config(fg='white',bg='slate gray',font=('arial','10','bold'))
			self.temp_RefreshButton.grid(row=0,column=4,sticky=W,padx=2,pady=2)
		
			self.temp_agents_results_scrolledtext = ScrolledText(self.temp_agent_results_labelframe,height=25,width=147)
			self.temp_agents_results_scrolledtext.config(bg='ghost white')
			self.temp_agents_results_scrolledtext.grid(row=1,column=0,columnspan=50,sticky='NEWS',padx=2,pady=2)
			self.temp_agents_results_scrolledtext.config(state="disabled")
			
			# call to Agent Results to load display
			self.api_get_agent_results(self.selected_agent_name)
						
		# parsing json failed
		except Exception as e:
			
			tkMessageBox.showerror("ERROR","Error parsing Get Agent by Name : " + str(e))
			
	# remove agent popup window
	def api_remove_agent(self):
		
		# check if remove_agent boolean True, if so remove agent
		if tkMessageBox.askyesno("Remove Agent", "Are you sure you want to delete the Agent?"):
			
			# call to api function
			response = self.eac_object.agents_remove_agent(self.selected_agent_name)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			try:
				# removal was successful
				if response['success']:
				
					# rerun the get current agents
					self.api_get_current_agents()
			
					# clear the Agent Temp frame
					try:
						for child in self.agent_info_action_lframe.winfo_children():
							child.destroy()
			
					except:
						pass
					
				# removal failed
				else:
					tkMessageBox.showerror("ERROR","Removal of " + self.selected_agent_name + " Failed.")
		
			# request bombed
			except Exception as e:
		
				tkMessageBox.showerror("ERROR","Reques to remove Agent failed : " + str(e))
	
	# task agent to run shell command
	def api_task_agent_run_shell_cmd(self):

		try:
			# check if command value not blank
			if str(self.task_agent_shell_entry.get()) != "":
				
				# define the command data			
				command_data = {}
				command_data['command'] = str(self.task_agent_shell_entry.get())
				
				# call to api function
				self.eac_object.agents_task_agent_run_shell_cmd(self.selected_agent_name,command_data)
				self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			# blank command value
			else:
				tkMessageBox.showerror("ERROR","No Command entered to run on Agent")

		except Exception as e:
			tkMessageBox.showerror("ERROR","Error running command on Agent: " + str(e))
	
	# task all agents to run shell command
	def api_task_all_agents_run_shell_cmd(self):
		
		# create instance of task run shell dialog window
		command_dialog = api_task_all_agents_run_shell_popup(self.form)
		self.form.wait_window(command_dialog.top)
		
		try:
			# check if command value not blank
			if str(command_dialog.command) != "":
				
				# define the command data			
				command_data = {}
				command_data['command'] = str(command_dialog.command)
				
				# call to api function
				self.eac_object.agents_task_all_agents_run_shell_cmd(command_data)
				self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			# blank command value
			else:
				tkMessageBox.showerror("ERROR","No Command entered to run on All Agents.")

		except:
			pass

	# get agent results
	def api_get_agent_results(self,agent):
		
		try:
		 
			# call to the api with listener name
			response = self.eac_object.agents_get_agent_results(agent)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			# set to writing
			self.temp_agents_results_scrolledtext.config(state="normal")
		
			# clear the scrolltext beforehand
			self.temp_agents_results_scrolledtext.delete('1.0', END)
		
			# parse the list of dicts
			for item in response['results']:
			
				for key,value in item.iteritems():
				
					if key == "AgentResults":
					
						for dicts in value:
						
							try:
							
								for key2,value2 in dicts.iteritems():
								
									self.temp_agents_results_scrolledtext.insert(Tkinter.END,value2 + "\n\n")
									#self.results += value2
								
							except Exception as e:
								
								# no error handling necessary
								pass
						
			# disable and set scroll to bottom
			self.temp_agents_results_scrolledtext.config(state="disabled")
			self.temp_agents_results_scrolledtext.see(Tkinter.END)
		
		except Exception as e:
			
			tkMessageBox.showerror("ERROR","Error in Get Agent Results function: " + str(e))
		
	# delete agent results
	def api_delete_agent_results(self,agent):
	
		# check if remove_agent boolean True, if so delete results
		if tkMessageBox.askyesno("Delete Agent Results","Are you sure you want to delete the Agent results?"):
			
			# call to api function
			self.eac_object.agents_delete_agent_results(agent)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
	# delete all agent results
	def api_delete_all_agent_results(self):
	
		# check if delete all results boolean True, if so delete all results
		if tkMessageBox.askyesno("Delete ALL Agent Results","Are you sure you want to delete ALL Agent results?"):
			
			# call to api function
			self.eac_object.agents_delete_all_agent_results()
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
						
	# clear queued agent taskings
	def api_clear_queued_agent_taskings(self):
	
		# check if remove_agent boolean True, if so remove agent
		if tkMessageBox.askyesno("Clear Queued Agent Tasks","Are you sure you want to clear ALL queued tasks?"):
			
			# call to api function
			self.eac_object.agents_clear_queued_agent_tasking(self.selected_agent_name)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
	# rename agent
	def api_rename_agent(self):
		
		# create instance of clear queue dialog window
		rename_agent_dialog = api_rename_agent_popup(self.form)
		self.form.wait_window(rename_agent_dialog.top)
		
		try:
			# check if name value not blank and does not contain a blank space
			if  ( str(rename_agent_dialog.new_name) != "" ) and ( " " not in str(rename_agent_dialog.new_name) ):
				
				# define the newname data			
				newname_data = {}
				newname_data['newname'] = str(rename_agent_dialog.new_name)
				
				# call to api function
				response = self.eac_object.agents_rename_agent(self.selected_agent_name,newname_data)
				self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
				try:
					
					# rename was successful
					if response['success']:
						
						# re populate current agents
						self.api_get_current_agents()
						self.api_get_current_agents_reporting()
						
						# disable the action buttons on old data
						self.mb_agent_actions.config(state="disabled")
						self.mb_all_agent_actions.config(state="disabled")
						self.agent_automator_button.config(state="disabled")
						
					# rename failed
					else:
						tkMessageBox.showerror("ERROR","Rename Agent failed for " + self.selected_agent_name)
			
				# request bombed
				except Exception as e:
				
					tkMessageBox.showerror("ERROR","Rename Agent failed - " + str(e))

			# blank command or invalid value
			else:
				tkMessageBox.showerror("ERROR","Blank or invalid new Name value for " + self.selected_agent_name)
		
		# handles the cancel action
		except Exception as e:
			pass

	# kill agent
	def api_kill_agent(self):
		
		# check if remove_agent boolean True, if so remove agent
		if tkMessageBox.askyesno("Confirm Kill Agent","Are you sure you want to kill the Agent?"):
			
			# call to api function
			response = self.eac_object.agents_kill_agent(self.selected_agent_name)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			try:
				# kill was successful
				if response['success']:
				
					# rerun the get current agents
					self.api_get_current_agents()
			
				# kill failed
				else:
					tkMessageBox.showerror("ERROR","Attempt to Kill Agent FAILED - " + self.selected_agent_name)
		
			# request bombed
			except Exception as e:
				tkMessageBox.showerror("ERROR","Killing Agent failed - " + str(e))
	
	# kill all agents
	def api_kill_all_agents(self):
		
		# check if remove_agent boolean True, if so remove agent
		if tkMessageBox.askyesno("Confirm Kill ALL Agents","Are you sure you want to kill ALL Agents?"):
			
			# call to api function
			response = self.eac_object.agents_kill_all_agents()
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
			try:
				# kill all was successful
				if response['success']:
				
					# rerun the get current agents
					self.api_get_current_agents()
			
				# kill failed
				else:
					tkMessageBox.showerror("ERROR","Attempt to Kill All Agents FAILED.")
		
			# request bombed
			except Exception as e:
				tkMessageBox.showerror("ERROR","Killing All Agents failed - " + str(e))
	
		
	####### MODULES FUNCTIONS #############
	
	# get current modules
	def api_get_current_modules(self):
		
		# call to api function
		response = self.eac_object.modules_get_current_modules()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
		# JSON Parsing - response is a {'agents':[{dict1},{dict2},...]}
		try:
			
			# temp list of agent names
			holder = []
		
			for item in response['modules']:
				
				holder.append(item['Name'])
				holder.sort()
			
			# clear the treeview
			self.modules_all_treeview.delete(*self.modules_all_treeview.get_children())
			
			# populate treeview
			for l in holder:
				self.modules_all_treeview.insert("","end", text=str(l))
		
		# JSON Parsing Failed
		except Exception as e:
			tkMessageBox.showerror("ERROR","Get Current Modules failed - " + str(e))
		
	# get current modules by keyword
	def api_search_for_module(self):
		
		# get the keyword value
		keyword = self.modules_search_str.get()
	
		# if keyword is not blank, and does not contain " ", then search
		if ( keyword.strip() != "" ) and ( " " not in keyword.strip() ):
			
			# valid keyword, build data
			keyword_data = {}
			keyword_data = { "term" : keyword }
			
			# make api call with keyword data
			response = self.eac_object.modules_search_for_module(keyword_data)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
			# JSON Parsing - response is a {'agents':[{dict1},{dict2},...]}
			try:
				
				# temp list of agent names
				holder = []
			
				for item in response['modules']:
					
					holder.append(item['Name'])
					holder.sort()
				
				# clear the treeview
				self.modules_all_treeview.delete(*self.modules_all_treeview.get_children())
				
				# populate treeview
				for l in holder:
					self.modules_all_treeview.insert("","end", text=str(l))
				
			# JSON Parsing Failed
			except Exception as e:
				tkMessageBox.showerror("ERROR","Get Current Modules failed." + str(e))
			
		# invalid keyword
		else:
			tkMessageBox.showerror("ERROR","Invalid Module Search keyword entered.")
	
	# get module by name
	def api_get_module_by_name(self,event):
		
		# Global Option Agent Field
		self.option_agent_field_str = Tkinter.StringVar()
		self.option_listener_field_str = Tkinter.StringVar()
		
		# get the selected item
		try:
			self.selected_module = self.modules_all_treeview.selection()[0]
			self.selected_module_name =  str(self.modules_all_treeview.item(self.selected_module,"text"))
			
		except Exception as e:
			# log the URL requested
			tkMessageBox.showerror("ERROR","Exception on blank click: " + str(e))
			return
		
		# call to the api with stager name
		response = self.eac_object.modules_get_module_by_name(self.selected_module_name)
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
	
		try:
			
			# clear the frame
			try:
				for child in self.modules_api_canvas.winfo_children():
					child.destroy()
			
			except:
				pass
			
			# define the core frame
			# required to hold the multiple dynamic labelframes in the canvas
			self.temp_modules_dynamic_coreframe = Tkinter.Frame(self.modules_api_canvas)
			self.modules_api_canvas.create_window(0,10,window=self.temp_modules_dynamic_coreframe,anchor=NW)
			
			# build details temporary frame
			self.temp_modules_details_labelframe = Tkinter.LabelFrame(self.temp_modules_dynamic_coreframe)
			self.temp_modules_details_labelframe.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
			
			# build options temporary frame
			self.temp_modules_options_labelframe = Tkinter.LabelFrame(self.temp_modules_dynamic_coreframe)
			self.temp_modules_options_labelframe.grid(row=1,column=0,sticky=NW,padx=5,pady=5)
			
			# ---------- Execute Button----------#
			modules_execute_action_button = Tkinter.Button(self.temp_modules_options_labelframe,text="Execute Module",command=self.api_execute_module)
			modules_execute_action_button.config(fg='white',bg='blue',font=('arial','10','bold'))
			modules_execute_action_button.grid(row=0,column=1,sticky=NW,padx=2,pady=2)
			
			# track the row count for placement
			# start at 1 to account for top row buttons
			row_count = 1
			
			# track all required key name values
			self.temp_module_reqd_keys_list = []
			
			# track all key name values
			self.temp_module_keys_list = []

			for item in response['modules']:
				
				for key,value in item.iteritems():
					
					# regular key value print
					if (key == "Name") or \
					   (key == "Background") or \
					   (key == "MinPSVersion") or \
					   (key == "NeedsAdmin") or \
					   (key == "OpsecSafe") or \
					   (key == "OutputExtension"):
						
						# Option Name
						self.option_name_str = Tkinter.StringVar()
						self.option_name_str.set(str(key))
						self.option_name_dlabel = Tkinter.Label(self.temp_modules_details_labelframe,textvariable=self.option_name_str,justify=LEFT)
						self.option_name_dlabel.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
					
						# Option Field Value
						self.option_field_str = Tkinter.StringVar()
						self.option_field_str.set(str(value))
						self.option_entry_field = Tkinter.Entry(self.temp_modules_details_labelframe,textvariable=self.option_field_str,width=70)
						self.option_entry_field.config(state="disabled",disabledbackground="ghost white",disabledforeground="black")
						self.option_entry_field.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
												
						# increment the row count
						row_count += 1
					
					elif (key == "Description"):
						
						# Option Name
						self.option_name_str = Tkinter.StringVar()
						self.option_name_str.set(str(key))
						self.option_name_dlabel = Tkinter.Label(self.temp_modules_details_labelframe,textvariable=self.option_name_str,justify=LEFT)
						self.option_name_dlabel.grid(row=row_count,column=0,sticky=NE,padx=2,pady=2)
						
						# Option Field Value
						self.option_entry_textbox = ScrolledText(self.temp_modules_details_labelframe,width=80,height=3)
						self.option_entry_textbox.config(bg="ghost white",state="disabled")
						self.option_entry_textbox.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
						
						self.option_entry_textbox.config(state="normal")
						self.option_entry_textbox.insert(Tkinter.END,str(value))
						self.option_entry_textbox.config(state="disabled")
												
						# increment the row count
						row_count += 1
						
					elif (key == "Author"):
							 
						# Option Name
						self.option_name_str = Tkinter.StringVar()
						self.option_name_str.set(str(key))
						self.option_name_dlabel = Tkinter.Label(self.temp_modules_details_labelframe,textvariable=self.option_name_str,justify=LEFT)
						self.option_name_dlabel.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
						
						 # Option Field Value
						authors = ""							
						
						# grab the list values
						for i in value:
							authors += i + " " 
							
						# Option Field Value
						self.option_field_str = Tkinter.StringVar()
						self.option_field_str.set(str(authors))
						self.option_entry_field = Tkinter.Entry(self.temp_modules_details_labelframe,textvariable=self.option_field_str,width=70)
						self.option_entry_field.config(state="disabled",disabledbackground="ghost white",disabledforeground="black")
						self.option_entry_field.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
						
						# increment the row count
						row_count += 1
					
					elif (key == "Comments"):
							 
						# Option Name
						self.option_name_str = Tkinter.StringVar()
						self.option_name_str.set(str(key))
						self.option_name_dlabel = Tkinter.Label(self.temp_modules_details_labelframe,textvariable=self.option_name_str,justify=LEFT)
						self.option_name_dlabel.grid(row=row_count,column=0,sticky=NE,padx=2,pady=2)
												
						# comment string
						comments = "" 
						 
						# grab the list values
						for i in value:
							comments += i + " "
								
						# Option Field Value
						self.option_entry_textbox = ScrolledText(self.temp_modules_details_labelframe,width=80,height=3)
						self.option_entry_textbox.config(bg="ghost white",state="disabled")
						self.option_entry_textbox.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
						
						self.option_entry_textbox.config(state="normal")
						self.option_entry_textbox.insert(Tkinter.END,str(comments))
						self.option_entry_textbox.config(state="disabled")
						
						# increment the row count
						row_count += 1
					
					elif (key == "options"):
						
						# we have to do some digging here: value is a dictionary of dictionaries
						for key2,value2 in value.iteritems():
							
							# append to stager temp list of keys
							self.temp_module_keys_list.append(key2)
							
							for key3,value3 in value2.iteritems():
								
								if key3 == "Description":
									description_str = value3
					
								elif key3 == "Required":
									required_bool = value3
					
								elif key3 == "Value":
									val = value3
									
							# Option Name
							name_label = Tkinter.Label(self.temp_modules_options_labelframe,text=str(key2) + ": ")
							name_label.grid(row=row_count,column=0,sticky=NE,padx=1,pady=1)
						
							# check if field required
							# if so, append to reqd keys name list and change entry bgcolor
							if required_bool:
								
								# append key name to reqd key name list
								self.temp_module_reqd_keys_list.append(key2)
								
								# add drop down for Agent value
								if key2 == "Agent":
									
									# grid universal Listener drop down
									agent_response = self.eac_object.agents_get_current_agents()
									self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
									
									# list holding listener names, dropdown choices
									agent_choices = []
									
									# if no listeners, append blank
									if len(agent_response['agents']) == 0: agent_choices.append('');
								
									# else, grab name for each listener, append to choices list
									else:
								
										try:
									
											for item in agent_response['agents']:
										
												agent_choices.append(str(item['name']))
										
										except Exception as e:
											tkMessageBox.showerror("ERROR","Creating Agent optionmenu for Modules tab: " + str(e))
									
									# build the drop down menu
									option_agent_field = Tkinter.OptionMenu(self.temp_modules_options_labelframe,self.option_agent_field_str,*agent_choices,command=self.misc_set_modules_agent_field_str)
									option_agent_field.grid(row=row_count,column=1,sticky=NW,padx=1,pady=1)
									option_agent_field.config(background="wheat",width=25)
								
								
								# add drop down for Listener value
								elif key2 == "Listener":
									
									# grid universal Listener drop down
									listener_response = self.eac_object.listeners_get_current_listeners()
									self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
									
									# list holding listener names, dropdown choices
									listener_choices = []
									
									# if no listeners, append blank
									if len(listener_response['listeners']) == 0: listener_choices.append('');
								
									# else, grab name for each listener, append to choices list
									else:
								
										try:
									
											for item in listener_response['listeners']:
										
												listener_choices.append(str(item['name']))
										
										except Exception as e:
											tkMessageBox.showerror("ERROR","Creating Listener optionmenu for Modules tab: " + str(e))
									
									# build the drop down menu
									option_listener_field = Tkinter.OptionMenu(self.temp_modules_options_labelframe,self.option_listener_field_str,*listener_choices,command=self.misc_set_modules_listener_field_str)
									option_listener_field.grid(row=row_count,column=1,sticky=NW,padx=1,pady=1)
									option_listener_field.config(background="wheat",width=25)
								
								
								# regular required field, use Entry 
								else:
									# change the bgcolor of the entry field
									temp_entry_field_str = Tkinter.StringVar()
									temp_entry_field_str.set(str(val))
									
									entry_field = Tkinter.Entry(self.temp_modules_options_labelframe,textvariable=temp_entry_field_str)
									entry_field.grid(row=row_count,column=1,sticky=NW,padx=1,pady=1)
									entry_field.config(background="wheat",width=30) 
								
							# not a required field, display white background	
							else:
								temp_entry_field_str = Tkinter.StringVar()
								temp_entry_field_str.set(str(val))
													
								entry_field = Tkinter.Entry(self.temp_modules_options_labelframe,textvariable=temp_entry_field_str,width=30)
								entry_field.grid(row=row_count,column=1,sticky=NW,padx=1,pady=1) 
														
							# Option Description
							description_label = Tkinter.Label(self.temp_modules_options_labelframe,text=str(description_str),wraplength=300,justify=LEFT)
							description_label.grid(row=row_count,column=2,sticky=NW,padx=1,pady=1)
								
							# increment the row count
							row_count += 1

		except Exception as e:
			# log the URL requested
			tkMessageBox.showerror("ERROR","Exception parsing Module options JSON - " + str(e))

	# execute module
	def api_execute_module(self):
		
		# grab all child item values from module options frame
		try:
			
			# temp list holding values
			vals = []
			
			# for each child item within the frame (dynamic, depends on options for selected listener type)
			for i in range(0,len(self.temp_modules_options_labelframe.winfo_children())):
				
				# grab value and append to temp values list
				try:
					
					if self.temp_modules_options_labelframe.winfo_children()[i].winfo_class() == "Menubutton":
						
						vals.append(str(self.temp_modules_options_labelframe.winfo_children()[i].cget("text")))
						
					else:
						vals.append(self.temp_modules_options_labelframe.winfo_children()[i].get())
						
				# appending values to vals[] failed
				except Exception as e:
					
					# do nothing if you cant get it
					pass
			
			# check if value list is same size as temp keys list for module type selected
			if len(vals) == len(self.temp_module_keys_list):
				
				# temp dictionary for the JSON data
				temp_dict = {}

				# build the dictionary with key->value pairs for listener type options
				for i in range(0,len(vals)):
					
					# check if option is required, and if blank
					# if so, error out and stop
					if (self.temp_module_keys_list[i] in self.temp_module_reqd_keys_list) and (vals[i] == ""):
						
						tkMessageBox.showerror("ERROR","Required field missing - " +  str(self.temp_module_keys_list[i]))
						return
					
					# required fields met, append to dictionary
					# perform check to see if outfile creation required
					else:
				
						temp_dict[self.temp_module_keys_list[i]] = vals[i]
						
						# if OutFile has a value, we need to create file
						# set global outfile path variable
						if (self.temp_module_keys_list[i] == "OutFile"): 
							
							if (temp_dict[self.temp_module_keys_list[i]] != ""): 
								self.module_outfile_path = temp_dict[self.temp_module_keys_list[i]]
									
			
			# -- Send the Create Stagers Command --- #
			self.eac_object.modules_execute_module(self.selected_module_name,temp_dict)
			self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
		except Exception as e:
			tkMessageBox.showerror("ERROR","Execute Module JSON Parse failed - " + str(e))
			
	####### REPORTING FUNCTIONS ############
		
	# display report output 
	def reporting_display_output(self):

		# make call to api
		response = self.eac_object.reporting_get_all_logged_events()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
		# clear the reporting treerview textbox
		self.reporting_tree.delete(*self.reporting_tree.get_children())
			
		try:
				
			for item in response['reporting']:
				
				holder = ()
				
				for key,value in item.iteritems():
				
					holder += (str(value),)
					
				# add to reporting tree
				self.reporting_tree.insert('','end',values=holder)
				
			# set to the end of entrie
			self.reporting_tree.yview_moveto(1)
			
		except Exception as e:
			tkMessageBox.showerror("ERROR","Error parsing Get All Events - " + str(e))


	######### CREDENTIAL FUNCTIONS #######
	def api_get_stored_credentials(self):
		
		# make call to api
		response = self.eac_object.creds_get_stored_credentials()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
			
		# clear the reporting treerview textbox
		self.creds_tree.delete(*self.creds_tree.get_children())

		try:
			
			# check if creds response has items
			if len(response['creds']) != 0:
				
				for item in response['creds']:
					
					holder = ()
					
					for key,value in item.iteritems():
										
						holder += (str(value),)
						
					# add to reporting tree
					self.creds_tree.insert('','end',values=holder)
			
			# if no creds, continue
			else: pass;
			
		except Exception as e:
			tkMessageBox.showerror("ERROR","Error parsing Get Credentials - " + str(e))

	
	####### ERROR HANDLING AND RESET FUNCTIONS #############
	
	# Error Checking - Admin / API Authentication Function
	def error_check_api_auth_fields(self):
		
		# attempt to set values
		# return if value missing and log
		if not self.eac_object.api_set_username(self.api_username_str.get()):
			tkMessageBox.showerror("ERROR","Please enter a value for Username.")
			return False
		
		elif not self.eac_object.api_set_password(self.api_password_str.get()):
			tkMessageBox.showerror("ERROR","Please enter a value for Password.")
			return False
			
		elif not self.eac_object.api_set_host(self.api_host_str.get()):
			tkMessageBox.showerror("ERROR","Please enter a value for Host.")
			return False
			
		elif not self.eac_object.api_set_port(self.api_port_str.get()):
			tkMessageBox.showerror("ERROR","Please enter a value for Port.")
			return False
		
		else: return True
	
	###### MISC FUNCTIONS
	
	# API Log ScrollText
	#------------------
	
	# write to the API log ScrollText
	def misc_api_log_write(self,value):
		
		try:
			# add to the log window
			self.api_log_textbox.config(state="normal")
			self.api_log_textbox.tag_config('api_log',font=('1'))
			self.api_log_textbox.insert(Tkinter.END,"[API LOG] " + str(value),'api_log')
			self.api_log_textbox.config(state="disabled")
			self.api_log_textbox.see(Tkinter.END)
		
		except Exception as e:
			tkMessageBox.showerror("ERROR","Failed to write to API Log: " + str(e))
			
	# write to the API log ScrollText - POLLING
	def misc_api_log_polling_write(self,value):
		
		dstr = "" # detail string
		mstr = "" # message string
		fstr = ""
		
		holder = ast.literal_eval(value)
		
		for key,val in holder.iteritems():
			
			if key == "message":
				
				for key2,val2 in val.iteritems():
					
					if key2 == "message":
						
						if "[!]" in str(val2):
							
							if "Nonce verified" in str(val2):
								dstr += str(val2)
								
							else:
								fstr += str(val2).replace('\n',' ')
						
						elif "[+]" in str(val2):
							
							mstr += str(val2)
							
						elif "[*]" in str(val2):
							
							if ("TASKING_REQUEST" in str(val2)) or \
							   ("GET cookie" in str(val2)) or \
							   ("GET request" in str(val2)):
								   continue
							
							else:
								dstr += str(val2)
								continue
		
		# try to write to the log output frame
		try:
			
			if dstr != "":
				# add to the log window
				self.api_log_textbox.config(state="normal")
				self.api_log_textbox.tag_config('api_poll_dstr',foreground='cyan',font=('1','12'))
				self.api_log_textbox.insert(Tkinter.END,"[API POLL] " + dstr + "\n",'api_poll_dstr')
				self.api_log_textbox.config(state="disabled")
				self.api_log_textbox.see(Tkinter.END)
				
			if mstr != "":

				self.api_log_textbox.config(state="normal")
				self.api_log_textbox.tag_config('api_poll_mstr',foreground='lawn green',font=('1','12'))
				self.api_log_textbox.insert(Tkinter.END,"[API MSG] " + mstr + "\n",'api_poll_mstr')
				self.api_log_textbox.config(state="disabled")
				self.api_log_textbox.see(Tkinter.END)
				
			if fstr != "":
				
				self.api_log_textbox.config(state="normal")
				self.api_log_textbox.tag_config('api_poll_fstr',foreground='indianred1',font=('1','12'))
				self.api_log_textbox.insert(Tkinter.END,"[API ERROR] " + fstr + "\n",'api_poll_fstr')
				self.api_log_textbox.config(state="disabled")
				self.api_log_textbox.see(Tkinter.END)
				
	
		except Exception as e:
			tkMessageBox.showerror("ERROR","Failed to write to API Poll Log: " + str(e))		
	
	# Stager Misc
	# ------------
	
	# set the listener drop down global value on stager create
	def misc_set_listener_field_str(self,value):
		
		self.option_listener_field_str.set(value)
	
	# Modules Misc
	# -------------
	
	# set the agent dropdown for Modules tab global value on module create
	def misc_set_modules_agent_field_str(self,value):

		self.option_agent_field_str.set(value)
	
	# set the listener dropdown for Modules tab global value on module create
	def misc_set_modules_listener_field_str(self,value):

		self.option_listener_field_str.set(value)
	
	# Reporting Misc
	# ------------
	
	# set the agent drop down global value on reporting select
	def misc_set_reporting_agent_field_str(self,value):
		
		self.reporting_agent_field_str.set(value)
		
	# set the type drop down global value on reporting select
	def misc_set_reporting_type_field_str(self,value):
		
		self.reporting_type_field_str.set(value)
	
	# check the reporting type option menu selection
	def misc_reporting_type_option_select(self):
		
		# get the value of the IntVar for the reporting radio buttons
		selection = str(self.reporting_type_int.get())
		
		# all event option selected
		if selection == "1":
			
			# disable all three input flds
			self.reporting_agent_option_menu.config(state="disabled")
			self.reporting_type_option_menu.config(state="disabled")
			self.reporting_type_specificmsg_entry.config(state="disabled")
	
		# agent event option selected
		elif selection == "2":
			
			# enable agent dropdown
			self.reporting_agent_option_menu.config(state="normal")
			
			# disable rest
			self.reporting_type_option_menu.config(state="disabled")
			self.reporting_type_specificmsg_entry.config(state="disabled")
	
		# type event option selected
		elif selection == "3":
			
			# enable type dropdown
			self.reporting_type_option_menu.config(state="normal")
			
			# disable rest
			self.reporting_agent_option_menu.config(state="disabled")
			self.reporting_type_specificmsg_entry.config(state="disabled")
	
		# msg event option selected
		elif selection == "4":
			
			# enable msg entry
			self.reporting_type_specificmsg_entry.config(state="normal")
			
			# disable rest
			self.reporting_agent_option_menu.config(state="disabled")
			self.reporting_type_option_menu.config(state="disabled")
			
	# run the reporting agent global dict update
	# rebuild the reporting tab
	def misc_reporting_action_refresh(self):
		
		# try to update the reporting agents global dict
		try:
			self.api_get_current_agents_reporting()
		except:
			pass
		
		# try to rebuild reporting tab
		try:
			self.build_reporting_tab()
		except:
			pass
	
	# handle report event click event for results window
	def misc_reporting_display_event_details(self,event):
		
		# get the selected item
		try:

			c = self.reporting_tree.focus()
			holder = self.reporting_tree.item(c,"values")
						
			if holder != "":
				event_display = reporting_event_details_window(self.form,holder)
				self.form.wait_window(event_display.top)
			else:
				pass
			
		except Exception as e:
			tkMessageBox.showerror("ERROR","Exception on Report Event click: " + str(e))
	
	# Credentials Misc
	# ------------
	
	# handle credential display event for details window
	def misc_creds_display_event_details(self,event):
	
		# get the selected item
		try:

			c = self.creds_tree.focus()
			holder = self.creds_tree.item(c,"values")
			
			if holder != "":
				creds_display = credentials_event_details_window(self.form,holder)
				self.form.wait_window(creds_display.top)
			else:
				pass
			
		except Exception as e:
			tkMessageBox.showerror("ERROR","Exception on Credentials Event click: " + str(e))
	
	# Universal Misc
	def misc_col_sort(self,tree,col,descending):
	
		# grab the data to sort
		data = [(tree.set(child, col), child) \
			for child in tree.get_children('')]
			
		# sort the data data in place
		data.sort(reverse=descending)
		for ix, item in enumerate(data):
			tree.move(item[1], '', ix)
			

	# API LOGGING THREADS
	
	# Display to scrolledtext function - THREAD FUNCTION
	def api_thread_display_queue(self):
	
		# infinite loop
		while True:
			
			try:
				# print the content to screen
				self.misc_api_log_polling_write(str(self.api_log_queue.get())+"\n")
				self.api_log_queue.task_done()
			except:
				pass
				
	# Grab new content and send to Queue for display - THREAD FUNCTION
	def api_thread_update_queue(self,q):
		
		# 1. get all past events
		response = self.eac_object.reporting_get_all_logged_events()
		self.misc_api_log_write(self.eac_object.api_url_holder + "\n")
		
		# temp lists for events
		temp_events = []
		
		for item in response['reporting']:
			
			temp_events.append(item)
						
		# infinite loop
		while True:
			
			# continue to poll events; append to queue if necessary
			response = self.eac_object.reporting_get_all_logged_events()
			
			for item in response['reporting']:
				
				if item not in temp_events:
					
					q.put(item)
					temp_events.append(item)
			
			# loop control
			time.sleep(1)
		
	###### START APPLICATION #######	
	def start_application(self):
		self.form.mainloop() 
		
if __name__ == '__main__':
	
	vader()
