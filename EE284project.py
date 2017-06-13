import sys
import time
import threading
import os
import pjsua as p

# Method to print logs
def log_cb(level, str, len):

    print(str),

# SIP Account Callback class to get registration notifications for the account
class SIPAccountCallback(p.AccountCallback):

    def __init__(self, account):

        p.AccountCallback.__init__(self, account)


    
try:

	#To create library instance
	lib=p.Lib()

	#To instantiate library
	lib.init(log_cfg = p.LogConfig(level=3, callback=log_cb))

	#To create a transport object
	t_conf = p.TransportConfig()

	#Setting the port number for transport object
	t_conf.port = 5060

	#Getting the client ip address automatically from the system
    	f = os.popen('ifconfig eth0 | grep "inet\ addr" | cut -d: -f2 | cut -d" " -f1')
    	client_ip=f.read()
    
	#Bounding the transport to the client IP address
	t_conf.bound_addr = client_ip
    
	#creating a transport
	trans = lib.create_transport(p.TransportType.UDP,t_conf)

	#Starting the library instance
	lib.start()
	
    #Storing the command line arguments to the python variables
	server_ip= sys.argv[1] 
	user= sys.argv[2] 
	passwd= sys.argv[3]
	client=sys.argv[4]
        
	print "The Client IP address is "+client_ip;
	print "The Asterisk server IP address is "+server_ip
	print "The User name is "+user
	
	#Configuration of Account class to register with the server

	aconf = p.AccountConfig(domain = server_ip, username = user, password =passwd, display = user)
	aconf.id ="sip:"+user
	aconf.reg_uri ='sip:'+user+':5060'
	sip_callback = SIPAccountCallback(aconf)
	account = lib.create_account(aconf,cb=sip_callback)
	account.set_callback(sip_callback)

	#Printing the registration status and message
	
	print('Status= ',account.info().reg_status, \

		 '(' + account.info().reg_reason + ')')

	time.sleep(2)



	print('Status= ',account.info().reg_status, \

		 '(' + account.info().reg_reason + ')')
	
	time.sleep(2)
	#Registration is successfull only if the status is 200 
	if account.info().reg_status==200:
	  print "Registration is successfully completed"
	else:
	  print("\n")
	  print "Registration is failed as the number is not present in sip.conf!!"
          print("\n")
	  lib.destroy()
	  lib = None
	  sys.exit(1)

        
	print "\n"
	call=raw_input("Do you want to make a call ?   Y/N\n")

        
	if call=="y" or call=="Y":

	    # Initiate call if Y is pressed
		print("\n")
		dest="sip:"+client+"@"+server_ip+":"+str(t_conf.port)
		print "Making a call to "+client+"@"+server_ip+" through port "+str(t_conf.port)
		call_list=["2000","2010","2020"]
                client_str=str(client)
		user_str=str(user)
		
		#Make call only if the dialled number is registered
                if any(client_str in a for a in call_list):
            
		     if client_str != user_str:
		        call_dest = account.make_call(dest)
			print "Call Ringing"
			print "\n"
			time.sleep(3)
			 
			print('Press ENTER for unregistration')
		
			input = sys.stdin.readline().rstrip('\r\n')



			# shutdown the library and do the unregistration

			lib.destroy()

			lib = None
		  	sys.exit(2)
                     else:
			print("\n")
			print "Dialled and Dialling number are same. So cannot make a call!"
			print("\n")
                        lib.destroy()

			lib = None
		  	sys.exit(2)
                else:
		 	print("\n")
			print "Dialled number is not registered!!"
			print("\n")
			lib.destroy()

			lib = None
		  	sys.exit(2)
                   
	else:

		lib.destroy()
		lib = None
		sys.exit(3)
except p.Error, e:

    	print("Exception: " + str(e))

   	lib.destroy()

    	lib = None

    	sys.exit(4)



except KeyboardInterrupt:
    
	print("\n")
        print("Program is interrupted.")

   	lib.destroy()

    	lib = None

    	sys.exit(5)
except IndexError:
	print("\n")
	print("Exiting the program due to incorrect number of arguments.Can enter only 4 argments in the order serverip,username,password,clientip ")

   	lib.destroy()

    	lib = None

    	sys.exit(6)

