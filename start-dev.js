// start-dev.js
const { spawn } = require("node:child_process");
const chalk = require("chalk");

console.log(chalk.blue.bold("🚀 Démarrage de l'application complète...\n"));

// Configuration des services
const services = [
	{
		name: "Backend FastAPI",
		command: "uvicorn",
		args: ["main:app", "--reload", "--port", "8000"],
		cwd: "./backend",
		color: chalk.magenta,
	},
	{
		name: "Marketing (Astro)",
		command: "npm",
		args: ["run", "dev"],
		cwd: "./frontend/marketing",
		color: chalk.cyan,
	},
	{
		name: "App (Next.js)",
		command: "npm",
		args: ["run", "dev"],
		cwd: "./frontend/app",
		color: chalk.green,
	},
];

const processes = [];

// Démarrer chaque service
for (const service of services) {
	console.log(service.color(`📦 Démarrage de ${service.name}...`));

	const child = spawn(service.command, service.args, {
		cwd: service.cwd,
		stdio: "pipe",
		shell: true,
	});

	child.serviceName = service.name;
	child.color = service.color;

	// Gestion de la sortie standard
	child.stdout.on("data", (data) => {
		const output = data.toString().trim();
		if (output) {
			console.log(service.color(`[${service.name}] ${output}`));
		}
	});

	// Gestion des erreurs
	child.stderr.on("data", (data) => {
		const error = data.toString().trim();
		if (error && !error.includes("warning")) {
			// Filtrer les warnings
			console.log(service.color(`[${service.name}] ${error}`));
		}
	});

	child.on("close", (code) => {
		if (code !== 0 && code !== null) {
			console.log(
				chalk.red(`❌ ${service.name} s'est arrêté avec le code ${code}`),
			);
		}
	});

	processes.push(child);
}

// Gestion propre de la fermeture
process.on("SIGINT", () => {
	console.log(chalk.yellow("\n🛑 Arrêt de tous les services..."));
	for (const child of processes) {
		child.kill("SIGINT");
	}
	setTimeout(() => {
		process.exit();
	}, 1000);
});

process.on("SIGTERM", () => {
	for (const child of processes) {
		child.kill();
	}
	process.exit();
});

console.log(chalk.green("\n✅ Tous les services sont en cours de démarrage!"));
console.log(chalk.gray("📍 Backend: http://localhost:8000"));
console.log(chalk.gray("📍 Marketing: http://localhost:3000"));
console.log(chalk.gray("📍 App: http://localhost:3001"));
console.log(chalk.yellow("💡 Press Ctrl+C pour arrêter tous les services\n"));
