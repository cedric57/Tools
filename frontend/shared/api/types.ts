export interface ContactMessage {
	name: string;
	email: string;
	subject: string;
	message: string;
	company?: string; // Optionnel
	phone?: string; // Optionnel
}

// Types pour les réponses API
export interface ApiSuccessResponse<T = Record<string, unknown>> {
	success: true;
	data: T;
	message: string;
}

export interface ApiErrorResponse {
	success: false;
	message: string;
	error: string;
}

export type ApiResponse<T = Record<string, unknown>> =
	| ApiSuccessResponse<T>
	| ApiErrorResponse;

// Type guard pour vérifier le succès
export function isApiSuccess<T>(
	response: ApiResponse<T>,
): response is ApiSuccessResponse<T> {
	return response.success === true;
}

// Type guard pour vérifier l'erreur
export function isApiError<T>(
	response: ApiResponse<T>,
): response is ApiErrorResponse {
	return response.success === false;
}
