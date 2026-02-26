import matplotlib.pyplot as plt
import math
import os

# Create output directory if it doesn't exist
os.makedirs("outputs", exist_ok=True)

# Replicate JS functions
def mag(k, e):
    return math.sqrt(k*k + e*e)

def organism(x, y, t):
    # let k = 5 * cos(x / 14) * cos(y / 30);
    k = 5 * math.cos(x / 14) * math.cos(y / 30)

    # let e = y / 8 - 13;
    e = y / 8 - 13

    # let d = pow(mag(k, e), 2) / 59 + 4;
    d = (mag(k, e)**2) / 59 + 4

    # let angleTerm = atan2(k, e);
    # In JS atan2(y, x). The code uses atan2(k, e) so k is y-component, e is x-component.
    angleTerm = math.atan2(k, e)

    # let q = 60 - 3 * sin(angleTerm * e);
    q = 60 - 3 * math.sin(angleTerm * e)

    # let wave = k * (3 + 4 / d * sin(d * d - t * 2));
    wave = k * (3 + 4 / d * math.sin(d * d - t * 2))

    # let c = d / 2 + e / 99 - t / 18;
    c = d / 2 + e / 99 - t / 18

    # let xCoord = (q + wave) * sin(c) + 200;
    # let yCoord = (q + d * 9) * cos(c) + 200;
    xCoord = (q + wave) * math.sin(c) + 200
    yCoord = (q + d * 9) * math.cos(c) + 200

    return xCoord, yCoord

def main():
    t = math.pi / 20 * 10 # Simulate 10 frames in

    x_coords = []
    y_coords = []

    # for (let i = 0; i < 10000; i++)
    for i in range(10000):
        x = i % 80
        y = i / 43 # Python 3 float division
        xc, yc = organism(x, y, t)
        x_coords.append(xc)
        y_coords.append(yc)

    plt.figure(figsize=(6, 6))
    plt.scatter(x_coords, y_coords, s=1, alpha=0.5, c='black')
    plt.xlim(0, 400)
    plt.ylim(400, 0) # Flip Y to match canvas coords
    plt.title("Simulated p5.js Organism (t=10 frames)")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.grid(True)

    output_path = "outputs/p5_organism.png"
    plt.savefig(output_path)
    print(f"Saved plot to {output_path}")

if __name__ == "__main__":
    main()
