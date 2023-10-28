# Boids

Back-end Python service which implements the Boid behavior.

## Development Environment

### Prerequisites:

- Elasticsearch
- NATS

### Running inside the container
```
user@host:~ ./boids-gateway.py -v /etc/boids/*
2023-10-28T18:07:12 DEBUG             boids_utils.elastic: Connecting to http://elasticsearch.boids:9200...
.
.
.
```
### Running Unit Tests
```
$ cd /opt/boids-gateway
$ clear; pytest
```

**Warning: Nees update!**
```mermaid
classDiagram
    class Boid {
        +dict configuration
        +Number id
        +geometry.Vector velocity
        +geometry.Point position
        +update()
    }

    class GlBoid {
        +geometry.Vector[]  body
        +gl.Color           color

        +batch(gl.Batch batch, **kwargs)
    }

    class World {
        +dict           configuration
        +geometry.Point extents
        +dict           neighbors
        +update(dt)
        +batch()
    }

    class Behavior {
        +Number     order
        +String[]   tags
    }

    class BehaviorManager{

    }

    class Simulation{
        +Number rate

        +tick()
        +update()
    }

    class SimulationState{
        <<enumeration>>
        PAUSED
        RUNNING
        STEP
    }

    Simulation          ..>         World
    Simulation          *--         SimulationState
    Boid                *--     "1" BehaviorManager
    BehaviorManager     *..     "*" Behavior
    Behavior            <|--        WallAvoider
    WallAvoider         <|--        NorthWallAvoider
    WallAvoider         <|--        SouthWallAvoider
    WallAvoider         <|--        EastWallAvoider
    WallAvoider         <|--        WestWallAvoider
    Behavior            <|--        NormalizeVelocity
    Behavior            <|--        ConstrainVelocity
    Behavior            <|--        ConstrainPosition

    GlBoid              ..>         gl
    Boid                <|--        GlBoid

```

```mermaid
stateDiagram-v2
    direction LR
    [*] -->  Paused
    Paused  --> Running
    Running --> Paused

    Paused  --> Step
    Step    --> Paused

    note right of Step
        while ticks--
    end note

```
