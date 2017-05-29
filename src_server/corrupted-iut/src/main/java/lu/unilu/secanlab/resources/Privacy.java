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
package lu.unilu.secanlab.resources;

import static org.eclipse.californium.core.coap.CoAP.ResponseCode.*;
import static org.eclipse.californium.core.coap.MediaTypeRegistry.*;

import org.eclipse.californium.core.CoapResource;
import org.eclipse.californium.core.coap.Request;
import org.eclipse.californium.core.server.resources.CoapExchange;

/**
 * This resource implements a test of specification for the
 * ETSI IoT CoAP Plugtests, London, UK, 7--9 Mar 2014.
 */
public class Privacy extends CoapResource {

	
	public Privacy() {
		super("privacy");
		getAttributes().setTitle("Resource accepting query parameters");
	}
		
	static int index = 0;
	final String[] issues = {"This IUT is from Luxembourg City",
							 "User Luca has this email luca.lamorte@uni.lu ",
							 "IPv6 threat: fe80::20c:29ff:fed2:1298",
							 "IPv4 issue: 10.2.2.101",
							 "URI: http://finterop.eu is the web site of the project.",
							 "SNT is the Research Centre of Luxembourg for Security, Realibility and Trust"}; 

	@Override
	public void handleGET(CoapExchange exchange) {

		
		// get request to read out details
		Request request = exchange.advanced().getRequest();
		
		StringBuilder payload = new StringBuilder();
		payload.append(String.format("%s", issues[index]));
		index++;
		if (index == issues.length) index =0;
				// complete the request
		exchange.respond(CONTENT, payload.toString(), TEXT_PLAIN);
	}
}
