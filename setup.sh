#!/bin/bash

set -e

INSTALL_DIR="/opt/pdf2txtconvert"
INPUT_DIR="$INSTALL_DIR/input"
OUTPUT_DIR="$INSTALL_DIR/output"
VENV_DIR="$INSTALL_DIR/venv"
RUN_SCRIPT="$INSTALL_DIR/run_converter.sh"
GPU=0

usage() {
    echo "Usage: $0 [--install|--deinstall|--update] [--daemon] [--gpu]"
    exit 1
}

install() {
    echo "Installing to $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
    rsync -a --delete "$PWD/" "$INSTALL_DIR/"
    if ! command -v tesseract >/dev/null; then
        echo "Tesseract not found. Attempting to install..."
        if command -v apt-get >/dev/null; then
            sudo apt-get update && sudo apt-get install -y tesseract-ocr
        else
            echo "Could not install tesseract automatically."
        fi
    fi
    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"
    pip install --upgrade pip
    pip install -r "$INSTALL_DIR/requirements.txt"
    if [ "$GPU" -eq 1 ]; then
        pip install --extra-index-url https://download.pytorch.org/whl/cu118 torch torchvision torchaudio
    fi
    deactivate
    mkdir -p "$INPUT_DIR" "$OUTPUT_DIR"
    cat <<EOS > "$RUN_SCRIPT"
#!/bin/bash
source "$VENV_DIR/bin/activate"
python -m pdf2txt --input-folder "$INPUT_DIR" --output-folder "$OUTPUT_DIR" "$@"
EOS
    chmod +x "$RUN_SCRIPT"
    echo "Installation complete."
}

deinstall() {
    echo "Removing $INSTALL_DIR"
    crontab -l 2>/dev/null | grep -v "$RUN_SCRIPT" | crontab - || true
    rm -rf "$INSTALL_DIR"
    echo "Deinstallation complete."
}

update() {
    if [ -d "$INSTALL_DIR/.git" ]; then
        git -C "$INSTALL_DIR" pull
        source "$VENV_DIR/bin/activate"
        pip install -r "$INSTALL_DIR/requirements.txt"
        if [ "$GPU" -eq 1 ]; then
            pip install --extra-index-url https://download.pytorch.org/whl/cu118 torch torchvision torchaudio
        fi
        deactivate
    else
        echo "No git repository found in $INSTALL_DIR"
    fi
}

DAEMON=0
ACTION=""
while [ $# -gt 0 ]; do
    case "$1" in
        --install) ACTION="install" ; shift ;;
        --deinstall) ACTION="deinstall" ; shift ;;
        --update) ACTION="update" ; shift ;;
        --daemon) DAEMON=1 ; shift ;;
        --gpu) GPU=1 ; shift ;;
        *) usage ;;
    esac
done

[ -z "$ACTION" ] && usage

case "$ACTION" in
    install)
        install
        if [ "$DAEMON" -eq 1 ]; then
            echo "Adding cron job for daemon mode"
            (crontab -l 2>/dev/null; echo "*/5 * * * * $RUN_SCRIPT >> $INSTALL_DIR/cron.log 2>&1") | sort - | uniq - | crontab -
        fi
        ;;
    deinstall)
        deinstall ;;
    update)
        update ;;
    *) usage ;;
esac
