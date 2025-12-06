// Client API léger pour Astro
export class MarketingApiClient {
	constructor(baseUrl = "http://localhost:8000/api/v1") {
		this.baseUrl = baseUrl;
	}

	async sendContactMessage(contactData) {
		const response = await fetch(`${this.baseUrl}/contact/send`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify(contactData),
		});
		return response.json();
	}

	async getToolConfig() {
		const response = await fetch(`${this.baseUrl}/tools/config`);
		return response.json();
	}
}
