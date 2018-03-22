# Final Skeleton
#Cole Teza 1361038
#cteza@ucsc.edu
# Hints/Reminders from Lab 4:
# 
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the 
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):
    # This is where you'll put your code. The following modifications have 
    # been made from Lab 4:
    #   - port_on_switch represents the port that the packet was received on.
    #   - switch_id represents the id of the switch that received the packet
    #      (for example, s1 would have switch_id == 1, s2 would have switch_id == 2, etc...)
   
    dh = str(packet.dst)
    sh = str(packet.src)
    destination = -1
    source = -1

	# if Destintion host as reached 0 then revert to the last iteration 
    if '0' in dh:
	  #print "reached DH limit"
      destination = int(dh[-1])
    
    if '0' in sh:
	  #print "reached SH limit"
      source = int(sh[-1])
    
		#Search to see packet type does not contain ICMP before continuing 
		
    if packet.find("icmp")is None:
	
		#Search to see that the packet is of type ipv4 
		#This in a real world system would be checking 
		#whehter or not capsulation needs to occur 
		
	  if packet.find("ipv4") is None: 
	  
        #Given
	    msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
		
        #Given
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        msg.data = packet_in
        self.connection.send(msg)
	  
	 #Search to see packet type does contain ICMP before continuing 
	 
    elif packet.find("icmp"):

      if source == 5 or destination ==5:
		msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
		
        #Given
        self.connection.send(msg)

		#This case is port nunber is 5 (ie the 'CORE' then...)
		#if switch id is 5 AKA is CORE 
		
      elif switch_id ==5:
	  
        #Given
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
		
		#Given
        msg.actions.append(of.ofp_action_output(port = destination))
        msg.data = packet_in
        self.connection.send(msg)
       
		#If the switch port is not equal to host port 
      elif switch_id != source:
	  
        #Given
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
		
        #Given
        msg.actions.append(of.ofp_action_output(port = switch_id))
        msg.data = packet_in
        self.connection.send(msg)

      else:
        #Given
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
        msg.actions.append(of.ofp_action_output(port = switch_id + 1))
        msg.data = packet_in
        self.connection.send(msg)

		#Search to see that the packet is of type ipv4 
		#This in a real world system would be checking 
		#whehter or not capsulation needs to occur 		
		
    elif packet.find("ipv4"):
      
	  #If source is equal to Core and detination is equal to Data Center or vice versa
      if (source == 4 and destination == 5) or (source == 5 and destination == 4):
	  
         #Given
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
        self.connection.send(msg)
      
	  #if the switch is Data Center
      elif switch_id == 4:

         #Given
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
		
        #Given
        msg.actions.append(of.ofp_action_output(port = destination))
        msg.data = packet_in
        self.connection.send(msg)

      elif switch_id != source:

         #Given
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
		
        #Given
        msg.actions.append(of.ofp_action_output(port = switch_id))
        msg.data = packet_in
        self.connection.send(msg)

      else:
        
         #Given
        msg = of.ofp_flow_mod()
        msg.match = of.ofp_match.from_packet(packet)
        msg.idle_timeout = 30
        msg.hard_timeout = 30
		
        #Given
        msg.actions.append(of.ofp_action_output(port = switch_id + 1))
        msg.data = packet_in
        self.connection.send(msg)

    #print "Hello, World!"

  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
