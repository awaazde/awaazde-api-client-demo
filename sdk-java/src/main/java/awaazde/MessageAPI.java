package awaazde;

public class MessageAPI extends BaseAPI {

	public MessageAPI(String baseUrl, String username, String password) {
		super("xact/message/", baseUrl, username, password);
	}

	public String upload(String filePath) {
		return upload("import/", filePath);
	}
}
