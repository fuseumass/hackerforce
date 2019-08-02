confirm() {
    # call with a prompt string or use a default
    read -r -p "${1:-Are you sure? [yes/N]} " response
    case "$response" in
        [yY][eE][sS]) 
            true
            ;;
        *)
            false
            ;;
    esac
}


# A script that automates the reconstruction of the entire database.
echo "WARNING WARNING WARNING WARNING WARNING"
echo "  We are about to delete the local DB. "
echo "  Are you sure you want to do this?    "
echo "WARNING WARNING WARNING WARNING WARNING"

confirm || exit 0

rm -f db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py shell < init.py
