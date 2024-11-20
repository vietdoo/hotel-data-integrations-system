
if [ $# -ne 2 ]; then
  echo "Usage: $0 <hotel_ids> <destination_ids>"
  exit 1
fi

# Assign arguments to variables
HOTEL_IDS=$1
DESTINATION_IDS=$2

# Run the Python script with the provided arguments
python3 main.py "$HOTEL_IDS" "$DESTINATION_IDS"