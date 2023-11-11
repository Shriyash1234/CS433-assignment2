from mininet.net import Mininet
from mininet.topo import Topo

class MyTopo(Topo):
    def build(self):
        H1 = self.addHost('H1')
        H2 = self.addHost('H2')
        H3 = self.addHost('H3')
        H4 = self.addHost('H4')

        S1 = self.addSwitch('S1')
        S2 = self.addSwitch('S2')

        self.addLink(H1,S1, bw = 10000)
        self.addLink(H2,S1, bw = 10000)
        self.addLink(H3,S2, bw = 10000)
        self.addLink(H4,S2, bw = 10000)
        self.addLink(S1,S2,loss=3)

if __name__ == '__main__':
    from mininet.net import Mininet
    from mininet.cli import CLI
    from mininet.log import setLogLevel

    setLogLevel('info')

    topo = MyTopo()
    net = Mininet(topo=topo)

    net.start()
    CLI(net)
    net.stop()
