import re
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from IPython.display import HTML
def parse_cannon(s):
    x, t = map(int, re.search(r'cannon\((\d+),(\d+)\)', s).groups())
    return x, t


def parse_move(s):
    x, t = map(int, re.search(r'move\((\d+),(\d+)\)', s).groups())
    return x, t


def parse_shot(s):
    alien, x, t = re.search(
        r'shot\(([^,]+),(\d+),(\d+)\)', s
    ).groups()
    return alien, int(x), int(t)


def parse_alien(s):
    alien, x, y, t = re.search(
        r'alien\(([^,]+),(\d+),(\d+),(\d+)\)', s
    ).groups()
    return alien, int(x), int(y), int(t)

def animate_model(models, model_name, interval=1000):
    
    model = models[model_name]

    cannons = [parse_cannon(x) for x in model["cannon"]]
    moves = [parse_move(x) for x in model["move"]]
    shots = [parse_shot(x) for x in model["shot"]]
    aliens = [parse_alien(x) for x in model["alien"]]

    max_time = max(
        [t for _, t in cannons] +
        [t for _, _, t in shots] +
        [t for _, _, _, t in aliens]
    )

    max_x = max(
        [x for x, _ in cannons] +
        [x for _, x, _, _ in aliens]
    )

    max_y = max(
        [y for _, _, y, _ in aliens]
    )

    fig, ax = plt.subplots(figsize=(8, 8))

    def update(t):
        ax.clear()

        ax.set_xlim(-1, max_x + 1)
        ax.set_ylim(-1, max_y + 1)

        ax.set_xticks(range(max_x + 1))
        ax.set_yticks(range(max_y + 1))

        ax.set_title(f"SPACE INVADERS — {model_name} — t = {t}")


        current_aliens = [
            (alien, x, y)
            for alien, x, y, time in aliens
            if time == t
        ]

        for alien, x, y in current_aliens:
            ax.text(
                x,
                y,
                f"▲ \n {alien}",
                ha="center",
                va="center",
                fontsize=18
            )

 
        cannon_positions = [
            (x, time)
            for x, time in cannons
            if time == t
        ]

        if cannon_positions:
            cannon_x = cannon_positions[0][0]

            ax.text(
                cannon_x,
                0,
                "▲",
                ha="center",
                va="center",
                fontsize=20
            )

 
        current_shots = [
            (alien, x)
            for alien, x, time in shots
            if time == t
        ]

        for alien, x in current_shots:

            # Troviamo la posizione dell'alieno
            target = [
                (ax_, ay_)
                for alien_, ax_, ay_, time in aliens
                if alien_ == alien and time == t
            ]

            if target:
                target_x, target_y = target[0]

                # Disegniamo il proiettile
                ax.text(
                    x,
                    target_y - 1,
                    "|",
                    ha="center",
                    va="center",
                    fontsize=20
                )


        current_moves = [
            x
            for x, time in moves
            if time == t
        ]

        if current_moves:
            new_x = current_moves[0]

            ax.text(
                new_x,
                -0.5,
                "x",
                ha="center",
                va="center",
                fontsize=12
            )

        ax.grid(True)

    animation = FuncAnimation(
        fig,
        update,
        frames=range(max_time + 1),
        interval=interval,
        repeat=False
    )

    plt.close(fig)

    return HTML(animation.to_jshtml())