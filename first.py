from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class LinuxRouter(Node):
    def config(self, **params):
        super(LinuxRouter, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(LinuxRouter, self).terminate()

class NetworkTopo(Topo):
    def build(self, **_opts):
        # Add 3 routers in a triangular fashion
        ra = self.addHost('ra', cls=LinuxRouter, ip='10.0.0.1/24')
        rb = self.addHost('rb', cls=LinuxRouter, ip='10.1.0.1/24')
        rc = self.addHost('rc', cls=LinuxRouter, ip='10.2.0.1/24')

        # Add 2 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add host-switch links
        h1 = self.addHost(name='h1', ip='10.0.0.2/24', defaultRoute='via 10.0.0.1')
        h2 = self.addHost(name='h2', ip='10.0.0.3/24', defaultRoute='via 10.0.0.1')
        h3 = self.addHost(name='h3', ip='10.1.0.2/24', defaultRoute='via 10.1.0.1')
        h4 = self.addHost(name='h4', ip='10.1.0.3/24', defaultRoute='via 10.1.0.1')
        h5 = self.addHost(name='h5', ip='10.2.0.2/24', defaultRoute='via 10.2.0.1')
        h6 = self.addHost(name='h6', ip='10.2.0.3/24', defaultRoute='via 10.2.0.1')

        # Add links between routers and switches
        self.addLink(s1, ra, intfName2='ra-eth1', params2={'ip': '10.0.0.1/24'})
        self.addLink(s2, rb, intfName2='rb-eth1', params2={'ip': '10.1.0.1/24'})
        self.addLink(s3, rc, intfName2='rc-eth1', params2={'ip': '10.2.0.1/24'})

        # Add links between routers for the triangular connection
        self.addLink(ra, rb, intfName1='ra-eth2', intfName2='rb-eth2', params1={'ip': '10.100.0.1/24'}, params2={'ip': '10.100.0.2/24'})
        self.addLink(rb, rc, intfName1='rb-eth3', intfName2='rc-eth2', params1={'ip': '10.101.0.1/24'}, params2={'ip': '10.101.0.2/24'})
        self.addLink(rc, ra, intfName1='rc-eth3', intfName2='ra-eth3', params1={'ip': '10.102.0.1/24'}, params2={'ip': '10.102.0.2/24'})

        # Add host-switch links
        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s2)
        self.addLink(h4, s2)
        self.addLink(h5, s3)
        self.addLink(h6, s3)


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)

    info(net['ra'].cmd("ip route add 10.2.0.0/24 via 10.102.0.1 dev ra-eth3"))
    info(net['ra'].cmd("ip route add 10.1.0.0/24 via 10.100.0.2 dev ra-eth2"))
    info(net['rb'].cmd("ip route add 10.2.0.0/24 via 10.101.0.2 dev rb-eth3"))
    info(net['rb'].cmd("ip route add 10.0.0.0/24 via 10.100.0.1 dev rb-eth2"))
    info(net['rc'].cmd("ip route add 10.0.0.0/24 via 10.102.0.2 dev rc-eth3"))
    info(net['rc'].cmd("ip route add 10.1.0.0/24 via 10.101.0.1 dev rc-eth2"))

    net.start()
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()

