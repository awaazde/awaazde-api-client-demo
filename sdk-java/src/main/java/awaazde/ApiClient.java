package awaazde;

import java.io.File;

import javax.ws.rs.core.MediaType;

import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;
import com.sun.jersey.api.client.config.ClientConfig;
import com.sun.jersey.api.client.config.DefaultClientConfig;
import com.sun.jersey.core.header.FormDataContentDisposition;
import com.sun.jersey.multipart.FormDataMultiPart;
import com.sun.jersey.multipart.file.FileDataBodyPart;
import com.sun.jersey.multipart.impl.MultiPartWriter;

public class ApiClient {

	private Client client;

	public ApiClient() {
		ClientConfig config = new DefaultClientConfig();
		config.getClasses().add(MultiPartWriter.class);
		this.client = Client.create(config);
	}

	public String login(String url, String data, String token) {
		WebResource webResource = client.resource(url);
		ClientResponse response = webResource.accept(MediaType.APPLICATION_JSON).type(MediaType.APPLICATION_JSON)
				.post(ClientResponse.class, data);

		if (response.getStatusInfo().getStatusCode() != 200) {
			return "Not Able to log in. Please Try Again";
		}
		return response.getEntity(String.class);
	}

	public String post(String url, String data, String token) {
		WebResource webResource = client.resource(url);
		ClientResponse response = webResource.header("Authorization", "JWT " + token).accept(MediaType.APPLICATION_JSON)
				.type(MediaType.APPLICATION_JSON).post(ClientResponse.class, data);

		if (response.getStatusInfo().getStatusCode() != 201) {
			System.out.println(response.getEntity(String.class));
			return "Resource Not Created";
		}
		return response.getEntity(String.class);
	}

	public String get(String url, String token) {
		WebResource webResource = client.resource(url);
		ClientResponse response = webResource.header("Authorization", "JWT " + token).accept(MediaType.APPLICATION_JSON)
				.type(MediaType.APPLICATION_JSON).get(ClientResponse.class);

		if (response.getStatusInfo().getStatusCode() != 200) {
			return "Resource Not Found";
		}
		return response.getEntity(String.class);
	}

	public String put(String url, String data, String token) {
		WebResource webResource = client.resource(url);
		ClientResponse response = webResource.header("Authorization", "JWT " + token).accept(MediaType.APPLICATION_JSON)
				.type(MediaType.APPLICATION_JSON).post(ClientResponse.class, data);

		if (response.getStatusInfo().getStatusCode() != 200) {
			return "Resource Not Updated";
		}
		return response.getEntity(String.class);
	}

	public String delete(String url, String token) {
		WebResource webResource = client.resource(url);
		ClientResponse response = webResource.header("Authorization", "JWT " + token).accept(MediaType.APPLICATION_JSON)
				.type(MediaType.APPLICATION_JSON).delete(ClientResponse.class);
		if (response.getStatusInfo().getStatusCode() != 204) {
			return "Can Not Delete Resource";
		}
		return "Resource Deleted";
	}

	public String upload(String url, File file, String token) {
		ClientResponse response;
		WebResource webResource = client.resource(url);
		final FormDataMultiPart multiPart = new FormDataMultiPart();
		if (file != null) {
			FileDataBodyPart filePart = new FileDataBodyPart("file", file);
			FileDataBodyPart fileDataBodyPart = new FileDataBodyPart("file", file,
					MediaType.APPLICATION_OCTET_STREAM_TYPE);
			FormDataContentDisposition.FormDataContentDispositionBuilder builder = FormDataContentDisposition
					.name(filePart.getName());
			builder.fileName(file.getName());
			builder.size(file.length());
			FormDataContentDisposition fdcd = builder.build();
			fileDataBodyPart.setContentDisposition(fdcd);
			multiPart.bodyPart(filePart);
			multiPart.field("filename", file.getName());
			
		}
		response = webResource.header("Authorization", "JWT " + token).accept(MediaType.APPLICATION_JSON)
				.type(MediaType.MULTIPART_FORM_DATA).post(ClientResponse.class, multiPart);
		System.out.println(response.getStatusInfo().getStatusCode() );
		if (response.getStatusInfo().getStatusCode() != 201) {
			return "Resources Not Created";
		}
		return response.getEntity(String.class);

	}
}