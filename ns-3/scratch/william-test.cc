/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "ns3/applications-module.h"
#include "ns3/core-module.h"
#include "ns3/internet-module.h"
#include "ns3/network-module.h"
#include "ns3/point-to-point-module.h"

#include "ns3/boolean.h"
#include "ns3/command-line.h"
#include "ns3/config.h"
#include "ns3/double.h"
#include "ns3/eht-phy.h"
#include "ns3/enum.h"
#include "ns3/internet-stack-helper.h"
#include "ns3/ipv4-address-helper.h"
#include "ns3/ipv4-global-routing-helper.h"
#include "ns3/log.h"
#include "ns3/mobility-helper.h"
#include "ns3/multi-model-spectrum-channel.h"
#include "ns3/on-off-helper.h"
#include "ns3/packet-sink-helper.h"
#include "ns3/packet-sink.h"
#include "ns3/rng-seed-manager.h"
#include "ns3/spectrum-wifi-helper.h"
#include "ns3/ssid.h"
#include "ns3/string.h"
#include "ns3/udp-client-server-helper.h"
#include "ns3/uinteger.h"
#include "ns3/wifi-acknowledgment.h"
#include "ns3/yans-wifi-channel.h"
#include "ns3/yans-wifi-helper.h"

#include <array>
#include <functional>
#include <numeric>

// Default Network Topology
//
//       10.1.1.0
// n0 -------------- n1
//    point-to-point
//

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("FirstScriptExample");

int
main(int argc, char* argv[])
{
    CommandLine cmd(__FILE__);
    cmd.Parse(argc, argv);

    Time::SetResolution(Time::NS);
    LogComponentEnable("UdpEchoClientApplication", LOG_LEVEL_INFO);
    LogComponentEnable("UdpEchoServerApplication", LOG_LEVEL_INFO);


    /////////////////////////////

    NodeContainer wifiStaNodes;
    wifiStaNodes.Create(10);   // Create 10 station node objects
    NodeContainer wifiApNode;
    wifiApNode.Create(1);   // Create 1 access point node object

    YansWifiChannelHelper wifiChannelHelper = YansWifiChannelHelper::Default();
    Ptr<Channel> wifiChannel = wifiChannelHelper.Create();
    
    YansWifiPhyHelper wifiPhyHelper;
    wifiPhyHelper.SetChannel(wifiChannel);

    // Create a WifiMacHelper, which is reused across STA and AP configurations
    WifiMacHelper mac;

    // Create a WifiHelper, which will use the above helpers to create
    // and install Wifi devices.  Configure a Wifi standard to use, which
    // will align various parameters in the Phy and Mac to standard defaults.
    WifiHelper wifi;
    wifi.SetStandard(WIFI_STANDARD_80211n);
    // Declare NetDeviceContainers to hold the container returned by the helper
    NetDeviceContainer wifiStaDevices;
    NetDeviceContainer wifiApDevice;

    // Perform the installation
    mac.SetType("ns3::StaWifiMac");
    wifiStaDevices = wifi.Install(phy, mac, wifiStaNodes);
    mac.SetType("ns3::ApWifiMac");
    wifiApDevice = wifi.Install(phy, mac, wifiApNode);

    /////////////////////////////


    // NodeContainer nodes;
    // nodes.Create(2);

    // PointToPointHelper pointToPoint;
    // pointToPoint.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
    // pointToPoint.SetChannelAttribute("Delay", StringValue("2ms"));

    // NetDeviceContainer devices;
    // devices = pointToPoint.Install(nodes);

    // InternetStackHelper stack;
    // stack.Install(nodes);

    // Ipv4AddressHelper address;
    // address.SetBase("10.1.1.0", "255.255.255.0");

    // Ipv4InterfaceContainer interfaces = address.Assign(devices);

    // UdpEchoServerHelper echoServer(9);

    // ApplicationContainer serverApps = echoServer.Install(nodes.Get(1));
    // serverApps.Start(Seconds(1.0));
    // serverApps.Stop(Seconds(10.0));

    // UdpEchoClientHelper echoClient(interfaces.GetAddress(1), 9);
    // echoClient.SetAttribute("MaxPackets", UintegerValue(1));
    // echoClient.SetAttribute("Interval", TimeValue(Seconds(1.0)));
    // echoClient.SetAttribute("PacketSize", UintegerValue(1024));

    // ApplicationContainer clientApps = echoClient.Install(nodes.Get(0));
    // clientApps.Start(Seconds(2.0));
    // clientApps.Stop(Seconds(10.0));

    Simulator::Run();
    Simulator::Destroy();
    return 0;
}
