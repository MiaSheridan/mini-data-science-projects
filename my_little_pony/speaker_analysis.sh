#!/bin/bash


input=$1
output=$2

ponies=("Twilight Sparkle" "Rarity" "Pinkie Pie" "Rainbow Dash" "Fluttershy")

total=$(($(csvtool -t ',' height $input)-1))

echo "pony_name"

echo "pony_name, total_line_count, percent_all_lines\n" > $output
echo "total lines: $total"
for pony in "${ponies[@]}"
do
	echo -e "\nSearching lines for $pony"
	value=$(csvtool -t ',' col 3 $input | grep -i "$pony" | wc -l)
	echo "Lines spoken by $pony: $value"

	pct=$(echo "scale=2; 100 * $value/$total" | bc)
	echo "% of total = $pct"

	echo "$pony, $value, $pct%" >> $output

done

