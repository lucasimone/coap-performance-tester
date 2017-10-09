package org.eclipse.californium.plugtests;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.io.StringWriter;
import java.io.Writer;

public class TcpDump {

	
	public static String runTCPDump(String crunchifyCmd, boolean waitForResult) {
		System.out.println("inside runTCPDUmp()");
		String tcpdumpCmdResponse = "";
		ProcessBuilder crunchifyProcessBuilder = null;
 
		// Find OS running on VM
		String operatingSystem = System.getProperty("os.name");
 
		if (operatingSystem.toLowerCase().contains("window")) {
			// In case of windows run command using "crunchifyCmd"
			crunchifyProcessBuilder = new ProcessBuilder("cmd", "/c", crunchifyCmd);
		} else {
			// In case of Linux/Ubuntu run command using /bin/bash
			crunchifyProcessBuilder = new ProcessBuilder("/bin/bash", "-c", crunchifyCmd);
		}
 
		crunchifyProcessBuilder.redirectErrorStream(true);
 
		try {
			Process process = crunchifyProcessBuilder.start();
			if (waitForResult) {
				InputStream crunchifyStream = process.getInputStream();
				tcpdumpCmdResponse = getStringFromStream(crunchifyStream);
				crunchifyStream.close();
			}
 
		} catch (Exception e) {
			System.out.println("Error Executing tcpdump command" + e);
		}
		return tcpdumpCmdResponse;
	}
	
	
	private static String getStringFromStream(InputStream crunchifyStream) throws IOException {
		System.out.println("inside getStringFromStream()");
		if (crunchifyStream != null) {
			Writer crunchifyWriter = new StringWriter();
 
			char[] crunchifyBuffer = new char[2048];
			try {
				Reader crunchifyReader = new BufferedReader(new InputStreamReader(crunchifyStream, "UTF-8"));
				int count;
				while ((count = crunchifyReader.read(crunchifyBuffer)) != -1) {
					crunchifyWriter.write(crunchifyBuffer, 0, count);
				}
			} finally {
				crunchifyStream.close();
			}
			return crunchifyWriter.toString();
		} else {
			return "";
		}
	}
 
}
