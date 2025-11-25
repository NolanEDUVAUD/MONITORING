from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, DataTable
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
from rich.table import Table as RichTable
from datetime import datetime
import asyncio

from .theme import GruvboxTheme

class ServerCard(Static):
    """Widget pour afficher les infos d'un serveur"""

    def __init__(self, server_data: dict):
        super().__init__()
        self.server_data = server_data

    def render(self) -> Panel:
        """Rendu du widget"""
        data = self.server_data
        theme = GruvboxTheme()

        # Création du tableau
        table = RichTable.grid(padding=(0, 2))
        table.add_column(justify="right", style=theme.TEXT_DIM)
        table.add_column(justify="left")

        # Nom du serveur
        name = data.get('hostname', 'Unknown')
        status = "[ONLINE]" if data.get('status') == 'online' else "[OFFLINE]"

        # Métriques
        cpu = data.get('cpu', {}).get('percent', 0)
        ram = data.get('memory', {}).get('percent', 0)
        temp = data.get('temperature', {}).get('cpu', 0)

        # Ajout des lignes avec couleurs selon seuils
        table.add_row("Status:", status)
        table.add_row("OS:", data.get('os', 'N/A'))
        table.add_row("CPU:", f"[{theme.get_threshold_color(cpu)}]{cpu:.1f}%[/]")
        table.add_row("RAM:", f"[{theme.get_threshold_color(ram)}]{ram:.1f}%[/]")

        if temp > 0:
            table.add_row("Temp:", f"[{theme.get_temp_color(temp)}]{temp:.1f}°C[/]")

        # Disques
        for disk in data.get('disks', [])[:3]:  # Max 3 disques affichés
            usage = disk.get('percent', 0)
            table.add_row(
                f"Disk {disk.get('device', '?')}:",
                f"[{theme.get_threshold_color(usage)}]{usage:.1f}%[/]"
            )

        # Dernière mise à jour
        last_update = data.get('last_update', 'N/A')
        if isinstance(last_update, (int, float)):
            from datetime import datetime
            last_update = datetime.fromtimestamp(last_update).strftime('%H:%M:%S')
        table.add_row("Updated:", f"[{theme.TEXT_DIM}]{last_update}[/]")

        # Panel avec bordure Gruvbox
        return Panel(
            table,
            title=f"[{theme.PRIMARY}]▶ {name}[/]",
            border_style=theme.BORDER,
            padding=(1, 2)
        )

class MonitorDashboard(App):
    """Interface TUI principale"""

    CSS = """
    Screen {
        background: #1d2021;
    }

    #server-grid {
        layout: grid;
        grid-size: 2;
        grid-gutter: 1;
        padding: 1;
    }

    ServerCard {
        height: auto;
        margin: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
        ("a", "add_server", "Add Server"),
    ]

    # État réactif
    servers_data = reactive({})

    def __init__(self, api):
        super().__init__()
        self.api = api
        self.theme = GruvboxTheme()
        self.refresh_task = None

    def compose(self) -> ComposeResult:
        """Composition de l'interface"""
        yield Header(show_clock=True)

        with Container(id="server-grid"):
            # Les serveurs seront ajoutés dynamiquement
            pass

        yield Footer()

    async def on_mount(self) -> None:
        """Appelé quand l'app est montée"""
        self.title = "HyperMonitor - Server Monitoring"
        self.sub_title = "Gruvbox Dark Hard Theme | Refresh: 3s"

        # Lancer le refresh
        await self.refresh_servers()
        self.refresh_task = self.set_interval(3, self.refresh_servers)

    async def refresh_servers(self) -> None:
        """Rafraîchit les données des serveurs"""
        try:
            # Récupérer les serveurs depuis l'API
            servers = self.api.get_servers()
            
            # Mettre à jour les données
            self.servers_data = servers
            
            # Mettre à jour l'affichage
            container = self.query_one("#server-grid")
            
            # Vider le conteneur
            await container.remove_children()
            
            # Ajouter les cartes
            if not servers:
                await container.mount(Static(
                    "[dim]⏳ En attente des agents...\n\n"
                    "Lancez un agent avec :\n"
                    "  python agent.py[/dim]"
                ))
            else:
                for hostname, data in servers.items():
                    card = ServerCard(data)
                    await container.mount(card)
                    
        except Exception as e:
            self.notify(f"Erreur refresh: {e}", severity="error")
            container = self.query_one("#server-grid")
            await container.mount(Static(f"[red][ERROR] Erreur: {str(e)}[/red]"))

    def action_refresh(self) -> None:
        """Action manuelle de refresh"""
        self.notify("🔄 Rafraîchissement manuel...", timeout=2)
        asyncio.create_task(self.refresh_servers())

    def action_add_server(self) -> None:
        """Action d'ajout de serveur (TODO)"""
        self.notify("[!] Fonctionnalite a venir", severity="warning")

    async def on_unmount(self) -> None:
        """Nettoyage à la fermeture"""
        if self.refresh_task:
            self.refresh_task.stop()
