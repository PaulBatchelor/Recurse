IDENTIFIER="Wacom"

# TABLET=$(swaymsg -t get_inputs | jq -r '.[] | select(.type=="touchpad") | select(.identifier | test("$IDENTIFIER")) | .identifier')
# 
# TABLET_TOOL=$(swaymsg -t get_inputs | jq -r '.[] | select(.type=="tablet_tool") | select(.identifier | test("$IDENTIFIER")) | .identifier'
DEVS=$(swaymsg -t get_inputs | jq -r '.[]| select(.product==2313) | .identifier' | uniq)

for DEV in $DEVS
do
    swaymsg input "$DEV" events disabled
done

# swaymsg input $TABLET events disabled
# swaymsg input $TABLET_TOOL events disabled
