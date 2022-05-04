from random import uniform
from random import randrange


class Equipment:
    def __init__(self):
        self.legendary_sword = frostmourne
        self.legendary_cape = gladiator_cape
        self.normal_sword = long_sword
        self.normal_cape = cloak_cape
        self.rng = [frostmourne, gladiator_cape, long_sword, cloak_cape]


class Sword:
    def __init__(self, name, lege):
        self.name = name
        self.power = uniform(1.1, lege)

    def __str__(self):
        return f"{self.name}"


class Cape:
    def __init__(self, name, lege):
        self.power = uniform(1.1, lege)
        self.name = name

    def __str__(self):
        return f"{self.name}"


class Character:
    def __init__(self, name, attack_speed=2, delay=0):
        self.equipment = Equipment()
        self.item = self.equipment.rng[randrange(len(self.equipment.rng))]
        self.name = name
        self.hp = 100
        self.attack_speed = attack_speed
        self.delay = delay
        self.max_health = 100
        if isinstance(self.item,Cape):
            self.hp *= self.item.power
            self.max_health *= self.item.power


    def attack(self):
        self.delay = 6 - self.attack_speed
        if isinstance(self.item,Sword):
            return round(randrange(3, 10 + 1) * self.item.power)
        else:
            return randrange(3, 10 + 1)

    def is_dead(self):
        return self.hp <= 0

    def end_round(self):
        self.hp = self.hp + 1 if self.hp + 1 <= self.max_health else self.max_health
        self.delay -= 1

    def __str__(self):
        return f"{self.name}: HP:{round(self.hp)} DELAY: {self.delay}"

    def __repr__(self):
        return f"Character {self.name}: HP:{self.hp} DELAY: {self.delay}"

    def __iadd__(self, other):
        self.hp += other
        return self

    def __isub__(self, other):
        self.hp -= other
        return self


class Arena:
    def __init__(self, team_a, team_b):
        self.a = team_a
        self.b = team_b

    def __str__(self):
        st = "\n" + "=" * 30
        st += f"\n TEAM A"
        for member in self.a:
            st += f"\n {member}"
        st += "\n" + "=" * 30
        st += f"\n TEAM B"
        for member in self.b:
            st += f"\n {member}"
        st += "\n" + "=" * 30
        return st

    def __repr__(self):
        st = f"ARENA STATUS \n Alive in team A: {len(self.a)} \n Alive in team B: {len(self.b)} \n (["
        st += ", ".join([repr(character) for character in self.a])
        st += "],["
        st += ", ".join([repr(character) for character in self.b])
        st += "])"
        return st

    def play(self):
        play_timeA = []
        play_timeB = []
        while True:
            print(self)
            for team in self.a:
                if team.delay == 0:
                    play_timeA.append(team)
            for team in self.b:
                if team.delay == 0:
                    play_timeB.append(team)
            print("BATTLE PHASE")
            print("=" * 15)
            for team in play_timeA:
                if len(self.b) == 0:
                    break
                x = randrange(len(self.b))
                dmg = team.attack()
                self.b[x].hp -= dmg
                if isinstance(team.item,Sword):
                    print(f"{team.name} attacked dealt {dmg} damage with {team.item.name} the opponent {self.b[x].name}")
                else:
                    print(f"{team.name} attacked with {dmg} damage the opponent {self.b[x].name}")
                if self.b[x].is_dead():
                    print(f"{self.b[x].name} is DEAD")
                    self.b.pop(x)
            for team in play_timeB:
                if len(self.a) == 0:
                    break
                x = randrange(len(self.a))
                dmg = team.attack()
                self.a[x].hp -= dmg
                if isinstance(team.item,Sword):
                    print(f"{team.name} attacked dealt {dmg} damage with {team.item.name} the opponent {self.a[x].name}")
                else:
                    print(f"{team.name} attacked with {dmg} damage the opponent {self.a[x].name}")
                if self.a[x].is_dead():
                    print(f"{self.a[x].name} is DEAD")
                    self.a.pop(x)
            play_timeA.clear()
            play_timeB.clear()
            if len(self.a) == 0 and len(self.b) == 0:
                print("ITS A DRAW")
                return
            if len(self.b) == 0:
                print("winner is ORCS")
                return
            elif len(self.a) == 0:
                print("winner is ELFS")
                return
            for alive in self.a:
                alive.end_round()
            for alive in self.b:
                alive.end_round()


def main():
    orcs = [Character("ORC" + str(i + 1), delay=randrange(0, 3 + 1)) for i in range(5)]
    night_elfs = [Character("NIGHT ELF" + str(i + 1), delay=randrange(0, 2 + 1)) for i in range(4)]
    Stormwind = Arena(orcs, night_elfs)
    for i in orcs:
        print(type(i.item))
    for i in night_elfs:
        print(i.item)
    Stormwind.play()


frostmourne = Sword("Frostmourne", 2.1)
long_sword = Sword("long sword", 1.5)
gladiator_cape = Cape("Gladiator cape", 1.8)
cloak_cape = Cape("cloak cape", 1.3)

main()
