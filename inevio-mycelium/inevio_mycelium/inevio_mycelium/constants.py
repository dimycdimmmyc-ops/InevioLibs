"""Mycelium constants."""

# Глубина
MAX_DEPTH_DEFAULT = 10
DEPTH_INCREMENT = 1

# Heartbeat (адаптивный)
HEARTBEAT_MIN = 5
HEARTBEAT_MAX = 60
HEARTBEAT_BASE = 15

# Batch sizes
BATCH_SCOUT = 100
BATCH_ATTACH = 50
BATCH_PENETRATE = 20

# Память
MEMORY_NODES_MAX = 10000
MEMORY_PHASE_LOG_MAX = 200

# Топики (topics) для spore-bridge
TOPIC_HELLO = 'mycelium.hello'
TOPIC_MAP = 'mycelium.map'
TOPIC_REQUEST_MAP = 'mycelium.request_map'
TOPIC_PENETRATE = 'mycelium.penetrate'

# Фазы
PHASES = [
    'scout', 'attach', 'penetrate',
    'assess', 'teach', 'merge', 'breathe',
]