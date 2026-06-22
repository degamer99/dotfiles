Here is a direct analysis of your approach, why GNU Stow might frustrate you based on your requirements, and the best alternative to achieve exactly what you want.

### 1. The Problem with GNU Stow for Your Needs

While GNU Stow is a fantastic, classic symlink manager, **it strictly violates your main requirement.**

Stow operates on a "mirroring" philosophy. If you want a file to end up in `~/.config/mpv/mpv.conf`, Stow **forces** you to recreate that exact folder structure inside your dotfiles repository (e.g., `~/dotfiles/mpv/.config/mpv/mpv.conf`). You cannot just keep a flat folder of files and tell Stow where to send them.

Furthermore, Stow on Windows is clunky. It requires environments like MSYS2 or Cygwin to run, which is overkill if you just want to link some files.

### 2. The Best Alternative: Dotbot

Based on your strict requirements (cross-platform, defining storage paths manually, and avoiding nested `.config` folder structures), the absolute best tool for you is **Dotbot**.

Dotbot uses a simple YAML or JSON file where you explicitly map your source files to their destination targets. It doesn't care how your repository is structured; you can keep all your files completely flat. It also has native support for both Linux (via Bash) and Windows (via PowerShell).

---

### 3. How to Set Up Dotbot for Your MPV Config

Here is exactly how you would set this up to work seamlessly across both Linux and Windows.

#### Step 1: The Golden Rule for Windows Symlinks

Before doing anything, you must know that Windows restricts symlink creation by default. To make cross-platform dotfiles work without running your terminal as an Administrator every time, you must **Enable Developer Mode** in Windows:

1. Open Windows Settings.
2. Search for **Developer Mode**.
3. Toggle it **On**.

#### Step 2: Create Your Flat Directory

Create a folder for your dotfiles (e.g., `~/dotfiles`) and drop the `mpv.conf` and `input.conf` files we created earlier directly into the root of that folder. No need for `.config/mpv` subfolders.

```text
dotfiles/
├── mpv.conf
├── input.conf
└── install.conf.yaml

```

#### Step 3: Define Your Config (`install.conf.yaml`)

Create an `install.conf.yaml` file. This is where Dotbot shines. You can define where the files go based on the operating system, mapping them directly to the correct locations.

* On Linux, `mpv` looks in `~/.config/mpv/`.
* On Windows, `mpv` looks in `~/AppData/Roaming/mpv/`.

Here is your configuration:

```yaml
- defaults:
    link:
      create: true  # Automatically create the parent folders if they don't exist
      relink: true  # Overwrite existing symlinks if they are broken

# ==========================================
# LINUX ROUTING
# ==========================================
- link:
    ~/.config/mpv/mpv.conf:
      path: mpv.conf
      if: '[ "$(uname)" = "Linux" ]'
    ~/.config/mpv/input.conf:
      path: input.conf
      if: '[ "$(uname)" = "Linux" ]'

# ==========================================
# WINDOWS ROUTING
# ==========================================
- link:
    ~/AppData/Roaming/mpv/mpv.conf:
      path: mpv.conf
      if: ver  # 'ver' is a quick command that only returns true on Windows
    ~/AppData/Roaming/mpv/input.conf:
      path: input.conf
      if: ver

```

#### Step 4: Add the Dotbot Submodule and Install Scripts

Dotbot is designed to be included as a Git submodule so you don't have to install it system-wide on every new machine.

Open your terminal inside your `dotfiles` folder and run:

**On Linux/Mac:**

```bash
git init
git submodule add https://github.com/anishathalye/dotbot
cp dotbot/tools/git-submodule/install .
chmod +x install

```

**On Windows (PowerShell):**

```powershell
git init
git submodule add https://github.com/anishathalye/dotbot
Copy-Item dotbot\tools\git-submodule\install.ps1 .\install.ps1

```

### The Result

You now have a perfectly flat repository.

* When you are on your Linux machine, you simply run `./install` and Dotbot will create the folders and symlink the files to `~/.config/mpv/`.
* When you are on your Windows machine, you run `.\install.ps1` and it will securely route those exact same files to `AppData/Roaming`.

No mirrored folders, total control over destinations, and clean cross-platform logic.


Here is the complete, step-by-step guide to installing Dotbot and setting it up to work seamlessly across both Fedora Linux and Windows.

Because `dotbot` is written in Python, the core engine is natively cross-platform. However, the default bootstrap script it provides is written in Bash (for Linux/macOS). To make this truly cross-platform without relying on MSYS2 or WSL on Windows, we will use the default Bash script for Fedora and create a tiny PowerShell equivalent for Windows.

### 1. Prerequisites

Dotbot only requires two things to run: **Git** and **Python**.

**On Fedora Linux:**
Open your terminal and ensure both are installed:

```bash
sudo dnf install git python3

```

**On Windows:**
Open PowerShell and install Git and Python (if you don't have them already):

```powershell
winget install Git.Git Python.Python.3.11

```

*(Crucial for Windows: Ensure **Developer Mode** is turned ON in your Windows Settings so you can create symlinks without needing to run PowerShell as an Administrator every time).*

---

### 2. Initialize the Repository

Pick a location for your dotfiles (e.g., `~/dotfiles`) and set up the Git repository with the Dotbot submodule. You can do this on either OS.

```bash
mkdir ~/dotfiles
cd ~/dotfiles
git init
git submodule add https://github.com/anishathalye/dotbot

```

---

### 3. Setup the Install Scripts

You need a way to execute Dotbot easily on both operating systems.

#### For Fedora (The Bash Script)

Dotbot provides a ready-to-use Bash script. Copy it to the root of your `dotfiles` folder and make it executable:

```bash
cp dotbot/tools/git-submodule/install .
chmod +x install

```

#### For Windows (The PowerShell Script)

Dotbot doesn't ship with an official PowerShell script by default, but it is very easy to trigger the Python module directly.
Create a file named `install.ps1` in the root of your `dotfiles` folder and paste this inside:

```powershell
# Ensure the submodule is downloaded and updated
git submodule update --init --recursive

# Run the Dotbot Python script
python dotbot\bin\dotbot -d $PSScriptRoot -c install.conf.yaml

```

---

### 4. Create the Configuration (`install.conf.yaml`)

Place your `mpv.conf` and `input.conf` directly in the root of your `dotfiles` folder.
Then, create the `install.conf.yaml` file.

Dotbot uses the `if` directive to evaluate a shell command.

* `ver` is a built-in Windows command. It succeeds on Windows and fails on Linux.
* `[ "$(uname)" = "Linux" ]` succeeds on Linux and fails on Windows.

Paste this into `install.conf.yaml`:

```yaml
- defaults:
    link:
      create: true  # Automatically create parent folders like ~/.config/mpv/
      relink: true  # Overwrite existing symlinks

# ==========================================
# LINUX ROUTING (Fedora)
# ==========================================
- link:
    ~/.config/mpv/mpv.conf:
      path: mpv.conf
      if: '[ "$(uname)" = "Linux" ]'
    ~/.config/mpv/input.conf:
      path: input.conf
      if: '[ "$(uname)" = "Linux" ]'

# ==========================================
# WINDOWS ROUTING
# ==========================================
- link:
    ~/AppData/Roaming/mpv/mpv.conf:
      path: mpv.conf
      if: ver
    ~/AppData/Roaming/mpv/input.conf:
      path: input.conf
      if: ver

```

---

### 5. Running the Setup

Your repository structure should now look exactly like this:

```text
dotfiles/
├── dotbot/             # The git submodule folder
├── install             # The bash script for Fedora
├── install.ps1         # The powershell script for Windows
├── install.conf.yaml   # The routing logic
├── mpv.conf            # Your mpv settings
└── input.conf          # Your mpv keybindings

```

Whenever you pull this repository to a new machine or add new files to the config, simply run the respective install script.

* **On Fedora:** Open terminal in your `dotfiles` folder and run `./install`
* **On Windows:** Open PowerShell in your `dotfiles` folder and run `.\install.ps1`

Dotbot will read the YAML file, detect your OS, create the necessary destination folders automatically, and securely drop the symlinks exactly where `mpv` expects them.

