import type { ApiResponse, ContactMessage } from "../../shared/api/types";

const API_BASE_URL =
	process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export class ApiClient {
	private baseUrl: string;

	constructor(baseUrl: string = API_BASE_URL) {
		this.baseUrl = baseUrl;
	}

	async encodeBase64(text: string, charset = "auto") {
		const response = await fetch(`${this.baseUrl}/tools/encode`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ text, charset }),
		});
		return response.json();
	}

	async decodeBase64(base64Text: string, charset = "auto", lineByLine = false) {
		const response = await fetch(`${this.baseUrl}/tools/decode`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({
				base64_text: base64Text,
				charset,
				decode_line_by_line: lineByLine,
			}),
		});
		return response.json();
	}

	async getEncodingCategories() {
		const response = await fetch(`${this.baseUrl}/tools/encodings`);
		return response.json();
	}

	async sendContactMessage(contactData: ContactMessage): Promise<ApiResponse> {
		try {
			const response = await fetch(`${this.baseUrl}/contact/send`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify(contactData),
			});

			if (!response.ok) {
				throw new Error(`HTTP error! status: ${response.status}`);
			}

			const result: ApiResponse = await response.json();

			// Ici, nous pouvons utiliser le guard si nous voulons effectuer des actions spécifiques
			if (isApiSuccess(result)) {
				// Faire quelque chose en cas de succès, par exemple logger
				console.log("Message sent successfully");
			} else {
				// Faire quelque chose en cas d'erreur, par exemple logger
				console.error("Failed to send message:", result.error);
			}

			return result;
		} catch (error) {
			console.error("Failed to send contact message:", error);
			return {
				success: false,
				message: "Failed to send message",
				error: error instanceof Error ? error.message : "Unknown error",
			};
		}
	}
}

export const apiClient = new ApiClient();
