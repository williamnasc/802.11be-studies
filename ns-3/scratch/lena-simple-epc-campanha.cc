/* -*-  Mode: C++; c-file-style: "gnu"; indent-tabs-mode:nil; -*- */
/*
 * Copyright (c) 2011-2018 Centre Tecnologic de Telecomunicacions de Catalunya (CTTC)
 *
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
 *
 * Authors: Jaume Nin <jaume.nin@cttc.cat>
 *          Manuel Requena <manuel.requena@cttc.es>
 */

#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/mobility-module.h"
#include "ns3/config-store-module.h"
#include "ns3/lte-module.h"
//#include "ns3/gtk-config-store.h"

#include "ns3/flow-monitor-module.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/flow-probe.h"

using namespace std;
using namespace ns3;

/**
 * Sample simulation script for LTE+EPC. It instantiates several eNodeBs,
 * attaches one UE per eNodeB starts a flow for each UE to and from a remote host.
 * It also starts another flow between each UE pair.
 */

NS_LOG_COMPONENT_DEFINE("LenaSimpleEpc");
std::ofstream m_TxTraceFile;
std::string m_TxTraceFileName;

void TraceSentPacket(std::string context, Ptr<const Packet > m_txTrace) {
//Vector position = model->GetPosition ();
//NS_LOG_UNCOND (context << "Time Tx: "
//              << Simulator::Now ().GetSeconds ()
//              << " Packet = " << m_txTrace);
    if (!m_TxTraceFile.is_open()) {
    	m_TxTraceFileName = "TxSentTrace.txt";
    	m_TxTraceFile.open(m_TxTraceFileName.c_str());
    	m_TxTraceFile << "Time" << std::endl;

    	if (!m_TxTraceFile.is_open()) {
    		NS_FATAL_ERROR("Could not open tracefile");
    	}
    }

    m_TxTraceFile << Simulator::Now() << std::endl;
}
// To be used in tic toc time counter
clock_t startTimer;
time_t beginTimer;

// Implementation of tic, i.e., start time counter
void tic() {
    beginTimer = time(&beginTimer);
    struct tm *timeinfo;
    timeinfo = localtime(&beginTimer);
    std::cout << "simulation start at: " << asctime(timeinfo) << std::endl;
}
// implementation of toc, i.e., stop time counter
    double toc() {
    time_t finishTimer = time(&finishTimer);
    double simTime = difftime(finishTimer, beginTimer) / 60.0;
    struct tm *timeinfo;
    timeinfo = localtime(&finishTimer);
    std::cout << "simulation finished at: " << asctime(timeinfo) << std::endl;
    //
    std::cout << "Time elapsed: " << simTime << " minutes" << std::endl;
    //
    return simTime;
}

int
main (int argc, char *argv[])
{
	string fadingEnd = "/home/wmcdnascimento/ns-3/ns-allinone-3.40/ns-3.40/src/lte/model/fading-traces";
	//string fadingEnd = "/home/wmcdnascimento/ns-3/ns-allinone-3.40/ns-3.40/src/lte/model/fading-traces";
/*string fadingEnd = "/home/marilia/ns-3.36/ns-allinone-3.36/ns-3.36/src/lte/model/fading-traces";*/
	string lambda = "0.25";
	uint32_t packetSize = 125;
	uint16_t numEnbs = 1;
	uint16_t numUes = 1;
	double appStartTime = 0.01;
	double simTime = 10.0;
	std::string ssimTime = to_string(simTime);
	std::string snumEnbs = to_string(numEnbs);
	std::string snumUes = to_string(numUes);
	Time interPacketInterval = MilliSeconds(100);
	double radius = 10.0;
	double distance = 20;
	bool useUdp = false;
	bool usePoisson = true;
	bool useShadowing = false;
	bool useFading = true;
	bool useDl = true;
	bool useUl = false;
	bool usePl = false;
	bool verbose = false;

	std::string outputDir = "./";
	std::string outputDir2 = "Results/";
	std::string NameFile;

	std::ifstream src;
	std::fstream dst;

	NameFile = "SimTime" + ssimTime + "ueNum" + snumUes + "enbNum" + snumEnbs;

	// Command line arguments
	CommandLine cmd;
	cmd.AddValue("lambda", "Lambda to be used in the model traffic", lambda);
	cmd.AddValue("packetSize", "Packet size (in bytes) to be used in the traffic with poisson distribution", packetSize);
	cmd.AddValue("numEnbs", "Number of eNodeBs", numEnbs);
	cmd.AddValue("numUes", "Number of UE", numUes);
	cmd.AddValue("simTime", "Total duration of the simulation", simTime);
	cmd.AddValue("distance", "Distance between eNBs [m]", distance);
	cmd.AddValue("interPacketInterval", "Inter packet interval",interPacketInterval);
	cmd.AddValue("radius", "Radius of the UE's distribution circle", radius);
	cmd.AddValue("distance", "Distance between eNodeBs", distance);
	cmd.AddValue("useUdp", "Use classic Udp traffic in the application",useUdp);
	cmd.AddValue("usePoisson", "Allow use of poisson distribution in the application", usePoisson);
	cmd.AddValue("useShadowing", "Disable the shadowing parameter of the propagation loss model", useShadowing);
	cmd.AddValue("useFading", "Disable the shadowing parameter of the propagation loss model", useFading);
	cmd.AddValue("useDl", "Disable downlink data flows", useDl);
	cmd.AddValue("useUl", "Disable uplink data flows", useUl);
	cmd.AddValue("usePl", "Disable data flows between peer UEs", usePl);
	cmd.AddValue("verbose", "Allow debug LOGs", verbose);
	cmd.AddValue("outputDir", "",outputDir);
	cmd.AddValue("outputDir2", "",outputDir2);
	cmd.Parse(argc, argv);

  ConfigStore inputConfig;
  inputConfig.ConfigureDefaults ();

  // parse again so you can override default values from the command line
  cmd.Parse(argc, argv);



  Ptr<LteHelper> lteHelper = CreateObject<LteHelper> ();

  if(useFading == true){
	  lteHelper->SetAttribute ("FadingModel", StringValue ("ns3::TraceFadingLossModel"));
	  lteHelper->SetFadingModelAttribute ("TraceFilename", StringValue (fadingEnd));
	  // these parameters have to be set only in case of the trace format
	  // differs from the standard one, that is
	  // - 10 seconds length trace
	  // - 10,000 samples
	  // - 0.5 seconds for window size
	  // - 100 RB
	  lteHelper->SetFadingModelAttribute ("TraceLength", TimeValue (Seconds (10.0)));
	  lteHelper->SetFadingModelAttribute ("SamplesNum", UintegerValue (10000));
	  lteHelper->SetFadingModelAttribute ("WindowSize", TimeValue (Seconds (0.5)));
	  lteHelper->SetFadingModelAttribute ("RbNum", UintegerValue (100));

  }

  lteHelper->SetAttribute("PathlossModel",StringValue ("ns3::ThreeGppUmaPropagationLossModel"));

  if(useShadowing == false){
	  lteHelper->SetPathlossModelAttribute("ShadowingEnabled",BooleanValue (false));
  }

  Ptr<PointToPointEpcHelper> epcHelper = CreateObject<PointToPointEpcHelper> ();
  lteHelper->SetEpcHelper (epcHelper);

  Ptr<Node> pgw = epcHelper->GetPgwNode ();

   // Create a single RemoteHost
  NodeContainer remoteHostContainer;
  remoteHostContainer.Create (1);
  Ptr<Node> remoteHost = remoteHostContainer.Get (0);
  InternetStackHelper internet;
  internet.Install (remoteHostContainer);

  // Create the Internet
  PointToPointHelper p2ph;
  p2ph.SetDeviceAttribute ("DataRate", DataRateValue (DataRate ("100Gb/s")));
  p2ph.SetDeviceAttribute ("Mtu", UintegerValue (1500));
  p2ph.SetChannelAttribute ("Delay", TimeValue (MilliSeconds (10)));
  NetDeviceContainer internetDevices = p2ph.Install (pgw, remoteHost);
  Ipv4AddressHelper ipv4h;
  ipv4h.SetBase ("1.0.0.0", "255.0.0.0");
  Ipv4InterfaceContainer internetIpIfaces = ipv4h.Assign (internetDevices);
  // interface 0 is localhost, 1 is the p2p device
  Ipv4Address remoteHostAddr = internetIpIfaces.GetAddress (1);

  Ipv4StaticRoutingHelper ipv4RoutingHelper;
  Ptr<Ipv4StaticRouting> remoteHostStaticRouting = ipv4RoutingHelper.GetStaticRouting (remoteHost->GetObject<Ipv4> ());
  remoteHostStaticRouting->AddNetworkRouteTo (Ipv4Address ("7.0.0.0"), Ipv4Mask ("255.0.0.0"), 1);

  NodeContainer ueNodes;
  NodeContainer enbNodes;
  enbNodes.Create (numEnbs);
  ueNodes.Create (numUes);

  // Install Mobility Model
  Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();
  for (uint16_t i = 0; i < numEnbs; i++)
    {
      positionAlloc->Add (Vector (distance * i, 0, 0));
    }
  MobilityHelper mobility;
  mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
  mobility.SetPositionAllocator(positionAlloc);
  mobility.Install(enbNodes);
  mobility.Install(ueNodes);

  // Install LTE Devices to the nodes
  NetDeviceContainer enbLteDevs = lteHelper->InstallEnbDevice (enbNodes);
  NetDeviceContainer ueLteDevs = lteHelper->InstallUeDevice (ueNodes);

  // Install the IP stack on the UEs
  internet.Install (ueNodes);
  Ipv4InterfaceContainer ueIpIface;
  ueIpIface = epcHelper->AssignUeIpv4Address (NetDeviceContainer (ueLteDevs));
  // Assign IP address to UEs, and install applications
  for (uint32_t u = 0; u < ueNodes.GetN (); ++u)
    {
      Ptr<Node> ueNode = ueNodes.Get (u);
      // Set the default gateway for the UE
      Ptr<Ipv4StaticRouting> ueStaticRouting = ipv4RoutingHelper.GetStaticRouting (ueNode->GetObject<Ipv4> ());
      ueStaticRouting->SetDefaultRoute (epcHelper->GetUeDefaultGatewayAddress (), 1);
    }

  // Attach one UE per eNodeB
  for (uint16_t i = 0; i < numEnbs; i++){
  	  for(uint16_t j = 0; j < numUes; j++){
  		  lteHelper->Attach(ueLteDevs.Get(j),enbLteDevs.Get(i));
  	  }
  }

  Ptr<EpcTft> tft = Create<EpcTft> ();
  EpcTft::PacketFilter pf;
  pf.localPortStart = 1100;
  pf.localPortEnd = 1100;
  tft->Add (pf);
  lteHelper->ActivateDedicatedEpsBearer (ueLteDevs,
                                         EpsBearer (EpsBearer::NGBR_VIDEO_TCP_DEFAULT),
                                         tft);

  // Install and start applications on UEs and remote host
      uint16_t dlPort = 1100;
      uint16_t ulPort = 2000;
      uint16_t otherPort = 3000;
      ApplicationContainer clientApps;
      ApplicationContainer serverApps;
      if ((useUdp == true) && (usePoisson == false)) {
         	for (uint32_t u = 0; u < ueNodes.GetN(); ++u) {
         		if (useDl) {
         			PacketSinkHelper dlPacketSinkHelper("ns3::UdpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), dlPort));
         			serverApps.Add(dlPacketSinkHelper.Install(ueNodes.Get(u)));

         			UdpClientHelper dlClient(ueIpIface.GetAddress(u), dlPort);
         			dlClient.SetAttribute("Interval", TimeValue(interPacketInterval));
         			dlClient.SetAttribute("MaxPackets", UintegerValue(1000000));
         			clientApps.Add(dlClient.Install(remoteHost));
         		}

         		if (useUl) {
         			++ulPort;
         			PacketSinkHelper ulPacketSinkHelper("ns3::UdpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), ulPort));
         			serverApps.Add(ulPacketSinkHelper.Install(remoteHost));

         			UdpClientHelper ulClient(remoteHostAddr, ulPort);
         			ulClient.SetAttribute("Interval", TimeValue(interPacketInterval));
         			ulClient.SetAttribute("MaxPackets", UintegerValue(1000000));
         			clientApps.Add(ulClient.Install(ueNodes.Get(u)));
         		}

         		if (usePl && numUes > 1) {
         			++otherPort;
         			PacketSinkHelper packetSinkHelper("ns3::UdpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), otherPort));
         			serverApps.Add(packetSinkHelper.Install(ueNodes.Get(u)));

         			UdpClientHelper client(ueIpIface.GetAddress(u), otherPort);
         			client.SetAttribute("Interval", TimeValue(interPacketInterval));
         			client.SetAttribute("MaxPackets", UintegerValue(1000000));
         			clientApps.Add(client.Install(ueNodes.Get((u + 1) % numUes)));
         		}
         	}
         	serverApps.Start(MilliSeconds(appStartTime));
         	clientApps.Start(MilliSeconds(appStartTime));
         	serverApps.Stop(Seconds(simTime));
         	clientApps.Stop(Seconds(simTime));
         	lteHelper->EnableTraces();
         }

         if ((useUdp == false) && (usePoisson == true)) {
         	for (uint32_t u = 0; u < ueNodes.GetN(); ++u) {
         		if (useDl) {
         			PacketSinkHelper dlPacketSinkHelper("ns3::UdpSocketFactory", InetSocketAddress(ueIpIface.GetAddress(u), dlPort));
         			serverApps.Add(dlPacketSinkHelper.Install(ueNodes.Get(u)));

         			OnOffHelper dlClient("ns3::UdpSocketFactory", InetSocketAddress(ueIpIface.GetAddress(u), dlPort));
         			dlClient.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=0.001]"));
         			dlClient.SetAttribute("OffTime", StringValue("ns3::ExponentialRandomVariable[Mean=" + lambda + "]"));
         			dlClient.SetAttribute("PacketSize", UintegerValue(packetSize));
         			dlClient.SetAttribute("StartTime", TimeValue(MilliSeconds(100)));
         			dlClient.SetAttribute("StopTime", TimeValue(Seconds(simTime)));
         			clientApps.Add(dlClient.Install(remoteHost));
         		}
         		if (useUl) {
         			++ulPort;
         			PacketSinkHelper ulPacketSinkHelper("ns3::UdpSocketFactory", InetSocketAddress(remoteHostAddr, ulPort));
         			serverApps.Add(ulPacketSinkHelper.Install(remoteHost));

         			OnOffHelper ulClient("ns3::UdpSocketFactory", InetSocketAddress(remoteHostAddr, ulPort));
         			ulClient.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=0.001]"));
         			ulClient.SetAttribute("OffTime", StringValue("ns3::ExponentialRandomVariable[Mean=" + lambda + "]"));
         			ulClient.SetAttribute("PacketSize", UintegerValue(packetSize));
         			ulClient.SetAttribute("StartTime", TimeValue(MilliSeconds(100)));
         			ulClient.SetAttribute("StopTime", TimeValue(Seconds(simTime)));
         			clientApps.Add(ulClient.Install(ueNodes.Get(u)));
         		}

         	}
         	serverApps.Start(MilliSeconds(appStartTime));
         	clientApps.Start(MilliSeconds(appStartTime));
         	serverApps.Stop(Seconds(simTime));
         	clientApps.Stop(Seconds(simTime));
         	lteHelper->EnableTraces();
         	std::ostringstream oss;
         	    	oss << "/NodeList/"
         	    		<< remoteHost->GetId()
         	    		<< "/ApplicationList/0"
         	    		<< "/$ns3::OnOffApplication/Tx";
         	Config::Connect(oss.str(), MakeCallback(&TraceSentPacket));
         }

 //Uncomment to enable PCAP tracing
 //p2ph.EnablePcapAll("lena-simple-epc");
  //Ptr<RadioEnvironmentMapHelper> remHelper = CreateObject<RadioEnvironmentMapHelper> ();
  //remHelper->SetAttribute ("Channel", PointerValue (lteHelper->GetDownlinkSpectrumChannel ()));
  //remHelper->SetAttribute ("OutputFile", StringValue ("rem.out"));
  //remHelper->SetAttribute ("XMin", DoubleValue (-400.0));
  //remHelper->SetAttribute ("XMax", DoubleValue (400.0));
  //remHelper->SetAttribute ("YMin", DoubleValue (-300.0));
  //remHelper->SetAttribute ("YMax", DoubleValue (300.0));
  //remHelper->SetAttribute ("Z", DoubleValue (0.0));
  //remHelper->Install ();
  FlowMonitorHelper flowmonHelper;
  NodeContainer endpointNodes;
  endpointNodes.Add(remoteHost);
  endpointNodes.Add(ueNodes);

  Ptr<ns3::FlowMonitor> monitor = flowmonHelper.Install(endpointNodes);
  monitor->SetAttribute("DelayBinWidth", DoubleValue(0.001));
  monitor->SetAttribute("JitterBinWidth", DoubleValue(0.001));
  monitor->SetAttribute("PacketSizeBinWidth", DoubleValue(20));
  AsciiTraceHelper asciiTraceHelper;
  Simulator::Stop (Seconds(simTime));

  Simulator::Run ();
  /*
      * To check what was installed in the memory, i.e., BWPs of eNb Device, and its configuration.
      * Example is: Node 1 -> Device 0 -> BandwidthPartMap -> {0,1} BWPs -> NrGnbPhy -> NrPhyMacCommong-> Numerology, Bandwidth, ...
       GtkConfigStore config;
       config.ConfigureAttributes ();
       */

      // Print per-flow statistics
      monitor->CheckForLostPackets();
       Ptr <Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier>(flowmonHelper.GetClassifier());
      FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats();

      double averageFlowThroughput = 0.0;
      double averageFlowDelay = 0.0;

      /*
       std::ofstream outFile;
       std::string filename = outputDir + "/" + simTag;
       outFile.open (filename.c_str (), std::ofstream::out | std::ofstream::trunc);
       if (!outFile.is_open ())
       {
       std::cerr << "Can't open file " << filename << std::endl;
       return 1;
       }

       outFile.setf (std::ios_base::fixed);
       */

      for (std::map<FlowId,FlowMonitor::FlowStats>::const_iterator i = stats.begin(); i != stats.end(); ++i) {
      	Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(i->first);
      	std::stringstream protoStream;
      	protoStream << (uint16_t) t.protocol;
      	if (t.protocol == 6) {
      		protoStream.str("TCP");
      	}
      	if (t.protocol == 17) {
      		protoStream.str("UDP");
      	}
      	/*outFile << "Flow " << i->first << " (" << t.sourceAddress << ":" << t.sourcePort << " -> " << t.destinationAddress << ":" << t.destinationPort << ") proto " << protoStream.str () << "\n";
      	 outFile << "  Tx Packets: " << i->second.txPackets << "\n";
      	 outFile << "  Tx Bytes:   " << i->second.txBytes << "\n";
      	 outFile << "  TxOffered:  " << i->second.txBytes * 8.0 / (simTime - udpAppStartTime) / 1000 / 1000  << " Mbps\n";
      	 outFile << "  Rx Bytes:   " << i->second.rxBytes << "\n";*/
      	std::cout << "Flow " << i->first << " (" << t.sourceAddress << ":" << t.sourcePort << " -> " << t.destinationAddress << ":" << t.destinationPort << ") proto " << protoStream.str() << "\n";
      	std::cout << "  Tx Packets: " << i->second.txPackets << "\n";
      	std::cout << "  Tx Bytes:   " << i->second.txBytes << "\n";
      	std::cout << "  TxOffered:  " << i->second.txBytes * 8.0 / (simTime - appStartTime) / 1000 / 1000 << " Mbps\n";
      	std::cout << "  Rx Bytes:   " << i->second.rxBytes << std::endl;

      	if (i->second.rxPackets > 0) {
      		// Measure the duration of the flow from receiver's perspective
      		//double rxDuration = i->second.timeLastRxPacket.GetSeconds () - i->second.timeFirstTxPacket.GetSeconds ();
      		double rxDuration = (simTime - appStartTime);

      		averageFlowThroughput += i->second.rxBytes * 8.0 / rxDuration / 1000 / 1000;
      		averageFlowDelay += 1000 * i->second.delaySum.GetSeconds() / i->second.rxPackets;

      		/*outFile << "  Throughput: " << i->second.rxBytes * 8.0 / rxDuration / 1000 / 1000  << " Mbps\n";
      		 outFile << "  Mean delay:  " << 1000 * i->second.delaySum.GetSeconds () / i->second.rxPackets << " ms\n";
      		 //outFile << "  Mean upt:  " << i->second.uptSum / i->second.rxPackets / 1000/1000 << " Mbps \n";
      		 outFile << "  Mean jitter:  " << 1000 * i->second.jitterSum.GetSeconds () / i->second.rxPackets  << " ms\n";*/
      		std::cout << "  Throughput:  " << i->second.rxBytes * 8.0 / rxDuration / 1000 / 1000 << " Mbps\n";
      		std::cout << "  Mean delay:  " << 1000 * i->second.delaySum.GetSeconds() / i->second.rxPackets << " ms\n";
      		//std::cout << "  Mean upt:  " << i->second.uptSum / i->second.rxPackets / 1000/1000 << " Mbps \n";
      		std::cout << "  Mean jitter:  " << 1000 * i->second.jitterSum.GetSeconds() / i->second.rxPackets << " ms\n";

      	} else {
      		/*outFile << "  Throughput:  0 Mbps\n";
      		 outFile << "  Mean delay:  0 ms\n";
      		 outFile << "  Mean jitter: 0 ms\n";*/
      		std::cout << "  Throughput:  0 Mbps\n";
      		std::cout << "  Mean delay:  0 ms\n";
      		std::cout << "  Mean jitter: 0 ms\n";
      	}
      	//outFile << "  Rx Packets: " << i->second.rxPackets << "\n";
      	std::cout << "  Rx Packets: " << i->second.rxPackets << std::endl;
      }

      /*outFile << "\n\n  Mean flow throughput: " << averageFlowThroughput / stats.size () << "\n";
       outFile << "  Mean flow delay: " << averageFlowDelay / stats.size () << "\n";*/

      std::cout << "\n  Mean flow throughput: " << averageFlowThroughput / stats.size() << "\n";
      std::cout << "  Mean flow delay: " << averageFlowDelay / stats.size() << "\n";

      std::string dl_results, ul_results, dl_results2, ul_results2;
      dl_results = outputDir + "/" + "DL_" + NameFile + ".txt";
      ul_results = outputDir + "/" + "UL_" + NameFile + ".txt";
      //dl_results2 = outputDir2 + "/" + "DL_" + NameFile + ".txt";
      //ul_results2 = outputDir2 + "/" + "UL_" + NameFile + ".txt";

      Ptr<OutputStreamWrapper> DLstreamMetricsInit = asciiTraceHelper.CreateFileStream((dl_results));
      *DLstreamMetricsInit->GetStream()
      		<< "Flow_ID, Lost_Packets, Tx_Packets, Tx_Bytes, TxOffered(Mbps),  Rx_Packets, Rx_Bytes, T_put(Mbps), Mean_Delay_Rx_Packets, Mean_Jitter, Packet_Loss_Ratio"
      		<< std::endl;

      Ptr<OutputStreamWrapper>  ULstreamMetricsInit = asciiTraceHelper.CreateFileStream((ul_results));
      *ULstreamMetricsInit->GetStream()
      		<< "Flow_ID, Lost_Packets, Tx_Packets, Tx_Bytes, TxOffered(Mbps),  Rx_Packets, Rx_Bytes, T_put(Mbps), Mean_Delay_Rx_Packets, Mean_Jitter, Packet_Loss_Ratio"
      		<< std::endl;

      double statDurationTX = 0;
      double statDurationRX = 0;
      //Ptr classifier = DynamicCast(flowHelper.GetClassifier());
      //std::map stats = flowMonitor->GetFlowStats();
      uint16_t DlPort = 1234;
      uint16_t UlPort = DlPort + numEnbs * numUes + 1;
      for (std::map<FlowId,FlowMonitor::FlowStats>::const_iterator iter = stats.begin(); iter != stats.end(); ++iter) {
      	// some metrics calculation
      	statDurationRX = iter->second.timeLastRxPacket.GetSeconds() - iter->second.timeFirstTxPacket.GetSeconds();
      	statDurationTX = iter->second.timeLastTxPacket.GetSeconds()- iter->second.timeFirstTxPacket.GetSeconds();

      	double meanDelay, meanJitter, packetLossRatio, txTput, rxTput; //,NavComsumption,NavModemComsumption;
      	if (iter->second.rxPackets > 0) {
      		meanDelay = (iter->second.delaySum.GetSeconds() / iter->second.rxPackets);
      	} else // this value is set to zero because the STA is not receiving any packet
      	{
      		meanDelay = 0;
      	}
      	//
      	if (iter->second.rxPackets > 1) {
      		meanJitter = (iter->second.jitterSum.GetSeconds() / (iter->second.rxPackets - 1));
      	} else // this value is set to zero because the STA is not receiving any packet
      	{
      		meanJitter = 0;
      	}
      	//
      	if (statDurationTX > 0) {
      		txTput = iter->second.txBytes * 8.0 / statDurationTX / 1000 / 1000;
      	} else {
      		txTput = 0;
      	}
      	//
      	if (statDurationRX > 0) {
      		rxTput = iter->second.rxBytes * 8.0 / statDurationRX / 1000 / 1000;
      	} else {
      		rxTput = 0;
      	}
      	//
      	if ((iter->second.lostPackets > 0) & (iter->second.rxPackets > 0)) {
      		packetLossRatio = (double) (iter->second.lostPackets / (double) (iter->second.rxPackets + iter->second.lostPackets));
      	} else {
      		packetLossRatio = 0;
      	}
      	/*if(iter->first == auv.Get(0)->GetId()){
      	 NavComsumption = energyModel->GetTotalEnergyConsumption ();
      	 NavModemComsumption = basicSourcePtr ->GetInitialEnergy() - basicSourcePtr -> GetRemainingEnergy();
      	 }else{
      	 NavComsumption=0;
      	 NavModemComsumption=0;
      	 }*/
      	//
      	Ipv4FlowClassifier::FiveTuple t = classifier->FindFlow(iter->first);
      	//
      	Ptr <OutputStreamWrapper>  streamMetricsInit = NULL;
      	// Get file pointer for DL, if DL flow (using port and IP address to assure correct result)
      	std::cout << "\nFlow: " << iter->first << std::endl;
      	std::cout << "  t destination port " << t.destinationPort << std::endl;
      	std::cout << "  source address " << internetIpIfaces.GetAddress(1) << std::endl;
      	std::cout << "  t source address " << t.sourceAddress << std::endl;
      	std::cout << "  t destination port " << t.destinationPort << std::endl;
      	std::cout << "  sink address " << ueIpIface.GetAddress(0) << std::endl;
      	std::cout << "  t destination address " << t.destinationAddress << "\n";
      	if ((t.destinationPort == DlPort) || (t.sourceAddress == remoteHostAddr)) {
      		streamMetricsInit = DLstreamMetricsInit;
      		DlPort++;
      	}
      	// Get file pointer for UL, if UL flow (using port and IP address to assure correct result))
      	//else if ((t.destinationPort == UlPort)
      	else if ((t.destinationPort == UlPort) || (t.destinationAddress == remoteHostAddr)) {
      		streamMetricsInit = ULstreamMetricsInit;
      		UlPort++;
      	}
      	//
      	if (streamMetricsInit) {

      		*streamMetricsInit->GetStream() << (iter->first) << ", "
      				<< (iter->second.lostPackets) << ", "
      				//
      				<< (iter->second.txPackets) << ", "
      				//
      				<< (iter->second.txBytes) << ", "
      				//
      				<< txTput << ", "
      				//
      				<< (iter->second.rxPackets) << ", "
      				//
      				<< (iter->second.rxBytes) << ", "
      				//
      				<< rxTput << ", "
      				//
      				<< meanDelay << ", "
      				//
      				<< meanJitter << ", "
      				//
      				<< packetLossRatio
      				//
      				//<< NavComsumption << ", "
      				//
      				//<< NavModemComsumption
      				//
      				<< std::endl;
      	} else {
      		//TODO: chance for an ASSERT
      		if (true) {
      			std::cout << "Some problem to save metrics" << std::endl;
      			std::cout << "Flow ID: " << iter->first << ", Source Port: " << t.sourcePort << ", Destination Port: "
      					  << t.destinationPort << " (" << t.sourceAddress
      					  << " -> " << t.destinationAddress << ")" << std::endl;
      			std::cout << "gNB Address: " << t.destinationAddress << std::endl;
      			std::cout << "DLport: " << t.sourcePort << std::endl;
      			std::cout << "ULport: " << t.destinationPort << std::endl;
      		}
      	}

      	//m_bytesTotal =+ iter->second.rxPackets;
      }

      src.open(dl_results, std::ios::in | std::ios::binary);
      dst.open(dl_results2, std::ios::out | std::ios::binary);
      dst << src.rdbuf();

      src.close();
      dst.close();

      src.open(ul_results, std::ios::in | std::ios::binary);
      dst.open(ul_results2, std::ios::out | std::ios::binary);
      dst << src.rdbuf();

      src.close();
      dst.close();

      /*outFile.close ();

       std::ifstream f (filename.c_str ());

       if (f.is_open ())
       {
       std::cout << f.rdbuf ();
       }
       */
      toc();

  /*GtkConfigStore config;
  config.ConfigureAttributes();*/

  Simulator::Destroy ();
  return 0;
}