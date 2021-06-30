package awaazde;

import java.io.File;
import java.io.IOException;
import java.util.Map;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.sun.jersey.core.header.Token;

import model.User;

public class BaseAPI {

	public String resourceUrl;

	public ApiClient client;

	public String baseUrl;

	public String token;

	public String username;

	public String password;

	ObjectMapper mapper;

	public BaseAPI(String resourceUrl, String baseUrl, String username, String password) {
		super();
		this.resourceUrl = resourceUrl;
		this.client = new ApiClient();
		this.baseUrl = baseUrl;
		this.username = username;
		this.password = password;
		this.mapper = new ObjectMapper();
		this.mapper.disable(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES);
		performAuthentication();
	}

	public String getUrl() {
		return this.baseUrl + "/" + this.resourceUrl;
	}

	private void performAuthentication() {
		String url = this.baseUrl + "/account/login/";
		String token;
		try {
			token = new ApiClient().login(url, mapper.writeValueAsString(new User(this.username, this.password)), null);
			this.token = mapper.readValue(token, Token.class).getToken();
		} catch (JsonParseException e) {
			e.printStackTrace();
		} catch (JsonMappingException e) {
			e.printStackTrace();
		} catch (JsonProcessingException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	public String create(Map<String, Object> data) throws JsonParseException, JsonMappingException, IOException {
		System.out.println(mapper.writeValueAsString(data));
		return this.client.post(getUrl(), mapper.writeValueAsString(data), this.token);
	}

	public String get(String id) {
		String url = getUrl() + id;
		return this.client.get(url, this.token);
	}

	public String update(String id, String data) {
		String url = getUrl() + id + "/";
		return this.client.put(url, data, this.token);
	}

	public String delete(String id) {
		String url = getUrl() + id;
		return this.client.delete(url, this.token);
	}

	public String upload(String uploadUrl, String filePath) {
		File file = new File(filePath);
		String url = getUrl() + uploadUrl;
		return client.upload(url, file, token);
	}
}
