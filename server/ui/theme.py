"""
Thème Gruvbox Dark Hard pour HyperMonitor
Palette de couleurs et helpers
"""

class GruvboxTheme:
    """Thème Gruvbox Dark Hard"""
    
    # Couleurs principales
    BG = "#1d2021"
    BG_SOFT = "#282828"
    BG_HARD = "#1d2021"
    
    FG = "#ebdbb2"
    FG_DIM = "#a89984"
    
    # Couleurs d'accent
    RED = "#fb4934"
    GREEN = "#b8bb26"
    YELLOW = "#fabd2f"
    BLUE = "#83a598"
    PURPLE = "#d3869b"
    AQUA = "#8ec07c"
    ORANGE = "#fe8019"
    
    # Couleurs sémantiques
    PRIMARY = "#b8bb26"      # Vert
    SUCCESS = "#8ec07c"      # Aqua
    WARNING = "#fabd2f"      # Jaune
    ERROR = "#fb4934"        # Rouge
    INFO = "#83a598"         # Bleu
    
    # Interface
    BORDER = "#504945"
    TEXT_DIM = "#928374"
    
    # Seuils de couleurs
    THRESHOLDS = {
        'low': 50,      # < 50% : Vert
        'medium': 75,   # 50-75% : Aqua
        'high': 90,     # 75-90% : Jaune
        'critical': 90  # >= 90% : Rouge
    }
    
    TEMP_THRESHOLDS = {
        'low': 50,
        'medium': 65,
        'high': 75,
        'critical': 85
    }
    
    def get_threshold_color(self, value: float) -> str:
        """
        Retourne la couleur Rich selon le seuil de la valeur
        
        Args:
            value: Valeur en pourcentage (0-100)
            
        Returns:
            Nom de couleur Rich (ex: "bright_red")
        """
        if value >= self.THRESHOLDS['critical']:
            return "bright_red"
        elif value >= self.THRESHOLDS['high']:
            return "yellow"
        elif value >= self.THRESHOLDS['medium']:
            return "cyan"
        else:
            return "bright_green"
    
    def get_temp_color(self, temp: float) -> str:
        """
        Retourne la couleur Rich selon la température
        
        Args:
            temp: Température en °C
            
        Returns:
            Nom de couleur Rich
        """
        if temp >= self.TEMP_THRESHOLDS['critical']:
            return "bright_red"
        elif temp >= self.TEMP_THRESHOLDS['high']:
            return "yellow"
        elif temp >= self.TEMP_THRESHOLDS['medium']:
            return "cyan"
        else:
            return "bright_green"
    
    def get_status_icon(self, status: str) -> str:
        """
        Retourne l'icône selon le statut
        
        Args:
            status: 'online', 'offline', 'warning', 'error'
            
        Returns:
            Emoji ou caractère Unicode
        """
        icons = {
            'online': '[ONLINE]',
            'offline': '[OFFLINE]',
            'warning': '[WARNING]',
            'error': '[ERROR]',
            'unknown': '[UNKNOWN]'
        }
        return icons.get(status, icons['unknown'])
    
    def format_bytes(self, bytes_value: int) -> str:
        """
        Formate les octets en unité lisible
        
        Args:
            bytes_value: Taille en octets
            
        Returns:
            Chaîne formatée (ex: "1.5 GB")
        """
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
    
    def format_percent(self, value: float) -> str:
        """
        Formate un pourcentage avec couleur
        
        Args:
            value: Valeur en pourcentage
            
        Returns:
            Chaîne Rich formatée avec couleur
        """
        color = self.get_threshold_color(value)
        return f"[{color}]{value:.1f}%[/{color}]"


# Constantes globales pour compatibilité
GRUVBOX_THEME = {
    'background': GruvboxTheme.BG,
    'foreground': GruvboxTheme.FG,
    'red': GruvboxTheme.RED,
    'green': GruvboxTheme.GREEN,
    'yellow': GruvboxTheme.YELLOW,
    'blue': GruvboxTheme.BLUE,
    'purple': GruvboxTheme.PURPLE,
    'aqua': GruvboxTheme.AQUA,
    'orange': GruvboxTheme.ORANGE,
}


def get_color_for_value(value: float, thresholds: dict = None) -> str:
    """
    Fonction helper pour obtenir une couleur selon une valeur
    
    Args:
        value: Valeur à évaluer
        thresholds: Dict avec 'warning', 'critical', etc.
        
    Returns:
        Code couleur Rich
    """
    if thresholds is None:
        thresholds = GruvboxTheme.THRESHOLDS
    
    theme = GruvboxTheme()
    return theme.get_threshold_color(value)
