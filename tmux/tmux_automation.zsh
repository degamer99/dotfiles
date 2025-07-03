#!/bin/zsh

# This script automates the creation and setup of a tmux session
# with multiple windows and panes, each running specific commands.

# --- Configuration Variables ---
SESSION_NAME="dev-session" # Name of your tmux session

# Define commands for the FIRST window's panes.
# These will be mapped to positions in a 2x2 grid:
# +------------+------------+
# |  TOP-LEFT  | TOP-RIGHT  |
# |   (Pane 1) |   (Pane 2) |
# +------------+------------+
# | BOTTOM-LEFT| BOTTOM-RIGHT|
# |   (Pane 3) |   (Pane 4) |
# +------------+------------+
# If you provide fewer than 4, only the necessary panes will be created.
# If you provide more than 4, subsequent commands will create new windows.
#    ""                       # Dummy element at index 0 to align with 1-based human logic
CODE_WINDOW_CMDS=(
    "nvim ."                 # Command for TOP-LEFT (Pane 1) - CODE_WINDOW_CMDS[1]
    "echo second_line"            # Command for TOP-RIGHT (Pane 2) - CODE_WINDOW_CMDS[2]
    "htop"                   # Command for BOTTOM-LEFT (Pane 3) - CODE_WINDOW_CMDS[3]
    "echo hello"   # Command for BOTTOM-RIGHT (Pane 4) - CODE_WINDOW_CMDS[4]
    # Add more commands here if you want them in new windows automatically
    # "docker-compose up"      # This would create a new window if 4 above exist
    # "nix-shell"              # This would create another new window
)

# Define commands for additional, explicitly named windows (optional)
# These windows will be created *after* the dynamic 'code' windows.
CMD_GIT_WINDOW="git status"     # Command for a dedicated Git window
CMD_SERVER_WINDOW="python3 -m http.server 8000" # Command for a server window
CMD_TEST_WINDOW="npm test --watch" # Command for a testing window

# --- Main Script Logic ---

# Check if the tmux session already exists
if tmux has-session -t "${SESSION_NAME}" 2>/dev/null; then
    echo "Attaching to existing tmux session: ${SESSION_NAME}"
    tmux attach-session -t "${SESSION_NAME}"
else
    echo "Creating new tmux session: ${SESSION_NAME}"

    # --- Setup the first window with dynamic pane arrangement ---
    # Create a new detached session with the first window (named 'code-0')
    # and run the first command in the top-left pane (Pane 1, due to pane-base-index 1).
    # The session's first window will be at index 1 due to base-index 1.
    tmux new-session -d -s "${SESSION_NAME}" -n "code-0" "${CODE_WINDOW_CMDS[1]}"

    # Use a dummy element in the array to make indexing 1-based for easier reading
    # when associating with Pane 1, Pane 2, etc.
    # local pane_count=${#CODE_WINDOW_CMDS[@]}
    local pane_count=1

    tmux split-window -h -t "${SESSION_NAME}:code-0.1" "${CODE_WINDOW_CMDS[2]}"
        
    # Handle up to 4 panes in the first window (code-0)
    # Note: Window 'code-0' is tmux window index 1, its panes start from 1.
    # Pane 1 (TOP-LEFT) is already created.

    if (( pane_count > 1 )); then
        # Create TOP-RIGHT pane (Pane 2), splitting from Pane 1 (the initial pane)
        tmux split-window -h -t "${SESSION_NAME}:code-0.1" "${CODE_WINDOW_CMDS[2]}"
    fi

    if (( pane_count > 2 )); then
        # Create BOTTOM-LEFT pane (Pane 3), splitting from Pane 1 (the original TOP-LEFT pane)
        tmux split-window -v -t "${SESSION_NAME}:code-0.1" "${CODE_WINDOW_CMDS[3]}"
    fi

    if (( pane_count > 3 )); then
        # Create BOTTOM-RIGHT pane (Pane 4), splitting from Pane 2 (the TOP-RIGHT pane)
        tmux split-window -v -t "${SESSION_NAME}:code-0.2" "${CODE_WINDOW_CMDS[4]}"
    fi

    # --- Handle additional commands by creating new windows dynamically ---
    # current_window_index keeps track of how many 'code-X' windows were created beyond 'code-0'
    local current_window_index=0 # Starts at 0 for 'code-0' which is window 1

    # Start looping from the 5th command (index 5 in 1-based array)
    for i in {5..$pane_count}; do
        current_window_index=$((current_window_index + 1))
        local new_window_name="code-${current_window_index}"
        # Tmux window numbers start from 1, so if current_window_index is 1 (for code-1),
        # the window number will be 2. This aligns with base-index 1.
        local new_window_number=$((current_window_index + 1))

        # Create a new window for each additional command
        tmux new-window -t "${SESSION_NAME}:${new_window_number}" -n "${new_window_name}" "${CODE_WINDOW_CMDS[$i]}"
    done

    # --- Create additional, fixed-purpose windows ---
    # These will always be created regardless of the number of CODE_WINDOW_CMDS
    # Adjust their window numbers based on how many dynamic 'code-X' windows were created.
    # The first dynamic window ('code-0') is window 1.
    # If current_window_index is 0 (meaning only 'code-0' was made), the next window is 2.
    # If current_window_index is N (meaning 'code-0' to 'code-N' were made), the next window is N+2.
    local next_available_window_num=$((current_window_index + 2))

    tmux new-window -t "${SESSION_NAME}:${next_available_window_num}" -n "git" "${CMD_GIT_WINDOW}"
    next_available_window_num=$((next_available_window_num + 1))

    tmux new-window -t "${SESSION_NAME}:${next_available_window_num}" -n "server" "${CMD_SERVER_WINDOW}"
    next_available_window_num=$((next_available_window_num + 1))

    tmux new-window -t "${SESSION_NAME}:${next_available_window_num}" -n "test" "${CMD_TEST_WINDOW}"

    # Select the first window ('code-0') after setting up all windows/panes
    # This targets window 1, which is 'code-0'
    tmux select-window -t "${SESSION_NAME}:1"

    echo "Tmux session '${SESSION_NAME}' created and configured."
    echo "Attaching to session..."

    # Attach to the newly created session
    tmux attach-session -t "${SESSION_NAME}"
fi

# End of script
