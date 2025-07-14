# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

export ZSH="$HOME/.oh-my-zsh"

ZSH_THEME="agnosterzak"

plugins=( 
    git
    zsh-autosuggestions
    zsh-syntax-highlighting
)

source $ZSH/oh-my-zsh.sh


# Display Pokemon-colorscripts
# Project page: https://gitlab.com/phoneybadger/pokemon-colorscripts#on-other-distros-and-macos
#pokemon-colorscripts --no-title -s -r #without fastfetch
pokemon-colorscripts --no-title -s -r | fastfetch -c $HOME/.config/fastfetch/config-pokemon.jsonc --logo-type file-raw --logo-height 10 --logo-width 5 --logo -

# fastfetch. Will be disabled if above colorscript was chosen to install
#fastfetch -c $HOME/.config/fastfetch/config-compact.jsonc


# Set-up icons for files/directories in terminal using lsd
alias ls='lsd'
alias l='ls -l'
alias la='ls -a'
alias lla='ls -la'
alias lt='ls --tree'

alias sshlogin='ssh feez@104.237.3.163'
alias sshcopy='sshcopy.sh'
alias yt='yt.sh'
alias YtDownload='YtDownload.sh'
alias activatevenv='source ~/.venv/bin/activate'
alias run_bot_cryplex='cd ~/files/projects/crypto/new/Cryplex-Auto-Bot/ && node .'
alias android-dlp='YtDownload --Link https://youtu.be/blKkRoZPxLc?si=Qef1NW1xz6tAVw4Z --DownloadLocation /home/deen/files/videos/Courses'
alias run_tmux='~/tmux_automation.zsh'
export PATH="/home/deen/files/apps/platform-tools:/usr/local/nvim-linux64/bin:/home/deen/files/projects/myScripts:$HOME/cmake-4.0.2/bin:~/.emacs.d/bin/:$HOME/.tmuxifier/bin:$PATH"
eval "$(tmuxifier init -)"
export EDITOR=nvim
eval "$(zoxide init --cmd cd zsh)"

export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"                   # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion" # This loads nvm bash_completion
alias changeMacAddress='sudo macchanger -m 60:57:18:D7:26:A2 wlo1'
alias hibernate='sudo systemctl hibernate'
. "$HOME/.cargo/env"
