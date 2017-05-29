package lu.unilu.secanlab;

import static org.eclipse.californium.plugtests.PlugtestServer.ERR_INIT_FAILED;

import java.net.InetSocketAddress;
import java.util.Arrays;

import org.eclipse.californium.core.CoapServer;
import org.eclipse.californium.core.network.CoAPEndpoint;
import org.eclipse.californium.core.network.Endpoint;
import org.eclipse.californium.core.network.interceptors.MessageTracer;
import org.eclipse.californium.core.network.interceptors.OriginTracer;
import org.eclipse.californium.plugtests.PlugtestServer;

import lu.unilu.secanlab.resources.Privacy;
import lu.unilu.secanlab.resources.Query;
import lu.unilu.secanlab.resources.Shutdown;
import lu.unilu.secanlab.resources.res_100;
import lu.unilu.secanlab.resources.res_1024;
import lu.unilu.secanlab.resources.res_128;
import lu.unilu.secanlab.resources.res_1280;
import lu.unilu.secanlab.resources.res_16;
import lu.unilu.secanlab.resources.res_256;
import lu.unilu.secanlab.resources.res_32;
import lu.unilu.secanlab.resources.res_512;
import lu.unilu.secanlab.resources.res_64;

public class Main {

    public static void main(String[] args) {

        System.out.println(Arrays.toString(args));

        String address =  args[0];
        Integer port = Integer.parseInt(args[1]);

        // create server
        try {
            CoapServer server = new PlugtestServer();

            server.addEndpoint(new CoAPEndpoint(new InetSocketAddress(address, port)));
            server.add(new Query());
            server.add(new Privacy());
            server.add(new res_1280());
            server.add(new res_1024());
            server.add(new res_512());
            server.add(new res_256());
            server.add(new res_128());
            server.add(new res_64());
            server.add(new res_32());
            server.add(new res_16());
            server.add(new res_100());
            server.add(new Shutdown());
            server.start();
            
            
            // add special interceptor for message traces
            for (Endpoint ep:server.getEndpoints()) {
                ep.addInterceptor(new MessageTracer());
                // Eclipse IoT metrics
                ep.addInterceptor(new OriginTracer());
            }

            System.out.println(PlugtestServer.class.getSimpleName()+" listening on port " + port);

        } catch (Exception e) {

            System.err.printf("Failed to create "+PlugtestServer.class.getSimpleName()+": %s\n", e.getMessage());
            System.err.println("Exiting");
            System.exit(ERR_INIT_FAILED);
        }

    }
}
