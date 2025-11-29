export interface ContactMessage {
	name: string;
	email: string;
	subject: string;
	message: string;
	company?: string; // Optionnel
	phone?: string; // Optionnel
}

export interface ApiResponse<T = unknown> {
	success: boolean;
	data?: T;
	message: string;
	error?: string;
}
