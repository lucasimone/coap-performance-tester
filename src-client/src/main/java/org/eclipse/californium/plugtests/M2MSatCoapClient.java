/*******************************************************************************
 * Copyright (c) 2015 Institute for Pervasive Computing, ETH Zurich and others.
 * 
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Public License v1.0
 * and Eclipse Distribution License v1.0 which accompany this distribution.
 * 
 * The Eclipse Public License is available at
 *    http://www.eclipse.org/legal/epl-v10.html
 * and the Eclipse Distribution License is available at
 *    http://www.eclipse.org/org/documents/edl-v10.html.
 * 
 * Contributors:
 *    Matthias Kovatsch - creator and main architect
 ******************************************************************************/
/**
 * 
 */
package org.eclipse.californium.plugtests;

import java.util.Scanner;

import org.eclipse.californium.core.CoapClient;
import org.eclipse.californium.core.CoapResponse;
import org.eclipse.californium.core.Utils;
import org.eclipse.californium.core.network.config.NetworkConfig;


public class M2MSatCoapClient {

	/**
	 * Main entry point.
	 * 
	 * @param args the arguments
	 */
	
	
	static String ver = "1.0.3";
	
	static int retry  = 2;
	static int repeat = 3;
	//static Random rand = new Random();

	private static int val;
	private static String string_uri  = "coap://localhost";;

	
	public static void main(String[] args) {
		
		if (args.length == 0) {
			System.out.println("\n (M2M-SAT) CoAP Client - v."+ver);
			System.out.println("(c) 2017, SNT + LIST");
			System.out.println();
			
			Scanner sc = new Scanner(System.in);
			System.out.print("Enter COAP URL [coap://]: ");
			string_uri = sc.nextLine();
			System.out.print("Enter Timeout [default="+NetworkConfig.getStandard().getInt(NetworkConfig.Keys.ACK_TIMEOUT)+"]: ");
			try{
				NetworkConfig.getStandard().setInt(NetworkConfig.Keys.ACK_TIMEOUT, Integer.parseInt(sc.nextLine()));
			}
			catch(Exception ex){
				System.out.println("This value is not valid ==> use default = 2000");
				NetworkConfig.getStandard().setInt(NetworkConfig.Keys.ACK_TIMEOUT, 2000);
			}
			
			System.out.print("Enter ACK_Rand_Factor [default="+NetworkConfig.getStandard().getFloat(NetworkConfig.Keys.ACK_RANDOM_FACTOR)+"]: ");
			try{
				NetworkConfig.getStandard().setFloat(NetworkConfig.Keys.ACK_RANDOM_FACTOR, Float.parseFloat(sc.nextLine()));
			}
			catch(Exception ex){
				System.out.println("This value is not valid ==> use default = 1.5");
				NetworkConfig.getStandard().setFloat(NetworkConfig.Keys.ACK_RANDOM_FACTOR, 1.5f);
			}
			
			System.out.print("Enter max retransmission:  [default="+NetworkConfig.getStandard().getInt(NetworkConfig.Keys.MAX_RETRANSMIT)+"]: ");
			try{
				NetworkConfig.getStandard().setInt(NetworkConfig.Keys.MAX_RETRANSMIT, Integer.parseInt(sc.nextLine()));
			}
			catch(Exception ex){
				System.out.println("This value is not valid ==> use default = 4");
				NetworkConfig.getStandard().setInt(NetworkConfig.Keys.MAX_RETRANSMIT, 4);
			}
			
			
			System.out.print("Enter num. test iteration: ");
			try{
				repeat = Integer.parseInt(sc.nextLine());
			}
			catch(Exception ex){
				
				System.out.println("This value is not valid ==> use default = 1");
				repeat= 1;
			}
			
			
//			System.out.println("Usage: " + M2MSatCoapClient.class.getSimpleName() + " [-r -f -t] URI");
//			System.out.println("  -r        : Number of retransmission after TIMEOUT [default="+NetworkConfig.getStandard().getInt(NetworkConfig.Keys.MAX_RETRANSMIT)+"]");
//			System.out.println("  -t        : ACK timeout [default="+NetworkConfig.getStandard().getInt(NetworkConfig.Keys.ACK_TIMEOUT) +"]");
//			System.out.println("  -f        : ACK RANDOM FACTOR [default="+NetworkConfig.getStandard().getFloat(NetworkConfig.Keys.ACK_RANDOM_FACTOR) +"]");
//			System.out.println("  -N        : Number of GET request to sent consecutively");
//			System.out.println("  URI       : The CoAP URI of the Plugtest server to test (coap://...)");
//			System.out.println();
//			System.out.println("\n All parameters are present in the Californium.properties file");
//			
//			System.exit(-1);
		}
	
		
		// Config used for plugtest
		NetworkConfig.getStandard()
			.setInt(NetworkConfig.Keys.MAX_MESSAGE_SIZE, 64)
			.setInt(NetworkConfig.Keys.PREFERRED_BLOCK_SIZE, 64);
		String flag = "";
		
		
		
		try{
		    for (String arg: args){
		    	
//		    	System.out.println("Check arg: "+arg);
		    	if (arg.startsWith("coap://")){
		    		string_uri = arg;
		    	}
		    	else if (arg.startsWith("-")){
		    		flag = arg;
		    	}
		    	else if (flag.toLowerCase().equals("-r")){
		    		retry = Integer.parseInt(arg);
		    		NetworkConfig.getStandard().setInt(NetworkConfig.Keys.MAX_RETRANSMIT, retry);
		    	}
		    	else if (flag.toLowerCase().equals("-n")){
		    		repeat = Integer.parseInt(arg);
		    	}
		    	else if (flag.toLowerCase().equals("-t")){
		    		NetworkConfig.getStandard().setInt(NetworkConfig.Keys.ACK_TIMEOUT, Integer.parseInt(arg));
		    	}
		    	else if (flag.toLowerCase().equals("-f")){
		    		NetworkConfig.getStandard().setFloat(NetworkConfig.Keys.ACK_RANDOM_FACTOR, Float.parseFloat(arg));
		    	}
		    	else System.err.println("Parameter "+arg+" is not valid");	   
		    }
	    }catch(Exception ex){
	    	System.err.println("Some parameters passed are not valid");
	    	ex.printStackTrace();
	    }
	 
		// allow quick hostname as argument
		if (!string_uri.startsWith("coap://")) {
			string_uri = "coap://" + string_uri;
		}
		if (string_uri.endsWith("/")) {
			string_uri = string_uri.substring(-1);
		}
		
		
//		NetworkConfig.getStandard().setInt(NetworkConfig.Keys.ACK_TIMEOUT, 1000);
//		NetworkConfig.getStandard().setFloat(NetworkConfig.Keys.ACK_RANDOM_FACTOR, 1.5f);
//		NetworkConfig.getStandard().setInt(NetworkConfig.Keys.MAX_RETRANSMIT, 4);
		
		
			
	    System.out.println("=============== PARAMS =====================");
		System.out.println(" - MAX_MESSAGE_SIZE = "+ NetworkConfig.getStandard().getInt(NetworkConfig.Keys.MAX_MESSAGE_SIZE));
		System.out.println(" - PREFERRED_BLOCK_SIZE = "+ NetworkConfig.getStandard().getInt(NetworkConfig.Keys.PREFERRED_BLOCK_SIZE));
		System.out.println(" - ACK_TIMEOUT = "+ NetworkConfig.getStandard().getInt(NetworkConfig.Keys.ACK_TIMEOUT));
		System.out.println(" - ACK_RANDOM_FACTOR = "+ NetworkConfig.getStandard().getFloat(NetworkConfig.Keys.ACK_RANDOM_FACTOR));
		System.out.println(" - RETRANSMISSION = "+ NetworkConfig.getStandard().getInt(NetworkConfig.Keys.MAX_RETRANSMIT));
		System.out.println("=============== METHOD =====================");
		System.out.println("METHOD = GET");
		System.out.println("COAP URI = " + string_uri);
		System.out.println("NUM REQUEST = " + repeat);
		System.out.println("===============  READY =====================");
		
		
//		String tcpDumpCmd = "/usr/sbin/tcpdump -c 2 -v -A d";
//		String tcpDumpResult = TcpDump.runTCPDump(tcpDumpCmd, true);
		
		for (int i= 0; i<repeat; i++){
			System.out.println("[ CON ] SEND GET n."+(i+1));
			send_coap_message(string_uri);
		}
		
		//send_coap_put();
		System.out.println("\n\n");
		System.out.println("===============  RESULT REPORT=============");
		System.out.println(" SINGLE GET SENT = " + repeat);
//		System.out.println(" TOTAL  CON SENT = " + overhead +" (with retransmission)");
		System.out.println(" CON SUCCESS     = " + success);
		System.out.println(" CON FAILED      = " + failed);
//		System.out.println(" OVERHEAD        = " + (overhead - repeat));
//		System.out.println(" Packet drops    = " + ((overhead - repeat)/repeat)*100 + "%");
		System.out.println("===============  DONE =====================");
		System.exit(0);
	}
	
	static int overhead = 0;
	static int failed = 0;
	static int success  = 0;
	
	public static void send_coap_put(){
		CoapClient client = new CoapClient("coap://localhost/stop");
		client.useNONs();
		CoapResponse response = client.delete();
	}
	
	public static void send_coap_message(String uri) {
		
		// re-usable response object
		CoapResponse response = null;
		try{
			
				  	CoapClient client = new CoapClient(uri);
					response =  client.get();
					if (response!=null) {
						success ++;			 
						System.out.println("     |--- Response code:" +response.getCode());
						System.out.println("     |--- Response options:" + response.getOptions());
						System.out.println("     |--- Response text:" + response.getResponseText());
						
						System.out.println("     |--- ADVANCED:\n");
						// access advanced API with access to more details through .advanced()
						System.out.println(Utils.prettyPrint(response));
					}
					else{
						failed++;
						System.out.println("     |--- No response received.");
						
					}
		}catch(Exception ex){
			System.out.println("Something went wrong :(");
			ex.printStackTrace();
		}
		
	}


//	public static void send_coap_message(String uri, int retry, int times) {
//		
//		// re-usable response object
//		CoapResponse response = null;
//		try{
//			
//			
//			for (int i= 0; i<times; i++){
//				System.out.println("SEND  ======== GET ======> Message n." + (i+1));
//				
////				int timeout = rand.nextInt(val) + ack_to;
//				
//				System.out.println("----- ACK_TIMEOUT * ACK_RAND_FACT = " + val);
//				System.out.println("----- TIMEOUT RAND( ACK_TIMEOUT, (ACK_TIMEOUT* ACK_RAND_FACT) = " + timeout);
//				System.out.println("----- TEST ITERATION = " + retry);
////				for (int tentative=0; tentative <= retry && response==null; tentative++) {
//				    CoapClient client = new CoapClient(uri);
//					client.setTimeout(timeout);
//					overhead++;
//					
//					System.out.println("- [CON.n"+i+"]"); // Tentative n."+tentative);
//					System.out.println("     |--- Timeout: "+ timeout + " ms");
//					System.out.println("     |--- URI: "+ uri);
//					response = client.get();
//					if (response!=null) {
//						success ++;
//						System.out.println("     |--- Response code:" +response.getCode());
//						System.out.println("     |--- Response options:" + response.getOptions());
//						System.out.println("     |--- Response text:" + response.getResponseText());
//						
//						System.out.println("     |--- ADVANCED:\n");
//						// access advanced API with access to more details through .advanced()
//						System.out.println(Utils.prettyPrint(response));
//					}
//					else{
//						failed++;
//						System.out.println("     |--- Response TIMEOUT: No response received.");
//						timeout *=2;
//					}
//				}
////			}
//
//			if (response == null) System.out.println("CoAP Server or resource not available - > SKIP GET");
//		}catch(Exception ex){
//			System.out.println("Something went wrong :(");
//			ex.printStackTrace();
//		}
//		
//	}
	


	

}
