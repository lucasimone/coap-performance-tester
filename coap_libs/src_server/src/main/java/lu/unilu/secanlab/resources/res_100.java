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
import org.eclipse.californium.core.server.resources.CoapExchange;

/**
 * This resource implements a test of specification for the
 * ETSI IoT CoAP Plugtests, London, UK, 7--9 Mar 2014.
 */
public class res_100 extends CoapResource {

	public res_100() {
		super("res100");
		getAttributes().setTitle("Resource size 100");
		getAttributes().addResourceType("block");
		getAttributes().setMaximumSizeEstimate(100);
	}

	@Override
	public void handleGET(CoapExchange exchange) {
		
		StringBuilder builder = new StringBuilder();
		builder.append("Payload_100_byte-----Payload_100_byte-----Payload_100_byte-----Payload_100_byte-----Payload_100_byte\n");
		
		exchange.respond(CONTENT, builder.toString(), TEXT_PLAIN);
	}

}
