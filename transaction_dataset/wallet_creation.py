import subprocess

# Define the command to create the wallet
command = [
    "monero-wallet-cli",
    "--testnet",
    "--generate-new-wallet", "./wallet_01.bin",
    "--restore-deterministic-wallet",
    "--electrum-seed='joking today inroads hamburger together tagged deftly lofty sake hive bevel adhesive eternal ointment fixate boyfriend river foyer nocturnal noted petals evaluate omnibus paradise fixate'",
    "--password", "",
    "--log-file", "./wallet_01.log"
]

# Execute the command
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Wait for the command to finish and capture output
stdout, stderr = process.communicate()

# Check if there were any errors
if process.returncode != 0:
    print("Error:", stderr.decode())
else:
    print("Wallet created successfully.")
