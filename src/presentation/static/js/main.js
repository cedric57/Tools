// Fonctionnalités JavaScript pour les outils avec Bootstrap

// Copie dans le presse-papier
function copyToClipboard(text, buttonElement) {
	// Utiliser l'API Clipboard moderne
	navigator.clipboard
		.writeText(text)
		.then(() => {
			// Feedback visuel avec Bootstrap
			const originalHTML = buttonElement.innerHTML;
			buttonElement.innerHTML = '<i class="bi bi-check-lg"></i> Copié!';
			buttonElement.classList.remove("btn-outline-primary");
			buttonElement.classList.add("btn-success");

			setTimeout(() => {
				buttonElement.innerHTML = originalHTML;
				buttonElement.classList.remove("btn-success");
				buttonElement.classList.add("btn-outline-primary");
			}, 2000);
		})
		.catch((err) => {
			console.error("Erreur lors de la copie: ", err);

			// Fallback pour les navigateurs plus anciens
			fallbackCopyToClipboard(text, buttonElement);
		});
}

// Méthode de secours pour la copie
function fallbackCopyToClipboard(text, buttonElement) {
	try {
		// Créer un élément textarea temporaire
		const textArea = document.createElement("textarea");
		textArea.value = text;
		textArea.style.position = "fixed";
		textArea.style.left = "-999999px";
		textArea.style.top = "-999999px";
		document.body.appendChild(textArea);
		textArea.focus();
		textArea.select();

		// Essayer la commande de copie
		const successful = document.execCommand("copy");
		document.body.removeChild(textArea);

		if (successful) {
			// Feedback visuel pour la méthode de secours
			const originalHTML = buttonElement.innerHTML;
			buttonElement.innerHTML = '<i class="bi bi-check-lg"></i> Copié!';
			buttonElement.classList.remove("btn-outline-primary");
			buttonElement.classList.add("btn-success");

			setTimeout(() => {
				buttonElement.innerHTML = originalHTML;
				buttonElement.classList.remove("btn-success");
				buttonElement.classList.add("btn-outline-primary");
			}, 2000);
		} else {
			throw new Error("Méthode de secours échouée");
		}
	} catch (err) {
		console.error("Erreur méthode de secours: ", err);

		// Dernier recours
		buttonElement.innerHTML = '<i class="bi bi-x-lg"></i> Échec';
		buttonElement.classList.remove("btn-outline-primary");
		buttonElement.classList.add("btn-danger");

		setTimeout(() => {
			buttonElement.innerHTML = '<i class="bi bi-clipboard"></i> Copier';
			buttonElement.classList.remove("btn-danger");
			buttonElement.classList.add("btn-outline-primary");
		}, 2000);

		// Afficher une alerte Bootstrap
		showBootstrapAlert(
			"Échec de la copie automatique. Le texte est disponible pour copie manuelle.",
			"warning",
		);
	}
}

// Fonction pour afficher des alertes Bootstrap
function showBootstrapAlert(message, type = "info") {
	const alertDiv = document.createElement("div");
	alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
	alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

	// Ajouter au début du main content
	const mainContent = document.querySelector(".main-content");
	mainContent.insertBefore(alertDiv, mainContent.firstChild);

	// Auto-suppression après 5 secondes
	setTimeout(() => {
		if (alertDiv.parentNode) {
			alertDiv.remove();
		}
	}, 5000);
}

// Gestion des liens "coming soon"
document.addEventListener("DOMContentLoaded", () => {
	const comingSoonLinks = document.querySelectorAll(".nav-link.text-muted");

	for (const link of comingSoonLinks) {
		link.addEventListener("click", (e) => {
			e.preventDefault();
			showBootstrapAlert("🛠️ Cet outil arrive bientôt!", "info");
		});
	}
});

// Auto-sélection du texte dans les résultats
function selectText(element) {
	const range = document.createRange();
	range.selectNodeContents(element);
	const selection = window.getSelection();
	selection.removeAllRanges();
	selection.addRange(range);
}

// Amélioration de l'UX : Focus sur le premier champ
document.addEventListener("DOMContentLoaded", () => {
	// Focus sur le premier champ de texte selon la page
	const currentPath = window.location.pathname;

	if (currentPath === "/encode") {
		const encodeTextarea = document.getElementById("plain_text");
		if (encodeTextarea) {
			encodeTextarea.focus();
		}
	} else if (currentPath === "/decode") {
		const decodeTextarea = document.getElementById("base64_text");
		if (decodeTextarea) {
			decodeTextarea.focus();
		}
	} else if (currentPath === "/") {
		const decodeTextarea = document.getElementById("base64_text");
		if (decodeTextarea) {
			decodeTextarea.focus();
		}
	}

	// Détection automatique des entrées multiples
	autoDetectMultipleEntries();
});

// Détection automatique des entrées multiples
function autoDetectMultipleEntries() {
	const decodeTextarea = document.getElementById("base64_text");
	const lineByLineCheckbox = document.getElementById("decode_line_by_line");

	if (decodeTextarea && lineByLineCheckbox) {
		decodeTextarea.addEventListener("input", function () {
			const lines = this.value.split("\n").filter((line) => line.trim());

			// Si on détecte plusieurs lignes non vides, suggérer le décodage ligne par ligne
			if (lines.length > 1 && !lineByLineCheckbox.checked) {
				const existingSuggestion = document.getElementById(
					"multi-line-suggestion",
				);
				if (!existingSuggestion) {
					const suggestionDiv = document.createElement("div");
					suggestionDiv.id = "multi-line-suggestion";
					suggestionDiv.className =
						"alert alert-info alert-dismissible fade show mt-3";
					suggestionDiv.innerHTML = `
                        <i class="bi bi-info-circle me-2"></i>
                        Plusieurs lignes détectées.
                        <button type="button" class="btn btn-sm btn-outline-info ms-2" onclick="enableLineByLine()">
                            Activer le décodage ligne par ligne
                        </button>
                        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                    `;
					decodeTextarea.parentNode.insertBefore(
						suggestionDiv,
						decodeTextarea.nextSibling,
					);
				}
			} else {
				const suggestion = document.getElementById("multi-line-suggestion");
				if (suggestion) {
					suggestion.remove();
				}
			}
		});
	}
}

function enableLineByLine() {
	const checkbox = document.getElementById("decode_line_by_line");
	if (checkbox) {
		checkbox.checked = true;
		const suggestion = document.getElementById("multi-line-suggestion");
		if (suggestion) {
			suggestion.innerHTML =
				'<i class="bi bi-check-circle me-2"></i>Décodage ligne par ligne activé!';
			suggestion.className =
				"alert alert-success alert-dismissible fade show mt-3";
			setTimeout(() => {
				if (suggestion.parentNode) {
					suggestion.remove();
				}
			}, 3000);
		}
	}
}

// Fonction pour effacer tous les champs
function clearAllFields() {
	const encodeTextarea = document.getElementById("plain_text");
	const decodeTextarea = document.getElementById("base64_text");
	const results = document.querySelectorAll(".card.bg-light");
	const errors = document.querySelectorAll(".alert-danger");

	if (encodeTextarea) encodeTextarea.value = "";
	if (decodeTextarea) decodeTextarea.value = "";

	// Supprimer les résultats et erreurs
	for (const result of results) {
		result.remove();
	}

	for (const error of errors) {
		error.remove();
	}

	// Effacer le stockage local
	if (typeof Storage !== "undefined") {
		try {
			localStorage.removeItem("base64_tool_encode");
			localStorage.removeItem("base64_tool_decode");
		} catch (e) {
			console.warn("Impossible d'effacer le stockage:", e);
		}
	}

	showBootstrapAlert("🧹 Tous les champs ont été effacés!", "success");
}

// Raccourci clavier : Ctrl + K pour effacer tout
document.addEventListener("keydown", (e) => {
	if ((e.ctrlKey || e.metaKey) && e.key === "k") {
		e.preventDefault();
		clearAllFields();
	}
});

// Gestion des tooltips
document.addEventListener("DOMContentLoaded", () => {
	const tooltipTriggerList = [].slice.call(
		document.querySelectorAll('[data-bs-toggle="tooltip"]'),
	);
	const tooltipList = tooltipTriggerList.map(
		(tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl),
	);
});
