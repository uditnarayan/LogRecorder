import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;


public class WSTest {
	
	private static final String endpoint = "http://localhost:5000/message";
	
	public static void main(String[] args) {
		
		try{
			int i = 1;
			while(true){
		    	URL urlRequest = new URL(endpoint);
		    	HttpURLConnection conn = (HttpURLConnection) urlRequest.openConnection();
		    		    	
		    	conn.setDoOutput(true);
		    	conn.setDoInput(true);        	
		    	conn.setRequestProperty("Content-Type", "application/json");
		    	conn.setRequestMethod("POST");
				conn.setRequestProperty("Accept", "application/json");
				
				String msg= "this is a message" + i;
		        String payLoad = "{\"namespace\":\"udit\", \"text\":\"" + msg + "\"}";
		        //System.out.println(payLoad);
		        OutputStream os = conn.getOutputStream();
	    		os.write(payLoad.getBytes());
	    		os.flush();
	    		    		
	    		if (conn.getResponseCode() != HttpURLConnection.HTTP_CREATED) {
	    			throw new RuntimeException("Failed : HTTP error code : "
	    					+ conn.getResponseCode() + conn.getResponseMessage());
	    		}
	    		
	    		BufferedReader br = new BufferedReader(new InputStreamReader((conn.getInputStream())));
	    	 
	    	    String output;
	    		while ((output = br.readLine()) != null) {
	    			System.out.println(output);
	    		}    	 
	    		conn.disconnect();   
	    		Thread.sleep(1);
	    		i++;
			}
		}
		catch(MalformedURLException ex){
			ex.printStackTrace();
		}
		catch(IOException ex){
			ex.printStackTrace();
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
		

	}
}
