package demo;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;

import awaazde.AwaazDeAPI;

public class APIDemo {

	public static String username = "youremail";
	public static String password = "your password";
	public static String organisation = "your organisation";

	public static void main(String[] args) {
		try {

			AwaazDeAPI awaazde = new AwaazDeAPI(username, password, organisation);

			demoMessageApi(awaazde);

			demoTemplateApi(awaazde);

			demoTemplateLanguageApi(awaazde);
		} catch (Exception e) {
			e.printStackTrace();

		}
	}

	private static void demoMessageApi(AwaazDeAPI awaazde)
			throws JsonParseException, JsonMappingException, IOException {
		Map<String, Object> messageData = new HashMap<String, Object>();
		messageData.put("templatelanguage", 1);
		messageData.put("phone_number", "+919875612358");
		String[] values = { "1", "3" };
		messageData.put("values", values);

		System.out.println(awaazde.messages.create(messageData));
		System.out.println(awaazde.messages.upload("/home/jaydip/Documents/messages.csv"));
		System.out.println(awaazde.messages.get("19"));
		System.out.println(awaazde.messages.delete("19"));
	}

	private static void demoTemplateApi(AwaazDeAPI awaazde)
			throws JsonParseException, JsonMappingException, IOException {
		Map<String, Object> templateData = new HashMap<String, Object>();
		List<Object> adv = new ArrayList<Object>();

		Map<String, Object> phoneNumber = new HashMap<String, Object>();
		phoneNumber.put("option", "phone_numbers");
		phoneNumber.put("value", "+917961921009");
		adv.add(phoneNumber);

		Map<String, Object> response_type = new HashMap<String, Object>();
		response_type.put("option", "response_type");
		response_type.put("value", "none");
		adv.add(response_type);

		Map<String, Object> num_backups = new HashMap<String, Object>();
		num_backups.put("option", "num_backups");
		num_backups.put("value", 0);
		adv.add(num_backups);

		templateData.put("name", "EMI reminder call");
		templateData.put("description", "Demo Template");
		templateData.put("medium", "voice");
		templateData.put("advanced_options", adv);

		System.out.println(awaazde.template.create(templateData));
		System.out.println(awaazde.template.get("1"));
		System.out.println(awaazde.template.delete("2"));
	}

	private static void demoTemplateLanguageApi(AwaazDeAPI awaazde)
			throws JsonParseException, JsonMappingException, IOException {

		System.out.println(awaazde.templateLanguages.get("1"));
	}
}
