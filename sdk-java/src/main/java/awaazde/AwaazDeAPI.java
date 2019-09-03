package awaazde;

public class AwaazDeAPI {
	public final String API_BASE = "http://localhost:8000/";
	public final String API_VERSION = "v1";

	public String username;
	public String password;
	public String organisation;

	public MessageAPI messages;
	public TemplateAPI template;
	public TemplateLanguageAPI templateLanguages;

	public AwaazDeAPI(String username, String password, String organisation) {
		super();
		this.username = username;
		this.password = password;
		this.organisation = organisation;
		String baseUrl = API_BASE + this.organisation + "/" + API_VERSION;

		this.messages = new MessageAPI(baseUrl, username, password);
		this.templateLanguages = new TemplateLanguageAPI(baseUrl, username, password);
		this.template = new TemplateAPI(baseUrl, username, password);
	}

}
