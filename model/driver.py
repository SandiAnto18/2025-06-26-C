from dataclasses import dataclass

@dataclass
class Driver:
    driverId: int
    position: int
    raceId: int



    def __hash__(self):
        return hash(self.constructorId)

    def __str__(self):
        return f"({self.name})"