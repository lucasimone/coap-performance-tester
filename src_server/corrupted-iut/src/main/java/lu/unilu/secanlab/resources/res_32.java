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
public class res_32 extends CoapResource {

	public res_32() {
		super("res32");
		getAttributes().setTitle("Resource of 32 bytes");
		getAttributes().addResourceType("block");
		getAttributes().setMaximumSizeEstimate(32);
	}

	@Override
	public void handleGET(CoapExchange exchange) {
		
		StringBuilder builder = new StringBuilder();
		builder.append("/-------------------------------\n");
		
		
		exchange.respond(CONTENT, builder.toString(), TEXT_PLAIN);
	}

}
