// Fonctionnalités JavaScript pour les outils

// Copie dans le presse-papier - VERSION CORRIGÉE
function copyToClipboard(text, buttonElement) {
	// Utiliser l'API Clipboard moderne
	navigator.clipboard
		.writeText(text)
		.then(() => {
			// Feedback visuel
			const originalText = buttonElement.textContent;
			const originalBackground = buttonElement.style.background;

			buttonElement.textContent = "✅ Copié!";
			buttonElement.style.background = "#27ae60";
			buttonElement.style.color = "white";

			setTimeout(() => {
				buttonElement.textContent = originalText;
				buttonElement.style.background = originalBackground;
				buttonElement.style.color = "";
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
			const originalText = buttonElement.textContent;
			buttonElement.textContent = "✅ Copié!";
			buttonElement.style.background = "#27ae60";

			setTimeout(() => {
				buttonElement.textContent = originalText;
				buttonElement.style.background = "";
			}, 2000);
		} else {
			throw new Error("Méthode de secours échouée");
		}
	} catch (err) {
		console.error("Erreur méthode de secours: ", err);

		// Dernier recours : afficher le texte pour copie manuelle
		buttonElement.textContent = "❌ Échec";
		buttonElement.style.background = "#e74c3c";

		setTimeout(() => {
			buttonElement.textContent = "📋 Copier";
			buttonElement.style.background = "";
		}, 2000);

		// Afficher une alerte avec le texte pour copie manuelle
		alert(
			`Échec de la copie automatique. Voici le texte à copier manuellement :\n\n${text}`,
		);
	}
}

// Gestion des liens "coming soon"
document.addEventListener("DOMContentLoaded", () => {
	const comingSoonLinks = document.querySelectorAll(".coming-soon");

	// Remplacer forEach par for...of pour la performance
	for (const link of comingSoonLinks) {
		link.addEventListener("click", (e) => {
			e.preventDefault();

			// Créer une notification
			const notification = document.createElement("div");
			notification.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                background: #3498db;
                color: white;
                padding: 1rem 2rem;
                border-radius: 5px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                z-index: 10000;
                font-weight: 600;
            `;
			notification.textContent = "🛠️ Cet outil arrive bientôt!";

			document.body.appendChild(notification);

			setTimeout(() => {
				notification.remove();
			}, 3000);
		});
	}

	// Amélioration de l'accessibilité du menu
	const navLinks = document.querySelectorAll(".nav-link");

	// Remplacer forEach par for...of
	for (const link of navLinks) {
		link.addEventListener("keypress", function (e) {
			if (e.key === "Enter" || e.key === " ") {
				e.preventDefault();
				this.click();
			}
		});
	}

	// Initialiser les boutons de copie dynamiquement
	initializeCopyButtons();
});

// Initialiser les boutons de copie
function initializeCopyButtons() {
	const copyButtons = document.querySelectorAll(".btn-copy");

	for (const button of copyButtons) {
		button.addEventListener("click", function (e) {
			e.preventDefault();

			// Trouver le texte à copier dans le pre > code précédent
			const resultContent = this.closest(".result-content");
			if (resultContent) {
				const codeElement = resultContent.querySelector("pre code");
				if (codeElement) {
					const textToCopy = codeElement.textContent || codeElement.innerText;
					copyToClipboard(textToCopy, this);
				}
			}
		});
	}
}

// Auto-sélection du texte dans les résultats
function selectText(element) {
	const range = document.createRange();
	range.selectNodeContents(element);
	const selection = window.getSelection();
	selection.removeAllRanges();
	selection.addRange(range);
}

// Gestion des erreurs de formulaire
function clearErrorOnInput(inputId) {
	const input = document.getElementById(inputId);
	const errorDiv = input.closest(".form-group").nextElementSibling;

	if (errorDiv?.classList.contains("error")) {
		input.addEventListener("input", () => {
			errorDiv.style.display = "none";
		});
	}
}

// Fonction pour détecter et appliquer automatiquement l'encodage
function autoDetectEncoding(text) {
	// Cette fonction peut être étendue pour détecter l'encodage
	// Pour l'instant, retourne UTF-8 par défaut
	return "utf-8";
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
		// Sur la page d'accueil, focus sur le premier champ de décodage
		const decodeTextarea = document.getElementById("base64_text");
		if (decodeTextarea) {
			decodeTextarea.focus();
		}
	}
});

// Gestion du responsive menu pour mobile
function initMobileMenu() {
	const sidebar = document.querySelector(".sidebar");
	const mainContent = document.querySelector(".main-content");
	const menuToggle = document.createElement("button");

	// Créer le bouton toggle pour mobile
	menuToggle.innerHTML = "☰ Menu";
	menuToggle.style.cssText = `
        position: fixed;
        top: 10px;
        left: 10px;
        z-index: 1001;
        background: #3498db;
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 5px;
        cursor: pointer;
        display: none;
    `;

	document.body.appendChild(menuToggle);

	// Vérifier la taille de l'écran
	function checkScreenSize() {
		if (window.innerWidth <= 768) {
			menuToggle.style.display = "block";
			sidebar.style.transform = "translateX(-100%)";
			sidebar.style.transition = "transform 0.3s ease";
		} else {
			menuToggle.style.display = "none";
			sidebar.style.transform = "translateX(0)";
		}
	}

	// Toggle du menu mobile
	menuToggle.addEventListener("click", () => {
		if (
			sidebar.style.transform === "translateX(-100%)" ||
			!sidebar.style.transform
		) {
			sidebar.style.transform = "translateX(0)";
			menuToggle.innerHTML = "✕ Fermer";
		} else {
			sidebar.style.transform = "translateX(-100%)";
			menuToggle.innerHTML = "☰ Menu";
		}
	});

	// Fermer le menu en cliquant à l'extérieur
	mainContent.addEventListener("click", () => {
		if (
			window.innerWidth <= 768 &&
			sidebar.style.transform === "translateX(0)"
		) {
			sidebar.style.transform = "translateX(-100%)";
			menuToggle.innerHTML = "☰ Menu";
		}
	});

	// Écouter les changements de taille d'écran
	window.addEventListener("resize", checkScreenSize);

	// Initialiser
	checkScreenSize();
}

// Initialiser le menu mobile au chargement
document.addEventListener("DOMContentLoaded", initMobileMenu);

// Amélioration : Sauvegarde automatique des données (optionnel)
function autoSaveData(key, data) {
	if (typeof Storage !== "undefined") {
		try {
			localStorage.setItem(`base64_tool_${key}`, data);
		} catch (e) {
			console.warn("Impossible de sauvegarder les données:", e);
		}
	}
}

function loadAutoSavedData(key) {
	if (typeof Storage !== "undefined") {
		try {
			return localStorage.getItem(`base64_tool_${key}`) || "";
		} catch (e) {
			console.warn("Impossible de charger les données:", e);
			return "";
		}
	}
	return "";
}

// Charger les données sauvegardées au chargement de la page
document.addEventListener("DOMContentLoaded", () => {
	const encodeTextarea = document.getElementById("plain_text");
	const decodeTextarea = document.getElementById("base64_text");

	if (encodeTextarea) {
		const savedEncode = loadAutoSavedData("encode");
		if (savedEncode) {
			encodeTextarea.value = savedEncode;
		}

		encodeTextarea.addEventListener("input", function () {
			autoSaveData("encode", this.value);
		});
	}

	if (decodeTextarea) {
		const savedDecode = loadAutoSavedData("decode");
		if (savedDecode) {
			decodeTextarea.value = savedDecode;
		}

		decodeTextarea.addEventListener("input", function () {
			autoSaveData("decode", this.value);
		});
	}
});

// Fonction pour effacer tous les champs
function clearAllFields() {
	const encodeTextarea = document.getElementById("plain_text");
	const decodeTextarea = document.getElementById("base64_text");
	const results = document.querySelectorAll(".result");
	const errors = document.querySelectorAll(".error");

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
}

// Raccourci clavier : Ctrl + K pour effacer tout
document.addEventListener("keydown", (e) => {
	if ((e.ctrlKey || e.metaKey) && e.key === "k") {
		e.preventDefault();
		clearAllFields();

		// Notification
		const notification = document.createElement("div");
		notification.textContent = "🧹 Tous les champs ont été effacés!";
		notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f39c12;
            color: white;
            padding: 1rem 2rem;
            border-radius: 5px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            z-index: 10000;
            font-weight: 600;
        `;

		document.body.appendChild(notification);
		setTimeout(() => notification.remove(), 2000);
	}
});
