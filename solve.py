import socket
import time
import re
import sys

def parse_dice_rolls(lines):
    """Parse dice rolls from round output"""
    players = {}
    
    for line in lines:
        line = line.strip()
        if line.startswith('Player'):
            # Format: "Player X: 1 2 3 4 5"
            match = re.search(r'Player (\d+): ([\d\s]+)', line)
            if match:
                player_num = int(match.group(1))
                dice = list(map(int, match.group(2).split()))
                players[player_num] = sum(dice)
    
    return players

def determine_winner(players):
    """
    Replicate the flawed winner determination logic
    Original: sorted(dice_sum.items(), key=lambda x:x[1])[-1][0][1].split('_')[1]
    """
    if not players: return 0
    # Convert to list of (player_num, score)
    items = list(players.items())
    
    # Sort by score only (ascending)
    # Python's sort is stable, so items with same score keep original order
    # Original order is player 1, 2, ..., N
    items.sort(key=lambda x: x[1])
    
    # The original script takes [-1], which is the last one in the sorted list
    # For equal scores, this is the player with the HIGHER number
    return items[-1][0]

def solve():
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} <host> <port>")
        sys.exit(1)
    
    host = sys.argv[1]
    port = int(sys.argv[2])
    
    print(f"Connecting to {host}:{port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.settimeout(2)
    
    # Receive initial messages
    data = b""
    while b"2. No" not in data:
        chunk = sock.recv(1024)
        if not chunk: break
        data += chunk
    
    # Send "1" to start
    sock.send(b"1\n")
    print("Started the game.")
    
    # Process 100 rounds
    for round_num in range(100):
        # Receive until "Who wins this round?"
        round_data = b""
        while b"Who wins this round?" not in round_data:
            chunk = sock.recv(4096)
            if not chunk: break
            round_data += chunk
        
        # Decode and parse
        text = round_data.decode('utf-8', errors='ignore')
        lines = text.split('\n')
        
        # Parse dice rolls
        players = parse_dice_rolls(lines)
        
        # Calculate winner
        winner = determine_winner(players)
        
        # Send answer immediately
        answer = str(winner).encode() + b'\n'
        sock.send(answer)
        
        # Receive confirmation ("Yes.. Correct!" or error)
        # We need to read until the start of the next round or the end
        response = b""
        while b"Correct" not in response and b"Wrong" not in response and b"corrupted" not in response:
             chunk = sock.recv(1024)
             if not chunk: break
             response += chunk
        
        if b"Correct" in response:
            sys.stdout.write(f"\rRound {round_num + 1}/100: Winner Player {winner} - Correct!    ")
            sys.stdout.flush()
        else:
            print(f"\nRound {round_num + 1} Failed!")
            print(f"Response: {response.decode(errors='ignore')}")
            break
    
    print("\nGame finished. Waiting for flag...")
    time.sleep(0.5)
    
    # Receive remaining data including flag
    final_data = b""
    try:
        while True:
            chunk = sock.recv(1024)
            if not chunk: break
            final_data += chunk
    except socket.timeout:
        pass
    
    print("\nResult:")
    print(final_data.decode('utf-8', errors='ignore'))
    
    sock.close()

if __name__ == "__main__":
    solve()
