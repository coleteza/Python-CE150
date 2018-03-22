#!/usr/bin/python
#Cole Teza 1361038
#cteza@ucsc.edu


from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
  def build(self):
    
    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all 
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts! 
    
    h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.0.1.10/24', defaultRoute="h1-eth0")
    h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.0.2.20/24', defaultRoute="h2-eth0")
    h3 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.0.3.30/24', defaultRoute="h3-eth0")
	#DATA CENTER
    h4 = self.addHost('h4',mac='00:00:00:00:00:04',ip='10.0.4.10/24', defaultRoute="h4-eth0")
	#CORE
    h5 = self.addHost('h5',mac='00:00:00:00:00:05',ip='172.16.10.100/24', defaultRoute="h5-eth0")
	

    # Create a switch. No changes here from Lab 1.
    s1 = self.addSwitch('s1')
    s2 = self.addSwitch('s2')
    s3 = self.addSwitch('s3')
	
    s4 = self.addSwitch('s4')# Switch for Data Center
    s5 = self.addSwitch('s5')# Main Core Switch

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on 
    # Host 2. This is representing the physical port on the switch or host that you are 
    # connecting to.
	
    self.addLink(h1,s1, port1=0, port2=1)
    self.addLink(h2,s2, port1=0, port2=2)
    self.addLink(h3,s3, port1=0, port2=3)

    self.addLink(h4,s4, port1=0, port2=4)
    self.addLink(h5,s5, port1=0, port2=5)

    self.addLink(s5,s1, port1=1, port2=2)
    self.addLink(s5,s2, port1=2, port2=3)
    self.addLink(s5,s3, port1=3, port2=4)
    self.addLink(s5,s4, port1=4, port2=5)

def configure():
  topo = final_topo()
  net = Mininet(topo = topo, controller = RemoteController)
  net.start()

  CLI(net)
  
  net.stop()

if __name__ == '__main__':
  configure()
