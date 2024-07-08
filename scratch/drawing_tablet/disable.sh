TABLET=$(swaymsg -t get_inputs | jq -r '.[] | select(.type=="touchpad") | select(.identifier | test("Wacom")) | .identifier')

TABLET_TOOL=$(swaymsg -t get_inputs | jq -r '.[] | select(.type=="tablet_tool") | select(.identifier | test("Wacom")) | .identifier')

swaymsg input $TABLET events disabled
swaymsg input $TABLET_TOOL events disabled
