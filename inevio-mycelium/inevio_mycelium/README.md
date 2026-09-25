# inevio-mycelium

Живая грибница для Inevio. Растёт через сеть **слой за слоем**.

## Что делает

- **SCOUT** — ищет новых соседей через все каналы.
- **ATTACH** — закрепляется на найденных.
- **PENETRATE** — идёт глубже через gateways.
- **ASSESS** — решает, куда расти.
- **TEACH** — делится знанием.
- **MERGE** — сливает карты.

## Установка

    pip install inevio-mycelium

## Быстрый старт

    from spore_bridge import SporeBridge
    from inevio_mycelium import Mycelium

    bridge = SporeBridge('node-1', port=8700)
    bridge.loop(blocking=False)

    org = Mycelium(bridge, max_depth=10)
    org.start()

    print(org.get_stats())
    # {'attached': 42, 'depth_max': 5, ...}

## Что это даёт

- **Живой рост** — грибница сама ищет и закрепляется.
- **Глубина** — проникает через gateway в подсети.
- **Слияние** — обменивается картами с другими грибницами.
- **Адаптивный heartbeat** — быстрее при активности, медленнее в тишине.

## Лицензия

MIT