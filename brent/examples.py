from brent import DAG
from brent.datasets import generate_risk_dataset


def generate_risk_dag(attackers=3, defenders=2, battle_size=2):
    """
    This DAG generalises a scenario in the RISK board game. In this game
    typically three armies attack and two defend. The highest scoring attacker
    (based on a dice roll) is matched with the highest scoring defender, the second
    highest attacker goes with the second highest defender and so on. The defending
    party has the advantage so the attacker needs to roll higher than the defender
    in order to win. The `losses` node in the graph corresponds to the losses
    that the attacker incurs after the battle.

    This dag is used in the corresponding `brent.datasets.generate_risk_dataset`.

    ## Input

    - **num_attackers**: The number of dice rolled by the attacker (default: 3)
    - **num_defenders**: The number of dice rolled by the defender (default: 2)
    - **num_attackers**: The number of armies that take part in the battle (default: 2)

    ## Output

    A DAG object with correct arcs, ready for queries.
    """
    if min(attackers, defenders) < battle_size:
        raise ValueError(
            f"We demand min(num_attackers={attackers}, num_defenders={defenders}) >= battle_size={battle_size}.")
    attack_names = [f"a{i}" for i in range(1, attackers + 1)]
    defend_names = [f"d{i}" for i in range(1, defenders + 1)]
    dag = DAG(dataframe=generate_risk_dataset(attackers, defenders, battle_size))
    for side in ['a', 'd']:
        for b in range(1, battle_size + 1):
            names = attack_names if side == 'a' else defend_names
            for name in names:
                dag.add_edge(name, f"best_{side}{b}")
    for n in [_ for _ in dag.nodes if 'best' in _]:
        dag.add_edge(n, 'losses')
    return dag
