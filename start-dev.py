#!/usr/bin/env python3
# start-dev.py
import sys
import signal
import time
from pathlib import Path

# Utilisation de subprocess de manière sécurisée
import subprocess  # nosec B404


class DevStarter:
    def __init__(self):
        self.processes = []
        # Commandes fixes - pas d'entrée utilisateur non fiable
        self.services = [
            {
                "name": "Backend FastAPI",
                "directory": "backend",
                "command": ["uvicorn", "main:app", "--reload", "--port", "8000"],
                "url": "http://localhost:8000",
            },
            {
                "name": "Marketing Astro",
                "directory": "frontend/marketing",
                "command": ["npm", "run", "dev"],
                "url": "http://localhost:3000",
            },
            {
                "name": "App Next.js",
                "directory": "frontend/app",
                "command": ["npm", "run", "dev"],
                "url": "http://localhost:3001",
            },
        ]

    def check_directories(self):
        """Vérifier que tous les répertoires existent"""
        for service in self.services:
            if not Path(service["directory"]).exists():
                print(f"❌ Répertoire {service['directory']} introuvable!")
                return False
        return True

    def start_services(self):
        """Démarrer tous les services de manière sécurisée"""
        print("🚀 Démarrage de l'application complète...")

        for service in self.services:
            print(f"📦 Démarrage de {service['name']}...")

            try:
                # Vérifier que le répertoire existe
                service_dir = Path(service["directory"])
                if not service_dir.exists():
                    print(f"   ❌ Répertoire {service['directory']} introuvable")
                    continue

                # Démarrer le processus de manière sécurisée
                process = subprocess.Popen(  # nosec B603
                    service["command"],
                    cwd=str(service_dir),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                    shell=False,
                )

                self.processes.append(
                    {
                        "process": process,
                        "name": service["name"],
                        "directory": service["directory"],
                        "url": service["url"],
                    }
                )

                print(f"   ✅ {service['name']} démarré (PID: {process.pid})")
                print(f"   🌐 {service['url']}")

            except FileNotFoundError as e:
                print(f"   ❌ Commande non trouvée: {service['command'][0]} - {e}")
            except PermissionError as e:
                print(f"   ❌ Permission refusée: {e}")
            except Exception as e:
                print(f"   ❌ Erreur inattendue: {e}")

        print("\n✅ Tous les services sont en cours de démarrage!")
        print("💡 Press Ctrl+C pour arrêter tous les services\n")

    def monitor_services(self):
        """Surveiller l'état des services"""
        try:
            while True:
                time.sleep(5)
                self.check_processes()

                # Afficher un heartbeat toutes les 30 secondes
                if int(time.time()) % 30 == 0:
                    print("💓 Services toujours en cours d'exécution...")

        except KeyboardInterrupt:
            self.cleanup()

    def check_processes(self):
        """Vérifier que tous les processus tournent toujours"""
        active_processes = []
        for proc_info in self.processes:
            if proc_info["process"].poll() is None:
                active_processes.append(proc_info)
            else:
                print(f"❌ {proc_info['name']} s'est arrêté!")
                # Lire la sortie restante avec gestion d'erreurs appropriée
                self._read_process_output(proc_info)

        self.processes = active_processes

    def _read_process_output(self, proc_info):
        """Lire la sortie d'un processus avec une gestion d'erreurs appropriée"""
        try:
            output = proc_info["process"].stdout.read()
            if output and output.strip():
                # Limiter la longueur de l'affichage
                truncated_output = output[:200] + "..." if len(output) > 200 else output
                print(f"   Dernière sortie: {truncated_output}")
        except ValueError:
            # Le fichier stdout est déjà fermé
            print("   Impossible de lire la sortie: flux fermé")
        except OSError as e:
            # Erreur d'E/S
            print(f"   Erreur E/S lors de la lecture: {e}")
        except Exception as e:
            # Loguer toute autre erreur inattendue
            print(f"   Erreur inattendue lors de la lecture: {e}")

    def cleanup(self):
        """Arrêter tous les processus de manière sécurisée"""
        print("\n🛑 Arrêt des services...")

        for proc_info in self.processes:
            print(f"⏹️  Arrêt de {proc_info['name']}...")
            try:
                # Terminer gentiment d'abord
                proc_info["process"].terminate()

                # Attendre un peu puis tuer si nécessaire
                try:
                    proc_info["process"].wait(timeout=5)
                    print(f"   ✅ {proc_info['name']} arrêté proprement")
                except subprocess.TimeoutExpired:
                    print(f"   ⚠️  Forçage de l'arrêt de {proc_info['name']}...")
                    proc_info["process"].kill()
                    proc_info["process"].wait()
                    print(f"   ✅ {proc_info['name']} arrêté de force")

            except ProcessLookupError:
                print(f"   ℹ️  {proc_info['name']} était déjà arrêté")
            except Exception as e:
                print(f"   ❌ Erreur lors de l'arrêt de {proc_info['name']}: {e}")

        print("✅ Tous les services sont arrêtés.")
        sys.exit(0)


def main():
    starter = DevStarter()

    # Vérifier les répertoires
    if not starter.check_directories():
        print("❌ Vérification des répertoires échouée. Arrêt.")
        sys.exit(1)

    # Démarrer les services
    starter.start_services()

    # Gérer les signaux d'arrêt
    def signal_handler(signum, frame):
        print(f"\n📡 Signal {signum} reçu...")
        starter.cleanup()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Surveiller
    try:
        starter.monitor_services()
    except Exception as e:
        print(f"❌ Erreur inattendue dans le monitor: {e}")
        starter.cleanup()


if __name__ == "__main__":
    main()
