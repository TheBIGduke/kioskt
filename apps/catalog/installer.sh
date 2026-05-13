#!/bin/bash
# Made by Kaléin Tamaríz

print_banner() {
  cat << 'EOF'
___/\/\______/\/\____________________/\/\/\/\/\____/\/\/\/\____/\/\/\/\/\________/\/\______________/\/\___________________
_/\/\/\/\/\__/\/\__________/\/\/\____/\/\____/\/\____/\/\____/\/\________________/\/\__/\/\__/\/\__/\/\__/\/\____/\/\/\___
___/\/\______/\/\/\/\____/\/\/\/\/\__/\/\/\/\/\______/\/\____/\/\__/\/\/\____/\/\/\/\__/\/\__/\/\__/\/\/\/\____/\/\/\/\/\_
___/\/\______/\/\__/\/\__/\/\________/\/\____/\/\____/\/\____/\/\____/\/\__/\/\__/\/\__/\/\__/\/\__/\/\/\/\____/\/\_______
___/\/\/\____/\/\__/\/\____/\/\/\/\__/\/\/\/\/\____/\/\/\/\____/\/\/\/\/\____/\/\/\/\____/\/\/\/\__/\/\__/\/\____/\/\/\/\_
__________________________________________________________________________________________________________________________
EOF
}

PACKAGE_NAME="products_and_surveys"

# Directories
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_DIR="$BACKEND_DIR/.venv" # Virtual env named '.venv' inside backend

info()   { printf "\n\033[1;34m[INFO]\033[0m %s\n" "$*"; }
ok()  { printf "\033[1;32m[OK]\033[0m %s\n" "$*"; }
warn()  { printf "\033[1;33m[WARN]\033[0m %s\n" "$*"; }
fail()  { printf "\033[1;31m[FAIL]\033[0m %s\n" "$*"; exit 1; }

APT_PKGS=(
  python3-dev sqlite3 sqlitebrowser curl mkcert libnss3-tools
)

info "SCRIPT_DIR: $SCRIPT_DIR"

# Install pre-requisites
install_apt() {
  info "Updating system and installing packages ..."
  sudo apt update -y
  sudo apt install -y "${APT_PKGS[@]}"
  ok "System packages installed."
}

verify_uv_setup() {
    info "Verifying uv installation..."
    if [ -f "$HOME/.bashrc" ]; then
        source "$HOME/.bashrc"
    fi
    if [ ! -f "$HOME/.local/bin/uv" ] && ! command -v uv >/dev/null 2>&1; then
        warn "uv not found. Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        ok "uv installed."
    else
        ok "uv is already installed."
    fi
}

virtual_env_setup() {
    local clear_venv="${1:-false}"

    if [ -d "$VENV_DIR" ] && [ "$clear_venv" != "true" ]; then
        warn "Virtual environment already exists in backend."
        read -p "Do you want to delete and recreate it? [y/N] " response
        case "$response" in
            [yY][eE][sS]|[yY]) 
                clear_venv="true"
                ;;
            *)
                info "Using existing virtual environment."
                ;;
        esac
    fi

    # Create a virtual environment, if needed and not already created
    if [ ! -d "$VENV_DIR" ] || [ "$clear_venv" = "true" ]; then
        if [ "$clear_venv" = "true" ]; then
            info "Clearing existing virtual environment..."
            "$HOME/.local/bin/uv" venv --clear "$VENV_DIR"
        else
            "$HOME/.local/bin/uv" venv "$VENV_DIR"
        fi
        ok "Virtual environment created."
    fi

    source "$VENV_DIR/bin/activate"

    if [[ ! -f "$SCRIPT_DIR/requirements.txt" ]]; then
        fail "requirements.txt not found in $SCRIPT_DIR"
    fi

    uv pip install -r "$SCRIPT_DIR/requirements.txt"

    ok "Requirements successfully installed!!!"
}

ssl_cert_setup() {
    info "Setting up local SSL certificates with mkcert..."
    
    # Install the local CA in the system trust store
    mkcert -install

    # Get local IP address (first one found)
    LOCAL_IP=$(hostname -I | awk '{print $1}')
    
    if [ -z "$LOCAL_IP" ]; then
        warn "Could not detect local IP address. Falling back to 127.0.0.1"
        LOCAL_IP="127.0.0.1"
    fi

    # Create certs directory in backend
    mkdir -p "$BACKEND_DIR/certs"

    info "Generating certificate for localhost, 127.0.0.1, and $LOCAL_IP..."
    mkcert -cert-file "$BACKEND_DIR/certs/cert.pem" -key-file "$BACKEND_DIR/certs/key.pem" localhost 127.0.0.1 "$LOCAL_IP"
    
    ok "SSL certificates generated in $BACKEND_DIR/certs/"
}

env_setup() {
    local overwrite_file="${1:-false}"
    
    if [ -f "$BACKEND_DIR/.env" ] && [ "$overwrite_file" != "true" ]; then
        warn ".env file already exists in backend."
        read -p "Do you want to overwrite the .env file? [y/N] " response
        case "$response" in
            [yY][eE][sS]|[yY]) 
                overwrite_file="true"
                ;;
            *)
                info "Using existing .env file."
                ;;
        esac
    fi

    if [ ! -f "$BACKEND_DIR/.env" ] || [ "$overwrite_file" = "true" ]; then
        cat <<EOF > "$BACKEND_DIR/.env"
# Replace with the actual path to your images folder
EXTERNAL_IMAGE_PATH=/home/\${USER}/productsandsurveys_dashboard_back/media/products
# Base URL for media assets (relative path = same origin as the frontend; works in standalone, kiosk-iframe, HTTPS, LAN access, etc.)
BASE_MEDIA_URL=/media
# Set to sqlite:///../products_surveys.db or leave empty for mock data
DATABASE_URL=sqlite:////home/\${USER}/productsandsurveys_dashboard_back/products_surveys.db
EOF
        ok ".env file created/overwritten in $BACKEND_DIR."
    fi
}

verify_image_path() {
    if [ -f "$BACKEND_DIR/.env" ]; then
        local img_path=$(grep "^EXTERNAL_IMAGE_PATH=" "$BACKEND_DIR/.env" | cut -d'=' -f2)
        if [ -n "$img_path" ]; then
            # Expand tilde or variables
            local expanded_path=$(eval echo "$img_path")
            if [ ! -d "$expanded_path" ]; then
                warn "The image directory '$img_path' does not exist. Please create it or update EXTERNAL_IMAGE_PATH in backend/.env"
            else
                ok "Image directory '$img_path' verified."
            fi
        fi
    fi
}

download_frontend_assets() {
    info "Downloading frontend assets (Bootstrap)..."
    local FRONTEND_ASSETS="$SCRIPT_DIR/frontend/assets"
    mkdir -p "$FRONTEND_ASSETS"

    if [ ! -f "$FRONTEND_ASSETS/bootstrap.min.css" ]; then
        curl -sS -o "$FRONTEND_ASSETS/bootstrap.min.css" "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        ok "Downloaded bootstrap.min.css"
    else
        ok "bootstrap.min.css already exists."
    fi

    if [ ! -f "$FRONTEND_ASSETS/bootstrap.bundle.min.js" ]; then
        curl -sS -o "$FRONTEND_ASSETS/bootstrap.bundle.min.js" "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
        ok "Downloaded bootstrap.bundle.min.js"
    else
        ok "bootstrap.bundle.min.js already exists."
    fi
}

post_instructions() {
    info "Installation complete!"
    echo ""
    echo "To run the application:"
    echo "  cd backend"
    echo "  source .venv/bin/activate"
    echo "  uvicorn main:app --host 0.0.0.0 --port 9999"
    echo ""
    echo "Access the application at: http://localhost:9999"
    echo ""
    info "Please verify the paths and variables in backend/.env if needed."
}

main() {
  print_banner
  local clear_venv=false
  local overwrite_file=false

  # Process command-line arguments
  for arg in "$@"; do
    case $arg in
      --clear|-c)
        clear_venv=true
        shift
        ;;
    esac
    case $arg in
      --overwrite|-o)
        overwrite_file=true
        shift
        ;;
    esac
  done

  install_apt
  verify_uv_setup
  virtual_env_setup "$clear_venv"
  ssl_cert_setup
  env_setup "$overwrite_file"
  verify_image_path
  download_frontend_assets
  post_instructions
}

## Usage ##
# ./installer.sh
# ./installer.sh --clear --overwrite

main "$@"
