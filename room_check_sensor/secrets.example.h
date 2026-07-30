// Copy this file to secrets.h (which is git-ignored) and fill in your own
// values. Never commit real credentials to version control.

#define WIFI_SSID "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// From Firebase Console -> Project settings -> General
#define API_KEY "YOUR_FIREBASE_API_KEY"

// Host only, no "https://" prefix and no trailing slash
#define DATABASE_URL "roomcheek-default-rtdb.asia-southeast1.firebasedatabase.app"

// Unique id for the room this board is installed in, e.g. "2-304".
// Must match one of the room ids listed in config.py (BUILDINGS).
#define ROOM_ID "2-304"
