import Tkinter
from Tkinter import *
import ttk
import tkFont
from ScrolledText import ScrolledText
from empire_api_core import empire_api_core
from datetime import datetime
import tkFileDialog
import tkMessageBox
from tkMessageBox import *
import os
import ast
from ast import *
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# task all shell command class POPUP
class api_task_all_agents_run_shell_popup:
	
	def __init__(self,parent):
	
		top = self.top = Tkinter.Toplevel(parent)
		
		self.task_all_agents_shell_popup_label = ttk.Label(self.top, text = "Shell Command: ")
		self.task_all_agents_shell_popup_label.grid(row=0,column=0,sticky=W,padx=10,pady=10)
		
		self.task_all_agents_shell_entry = Tkinter.Entry(self.top,width=40)
		self.task_all_agents_shell_entry.grid(row=0,column=1,sticky=NW,padx=5,pady=5,columnspan=15)
		
		self.task_all_agents_shell_action_button = ttk.Button(self.top,text = "Send Command",command=self.send)
		self.task_all_agents_shell_action_button.grid(row=1,column=1,sticky=NW,padx=10,pady=10)
		
		self.task_all_agents_shell_cancel_button = ttk.Button(self.top,text = "Cancel", command = self.top.destroy)
		self.task_all_agents_shell_cancel_button.grid(row=1,column=2,sticky=NW,padx=10,pady=10)
	
	def send(self):
		
		self.command = self.task_all_agents_shell_entry.get()
		self.top.destroy()
		
# delete all agent results class POPUP
class api_delete_all_agent_results_popup:
	
	def __init__(self,parent):
		
		# define the delete all agent results check boolean
		self.delete_all_results = False
		
		# define the popup window
		top = self.top = Tkinter.Toplevel(parent)
		
		self.delete_all_agent_results_label = ttk.Label(self.top, text = "CAUTION: Are you sure you would like to Delete All Agent Results?")
		self.delete_all_agent_results_label.grid(row=0,column=0,sticky=W,padx=10,pady=10,columnspan=10)
		
		self.delete_all_agent_results_action_button = ttk.Button(self.top,text = "Delete All Agent Results",command=self.send)
		self.delete_all_agent_results_action_button.grid(row=1,column=0,sticky=NSEW,padx=10,pady=10)
		
		self.delete_all_agent_results__cancel_button = ttk.Button(self.top,text = "Cancel", command = self.top.destroy)
		self.delete_all_agent_results__cancel_button.grid(row=1,column=1,sticky=NSEW,padx=10,pady=10)
		
	def send(self):
		
		self.delete_all_results = True
		self.top.destroy()

# clear queued taskings for the agent POPUP
class api_clear_que_task_popup:
	
	def __init__(self,parent,agent_name):
		
		# define the remove_agent check boolean
		self.clear_que_results = False
		
		# define the popup window
		top = self.top = Tkinter.Toplevel(parent)
		
		self.clear_que_task_label = ttk.Label(self.top, text = "CAUTION: Are you sure you would like to Clear Queued Taskings for " + agent_name + "?")
		self.clear_que_task_label.grid(row=0,column=0,sticky=W,padx=10,pady=10,columnspan=10)
		
		self.clear_que_task_action_button = ttk.Button(self.top,text = "Clear Queued Tasks",command=self.send)
		self.clear_que_task_action_button.grid(row=1,column=0,sticky=NSEW,padx=10,pady=10)
		
		self.clear_que_task__cancel_button = ttk.Button(self.top,text = "Cancel", command = self.top.destroy)
		self.clear_que_task__cancel_button.grid(row=1,column=1,sticky=NSEW,padx=10,pady=10)
		
	def send(self):
		
		self.clear_que_results = True
		self.top.destroy()
	
# rename agent class POPUP
class api_rename_agent_popup:
	
	def __init__(self,parent):
	
		top = self.top = Tkinter.Toplevel(parent)
		
		self.rename_agent_label = ttk.Label(self.top, text = "New Agent Name: ")
		self.rename_agent_label.grid(row=0,column=0,sticky=W,padx=10,pady=10)
		
		self.rename_agent_entry = Tkinter.Entry(self.top,width=40)
		self.rename_agent_entry.grid(row=0,column=1,sticky=NW,padx=5,pady=5,columnspan=15)
		
		self.rename_agent_action_button = ttk.Button(self.top,text = "Rename Agent",command=self.send)
		self.rename_agent_action_button.grid(row=1,column=1,sticky=NW,padx=10,pady=10)
		
		self.rename_agent_cancel_button = ttk.Button(self.top,text = "Cancel", command = self.top.destroy)
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
				
		keys = [ "UserName", "Domain", "CredType", "Notes", "Host", "SID", "Password", "OS" ]
		
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
		
		# reporting by agent name choice dict
		self.reporting_agent_choices = []
		self.reporting_agent_choices.append("")
		
		# selected agent name for option execution
		self.selected_agent_name = ""
		
		# selected module name for option execution
		self.selected_module_name = ""
		
		# define the main form - super parent
		self.form = Tkinter.Tk()
		self.form.wm_title(' Empire RESTful API GUI ')
		self.form.resizable(0,0)
		
		
		###### ACTION TABS FRAME #######
		
		# application tabs notebook, child to the form, parent to the tabs
		self.nb = ttk.Notebook(self.form,height=475,width=1300)
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
		
		# Build the terminal window
		#self.termf = Tkinter.Frame(self.form,height=250)
		#self.termf.pack(fill=BOTH,expand=YES,padx=5)
		#self.termf_wid = self.termf.winfo_id()
		#os.system('xterm -into %d -geometry 250x15 -fa Monospace -sb -fs 11 -bg black -fg white &' % self.termf_wid)
							
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
		self.api_connection_lframe = Tkinter.LabelFrame(self.admin_api, text=" API Authentication: ")
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
		self.api_action_get_session_button = Tkinter.Button(self.api_connection_lframe,text="Session Token",command=self.api_get_session)
		self.api_action_get_session_button.config(fg='white',bg='blue',font=('arial','10','bold'))
		self.api_action_get_session_button.grid(row=3,column=2,sticky=W,padx=5,pady=5)
				
		##### CONNECTION INFO FRAME ##############
		
		##### API ACTION FRAME ##############
		self.api_action_lframe = Tkinter.LabelFrame(self.admin_api, text=" API Actions: ")
		self.api_action_lframe.grid(row=0,column=1,padx=10,pady=5,sticky=NW,rowspan=2)
		
		# Get Permanent Session Token
		self.api_action_get_perm_session_button = Tkinter.Button(self.api_action_lframe,text="Permanent Session Token",command=self.api_get_perm_session)
		self.api_action_get_perm_session_button.config(state="disabled",fg='white',bg='green',font=('arial','10','bold'))
		self.api_action_get_perm_session_button.grid(row=1,column=0,sticky=W,padx=5,pady=5)
		
		# Restart RESTful API Server
		self.api_action_restart_api_button = Tkinter.Button(self.api_action_lframe,text="Restart API Server",command=self.api_restart_api_server)
		self.api_action_restart_api_button.config(state="disabled",fg='white',bg='red',font=('arial','10','bold'))
		self.api_action_restart_api_button.grid(row=2,column=0,sticky=W,padx=5,pady=5)
		
		# Shutdown RESTful API Server
		self.api_action_shutdown_api_button = Tkinter.Button(self.api_action_lframe,text="Shutdown API Server",command=self.api_shutdown_api_server)
		self.api_action_shutdown_api_button.config(state="disabled",fg='white',bg='red',font=('arial','10','bold'))
		self.api_action_shutdown_api_button.grid(row=3,column=0,sticky=W,padx=5,pady=5)
		
		##### API ACTION FRAME ##############

		######## API CONFIG INFO FRAME #############
		self.api_config_lframe = Tkinter.LabelFrame(self.admin_api, text=" API Configuration: ")
		self.api_config_lframe.grid(row=1,column=0,columnspan=2,padx=10,pady=5,sticky=NW)
		
		self.api_config_textbox = ScrolledText(self.api_config_lframe,width=75,height=12)
		self.api_config_textbox.config(bg='ivory',state="disabled")
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
		
		self.listener_options_lframe = Tkinter.Frame(self.listeners_api)
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
		self.listener_all_treeview = ttk.Treeview(self.listener_options_lframe,height=10)
		self.listener_all_treeview.heading("#0",text="     Current Listeners:     ")
		self.listener_all_treeview.column("#0",minwidth="0",width="250")
		
		# Bind to Action
		self.listener_all_treeview.bind("<Double-1>", self.api_get_listener_by_name)
		self.listener_all_treeview.grid(row=2,column=0,sticky=NW,padx=5,pady=5)
		
		
		# ---------- Refresh Button----------#
		self.listener_refresh_button = Tkinter.Button(self.listener_options_lframe,text="  Refresh List  ",command=self.api_get_current_listeners)
		self.listener_refresh_button.config(state="normal",fg='white',bg='green',font=('arial','10','bold'))
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
		
		self.stagers_options_lframe = Tkinter.Frame(self.stagers_api)
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
		self.agents_current_treeview = ttk.Treeview(self.agents_current_options_lframe,height=10)
		self.agents_current_treeview.heading("#0",text="     Current Agents:     ")
		
		# Bind to Action and Grid
		self.agents_current_treeview.bind("<Double-1>", self.api_get_agent_by_name)
		self.agents_current_treeview.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
		
		# ---------- Refresh Current Agents----------#
		self.agents_current_refresh_button = Tkinter.Button(self.agents_current_options_lframe,text="  Refresh List  ",command=self.api_get_current_agents)
		self.agents_current_refresh_button.config(fg='white',bg='green',font=('arial','10','bold'))
		self.agents_current_refresh_button.grid(row=1,column=0,sticky=N,padx=5,pady=5)
		
		###### List STALE AGENTS ############
		self.agents_stale_treeview = ttk.Treeview(self.agents_current_options_lframe,height=5)
		self.agents_stale_treeview.heading("#0",text="     Stale Agents:     ")
		self.agents_stale_treeview.grid(row=3,column=0,sticky=NW,padx=5,pady=5)
		
		# ---------- Remove Stale Agents----------#
		self.agents_stale_remove_button = Tkinter.Button(self.agents_current_options_lframe,text="  Remove Stale Agents  ",command=self.api_get_remove_stale_agents)
		self.agents_stale_remove_button.config(fg='white',bg='red',font=('arial','10','bold'))
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
		self.modules_all_treeview = ttk.Treeview(self.modules_options_lframe,height=18)
		self.modules_all_treeview.heading("#0",text="     Modules:     ")
		self.modules_all_treeview.column("#0",minwidth="0",width="540")

		# Bind to Action
		self.modules_all_treeview.bind("<Double-1>", self.api_get_module_by_name)
		self.modules_all_treeview.grid(row=0,column=0,sticky=NW,padx=5,pady=5,rowspan=2,columnspan=3)
		
		# view all modules button
		self.modules_view_all_button = Tkinter.Button(self.modules_options_lframe,text="View All Modules",command=self.api_get_current_modules)
		self.modules_view_all_button.grid(row=2,column=0,sticky=W,padx=5,pady=5)
		
		# search entry and search button
		self.modules_search_str = Tkinter.StringVar()
		self.modules_search_field = Tkinter.Entry(self.modules_options_lframe,textvariable=self.modules_search_str,width=25)
		self.modules_search_field.grid(row=2,column=1,sticky=W,padx=5,pady=5) 
		
		self.modules_search_button = Tkinter.Button(self.modules_options_lframe,text="Search Modules",command=self.api_search_for_module)
		self.modules_search_button.config(fg='white',bg='green',font=('arial','10','bold'))
		self.modules_search_button.grid(row=2,column=2,sticky=W,padx=5,pady=5)
		
		
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
		
		##### REPORTING MAIN FRAME ##############
		
		self.reporting_main_lframe = Tkinter.LabelFrame(self.report_api,text="      Reporting Options:      ")
		self.reporting_main_lframe.grid(row=0,column=0,padx=5,pady=5,sticky=NW)
		
		# Reporting Type Radio Button
		self.reporting_type_int = IntVar()
		self.reporting_type_int.set(1)
		
		# 1. all events
		reporting_type_all_events = Radiobutton(self.reporting_main_lframe,text="Get All Logged Events",variable=self.reporting_type_int,value=1)
		reporting_type_all_events.config(command=self.misc_reporting_type_option_select)
		reporting_type_all_events.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
		
		
		# 2. agent events
		reporting_type_agent_events = Radiobutton(self.reporting_main_lframe,text="Get Agent Logged Events",variable=self.reporting_type_int,value=2)
		reporting_type_agent_events.config(command=self.misc_reporting_type_option_select)
		reporting_type_agent_events.grid(row=1,column=0,sticky=NW,padx=5,pady=5)
		
		# global reporting agent field string
		self.reporting_agent_field_str = Tkinter.StringVar()
		
		# build the agent drop down menu
		holder = []
		holder = self.reporting_agent_choices
				
		self.reporting_agent_option_menu = Tkinter.OptionMenu(self.reporting_main_lframe,self.reporting_agent_field_str,*holder,command=self.misc_set_reporting_agent_field_str)
		self.reporting_agent_option_menu.grid(row=1,column=1,sticky=NW,padx=5,pady=5)
		self.reporting_agent_option_menu.config(state="disabled")
		
		
		# 3. specific type events
		reporting_type_specifictype = Radiobutton(self.reporting_main_lframe,text="Get Logged Events of Specific Type",variable=self.reporting_type_int,value=3)
		reporting_type_specifictype.config(command=self.misc_reporting_type_option_select)
		reporting_type_specifictype.grid(row=2,column=0,sticky=NW,padx=5,pady=5)
		
		# global reporting type field string
		self.reporting_type_field_str = Tkinter.StringVar()
		
		# build the type drop down menu
		choices = ['checkin','task','result']
		self.reporting_type_option_menu = Tkinter.OptionMenu(self.reporting_main_lframe,self.reporting_type_field_str,*choices,command=self.misc_set_reporting_type_field_str)
		self.reporting_type_option_menu.grid(row=2,column=1,sticky=NW,padx=5,pady=5)
		self.reporting_type_option_menu.config(state="disabled")
		
		
		# 4. specific msg events
		reporting_type_specificmsg = Radiobutton(self.reporting_main_lframe,text="Get Logged Events w/ Specific Msg",variable=self.reporting_type_int,value=4)
		reporting_type_specificmsg.config(command=self.misc_reporting_type_option_select)
		reporting_type_specificmsg.grid(row=3,column=0,sticky=NW,padx=5,pady=5)
		
		# Define reporting msg string
		self.reporting_msg_field_str = Tkinter.StringVar()
		
		self.reporting_type_specificmsg_entry = Tkinter.Entry(self.reporting_main_lframe,textvariable=self.reporting_msg_field_str,width=20)
		self.reporting_type_specificmsg_entry.grid(row=3,column=1,sticky=NW,padx=5,pady=5) 
		self.reporting_type_specificmsg_entry.config(state="disabled")
		
		
		#### INFO LABEL ######
		reporting_info_label = Tkinter.StringVar()	
		reporting_info_label.set("*  Use the Refresh button to update the Agent option menu.") 
		reporting_info_dlabel = Tkinter.Label(self.report_api,textvariable=reporting_info_label)
		reporting_info_dlabel.grid(row=1,column=0,padx=5,pady=5,sticky='nw')
		
		
		######### ACTIONS Main FRAME ##############
		
		reporting_actions_lframe = Tkinter.LabelFrame(self.report_api,text="      Reporting Actions:      ")
		reporting_actions_lframe.grid(row=2,column=0,padx=5,pady=5,sticky='nw')
		
		
		# ---------- Request Events----------#
		reporting_request_button = Tkinter.Button(reporting_actions_lframe,text="  Request Events  ",command=self.reporting_display_output)
		reporting_request_button.config(fg='white',bg='blue',font=('arial','10','bold'))
		reporting_request_button.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
		
		# ---------- Refresh Events----------#
		reporting_refresh_button = Tkinter.Button(reporting_actions_lframe,text="  Refresh Agents  ",command=self.misc_reporting_action_refresh)
		reporting_refresh_button.config(fg='white',bg='green',font=('arial','10','bold'))
		reporting_refresh_button.grid(row=0,column=1,sticky=NW,padx=5,pady=5)
    
    
    
		##### REPORTING OUTPUT ##############
		
		self.reporting_output_lframe = Tkinter.LabelFrame(self.report_api,text="      Reporting Output:      ")
		self.reporting_output_lframe.grid(row=0,column=1,padx=5,pady=5,sticky='nw',rowspan=20)
		
		cols = [ "EventType", "TimeStamp", "TaskID", "AgentName", "Message", "ID" ]

		self.reporting_tree = ttk.Treeview(self.reporting_output_lframe, columns=cols, show="headings",height="18")
		self.reporting_tree.bind("<Double-1>", self.misc_reporting_display_event_details)
		
		for c in cols:
			self.reporting_tree.heading(c, text=str(c), command=lambda x=c: self.misc_col_sort(self.reporting_tree, x, 0) )
			self.reporting_tree.column(c, width=tkFont.Font().measure(c.title() + " " * 14))
		
		self.reporting_tree.grid(row=0,column=0,padx=2,pady=2)
	
	# CREDENTIALS tab
	def build_credentials_tab(self):
		
		# creds main frame
		self.creds_output_lframe = Tkinter.LabelFrame(self.creds_api,text = "       Credentials Store     ")
		self.creds_output_lframe.grid(row=0,column=0,padx=10,pady=10,sticky=NW)
		
		# refresh button
		self.creds_refresh_button = Button(self.creds_output_lframe,text="Refresh Creds",command=self.api_get_stored_credentials)
		self.creds_refresh_button.config(fg='white',bg='green',font=('arial','10','bold'))
		self.creds_refresh_button.grid(row=0,column=0,padx=5,pady=5,sticky=NW)
		
		# label info
		self.creds_label_info = Label(self.creds_output_lframe,text="* Double-click Credential row to view details in separate window.")
		self.creds_label_info.grid(row=1,column=0,padx=5,pady=5,sticky=NW)
		
		# build creds treeview
		cols = [ "UserName", "Domain", "CredType", "Notes", "Host", "SID", "Password", "OS" ]
		
		self.creds_tree = ttk.Treeview(self.creds_output_lframe, columns=cols, show="headings",height="15")
		self.creds_tree.bind("<Double-1>", self.misc_creds_display_event_details)
		
		for c in cols:
			self.creds_tree.heading(c, text=str(c), command=lambda x=c: self.misc_col_sort(self.creds_tree, x, 0))
			self.creds_tree.column(c, width=tkFont.Font().measure(c.title() + " " * 21))
		
		self.creds_tree.grid(row=2,column=0,padx=2,pady=2)
		
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
						
			else:
				tkMessageBox.showerror("ERROR","Unable to retrieve Session Token with provided authentication info:" + response)
				
	# get permanent token
	def api_get_perm_session(self):
		
		# get the permanent token
		if self.eac_object.admin_get_perm_token():
			
			# set the request token field
			self.api_request_token_str.set(self.eac_object.api_request_token)
		
	# restart the api server
	def api_restart_api_server(self):
	
		if tkMessageBox.askyesno("Restart API","Are you sure you want to restart the API?"):
	
			# restart api server call
			response = self.eac_object.admin_restart_restful_api_server()

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
			
		except:
			
			tkMessageBox.showerror("ERROR","An error has occurred defining selected listener.")
			
			return
			
		# call to the api with listener name
		response = self.eac_object.listeners_get_listener_by_name(listener_name)
			
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
			self.temp_labelframe = Tkinter.LabelFrame(self.listeners_api_canvas,text="Listener Options for: " + listener_name)
			self.listeners_api_canvas.create_window(0,10,window=self.temp_labelframe,anchor=NW)
					
			# display the kill listener and kill all listeners buttons
			# ---------- Kill Listener Button----------#
			listener_kill_button = Tkinter.Button(self.temp_labelframe,text="Kill Listener",command=self.api_delete_kill_listener)
			listener_kill_button.config(fg='white',bg='red',font=('arial','10','bold'))
			listener_kill_button.grid(row=0,column=1,sticky=NW,padx=2,pady=2)
			
		
			# ---------- Kill All Listener Button----------#
			listener_kill_all_button = Tkinter.Button(self.temp_labelframe,text="Kill All Listeners",command=self.api_delete_kill_all_listeners)
			listener_kill_all_button.config(fg='white',bg='red',font=('arial','10','bold'))
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
						self.option_entry_field = Tkinter.Entry(self.temp_labelframe,textvariable=self.option_field_str,width=30)
						self.option_entry_field.config(state="disabled",disabledbackground='ivory',disabledforeground='black')
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
							self.option_entry_field = Tkinter.Entry(self.temp_labelframe,textvariable=self.option_field_str,width=30)
							self.option_entry_field.config(state="disabled",disabledbackground='ivory',disabledforeground='black')
							self.option_entry_field.grid(row=row_count,column=1,columnspan=2,sticky=W,padx=2,pady=2)
							
							# Option Description
							self.option_description_str = Tkinter.StringVar()
							self.option_description_str.set(str(description_str))
							self.option_description_dlabel = Tkinter.Label(self.temp_labelframe,textvariable=self.option_description_str,wraplength=400,justify=LEFT)
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
			
		# parsing was successful
		try:
			
			# try to destory previous temp_labelframe if it exists
			try:
				for child in self.listeners_api_canvas.winfo_children():
					child.destroy()
			except:
				pass

			
			# define the temp labelframe
			self.temp_labelframe = Tkinter.LabelFrame(self.listeners_api_canvas,text="     " + str(self.listener_type_treeview.item(self.selected_item,"text")) + " Listener Options:       ")
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
					
					option_field = Tkinter.Entry(self.temp_labelframe,textvariable=temp_field_str,width=30)
					option_field.grid(row=row_count,column=1,sticky=W,padx=2,pady=2)
					option_field.config(background="wheat") 
					
				else:
					temp_field_str = Tkinter.StringVar()
					temp_field_str.set(str(val))
					entry_field = Tkinter.Entry(self.temp_labelframe,textvariable=temp_field_str,width=30)
					entry_field.grid(row=row_count,column=1,sticky=W,padx=2,pady=2) 
	 				 			
				# Option Description
				description_label = Tkinter.Label(self.temp_labelframe,text=str(description_str),wraplength=400,justify=LEFT)
				description_label.grid(row=row_count,column=2,sticky=W,padx=2,pady=2)
	
				
				# increment the row count
				row_count += 1
				
			
		# parsing json failed
		except Exception as e:
			
			print "ERROR: Get Listener Type parse failed - " + str(e) + ": " + str(response),str(datetime.now())
			
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
			
			print "ERROR: Grabbing child items failed on Create Listener - " + str(e) + str(datetime.now())
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
			self.temp_stagers_details_labelframe = Tkinter.LabelFrame(self.temp_stagers_dynamic_coreframe,text="Stager Details for : " + str(stager_name) + "     ")
			self.temp_stagers_details_labelframe.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
			
			# build options temporary frame
			self.temp_stagers_options_labelframe = Tkinter.LabelFrame(self.temp_stagers_dynamic_coreframe,text="Stager Options for : " + str(stager_name) + "     ")
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
					if (key == "Name") or \
					   (key == "Description"):
						   
						# Option Name
						name_label = Tkinter.Label(self.temp_stagers_details_labelframe,text=key + ": ",justify=LEFT)
						name_label.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
				
						# Option Field Value
						field_label = Tkinter.Label(self.temp_stagers_details_labelframe,text=str(value),wraplength=600,justify=LEFT)
						field_label.grid(row=row_count,column=1,sticky=W,padx=2,pady=2)
												
						# increment the row count
						row_count += 1
						
					elif (key == "Author"):
							 
						# Option Name
						name_label = Tkinter.Label(self.temp_stagers_details_labelframe,text=str(key) + ": ",justify=LEFT)
						name_label.grid(row=row_count,column=0,sticky=E,padx=2,pady=2)
						
						 # Option Field Value
						authors = ""
													
						# grab the list values
						for i in value:
							authors += str(i) + " "
							
						# grid the field dlablel
						field_label = Tkinter.Label(self.temp_stagers_details_labelframe,text=authors,wraplength=600,justify=LEFT)
						field_label.grid(row=row_count,column=1,sticky=W,padx=2,pady=2)
						
						# increment the row count
						row_count += 1
				
					elif (key == "Comments"):
							 
						# Option Name
						name_label = Tkinter.Label(self.temp_stagers_details_labelframe,text=str(key) + ": ",justify=LEFT)
						name_label.grid(row=row_count,column=0,sticky=NE,padx=2,pady=2)
												
						# Option Field Value
						comments = ""
						
						# grab the list values
						for i in value:
							comments += str(i) + " "
								
						# grid the field dlablel								
						field_label = Tkinter.Label(self.temp_stagers_details_labelframe,text=comments,wraplength=600,justify=LEFT)
						field_label.grid(row=row_count,column=1,sticky=NW,padx=2,pady=2)
						
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
									
									# list holding listener names, dropdown choices
									choices = []
									
									# if no listeners, append blank
									if len(response['listeners']) == 0: choices.append('');
								
									# else, grab name for each listener, append to choices list
									else:
								
										try:					
											for item in response['listeners']:
												choices.append(str(item['name']))
										
										except:
											print "ERROR: " + str(response) + str(datetime.now())
									
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
			print "ERROR: Get Current Agents failed." + str(e) + str(response) + str(datetime.now())
		
		### UPDATE - makes the call to api_get_stale_agents too
		self.api_get_stale_agents()
		
	# get current agents for reporting optionmenu
	def api_get_current_agents_reporting(self):
		
		# call to api function
		response = self.eac_object.reporting_get_all_logged_events()
		
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
			print "ERROR: Get Current Agents failed." + str(e) + str(response) + str(datetime.now())
		
	# get stale agents
	def api_get_stale_agents(self):
		
		# call to api function
		response = self.eac_object.agents_get_stale_agents()
		
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
			print "ERROR: Get Stale Agents failed." + str(e) + str(response) + str(datetime.now())
		
	# remove stale agents
	def api_get_remove_stale_agents(self):
		
		# call to api function
		self.eac_object.agents_remove_stale_agents()
		
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
			
		# parsing was successful
		try:
		
			# clear the frame
			try:
				for child in self.agent_info_action_lframe.winfo_children():
					child.destroy()
			except:
				pass
			
			# build temporary details frame
			self.temp_agent_labelframe = Tkinter.LabelFrame(self.agent_info_action_lframe,text="Agent Info for " + self.selected_agent_name)
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
						option_entry_field.config(state="disabled",disabledbackground='ivory',disabledforeground='black')
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
			
			self.task_agent_shell_popup_label = ttk.Label(self.temp_agent_results_labelframe, text = "SHELL CMD: ")
			self.task_agent_shell_popup_label.grid(row=0,column=0,sticky=E,padx=5,pady=5)
		
			self.task_agent_shell_entry = Tkinter.Entry(self.temp_agent_results_labelframe,width=40)
			self.task_agent_shell_entry.grid(row=0,column=1,sticky=W,padx=5,pady=5)
			
			self.task_agent_shell_action_button = Tkinter.Button(self.temp_agent_results_labelframe,text = "Execute",command=self.api_task_agent_run_shell_cmd)
			self.task_agent_shell_action_button.config(fg='white',bg='blue',font=('arial','10','bold'))
			self.task_agent_shell_action_button.grid(row=0,column=3,sticky=W,padx=2,pady=2)
			

			self.temp_RefreshButton = Tkinter.Button(self.temp_agent_results_labelframe,text="Refresh Results",command= lambda: self.api_get_agent_results(self.selected_agent_name))
			self.temp_RefreshButton.config(fg='white',bg='green',font=('arial','10','bold'))
			self.temp_RefreshButton.grid(row=0,column=4,sticky=W,padx=2,pady=2)
		
			self.temp_agents_results_scrolledtext = ScrolledText(self.temp_agent_results_labelframe,height=15,width=145)
			self.temp_agents_results_scrolledtext.config(bg='ivory')
			self.temp_agents_results_scrolledtext.grid(row=1,column=0,columnspan=15,sticky='NEWS',padx=2,pady=2)
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
			
			# blank command value
			else:
				print "ERROR: No Command entered to run on All Agents " + self.selected_agent_name + "." + str(datetime.now())

		except:
			pass

	# get agent results
	def api_get_agent_results(self,agent):
		
		try:
		 
			# call to the api with listener name
			response = self.eac_object.agents_get_agent_results(agent)
			
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
			
	# delete all agent results
	def api_delete_all_agent_results(self):
	
		# create instance of remove agent results dialog window
		delete_all_results_dialog = api_delete_all_agent_results_popup(self.form)
		self.form.wait_window(delete_all_results_dialog.top)
		
		# check if delete all results boolean True, if so delete all results
		if delete_all_results_dialog.delete_all_results:
			
			# call to api function
			self.eac_object.agents_delete_all_agent_results()
						
	# clear queued agent taskings
	def api_clear_queued_agent_taskings(self):
	
		# create instance of clear queue dialog window
		clear_que_dialog = api_clear_que_task_popup(self.form,self.selected_agent_name)
		self.form.wait_window(clear_que_dialog.top)
		
		# check if remove_agent boolean True, if so remove agent
		if clear_que_dialog.clear_que_results:
			
			# call to api function
			self.eac_object.agents_clear_queued_agent_tasking(self.selected_agent_name)
			

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
						print "ERROR: Rename Agent failed for " + self.selected_agent_name + ": " + str(response['success']) + str(datetime.now())
			
				# request bombed
				except Exception as e:
				
					print "ERROR: Rename Agent failed - " + str(e) + " : " + str(response) + str(datetime.now())

			# blank command or invalid value
			else:
				print "ERROR: Blank or invalid new Name value for " + self.selected_agent_name + "." + str(datetime.now())
		
		# handles the cancel action
		except Exception as e:
			pass

	# kill agent
	def api_kill_agent(self):
		
		# create instance of remove agent dialog window
		kill_dialog = api_kill_agent_popup(self.form,self.selected_agent_name)
		self.form.wait_window(kill_dialog.top)
		
		# check if remove_agent boolean True, if so remove agent
		if kill_dialog.kill_agent:
			
			# call to api function
			response = self.eac_object.agents_kill_agent(self.selected_agent_name)
			
			try:
				# kill was successful
				if response['success']:
				
					# rerun the get current agents
					self.api_get_current_agents()
			
				# kill failed
				else:
					print "ERROR: Attempt to Kill Agent " + self.selected_agent_name + ": " + str(response['success']) +str(datetime.now())
		
	
			# request bombed
			except Exception as e:
		
				print "ERROR: Killing Agent failed - " + str(e) + " : " + str(response) + str(datetime.now())
	
	# kill all agents
	def api_kill_all_agents(self):
		
		
		# create instance of remove agent dialog window
		kill_all_dialog = api_kill_all_agents_popup(self.form)
		self.form.wait_window(kill_all_dialog.top)
		
		# check if remove_agent boolean True, if so remove agent
		if kill_all_dialog.kill_all_agents:
			
			# call to api function
			response = self.eac_object.agents_kill_all_agents()
			
			try:
				# kill all was successful
				if response['success']:
				
					# rerun the get current agents
					self.api_get_current_agents()
			
				# kill failed
				else:
					print "ERROR: Attempt to Kill All Agents : " + str(response['success']) + str(datetime.now())
		
	
			# request bombed
			except Exception as e:
		
				print "ERROR: Killing All Agents failed - " + str(e) + " : " + str(response) + str(datetime.now())
	
		
	####### MODULES FUNCTIONS #############
	
	# get current modules
	def api_get_current_modules(self):
		
		# call to api function
		response = self.eac_object.modules_get_current_modules()
		
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
			print "ERROR: Get Current Modules failed." + str(e) + str(response) + str(datetime.now())
		
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
			self.temp_modules_details_labelframe = Tkinter.LabelFrame(self.temp_modules_dynamic_coreframe,text="Module Details for : " + str(self.selected_module_name) + "     ")
			self.temp_modules_details_labelframe.grid(row=0,column=0,sticky=NW,padx=5,pady=5)
			
			# build options temporary frame
			self.temp_modules_options_labelframe = Tkinter.LabelFrame(self.temp_modules_dynamic_coreframe,text="Module Options for : " + str(self.selected_module_name) + "     ")
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
					   (key == "Description") or \
					   (key == "Background") or \
					   (key == "MinPSVersion") or \
					   (key == "NeedsAdmin") or \
					   (key == "OpsecSafe") or \
					   (key == "OutputExtension"):
						   
						# Option Name
						name_label = Tkinter.Label(self.temp_modules_details_labelframe,text=str(key) + ": ")
						name_label.grid(row=row_count,column=0,sticky=NE)
				
						# Option Field Value
						field_label = Tkinter.Label(self.temp_modules_details_labelframe,text=str(value),wraplength=580,justify=LEFT)
						field_label.grid(row=row_count,column=1,sticky=NW)
												
						# increment the row count
						row_count += 1
					
					elif (key == "Author"):
							 
						# Option Name
						name_label = Tkinter.Label(self.temp_modules_details_labelframe,text=str(key) + ": ")
						name_label.grid(row=row_count,column=0,sticky=NE)
						
						 # Option Field Value
						authors = ""							
						
						# grab the list values
						for i in value:
							authors += i + " " 
							
						# grid the field dlablel
						field_label = Tkinter.Label(self.temp_modules_details_labelframe,text=str(authors),wraplength=580,justify=LEFT)
						field_label.grid(row=row_count,column=1,sticky=NW)
						
						# increment the row count
						row_count += 1
					
					elif (key == "Comments"):
							 
						# Option Name
						name_label = Tkinter.Label(self.temp_modules_details_labelframe,text=str(key) + ": ")
						name_label.grid(row=row_count,column=0,sticky=NE)
												
						# comment string
						comments = "" 
						 
						# grab the list values
						for i in value:
							comments += i + " "
								
						# grid the field dlablel								
						field_label = Tkinter.Label(self.temp_modules_details_labelframe,text=str(comments),wraplength=580,justify=LEFT)
						field_label.grid(row=row_count,column=1,sticky=NW)
						
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
									response = self.eac_object.agents_get_current_agents()
									
									# list holding listener names, dropdown choices
									choices = []
									
									# if no listeners, append blank
									if len(response['agents']) == 0: choices.append('');
								
									# else, grab name for each listener, append to choices list
									else:
								
										try:
									
											for item in response['agents']:
										
												choices.append(str(item['name']))
										
										except Exception as e:
											tkMessageBox.showerror("ERROR","Creating Agent optionmenu for Modules tab: " + str(e))
									
									# build the drop down menu
									option_agent_field = Tkinter.OptionMenu(self.temp_modules_options_labelframe,self.option_agent_field_str,*choices,command=self.misc_set_modules_agent_field_str)
									option_agent_field.grid(row=row_count,column=1,sticky=NW,padx=1,pady=1)
									option_agent_field.config(background="wheat",width=25)
								
								
								# add drop down for Listener value
								elif key2 == "Listener":
									
									# grid universal Listener drop down
									response = self.eac_object.listeners_get_current_listeners()
									
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
											tkMessageBox.showerror("ERROR","Creating Listener optionmenu for Modules tab: " + str(e))
									
									# build the drop down menu
									option_listener_field = Tkinter.OptionMenu(self.temp_modules_options_labelframe,self.option_listener_field_str,*choices,command=self.misc_set_modules_listener_field_str)
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
						vals.append(self.option_agent_field_str.get())
						
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
						
						print "ERROR: Required field missing - " +  str(self.temp_module_keys_list[i]) + str(datetime.now())
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
			
		except Exception as e:
			print "ERROR: Execute Module JSON Parse failed. " + str(response) + str(e) + str(datetime.now())
			
				
	####### REPORTING FUNCTIONS ############
		
	# display report output 
	def reporting_display_output(self):

		# get the value of the IntVar for the reporting radio buttons
		selection = str(self.reporting_type_int.get())
		
		# all event option selected
		if selection == "1":
			
			# make call to api
			response = self.eac_object.reporting_get_all_logged_events()
			
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
				print "ERROR: Error parsing Get All Events - " + str(e) + " : " + str(response) + str(datetime.now())
			
		
		# agent event option selected
		elif selection == "2":
			
			# grab the agent option menu value
			agent_name = self.reporting_agent_field_str.get()
			
			# check agent name not blank
			if agent_name != "":
			
				# make call to api
				response = self.eac_object.reporting_get_agent_logged_events(agent_name)
				
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
					print "ERROR: Error parsing Get Agent Events - " + str(e) + " : " + str(response) + str(datetime.now())
		
			# agent name is blank
			else:
				print "ERROR: Please select an Agent Name for request." + str(datetime.now())
		
		
		# type event option selected
		elif selection == "3":
			
			# grab the type option menu value
			type_name = self.reporting_type_field_str.get()
			
			# check type name not blank
			if type_name != "":
			
				# make call to api
				response = self.eac_object.reporting_get_logged_events_of_specific_type(type_name)
				
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
					print "ERROR: Error parsing Get Type Events - " + str(e) + " : " + str(response) + str(datetime.now())
		
			# type name is blank
			else:
				print "ERROR: Please select an Event Type for request." + str(datetime.now())
			
		
		# msg event option selected
		elif selection == "4":
			
			# grab the msg value
			msg_value = str(self.reporting_msg_field_str.get())
			
			# check msg not blank
			if msg_value != "":
			
				# make call to api
				response = self.eac_object.reporting_get_logged_events_with_specific_msg(msg_value)
				
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
					print "ERROR: Error parsing Msg Events - " + str(e) + " : " + str(response) + str(datetime.now())
		
			# agent name is blank
			else:
				print "ERROR: Please a Msg keyword for the request." + str(datetime.now())


	######### CREDENTIAL FUNCTIONS #######
	def api_get_stored_credentials(self):
		
		# make call to api
		response = self.eac_object.creds_get_stored_credentials()
			
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
			print "ERROR: Error parsing Get Credentials - " + str(e) + " : " + str(response) + str(datetime.now())

	
	####### ERROR HANDLING AND RESET FUNCTIONS #############
	
	# Error Checking - Admin / API Authentication Function
	def error_check_api_auth_fields(self):
		
		# attempt to set values
		# return if value missing and log
		if not self.eac_object.api_set_username(self.api_username_str.get()):
			print "ERROR: Please enter a value for Username." + str(datetime.now())
			return False
		
		elif not self.eac_object.api_set_password(self.api_password_str.get()):
			print "ERROR: Please enter a value for Password." + str(datetime.now())
			return False
			
		elif not self.eac_object.api_set_host(self.api_host_str.get()):
			print "ERROR: Please enter a value for Host." + str(datetime.now())
			return False
			
		elif not self.eac_object.api_set_port(self.api_port_str.get()):
			print "ERROR: Please enter a value for Port." + str(datetime.now())
			return False
		
		else: return True
	
	###### MISC FUNCTIONS
	
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
			print "ERROR: Exception on Report Event click: " + str(e) + str(datetime.now())
	
	
	# Credentials Misc
	
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
			print "ERROR: Exception on Credentials Event click: " + str(e) + str(datetime.now())
	
	# Universal Misc
	def misc_col_sort(self,tree,col,descending):
	
		# grab the data to sort
		data = [(tree.set(child, col), child) \
			for child in tree.get_children('')]
			
		# sort the data data in place
		data.sort(reverse=descending)
		for ix, item in enumerate(data):
			tree.move(item[1], '', ix)
			
		
	
	###### START APPLICATION #######
	
	def start_application(self):
		self.form.mainloop() 

		
if __name__ == '__main__':
	
	vader()
