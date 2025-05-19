
import matplotlib.pyplot as plt

# Data
algorithms = [
    "ECDSA (secp256k1)",
    "ECDSA (secp256r1)",
    "Ed25519",
    "Ed448",
    "ECDSA (secp384r1)",
    "Schnorr (BIP-340)"
]

signing_speed = [141, 103, 75, 71, 62, 109]  # ops/sec
verification_speed = [125, 62, 212, 40, 35, 72]  # ops/sec

x = range(len(algorithms))
width = 0.35

# Plot
plt.figure(figsize=(12, 6))
plt.bar(x, signing_speed, width=width, label='Signing Speed', color='#4caf50')
plt.bar([i + width for i in x], verification_speed, width=width, label='Verification Speed', color='#2196f3')

# Labels and titles
plt.xlabel('Signature Algorithm')
plt.ylabel('Operations per Second')
plt.title('Signing vs Verification Speed of ECC Signature Algorithms')
plt.xticks([i + width / 2 for i in x], algorithms, rotation=25, ha='right')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.tight_layout()
plt.show()
